from fastapi import APIRouter, HTTPException
from ..db import admins_coll, orgs_coll
from ..schemas import AdminLogin
from ..utils import verify_password, create_token

router = APIRouter()

# -------------------------------------
# ADMIN LOGIN
# -------------------------------------
@router.post("/admin/login")
async def admin_login(payload: AdminLogin):
    # check admin email exists
    admin = await admins_coll.find_one({"email": payload.email})
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # check password correct
    if not verify_password(payload.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # find admin's organization
    org = await orgs_coll.find_one({"admin_user_id": admin["_id"]})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # token payload
    token_data = {
        "admin_id": str(admin["_id"]),
        "organization": org["organization_name"]
    }

    token = create_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "organization": org["organization_name"]
    }
