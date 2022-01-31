
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
    def __init__(self, eventQueue, app, alarmChannel):
        super().__init__()
        self.daemon = True
        self.app = app
        self.alarmChannel = alarmChannel
        self.eventQueue = eventQueue

    # 스케줄 알람 메시지
    def handleAlarm(self, eventObject):
        eventName = eventObject.getEventName()
        eventTime = eventObject.getEventTime()
        alarmTime = eventObject.getAlarmTime()
        resource = eventObject.getEventResource()
        message = response.User.alarm.format(
            name=eventName,
            interval=(eventTime - alarmTime).seconds // 60,
            resource=resource
        )
        response.User.sendMessage(self.app, self.alarmChannel, message)

    def handleFile(self, eventObject):
        for file in eventObject["files"]:
            name = file["name"]
            url = file["url_private_download"]
            dataString = name + "\t" + url + "\n"
            self.saveData(dataString)

    def handleLink(self, eventObject):
        self.saveData(eventObject["text"] + "\n")

    def saveData(self, data):
        with open("./upload.txt", "a+", encoding="utf-8") as file:
            file.write(data)

    def classifyEvent(self, event):
        eventType, eventObject = event

        """
        ========== 이벤트 분류 (eventType) ==========
        "alarm" << 알림
        "file" << 파일 업로드
        "link" << 링크 업로드
        """

        if eventType == "alarm":
            self.handleAlarm(eventObject)
        elif eventType == "file":
            self.handleFile(eventObject)
        elif eventType == "link":
            self.handleLink(eventObject)

    def run(self):
        while True:
            try:
                event = self.eventQueue.get()
                self.classifyEvent(event)
                time.sleep(0.1)
            except:
                print(response.Console.errorThread.format(name="Manager"))
                log.systemLogger.error(traceback.format_exc())
