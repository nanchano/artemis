from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import artemis.db as db
from artemis.schemas import CreateEvent, Event, UpdateEvent

session = db.connect()

router = APIRouter(prefix="/events", tags=["Events"], on_startup=[db.migrations])


def get_db():
    database = session()
    try:
        yield database
    finally:
        database.close()


@router.post("/")
def create_event(event: CreateEvent, session: Session = Depends(get_db)) -> Event:
    return db.db_create_event(event, session)


@router.get("/{event_id}")
def read_event(event_id: int, session: Session = Depends(get_db)) -> Event:
    try:
        return db.db_read_event(event_id, session)
    except db.NotFoundError:
        raise HTTPException(status_code=404, detail="event not found")


@router.put("/{event_id}")
def update_event(
    event_id: int, event: UpdateEvent, session: Session = Depends(get_db)
) -> Event:
    try:
        return db.db_update_event(event_id, event, session)
    except db.NotFoundError:
        raise HTTPException(status_code=404, detail="event not found")


@router.delete("/{event_id}")
def delete_event(event_id: int, session: Session = Depends(get_db)) -> Event:
    try:
        return db.db_delete_event(event_id, session)
    except db.NotFoundError:
        raise HTTPException(status_code=404, detail="event not found")
