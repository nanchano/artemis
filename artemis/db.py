from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from artemis.schemas import CreateEvent, Event, UpdateEvent

DATABASE_URL = "sqlite:///events.db?_journal=WAL&_timeout=5000&_fk=true"
engine = create_engine(DATABASE_URL)


class NotFoundError(Exception):
    pass


class Base(DeclarativeBase):
    pass


class DBEvent(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    category: Mapped[str]
    location: Mapped[str]
    publisher: Mapped[str]
    start_ts: Mapped[datetime]
    end_ts: Mapped[datetime]


def connect() -> sessionmaker[Session]:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def migrations():
    Base.metadata.create_all(bind=engine)


def db_find_event(event_id: int, session: Session) -> DBEvent:
    db_event = session.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not db_event:
        raise NotFoundError("event not found")
    return db_event


def db_create_event(event: CreateEvent, session: Session) -> Event:
    db_event = DBEvent(**event.model_dump())
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return Event(**db_event.__dict__)


def db_read_event(event_id: int, session: Session) -> Event:
    db_event = db_find_event(event_id, session)
    return Event(**db_event.__dict__)


def db_update_event(event_id: int, event: UpdateEvent, session: Session) -> Event:
    db_event = db_find_event(event_id, session)
    for key, value in event.model_dump().items():
        setattr(db_event, key, value) if value else None
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return Event(**db_event.__dict__)


def db_delete_event(event_id: int, session: Session) -> Event:
    db_event = db_find_event(event_id, session)
    session.delete(db_event)
    session.commit()
    return Event(**db_event.__dict__)
