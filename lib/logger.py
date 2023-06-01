import logging
import logging.handlers
import os
import time
from conf.configs import logs_dir


class LoggerBasic(object):
    """ 日志库 """
    @classmethod
    def logger_basic(cls):
        logger = logging.getLogger(__name__)
        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        # 创建文件目录
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.txt' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        # rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
        #                                                            maxBytes=1024 * 1024 * 50,
        #                                                            backupCount=5)
        rotatingFileHandler = logging.handlers.TimedRotatingFileHandler(filename=logfilepath,
                                                                        when='D',
                                                                        interval=30,
                                                                        encoding='utf-8')  # 按照时间进行切割.

        # 设置输出格式
        formatter = logging.Formatter('%(asctime)s -%(filename)s -%(levelname)s[line:%(lineno)d]: -%(message)s',
                                      '%Y-%m-%d %H:%M:%S %p')
        rotatingFileHandler.setFormatter(formatter)
        # 加这一行if判断最为重要，如果不加的话，会重复打印日志
        if not logger.handlers:
            # 控制台句柄
            console = logging.StreamHandler()
            console.setLevel(logging.NOTSET)
            console.setFormatter(formatter)
            # 添加内容到日志句柄中
            logger.addHandler(rotatingFileHandler)
            logger.addHandler(console)
            logger.setLevel(LEVELS['INFO'])

        return logger


logs = LoggerBasic().logger_basic()
