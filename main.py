import logging
from log_setup import setup_logging
from ftp_access import ftp_transfer


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug('Connecting to ftp')
    # return ftp_transfer('test')


if __name__ == "__main__":
    main()
