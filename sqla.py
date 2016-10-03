from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from properties import get_property
import logging

SQLA_CONNECTION = get_property('properties.json', 'connection_string')


def get_engine():
    return create_engine(SQLA_CONNECTION)


def get_pending():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    meta = MetaData()
    meta.reflect(bind=engine)
    pending_records = Table('PendingExtracts',
                            meta,
                            autoload=True,
                            autoload_with=get_engine())

    return session.query(pending_records).first()


def test():
    Session = sessionmaker(bind=get_engine())
    session = Session()
    pending = get_pending()
    return session.query(pending).first()


if __name__ == "__main__":
    print(get_pending())
