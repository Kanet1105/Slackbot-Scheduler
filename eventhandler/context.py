
"""
========== Manager ==========
모든 event 요청 처리 함수를 관리하는 context manager 입니다.
eventQueue 로 들어오는 모든 이벤트 객체들에 대해 처리하고 값을 반환합니다.
"""


import datetime
from message import log, response
from threading import Thread
import time
import traceback


class Manager(Thread):
    def __init__(self, eventQueue):
        super().__init__()
        self.daemon = True
        self.eventQueue = eventQueue

    def run(self):
        while True:
            try:
                event = self.eventQueue.get()
                time.sleep(1)
            except:
                print(response.Console.errorThread.format(name="Scheduler"))
                log.logger.error(traceback.format_exc())
