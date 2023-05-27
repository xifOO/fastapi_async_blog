from pydantic import BaseModel


class Token(BaseModel):
    """Base schemas for token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Base schemas for token data"""
    username: str | None = None


class User(BaseModel):
    """Base schemas for user"""
    id: int
    username: str
    email: str | None = None


class UserInDB(User):
    """Schemas for user in database"""
    hashed_password: str


class UserRegistrationRequest(BaseModel):
    """Schemas for user registration request"""
    username: str
    password: str
    email: str


class UserRegistrationResponse(BaseModel):
    """Schemas for user registration response"""
    username: str
    email: str
