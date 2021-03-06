import logging
from log_setup import setup_logging
from ftp_access import ftp_transfer
from sqla import check_next_extract, complete_shift
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
        if not extract:
            logger.debug('No pending extracts')
        elif extract['result']:
            logger.debug('valid extract so upload to ftp')
            file_name = str(extract['season']) + '_' + str(extract['shift']) + '_' + strftime("%Y%m%d%H%m%S")
            ftp_transfer(extract['xml_output'], file_name)
            complete_shift(extract['shift'], extract['season'])
            send_mail('Shift: {shift}, season: {season} was sent successfully'.format(shift=extract['shift'],
                                                                                      season=extract['season']),
                      'Send success')
        else:
            send_mail('Shift: {shift}, season: {season} was unable to be sent'.format(shift=extract['shift'],
                                                                                      season=extract['season']),
                      'Send failure')
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        e = ''.join(line for line in lines)
        if extract['shift'] and extract['season']:
            message = 'Shift: {shift}, season: {season} failed on processing \n'.format(shift=extract['shift'],
                                                                                        season=extract['season'])
        else:
            message = 'MSA error on processing.'

        message += e
        logger.exception('Error occurred during processing')
        send_mail(message, 'Send error')


if __name__ == "__main__":
    main()
