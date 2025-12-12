from fastapi import APIRouter, HTTPException, Depends, Query
from ..db import master_db, orgs_coll, admins_coll
from ..schemas import OrgCreate, OrgUpdate
from ..utils import hash_password, get_current_admin
from bson.objectid import ObjectId
from datetime import datetime
import re

router = APIRouter(prefix="/org")

# --------------------------------------
# Helper: sanitize organization name
# --------------------------------------
def sanitize_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    return name

# --------------------------------------
# CREATE ORGANIZATION
# --------------------------------------
@router.post("/create")
async def create_org(payload: OrgCreate):
    name = sanitize_name(payload.organization_name)

    # check if organization already exists
    existing = await orgs_coll.find_one({"organization_name": name})
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    # hash password
    hashed = hash_password(payload.password)

    # create admin user
    admin_doc = {
        "email": payload.email,
        "password_hash": hashed,
        "organization_name": name,
        "role": "admin",
        "created_at": datetime.utcnow(),
    }
    admin_res = await admins_coll.insert_one(admin_doc)

    # dynamic collection create
    collection_name = f"org_{name}"

    try:
        master_db.create_collection(collection_name)
    except Exception:
        pass  # collection already created (rare case)

    # store organization metadata
    org_doc = {
        "organization_name": name,
        "collection_name": collection_name,
        "admin_user_id": admin_res.inserted_id,
        "created_at": datetime.utcnow(),
        "connection_details": None,
    }
    await orgs_coll.insert_one(org_doc)

    return {"status": "success", "organization": {"organization_name": name, "collection_name": collection_name}}

# --------------------------------------
# GET ORGANIZATION
# --------------------------------------
@router.get("/get")
async def get_org(organization_name: str = Query(..., min_length=1)):
    name = sanitize_name(organization_name)

    org = await orgs_coll.find_one({"organization_name": name}, {"_id": 0})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {"status": "success", "organization": org}

# --------------------------------------
# UPDATE ORGANIZATION
# --------------------------------------
@router.put("/update")
async def update_org(
    payload: OrgUpdate,
    admin_payload: dict = Depends(get_current_admin)
):
    current_name = sanitize_name(payload.organization_name)

    # admin should only update his own organization
    if admin_payload["organization"] != current_name:
        raise HTTPException(status_code=403, detail="Forbidden: not your organization")

    org = await orgs_coll.find_one({"organization_name": current_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # update admin info
    await admins_coll.update_one(
        {"_id": org["admin_user_id"]},
        {"$set": {"email": payload.email, "password_hash": hash_password(payload.password)}}
    )

    # if no renaming required
    if not payload.new_organization_name:
        return {"status": "success", "message": "Admin updated successfully"}

    # organization renaming
    new_name = sanitize_name(payload.new_organization_name)

    # check if new name already exists
    exists = await orgs_coll.find_one({"organization_name": new_name})
    if exists:
        raise HTTPException(status_code=400, detail="New name already exists")

    old_coll = org["collection_name"]
    new_coll = f"org_{new_name}"

    # copy data
    old_collection = master_db[old_coll]
    new_collection = master_db[new_coll]

    docs = []
    async for d in old_collection.find({}):
        d.pop("_id", None)
        docs.append(d)

    if docs:
        await new_collection.insert_many(docs)

    # drop old collection
    await master_db.drop_collection(old_coll)

    # update metadata
    await orgs_coll.update_one(
        {"_id": org["_id"]},
        {"$set": {"organization_name": new_name, "collection_name": new_coll}}
    )
    await admins_coll.update_one(
        {"_id": org["admin_user_id"]},
        {"$set": {"organization_name": new_name}}
    )

    return {
        "status": "success",
        "message": "Organization renamed successfully",
        "organization": {"organization_name": new_name, "collection_name": new_coll},
    }

# --------------------------------------
# DELETE ORGANIZATION
# --------------------------------------
@router.delete("/delete")
async def delete_org(
    organization_name: str = Query(..., min_length=1),
    admin_payload: dict = Depends(get_current_admin)
):
    name = sanitize_name(organization_name)

    # admin can delete only his org
    if admin_payload["organization"] != name:
        raise HTTPException(status_code=403, detail="Forbidden: not your organization")

    org = await orgs_coll.find_one({"organization_name": name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # drop collection
    await master_db.drop_collection(org["collection_name"])

    # delete admin
    await admins_coll.delete_one({"_id": org["admin_user_id"]})

    # delete organization
    await orgs_coll.delete_one({"_id": org["_id"]})

    return {"status": "success", "message": "Organization deleted"}
