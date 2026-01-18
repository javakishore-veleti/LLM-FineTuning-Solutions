import json
from typing import List, Optional
from .db import DBManager

class ProviderDAO:
    def __init__(self, db_manager: DBManager, ProviderModel, EventProviderModel):
        self.dbm = db_manager
        self.Provider = ProviderModel
        self.EventProvider = EventProviderModel

    def create_provider(self, data: dict):
        db = self.dbm.get_session()
        try:
            p = self.Provider(
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

    def list_providers(self) -> List:
        db = self.dbm.get_session()
        try:
            return db.query(self.Provider).order_by(self.Provider.created_at.desc()).all()
        finally:
            db.close()

    def get_provider(self, pid: int):
        db = self.dbm.get_session()
        try:
            return db.query(self.Provider).filter(self.Provider.provider_id == pid).first()
        finally:
            db.close()

    def update_provider(self, pid: int, data: dict):
        db = self.dbm.get_session()
        try:
            p = db.query(self.Provider).filter(self.Provider.provider_id == pid).first()
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

    def delete_provider(self, pid: int) -> bool:
        db = self.dbm.get_session()
        try:
            p = db.query(self.Provider).filter(self.Provider.provider_id == pid).first()
            if not p:
                return False
            db.delete(p)
            db.commit()
            return True
        finally:
            db.close()

    # EventProvider associations
    def add_provider_to_event(self, event_id: int, provider_id: int, cfg: Optional[dict] = None):
        db = self.dbm.get_session()
        try:
            ep = self.EventProvider(event_id=event_id, provider_id=provider_id, provider_config_json=(cfg and json.dumps(cfg)) or None)
            db.add(ep)
            db.commit()
            db.refresh(ep)
            return ep
        finally:
            db.close()

    def list_event_providers(self, event_id: int) -> List:
        db = self.dbm.get_session()
        try:
            return db.query(self.EventProvider).filter(self.EventProvider.event_id == event_id).all()
        finally:
            db.close()

    def remove_event_provider(self, ep_id: int) -> bool:
        db = self.dbm.get_session()
        try:
            ep = db.query(self.EventProvider).filter(self.EventProvider.id == ep_id).first()
            if not ep:
                return False
            db.delete(ep)
            db.commit()
            return True
        finally:
            db.close()
