import datetime

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from json import loads

Base = declarative_base()

from . import events

from sqlalchemy.engine import create_engine


class Event(Base):
    __tablename__ = 'event'
    # sqlalchemy inheritance is annoying and I have elected to ignore it
    id = Column(Integer, primary_key=True)
    event = Column(String, index=True)
    block_number = Column(Integer, index=True, nullable=True)
    txhash = Column(String, index=True, nullable=True)
    data = Column(JSONB, nullable=True)
    time = Column(DateTime(), server_default=func.now(), index=True)

    @classmethod
    def from_event(cls, e, session):
        return cls(event=e.event, block_number=e.block_number, txhash=e.txhash,
                   data=loads(e.json))


class Assertion(Base):
    __tablename__ = 'assertion'
    id = Column(Integer, primary_key=True)
    event = Column(String, index=True)
    block_number = Column(Integer, index=True, nullable=True)
    txhash = Column(String, index=True, nullable=True)
    time = Column(DateTime(), server_default=func.now(), index=True)

    bounty_id = Column(Integer, ForeignKey('bounty.id'), index=True, nullable=True)
    address = Column(String, index=True)
    bid = Column(BigInteger)
    bounty = relationship('Bounty', back_populates='assertions')
    assertion = Column(Boolean, index=True)
    bounty_guid = Column(String, index=True)

    @classmethod
    def from_event(cls, e, session):
        bounty = session.query(Bounty).filter(Bounty.guid == e.bounty_guid).first()

        return cls(event=e.event, block_number=e.block_number, txhash=e.txhash,
                   bounty_id=bounty.id if bounty else None, address=e.author,
                   bid=e.bid, bounty_guid=e.bounty_guid)


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    event = Column(String, index=True)
    block_number = Column(Integer, index=True, nullable=True)
    txhash = Column(String, index=True, nullable=True)
    time = Column(DateTime(), server_default=func.now(), index=True)

    bounty_id = Column(Integer, ForeignKey('bounty.id'), index=True, nullable=True)
    bounty = relationship('Bounty', back_populates='votes')
    vote = Column(Boolean, index=True)
    address = Column(String, index=True)
    bounty_guid = Column(String, index=True)

    @classmethod
    def from_event(cls, e, session):
        bounty = session.query(Bounty).filter(Bounty.guid == e.bounty_guid).first()
        return cls(event=e.event, block_number=e.block_number, txhash=e.txhash,
                   bounty_id=bounty.id if bounty else None, address=e.voter,
                   vote=e.votes, bounty_guid=e.bounty_guid)

class Bounty(Base):
    __tablename__ = 'bounty'
    id = Column(Integer, primary_key=True)
    event = Column(String, index=True)
    block_number = Column(Integer, index=True, nullable=True)
    txhash = Column(String, index=True, nullable=True)
    time = Column(DateTime(), server_default=func.now(), index=True)

    guid = Column(String, index=True)
    md5 = Column(String, index=True)
    sha1 = Column(String, index=True)
    sha256 = Column(String, index=True)
    mimetype = Column(String)
    extended_type = Column(String)
    uri = Column(String)
    expiration = Column(DateTime())
    assertions = relationship('Assertion', cascade='all, delete-orphan')
    votes = relationship('Vote', cascade='all, delete-orphan')
    address = Column(String, index=True)
    amount = Column(BigInteger)

    @classmethod
    def from_event(cls, e, session):
        # in case this is out of order
        assertions = session.query(Assertion).filter(e.guid == Assertion.bounty_guid).all()
        votes = session.query(Vote).filter(e.guid == Vote.bounty_guid).all()

        return cls(event=e.event, block_number=e.block_number, txhash=e.txhash,
                   assertions=assertions, votes=votes, address=e.author,
                   guid=e.guid, md5=e.md5, sha1=e.sha1, sha256=e.sha256,
                   mimetype=e.mimetype, extended_type=e.extended_type,
                   uri=e.uri, expiration=datetime.datetime.fromtimestamp(int(e.expiration)),
                   amount=e.amount)

model_names = {cls.__tablename__: cls for cls in [Bounty, Vote, Assertion, Event]}


class EventHandler:
    def __init__(self, sql):
        self.engine = create_engine(sql)
        self.Session = sessionmaker(bind=self.engine)
        self.engine.connect()

    def handle_event(self, e):
        with self.session_scope() as session:
            cls = model_names.get(e.event, Event)
            obj = cls.from_event(e, session)
            session.add(obj)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
