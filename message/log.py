
"""
========== loger ==========
Thread safe 하므로 multithreaded 프로그램 내에서 안전하게 로깅할 수 있습니다.

========== 사용처 ==========
- __main__
- eventhandler.context.Manager
- eventhandler.schedule.Scheduler
"""


import logging


# system logger
systemLogger = logging.getLogger()
systemLogger.setLevel(logging.ERROR)
writer = logging.FileHandler("./log.txt")
formatter = logging.Formatter("[%(asctime)s]: %(message)s\n")
writer.setFormatter(formatter)
systemLogger.addHandler(writer)
