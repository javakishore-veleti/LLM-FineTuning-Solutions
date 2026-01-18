from typing import Optional, List
from sqlalchemy.orm import Session
from .db import DBManager

class EventDAO:
    def __init__(self, db_manager: DBManager, EventModel):
        self.dbm = db_manager
        self.Event = EventModel

    def create_event(self, data: dict):
        db: Session = self.dbm.get_session()
        try:
            ev = self.Event(
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

    def get_event(self, event_id: int):
        db = self.dbm.get_session()
        try:
            return db.query(self.Event).filter(self.Event.event_id == event_id).first()
        finally:
            db.close()

    def list_events(self) -> List:
        db = self.dbm.get_session()
        try:
            return db.query(self.Event).order_by(self.Event.created_at.desc()).all()
        finally:
            db.close()

    def update_event(self, event_id: int, data: dict):
        db = self.dbm.get_session()
        try:
            ev = db.query(self.Event).filter(self.Event.event_id == event_id).first()
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

    def delete_event(self, event_id: int) -> bool:
        db = self.dbm.get_session()
        try:
            ev = db.query(self.Event).filter(self.Event.event_id == event_id).first()
            if not ev:
                return False
            db.delete(ev)
            db.commit()
            return True
        finally:
            db.close()
