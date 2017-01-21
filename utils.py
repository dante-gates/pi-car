import logging


class Logging:
    _format = '[%(asctime)s][%(levelname)-8s][%(module)-9s][%(msg)s]'

    @classmethod
    def get_logger(cls, name):
        logger = logging.getLogger(__name__)
        Logging.format_logger(logger)
        logger.setLevel('DEBUG')
        return logger

    @classmethod
    def format_logger(cls, logger):
        if not logger.handlers:
            hdl = logging.StreamHandler()
            fmt = logging.Formatter(cls._format)
            hdl.setFormatter(fmt)
            logger.addHandler(hdl)
