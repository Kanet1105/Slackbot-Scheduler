
"""
========== Crawler ==========
대상 웹사이트에 새로 올라온 게시물을 업로드해주는 크롤러 스레드입니다.
"""


from message import log, response
import requests
from threading import Thread
import time
import toml
import traceback


class Crawler(Thread):
    def __init__(self, eventQueue, urlPath):
        super().__init__()
        self.daemon = True
        self.eventQueue = eventQueue
        self.urlPath = urlPath
        self.targetUrl = self.getTargetUrl()
        self.posts = set()

    def getTargetUrl(self):
        with open(self.urlPath, "r", encoding="utf-8") as file:
            url = toml.load(file)
            return url

    def scrape(self):
        pass

    def run(self):
        while True:
            try:
                self.scrape()
                time.sleep(60)
            except:
                print(response.Console.errorThread.format(name="Crawler"))
                log.logger.error(traceback.format_exc())
