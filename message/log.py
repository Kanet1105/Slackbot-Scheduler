import logging

'''
파이썬 로깅 모듈입니다.
Thread safe 하므로 multithreaded 프로그램 내에서 안전하게 로깅할 수 있습니다.
    - main
    - eventhandler.context.Manager
    - eventhandler.schedule.Scheduler
'''

# create a logger
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# write a log to the file
writer = logging.FileHandler('./log.txt')
formatter = logging.Formatter('[%(asctime)s]: %(message)s\n')
writer.setFormatter(formatter)
logger.addHandler(writer)
