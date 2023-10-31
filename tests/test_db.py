from datetime import datetime, timedelta
from typing import Generator

import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

import artemis.db as db
import artemis.schemas as schemas

DATABASE_URL = "sqlite:///:memory:"
START = datetime.now()
END = START + timedelta(days=1)
CREATE_EVENT = schemas.CreateEvent(
    name="Test Event",
    description="Test Description",
    category="Test Category",
    location="Test Location",
    publisher="Test Publisher",
    start_ts=START,
    end_ts=END,
)

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session() -> Generator[Session, None, None]:
    db.Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()

    yield db_session

    db_session.close()
    db.Base.metadata.drop_all(bind=engine)


def test_db_create_event(session: Session) -> None:
    """Tests the db_create_event function.
    Expected: create the event keeping the attributes from the payload"""
    event = db.db_create_event(CREATE_EVENT, session)
    assert event.name == "Test Event"
    assert event.description == "Test Description"
    assert event.category == "Test Category"
    assert event.location == "Test Location"
    assert event.publisher == "Test Publisher"
    assert event.start_ts == START
    assert event.end_ts == END


def test_db_read_event(session: Session) -> None:
    """Tests the db_read_event function.
    Expected: grab the event from the DB and return the atrtibutes as they are"""
    event = db.db_create_event(CREATE_EVENT, session)
    event_id = event.id

    event = db.db_read_event(event_id, session)
    assert event.name == "Test Event"
    assert event.description == "Test Description"
    assert event.category == "Test Category"
    assert event.location == "Test Location"
    assert event.publisher == "Test Publisher"
    assert event.start_ts == START
    assert event.end_ts == END


def test_db_read_event_not_found(session: Session) -> None:
    """Tests the db_read_event function when the event does not exist.
    Expected: raise db.NotFoundError"""
    with pytest.raises(db.NotFoundError):
        db.db_read_event(1, session)


def test_db_update_event(session: Session) -> None:
    """Tests the db_update_event function.
    Expected: change attributes based on the UpdateEvent schema.
    If the attribute is not passed or is None, keep it as is."""
    event = db.db_create_event(CREATE_EVENT, session)
    event_id = event.id

    event = db.db_update_event(
        event_id, schemas.UpdateEvent(name="New Name", description=None), session
    )
    assert event.name == "New Name"
    assert event.description == "Test Description"
    assert event.category == "Test Category"
    assert event.location == "Test Location"
    assert event.publisher == "Test Publisher"
    assert event.start_ts == START
    assert event.end_ts == END


def test_db_update_event_not_found(session: Session) -> None:
    """Tests the db_update_event function when the event does not exist.
    Expected: raise db.NotFoundError"""
    with pytest.raises(db.NotFoundError):
        db.db_update_event(1, schemas.UpdateEvent(name="New Name"), session)


def test_db_delete_event(session: Session) -> None:
    """Tests the db_delete_event function.
    Expected: delete the event given an ID, while keeping the deleted event on state.
    Should raise db.NotFoundError when trying to retrieve it after it's deleted"""
    event = db.db_create_event(CREATE_EVENT, session)
    event_id = event.id

    event = db.db_delete_event(event_id, session)
    assert event.id == event_id
    assert event.name == "Test Event"
    assert event.description == "Test Description"
    assert event.category == "Test Category"
    assert event.location == "Test Location"
    assert event.publisher == "Test Publisher"
    assert event.start_ts == START
    assert event.end_ts == END

    with pytest.raises(db.NotFoundError):
        db.db_read_event(event_id, session)


def test_db_delete_event_not_found(session: Session) -> None:
    """Tests the db_delete_event function when the event does not exist.
    Expected: raise db.NotFoundError"""
    with pytest.raises(db.NotFoundError):
        db.db_delete_event(1, session)
