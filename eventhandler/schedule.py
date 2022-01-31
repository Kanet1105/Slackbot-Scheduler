
"""
========== Scheduler ==========
schedule.toml 파일을 참조하고 시간 역순으로 sort 해서 eventStack 에 추가합니다.
시간 역순으로 sorting 하기 때문에 schedule.toml 파일에 스케쥴을 추가할 때 시간순으로 넣을 필요 없습니다.
event stack 의 제일 마지막 오브젝트부터 pop() 하고 eventQueue 에 push 해주는 역할을 해 주는 thread 입니다.
런타임에 스케줄을 변경할 수 있습니다.


========== nptime 패키지 ==========
nptime 패키지는 python timedelta 연산을 돕는 외부 패키지 입니다.
nptime 간의 연산 결과는 datetime.timedelta 오브젝트를 반환합니다.


========== 시간의 부등호 연산 ==========
nptime 오브젝트끼리의 비교는 시간 순서의 비교를 bool 형태로 반환합니다.

    예)  a = nptime(hour=17, minute=30; b = nptime(hour=17, minute=40) 가 있을 때
        a > b 의 리턴값은 False 이며
        a < b 의 리턴값은 True 입니다.
"""


import datetime
from message import log, response
from nptime import nptime
import os
from threading import Thread
import time
import toml
import traceback


class Scheduler(Thread):
    def __init__(self, eventQueue, schedulePath):
        super().__init__()
        self.daemon = True
        self.eventQueue = eventQueue
        self.schedulePath = schedulePath
        self.fileModifiedTime = os.path.getmtime(self.schedulePath)
        self.alarmTime = self.setAlarmTime((1, 5))
        self.eventStack = self.buildEventStack()

    # 총 스케줄을 로드하고 리스트 형태로 반환
    def loadSchedule(self, schedulePath):
        with open(schedulePath, "r", encoding="utf-8") as file:
            schedule = toml.load(file)
            return schedule['Schedule']

    # alarm interval 을 timedelta 오브젝트 투플 형태로 저장
    def setAlarmTime(self, minute):
        return tuple(datetime.timedelta(minutes=value) for value in minute)

    # "hh:mm" 포맷의 시간을 nptime 오브젝트로 변환
    def parseTimeFormat(self, stringTime):
        hour, minute = map(int, stringTime.split(":"))
        eventTime = nptime(hour=hour, minute=minute)
        return eventTime

    # 전체 스케줄에서 오늘의 이벤트를 리스트 형태로 반환
    def getEventToday(self):
        schedule = self.loadSchedule(self.schedulePath)
        weekday, now = self.getNow()
        eventToday = []

        # 오늘의 이벤트를 필터링
        for eventDict in schedule:

            # 당일 이벤트가 아닐 시 제외
            if weekday not in eventDict["day"]:
                continue

            # 이미 지난 이벤트 제외
            eventDict['time'] = self.parseTimeFormat(eventDict['time'])
            for alarm in self.alarmTime:
                alarmTime = eventDict['time'] - alarm
                if alarmTime < now:
                    continue

                # 도래할 이벤트만 EventObject 형태로 저장
                eventDict['alarm'] = alarmTime
                eventObject = EventObject(eventDict)
                eventToday.append(eventObject)

        return eventToday

    # 요일에 맞는 스케줄을 리스트로 반환
    def buildEventStack(self):
        eventStack = self.getEventToday()

        # 이벤트가 있을 때만 시간 역순으로 정렬
        if eventStack:
            eventStack.sort(key=lambda eventObject: eventObject.getAlarmTime(), reverse=True)

        return eventStack

    # 현재 요일과 시간을 (weekday, nptime object) 투플 형태로 반환
    def getNow(self):
        now = datetime.datetime.now()
        weekday = now.weekday()
        timeFormat = nptime(hour=now.hour, minute=now.minute)
        return weekday, timeFormat

    # 이벤트 스택의 가장 위에 있는 이벤트와 현재 시간을 비교해서 같다면 이벤트를 발생
    def alarm(self, now):
        # 이벤트 없을 시 반환
        if not self.eventStack:
            return

        # 이벤트 발생 시 eventQueue 에 (type, object) 형태로 추가
        if self.eventStack[-1].getAlarmTime() == now:
            self.eventQueue.put(("alarm", self.eventStack.pop()))

    # Schedule.toml 파일 변경시 변경된 스케줄 런타임에 반영
    def updateSchedule(self):
        lastModifiedTime = os.path.getmtime(self.schedulePath)
        
        # 파일 변경시간 체크 후 이벤트스택 새로 생성
        if lastModifiedTime != self.fileModifiedTime:
            try:
                self.eventStack = self.buildEventStack()
                message = response.Console.scheduleChanged
                log.systemLogger.info(message)
                print(message)
            except:
                message = response.Console.scheduleWrongFormat.format(traceback=traceback.format_exc())
                log.systemLogger.error(message)
                print(message)
        self.fileModifiedTime = lastModifiedTime

    def run(self):
        while True:
            try:
                self.updateSchedule()
                weekday, now = self.getNow()
                self.alarm(now)
                time.sleep(1)
            except:
                print(response.Console.errorThread.format(name="Scheduler"))
                log.systemLogger.error(traceback.format_exc())
                break


"""
이벤트 dictionary 를 이벤트 오브젝트로 언패킹합니다.
각 field 마다 class attribute 로 할당되며 필드에 접근할 수 있는 class method를
따로 만듭니다.
"""


class EventObject:
    def __init__(self, event):
        self.name = None        # String
        self.day = None         # Weekday Index from 0 to 6
        self.eventTime = None   # nptime object
        self.alarmTime = None   # nptime object
        self.resource = None    # hyperlink String
        self.message = None     # user message String
        self.buildEventObject(event)

    # 이벤트 dictionary 를 이벤트 오브젝트로 변환
    def buildEventObject(self, event):
        self.name = event['name']
        self.day = event['day']
        self.eventTime = event['time']
        self.resource = event['resource']
        self.alarmTime = event['alarm']

    # 이벤트명 반환
    def getEventName(self):
        return self.name

    # 이벤트 발생 시간을 반환
    def getEventTime(self):
        return self.eventTime

    # 알람 시간을 반환
    def getAlarmTime(self):
        return self.alarmTime

    # 이벤트 리소스를 반환
    def getEventResource(self):
        return self.resource
