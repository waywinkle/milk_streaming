import logging
from log_setup import setup_logging
from ftp_access import ftp_transfer
from sqla import check_next_extract
from time import strftime
from mail import send_mail
import sys
import traceback


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug('extracting from db')
    try:
        extract = check_next_extract()
        if extract['result']:
            logger.debug('valid extract so upload to ftp')
            file_name = str(extract['season']) + '_' + str(extract['shift']) + '_' + strftime("%Y%m%d%H%m%S")
            ftp_transfer(extract['xml_output'], file_name)
        else:
            send_mail('Shift: {shift}, season: {season} was unable to be sent'.format(shift=extract['shift'],
                                                                                      season=extract['season']),
                      'Send failure')
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        e = ''.join(line for line in lines)
        message = 'Shift: {shift}, season: {season} failed on processing \n'.format(shift=extract['shift'],
                                                                                  season=extract['season'])
        message += e
        logger.exception('Error occurred during processing')
        send_mail(message, 'Send error')


if __name__ == "__main__":
    main()
