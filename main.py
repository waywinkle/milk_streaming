import logging
from log_setup import setup_logging
from ftp_access import ftp_transfer
from sqla import get_next_extract
from time import strftime


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug('Connecting to ftp')
    extract = get_next_extract()
    file_name = str(extract['season']) + '_' + str(extract['shift']) + '_' + strftime("%Y%m%d%H%m%S")
    return ftp_transfer(extract['xml_output'], file_name)


if __name__ == "__main__":
    main()
