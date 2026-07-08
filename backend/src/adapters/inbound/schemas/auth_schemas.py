"""Request/response schemas for the authentication endpoints."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.domain.models.user import UserRole


class RegisterRequest(BaseModel):
    """Payload to create a new user account."""

    email: EmailStr
    name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.CUSTOMER


class LoginRequest(BaseModel):
    """Payload to authenticate an existing user."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public representation of a user, safe to return over the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    role: UserRole


class TokenResponse(BaseModel):
    """Access token issued after a successful login."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105 — OAuth2 token type label, not a secret.
    user: UserResponse
