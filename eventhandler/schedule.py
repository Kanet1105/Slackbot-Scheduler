
"""
========== Scheduler ==========
schedule.toml 파일을 참조하고 시간 역순으로 sort 해서 eventStack 에 추가합니다.
시간 역순으로 sorting 하기 때문에 schedule.toml 파일에 스케쥴을 추가할 때 시간순으로 넣을 필요 없습니다.
event stack 의 제일 마지막 오브젝트부터 pop() 하고 eventQueue 에 push 해주는 역할을 해 주는 thread 입니다.
"""


import datetime
from message import log, response
from threading import Thread
import time
import toml
import traceback


class Scheduler(Thread):
    def __init__(self, eventQueue, schedulePath):
        super().__init__()
        self.daemon = True
        self.eventQueue = eventQueue
        self.schedule = self.loadSchedule(schedulePath)
        self.eventStack = self.buildEventStack()
        print(self.eventStack)

    # 총 스케줄을 로드하고 리스트 형태로 반환
    def loadSchedule(self, schedulePath):
        with open(schedulePath, "r", encoding="utf-8") as file:
            schedule = toml.load(file)
            return schedule['Schedule']

    # 요일에 맞는 스케줄을 리스트로 반환
    def buildEventStack(self):
        weekday, now = self.getNow()
        eventToday = [event for event in self.schedule if weekday in event['day']]
        eventStack = []

        # 오늘의 이벤트를 가져오고 시간을 datetime.time 오브젝트로 변경해서 저장
        for event in eventToday:
            hour, minute = map(int, event['time'].split(":"))
            event['time'] = datetime.time(hour=hour, minute=minute)

            # 이미 지나간 이벤트의 경우 eventStack 에 추가하지 않음
            # datetime.time 오브젝트끼리의 크기 비교 값 예시
            # 12:40 < 12:55 => True
            # 12:40 < 12:40 => True
            # 12:40 < 12:30 => False
            # 더 빠른 시간이 더 작은 값을 가짐
            if event['time'] > now:
                eventStack.append(event)

        # 이벤트가 있을 때만 시간 역순으로 정렬
        if eventStack:
            eventStack.sort(key=lambda item: item['time'], reverse=True)
        return eventStack

    # 현재 요일과 시간을 (요일, 시간) 투플 형태로 반환
    def getNow(self):
        now = datetime.datetime.now()
        weekday = now.weekday()
        timeFormat = datetime.time(hour=now.hour, minute=now.minute)
        return weekday, timeFormat

    # 이벤트 스택의 가장 위에 있는 이벤트와 현재 시간을 비교해서 같다면 이벤트를 발생
    def alarm(self, now):
        # 이벤트 없을 시 반환
        if not self.eventStack:
            return

        # 이벤트 발생 시 eventQueue 에 추가
        eventTime = self.eventStack[-1]['time']
        if eventTime == now:
            self.eventQueue.put(self.eventStack.pop())

    def run(self):
        while True:
            try:
                weekday, now = self.getNow()
                self.alarm(now)
                time.sleep(1)
            except:
                print(response.Console.errorThread.format(name="Scheduler"))
                log.logger.error(traceback.format_exc())
                break
