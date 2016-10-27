import smtplib
from email.mime.text import MIMEText
from properties import get_all_properties
import logging

PROPERTIES_FILE = 'properties.json'


def send_mail(content, mail_type):
    logger = logging.getLogger(__name__)
    properties = get_all_properties(PROPERTIES_FILE)
    msg = MIMEText(content)
    subject = 'MSA to Madcap upload - {mail_type}'.format(mail_type=mail_type)
    logger.info('Sending mail : {mail}'.format(mail=subject))
    msg['Subject'] = subject
    msg['From'] = properties['from_email']
    msg['To'] = properties['error_email']

    s = smtplib.SMTP(properties['smtp_server'])
    s.send_message(msg)
    s.quit()


if __name__ == "__main__":
    print(send_mail('test asdf', 'error'))
