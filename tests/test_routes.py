from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

import artemis.db as db
import artemis.routes as routes
from artemis.main import app

client = TestClient(app)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

START_TS = datetime.now()
START = START_TS.strftime("%Y-%m-%dT%H:%S:%M")
END = (START_TS + timedelta(days=1)).strftime("%Y-%m-%dT%H:%S:%M")
CREATE_EVENT = {
    "name": "Test Event",
    "description": "Test Description",
    "category": "Test Category",
    "location": "Test Location",
    "publisher": "Test Publisher",
    "start_ts": START,
    "end_ts": END,
}


def setup_function() -> None:
    db.Base.metadata.create_all(bind=engine)


def teardown_function() -> None:
    db.Base.metadata.drop_all(bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[routes.get_db] = override_get_db


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


def test_create_event():
    """Tests the create_event endpoint.
    Expected: create the event on the DB and return the same content as a JSON"""
    response = client.post("/events/", json=CREATE_EVENT)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Event"
    assert data["description"] == "Test Description"
    assert data["category"] == "Test Category"
    assert data["location"] == "Test Location"
    assert data["publisher"] == "Test Publisher"
    assert data["start_ts"] == START
    assert data["end_ts"] == END


def test_read_event():
    """Tests the read_event endpoint.
    Expected: read the event from the DB and return the same content as a JSON"""
    response = client.post("/events/", json=CREATE_EVENT)
    assert response.status_code == 200, response.text
    event_id = response.json()["id"]

    response = client.get(f"/events/{event_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["id"] == event_id
    assert data["name"] == "Test Event"
    assert data["description"] == "Test Description"
    assert data["category"] == "Test Category"
    assert data["location"] == "Test Location"
    assert data["publisher"] == "Test Publisher"
    assert data["start_ts"] == START
    assert data["end_ts"] == END


def test_read_event_not_found():
    """Tests the read_event endpoint when the event does not exist.
    Expected: return 404 status code"""
    response = client.get(f"/events/1")
    assert response.status_code == 404, response.text


def test_update_event():
    """Tests the update_event endpoint.
    Expected: Update the properties of a given event by ID.
    If some properties are not present, keep the original ones"""
    response = client.post("/events/", json=CREATE_EVENT)
    assert response.status_code == 200, response.text
    event_id = response.json()["id"]

    response = client.put(f"/events/{event_id}", json={"name": "Updated Event"})
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["id"] == event_id
    assert data["name"] == "Updated Event"
    assert data["description"] == "Test Description"
    assert data["category"] == "Test Category"
    assert data["location"] == "Test Location"
    assert data["publisher"] == "Test Publisher"
    assert data["start_ts"] == START
    assert data["end_ts"] == END


def test_read_update_not_found():
    """Tests the update_event endpoint when the event does not exist.
    Expected: return 404 status code"""
    response = client.put(f"/events/1", json={"name": "New Name"})
    assert response.status_code == 404, response.text


def test_delete_event():
    """Tests the delete_event endpoint.
    Expected: Delete the event from the DB given an ID."""
    response = client.post("/events/", json=CREATE_EVENT)
    assert response.status_code == 200, response.text
    event_id = response.json()["id"]

    response = client.delete(f"/events/{event_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == event_id

    # Try to get the deleted event
    response = client.get(f"/events/{event_id}")
    assert response.status_code == 404, response.text


def test_delete_event_not_found():
    """Tests the delete_event endpoint when the event does not exist.
    Expected: return 404 status code"""
    response = client.delete(f"/events/1")
    assert response.status_code == 404, response.text
