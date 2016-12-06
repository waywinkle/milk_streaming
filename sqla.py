from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from properties import get_property
import logging

logger = logging.getLogger(__name__)


def get_engine():
    return create_engine(get_property('properties.json', 'connection_string'))


def get_next_pending():
    logger.debug('Connect to DB and reflect PendingExtracts')
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    meta = MetaData()
    meta.reflect(bind=engine)
    pending_records = Table('PendingExtracts',
                            meta,
                            autoload=True,
                            autoload_with=get_engine())
    record = session.query(pending_records).first()
    logger.info('Extracted records {row}'.format(row=record))

    return record


def extract_xml(shift, season):
    logger.info('Extracting xml for {shift}, {season}'.format(shift=shift, season=season))
    conn = get_engine().raw_connection()
    with conn.cursor(as_dict=True) as cursor:
        cursor.callproc('GetExtract', (shift, season,))
        for row in cursor:
            results = row
    conn.commit()

    return results


def complete_shift(shift, season):
    logger.info('Closing shift for {shift}, {season}'.format(shift=shift, season=season))
    conn = get_engine().raw_connection()
    with conn.cursor(as_dict=True) as cursor:
        cursor.callproc('CloseUnloadQuantities', (shift, season,))
        conn.commit()


def fail_shift(shift, season):
    logger.info('Failing shift for {shift}, {season}'.format(shift=shift, season=season))
    conn = get_engine().raw_connection()
    with conn.cursor(as_dict=True) as cursor:
        cursor.callproc('FailUnloadQuantities', (shift, season,))
        conn.commit()


def get_next_extract():
    next_shift = get_next_pending()
    shift = {'shift': next_shift[0], 'season': next_shift[1]}
    shift.update(extract_xml(shift['shift'], shift['season']))

    return shift


def check_next_extract():
    next_shift = get_next_pending()
    shift = {'shift': next_shift[0], 'season': next_shift[1]}
    send_failure = next_shift[2]
    if send_failure == 1:
        fail_shift(shift['shift'], shift['season'])
        shift['result'] = False
        return shift
    else:
        shift.update(extract_xml(shift['shift'], shift['season']))
        shift['result'] = True
        return shift


if __name__ == "__main__":
    print(extract_xml('28', '2017'))
