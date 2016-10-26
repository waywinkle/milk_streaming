from ftplib import FTP
from properties import get_all_properties
import logging
from io import BytesIO
PROPERTIES_FILE = 'properties.json'


def ftp_transfer(string_to_send, file_name):
    logger = logging.getLogger(__name__)
    prop = get_all_properties(PROPERTIES_FILE)

    ftp = FTP(prop['ftp_address'])
    ftp.set_debuglevel(prop['ftp_debug'])
    response = ftp.login(prop['ftp_username'],
                         prop['ftp_password'])
    logger.debug('ftp login response : {response}'.format(response=response))

    ftp.set_pasv(False)

    ftp_command = 'STOR ' + prop['ftp_directory'] + '\\' + file_name + '.xml'
    logging.info('ftp command : {ftp_command}'.format(ftp_command=ftp_command))
    file = create_file_from_text(string_to_send)
    logging.debug('file : {file}'.format(file=file))

    response = ftp.storbinary(ftp_command, file)
    logger.info('transfered file to server : {response}'.format(response=response))

    ftp.quit()


def create_file_from_text(text):
    return BytesIO(text.encode('UTF-8'))
