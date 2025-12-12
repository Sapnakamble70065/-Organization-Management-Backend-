from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -----------------------------
# Organization CREATE schema
# -----------------------------
class OrgCreate(BaseModel):
    organization_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)

# -----------------------------
# Organization UPDATE schema
# -----------------------------
class OrgUpdate(BaseModel):
    organization_name: str = Field(..., min_length=1)
    new_organization_name: Optional[str] = None
    email: EmailStr
    password: str = Field(..., min_length=6)

# -----------------------------
# Admin LOGIN schema
# -----------------------------
class AdminLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
