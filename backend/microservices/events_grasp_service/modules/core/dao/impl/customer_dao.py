from sqlalchemy.orm import Session
from typing import Optional

class CustomerDAO:
    def __init__(self, dbm, CustomerModel):
        self.dbm = dbm
        self.Customer = CustomerModel

    def create_customer(self, data: dict):
        db: Session = self.dbm.get_session()
        try:
            cust = self.Customer(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                password_hash=data.get('password_hash')
            )
            db.add(cust)
            db.commit()
            db.refresh(cust)
            return cust
        finally:
            db.close()

    def get_customer_by_id(self, customer_id: int):
        db = self.dbm.get_session()
        try:
            return db.query(self.Customer).filter(self.Customer.customer_id == customer_id).first()
        finally:
            db.close()

    def get_customer_by_email(self, email: str):
        db = self.dbm.get_session()
        try:
            return db.query(self.Customer).filter(self.Customer.email == email).first()
        finally:
            db.close()

    def list_customers(self):
        db = self.dbm.get_session()
        try:
            return db.query(self.Customer).order_by(self.Customer.created_at.desc()).all()
        finally:
            db.close()

    def update_customer(self, customer_id: int, data: dict):
        db = self.dbm.get_session()
        try:
            cust = db.query(self.Customer).filter(self.Customer.customer_id == customer_id).first()
            if not cust:
                return None
            for k, v in data.items():
                if hasattr(cust, k):
                    setattr(cust, k, v)
            db.add(cust)
            db.commit()
            db.refresh(cust)
            return cust
        finally:
            db.close()

    def delete_customer(self, customer_id: int) -> bool:
        db = self.dbm.get_session()
        try:
            cust = db.query(self.Customer).filter(self.Customer.customer_id == customer_id).first()
            if not cust:
                return False
            db.delete(cust)
            db.commit()
            return True
        finally:
            db.close()
