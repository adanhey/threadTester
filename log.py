import datetime
import logging
import os


class TestLogger:
    def __init__(self, log_sign, log_clean=None):
        self.log_sign = log_sign
        if log_clean:
            self.clean_log()
        self.now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.logger = logging.getLogger("uweb_reference")
        self.logger.setLevel(logging.DEBUG)
        self.file_url = logging.FileHandler(f"./{self.now_time}{self.log_sign}.log", mode="a+",
                                            encoding="utf8")
        self.logger.addHandler(self.file_url)

    def log_event(self, title, data):
        self.logger.debug(f"-->%s" % datetime.datetime.now())
        self.logger.debug(f"%s：%s" % (title, data))

    def clean_log(self):
        for root, dirs, files in os.walk("./"):
            for file in files:
                if self.log_sign in str(file):
                    os.remove(file)
