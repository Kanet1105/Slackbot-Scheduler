
"""
========== Scheduler ==========
schedule.toml 파일을 참조하고 시간 역순으로 sort 해서 eventStack 에 추가합니다.
시간 역순으로 sorting 하기 때문에 schedule.toml 파일에 스케쥴을 추가할 때 시간순으로 넣을 필요 없습니다.
event stack 의 제일 마지막 오브젝트부터 pop() 하고 eventQueue 에 push 해주는 역할을
해 주는 thread 입니다.
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
        print(self.schedule)
        self.eventStack = self.buildEventStack()

    def loadSchedule(self, schedulePath):
        with open(schedulePath) as file:
            schedule = toml.load(file)
            return schedule

    def buildEventStack(self):
        weekday, _ = self.getNow()
        eventStack = []
        return eventStack

    def getNow(self):
        now = datetime.datetime.now()
        return now.weekday(), now.time()

    def run(self):
        while True:
            try:
                weekday, now = self.getNow()
                print(weekday, now)
                time.sleep(1)
            except:
                print(response.Console.errorThread.format(name="Scheduler"))
                log.logger.error(traceback.format_exc())
                break
