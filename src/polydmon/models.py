from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

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
    time = Column(DateTime(), server_default=func.now())

    @classmethod
    def from_event(cls, e):
        return cls(event=e.event, block_number=e.block_number, txhash=e.txhash,
                   data=e.data)


class Assertion(Base):
    __tablename__ = 'assertion'
    id = Column(Integer, primary_key=True)
    event = Column(String, index=True)
    block_number = Column(Integer, index=True, nullable=True)
    txhash = Column(String, index=True, nullable=True)
    data = Column(JSONB, nullable=True)
    time = Column(DateTime(), server_default=func.now())

    bounty_id = Column(Integer, ForeignKey('bounty.id'), index=True)
    address = Column(String, index=True)
    bid = Column(BigInteger)
    bounty = relationship('Bounty', back_populates='assertions')
    assertion = Column(Boolean, index=True, nullable=True)

    @classmethod
    def from_event(cls, e):
        pass


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    event = Column(String, index=True)
    block_number = Column(Integer, index=True, nullable=True)
    txhash = Column(String, index=True, nullable=True)
    data = Column(JSONB, nullable=True)
    time = Column(DateTime(), server_default=func.now())

    bounty_id = Column(Integer, ForeignKey('bounty.id'), index=True)
    bounty = relationship('Bounty', back_populates='votes')
    vote = Column(Boolean, index=True)

    @classmethod
    def from_event(cls, e):
        pass


class Bounty(Base):
    __tablename__ = 'bounty'
    id = Column(Integer, primary_key=True)
    event = Column(String, index=True)
    block_number = Column(Integer, index=True, nullable=True)
    txhash = Column(String, index=True, nullable=True)
    data = Column(JSONB, nullable=True)
    time = Column(DateTime(), server_default=func.now())

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

    @classmethod
    def from_event(cls, e):
        pass

model_names = {cls.__tablename__: cls for cls in [Bounty, Vote, Assertion, Event]}


class EventHandler:
    def __init__(self, sql):
        self.engine = create_engine(sql)
        self.Session = sessionmaker(bind=self.engine)
        self.engine.connect()

    def handle_event(self, e):
        with self.session_scope() as session:
            cls = model_names.get(e.event, Event)
            obj = cls.from_event(e)
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