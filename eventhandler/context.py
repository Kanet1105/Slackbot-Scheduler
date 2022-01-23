
"""
========== Manager ==========
모든 event 요청 처리 함수를 관리하는 context manager 입니다.
eventQueue 로 들어오는 모든 이벤트 객체들에 대해 처리하고 값을 반환합니다.
"""


from message import log, response
from threading import Thread
import time
import traceback


class Manager(Thread):
    def __init__(self, eventQueue):
        super().__init__()
        self.daemon = True
        self.eventQueue = eventQueue

    def handleAlarm(self):
        pass

    def classifyEvent(self, event):
        eventType, eventObject = event

        """
        ========== 이벤트 분류 (eventType) ==========
        "alarm" << 알림
        "update" << 새 공지사항 알림
        """

        if eventType == "alarm":
            self.handleAlarm()

    def run(self):
        while True:
            try:
                event = self.eventQueue.get()
                self.classifyEvent(event)
                time.sleep(1)
            except:
                print(response.Console.errorThread.format(name="Scheduler"))
                log.logger.error(traceback.format_exc())
