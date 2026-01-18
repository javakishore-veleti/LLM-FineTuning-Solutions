from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import secrets
from datetime import datetime, timedelta
from ...core.integrations.db import get_db_manager
from ...core.models.customer import create_customer_model
from ...core.models.customer_session import create_customer_session_model
from ...core.dao.impl.customer_dao import CustomerDAO
from ...core.dao.impl.customer_session_dao import CustomerSessionDAO
from ...core.utils.passwords import hash_password, verify_password

router = APIRouter(prefix='/api/auth')

DB = get_db_manager()
Base = DB.Base
Customer = create_customer_model(Base)
CustomerSession = create_customer_session_model(Base)
DB.init_db()

cust_dao = CustomerDAO(DB, Customer)
sess_dao = CustomerSessionDAO(DB, CustomerSession)

class SignUpReq(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class LoginReq(BaseModel):
    email: str
    password: str

class TokenResp(BaseModel):
    token: str
    expires_at: str

@router.post('/signup')
def signup(payload: SignUpReq):
    # Normalize email to lowercase and strip whitespace
    email = payload.email.lower().strip()

    # Check if email already exists
    existing = cust_dao.get_customer_by_email(email)
    if existing:
        raise HTTPException(status_code=400, detail='Email already in use')

    ph = hash_password(payload.password)
    cust = cust_dao.create_customer({
        'first_name': payload.first_name.strip(),
        'last_name': payload.last_name.strip(),
        'email': email,
        'password_hash': ph
    })
    return {'customer_id': cust.customer_id}

@router.post('/login', response_model=TokenResp)
def login(payload: LoginReq):
    # Normalize email to lowercase and strip whitespace
    email = payload.email.lower().strip()

    cust = cust_dao.get_customer_by_email(email)
    if not cust or not verify_password(payload.password, cust.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    # create token
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(days=7)
    sess = sess_dao.create_session({'customer_id': cust.customer_id, 'token': token, 'expires_at': expires})
    return {'token': token, 'expires_at': expires.isoformat()}

@router.post('/logout')
def logout(token: str):
    s = sess_dao.get_by_token(token)
    if not s:
        raise HTTPException(status_code=404, detail='session not found')
    sess_dao.delete_session(s.session_id)
    return {'ok': True}

@router.get('/me')
def me(token: str = ''):
    if not token:
        raise HTTPException(status_code=401, detail='token required')
    s = sess_dao.get_by_token(token)
    if not s:
        raise HTTPException(status_code=401, detail='invalid token')
    cust = cust_dao.get_customer_by_id(s.customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail='customer not found')
    return {'customer_id': cust.customer_id, 'email': cust.email, 'first_name': cust.first_name, 'last_name': cust.last_name}
