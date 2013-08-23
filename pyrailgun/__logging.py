#    coding: UTF-8
#    User: haku
#    Date: 13-2-27
#    Time: 下午11:23
#
import logging.config, os


class Logger:
    log_instance = None

    @staticmethod
    def InitLogConf():
        """
        >>> Logger.getLogger() # doctest: +ELLIPSIS
        load logging configure from logging.conf
        <logging.RootLogger object at ...>
        """

        if os.path.isfile("logging.conf"):
            file_path = "logging.conf"
        else:
            file_path = os.path.dirname(__file__) + "/logging.conf"
        print 'load logging configure from ' + file_path
        Logger.log_instance = logging.config.fileConfig(file_path)

    @staticmethod
    def getLogger(name=""):
        """
        :param name: string
        :return: Logger


        doctest:
        >>> Logger.getLogger().debug("debug message") # doctest: +ELLIPSIS
        [...] (DEBUG) : debug message
        >>> Logger.getLogger().info("info message") # doctest: +ELLIPSIS
        [...] (INFO) : info message
        >>> Logger.getLogger("c1").debug("customed message") # doctest: +ELLIPSIS
        [...] (DEBUG) : customed message
        """
        if Logger.log_instance == None:
            Logger.InitLogConf()
        Logger.log_instance = logging.getLogger(name)
        return Logger.log_instance


if __name__ == "__main__":
    import doctest

    doctest.testmod()
