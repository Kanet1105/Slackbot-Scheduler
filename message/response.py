
"""
========== Console ==========
콘솔 로그 메시지를 모아 놓은 클래스입니다.
headless interpreter 로 서버를 실행시킬 시 보이지 않습니다 (권장하지 않음).

========== User ==========
유저 응답 메시지를 모아 놓은 클래스입니다.
"""


class Console:
    # errors
    errorThread = "An error occurred while running the {name} thread."

    # info
    initThread = "{name} thread successfully initialized."


class User:
    alarm = "{name} 시작까지 {interval} 분 남았습니다.\n" \
            "{resource}"

    @staticmethod
    def sendMessage(app, message):
        pass
