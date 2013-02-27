#    coding: UTF-8
#    User: haku
#    Date: 13-2-27
#    Time: 下午11:23
#
import logging.config,os

class Logger:

    log_instance = None

    @staticmethod
    def InitLogConf():
        if os.path.isfile("logging.conf"):
            file_path = "logging.conf"
        else :
            file_path = os.path.dirname(__file__) + "/logging.conf"
        print 'load logging configure from ' + file_path
        Logger.log_instance = logging.config.fileConfig(file_path)

    @staticmethod
    def GetLogger(name = ""):
        if Logger.log_instance == None:
            Logger.InitLogConf()
        Logger.log_instance = logging.getLogger(name)
        return Logger.log_instance

if __name__ == "__main__":
    logger = Logger.GetLogger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")

    logHello = Logger.GetLogger("c1")
    logHello.info("Hello world!")