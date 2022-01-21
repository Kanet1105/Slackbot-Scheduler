from eventhandler.context import Manager
from eventhandler.schedule import Scheduler
from message.log import logger
from multiprocessing import Queue
import sys
import time
import traceback


"""
리소스 설정과 관련된 전역 변수입니다. 모든 리소스는 settings 디렉토리 내에서 
'파일명.toml' 파일 형식으로 관리되며 프로그램 내에서 dict 타입으로 로드됩니다.
"""


KEY = './settings/key.toml'
SCHEDULE = './settings/schedule.toml'


# 매니저 스레드 초기화
def initManager():
    manager = Manager(eventQueue)
    manager.start()
    return manager


# 스케줄러 스레드 초기화
def initScheduler():
    scheduler = Scheduler(eventQueue, SCHEDULE)
    scheduler.start()
    return scheduler


"""
=====Work Flow=====
모든 이벤트 (slack api 이벤트 및 schedule 과 관련된 시간이 정해진 이벤트)는
eventhandler 패키지 내 context 모듈 안에 있는 manager thread 에 thread-safe 한 Queue
오브젝트를 통해 (type, content) tuple 타입으로 전달됩니다.

manager thread 는 이벤트에 대한 요청을 처리하면서 io-bound 한 작업들의 경우 
worker thread 또는 worker process 를 spawn 하는 방식으로 처리합니다.

만약 메세지를 반환해야 할 경우 message 패키지 내에 있는 user 모듈을 참조합니다.
"""


if __name__ == "__main__":
    try:
        """
        리소스 및 작업 스레드를 초기화합니다.
        예외 발생시 종류에 상관없이 프로그램 종료하고 log 파일에 traceback 메시지를
        기록하고 프로그램을 종료합니다.
        """

        eventQueue = Queue()
        manager = initManager()
        scheduler = initScheduler()
    except:
        print()
        logger.error(traceback.format_exc())
        sys.exit(1)

    while True:
        time.sleep(1)
