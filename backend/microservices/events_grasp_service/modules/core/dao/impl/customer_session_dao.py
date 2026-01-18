from sqlalchemy.orm import Session
from typing import Optional

class CustomerSessionDAO:
    def __init__(self, dbm, CustomerSessionModel):
        self.dbm = dbm
        self.Model = CustomerSessionModel

    def create_session(self, data: dict):
        db: Session = self.dbm.get_session()
        try:
            s = self.Model(customer_id=data.get('customer_id'), token=data.get('token'), expires_at=data.get('expires_at'))
            db.add(s)
            db.commit()
            db.refresh(s)
            return s
        finally:
            db.close()

    def get_by_token(self, token: str):
        db = self.dbm.get_session()
        try:
            return db.query(self.Model).filter(self.Model.token == token).first()
        finally:
            db.close()

    def delete_session(self, session_id: int) -> bool:
        db = self.dbm.get_session()
        try:
            s = db.query(self.Model).filter(self.Model.session_id == session_id).first()
            if not s:
                return False
            db.delete(s)
            db.commit()
            return True
        finally:
            db.close()
