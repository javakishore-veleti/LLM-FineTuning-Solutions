from typing import List, Optional
from ..integrations.db import SessionLocal
from ..models.provider import Provider
from ..models.event_provider import EventProvider

# Providers

def create_provider(data: dict) -> Provider:
    db = SessionLocal()
    try:
        p = Provider(
            provider_type=data.get('provider_type'),
            display_name=data.get('display_name'),
            credentials_json=data.get('credentials_json'),
            is_active=data.get('is_active', True)
        )
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    finally:
        db.close()


def list_providers() -> List[Provider]:
    db = SessionLocal()
    try:
        return db.query(Provider).order_by(Provider.created_at.desc()).all()
    finally:
        db.close()


def get_provider(pid: int) -> Optional[Provider]:
    db = SessionLocal()
    try:
        return db.query(Provider).filter(Provider.provider_id == pid).first()
    finally:
        db.close()


def update_provider(pid: int, data: dict) -> Optional[Provider]:
    db = SessionLocal()
    try:
        p = db.query(Provider).filter(Provider.provider_id == pid).first()
        if not p:
            return None
        for k, v in data.items():
            if hasattr(p, k):
                setattr(p, k, v)
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    finally:
        db.close()


def delete_provider(pid: int) -> bool:
    db = SessionLocal()
    try:
        p = db.query(Provider).filter(Provider.provider_id == pid).first()
        if not p:
            return False
        db.delete(p)
        db.commit()
        return True
    finally:
        db.close()

# EventProvider associations

def add_provider_to_event(event_id: int, provider_id: int, cfg: Optional[dict] = None) -> EventProvider:
    db = SessionLocal()
    try:
        ep = EventProvider(event_id=event_id, provider_id=provider_id, provider_config_json=(cfg and json.dumps(cfg)) or None)
        db.add(ep)
        db.commit()
        db.refresh(ep)
        return ep
    finally:
        db.close()


def list_event_providers(event_id: int) -> List[EventProvider]:
    db = SessionLocal()
    try:
        return db.query(EventProvider).filter(EventProvider.event_id == event_id).all()
    finally:
        db.close()


def remove_event_provider(ep_id: int) -> bool:
    db = SessionLocal()
    try:
        ep = db.query(EventProvider).filter(EventProvider.id == ep_id).first()
        if not ep:
            return False
        db.delete(ep)
        db.commit()
        return True
    finally:
        db.close()
