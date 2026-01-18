from typing import List, Optional
from ..integrations.db import SessionLocal
from ..models.event import Event


def create_event(data: dict) -> Event:
    db = SessionLocal()
    try:
        ev = Event(
            event_name=data.get('event_name'),
            event_description=data.get('event_description'),
            source_url=data.get('source_url'),
            source_location_type=data.get('source_location_type', 'http_url'),
            is_active=data.get('is_active', True)
        )
        db.add(ev)
        db.commit()
        db.refresh(ev)
        return ev
    finally:
        db.close()


def get_event(event_id: int) -> Optional[Event]:
    db = SessionLocal()
    try:
        return db.query(Event).filter(Event.event_id == event_id).first()
    finally:
        db.close()


def list_events() -> List[Event]:
    db = SessionLocal()
    try:
        return db.query(Event).order_by(Event.created_at.desc()).all()
    finally:
        db.close()


def delete_event(event_id: int) -> bool:
    db = SessionLocal()
    try:
        ev = db.query(Event).filter(Event.event_id == event_id).first()
        if not ev:
            return False
        db.delete(ev)
        db.commit()
        return True
    finally:
        db.close()


def update_event(event_id: int, data: dict) -> Optional[Event]:
    db = SessionLocal()
    try:
        ev = db.query(Event).filter(Event.event_id == event_id).first()
        if not ev:
            return None
        for k, v in data.items():
            if hasattr(ev, k):
                setattr(ev, k, v)
        db.add(ev)
        db.commit()
        db.refresh(ev)
        return ev
    finally:
        db.close()
