# 🚀 Organization Management Backend (FastAPI + MongoDB)

A multi-tenant backend system where each organization gets its own dynamic MongoDB collection.  
The master database stores organization metadata and admin details.  
Built using **FastAPI**, **MongoDB**, **JWT Authentication**, and **Motor (Async MongoDB driver)**.

---

## 📁 Project Structure

```
ORG-MANAGEMENT-BACKEND/
│── app/
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── schemas.py
│   ├── utils.py
│   ├── routers/
│   │     ├── org_router.py
│   │     └── admin_router.py
│
│── venv/
│── .env
│── requirements.txt
```

---

## 🛠️ Tech Stack

- **FastAPI**
- **MongoDB Atlas**
- **Motor (AsyncIOMotorClient)**
- **JWT Authentication**
- **Bcrypt Password Hashing**
- **Uvicorn**

---

## ⚙️ Environment Setup (.env)

Your `.env` file should contain:

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
MASTER_DB=master_db
JWT_SECRET=super_secret_key_sapna_123
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## 📦 Installation & Running the Project

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/org-management-backend.git
cd org-management-backend
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate   # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run FastAPI Server
```bash
uvicorn app.main:app --reload
```

### 5️⃣ API Docs
Open in browser:
👉 http://127.0.0.1:8000/docs

---

## 🧩 Core Files Overview

### 📌 config.py  
Handles environment variables using Pydantic.

### 📌 db.py – Database Connection  
```python
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

# MongoDB Atlas se connect ho raha hai
client = AsyncIOMotorClient(settings.MONGO_URI)

# Master Database jisme organizations & admin ka data ayega
master_db = client[settings.MASTER_DB]

# Master collections
orgs_coll = master_db["organizations"]
admins_coll = master_db["admins"]
```

### 📌 utils.py  
- Password hashing  
- JWT token generation  

### 📌 schemas.py  
- Pydantic models for validation  

### 📌 routers/  
- `org_router.py` → Create, update, delete, get organizations  
- `admin_router.py` → Admin login  

### 📌 main.py  
Includes all routers + startup logic.

---

# 📚 API Endpoints

## **1️⃣ Create Organization**
```
POST /org/create
```
Body:
```json
{
  "organization_name": "myorg",
  "email": "admin@gmail.com",
  "password": "admin123"
}
```

---

## **2️⃣ Get Organization by Name**
```
GET /org/get?organization_name=myorg
```

---

## **3️⃣ Update Organization**
```
PUT /org/update
```

---

## **4️⃣ Admin Login**
```
POST /admin/login
```
Response contains:
- JWT Token  
- Organization ID  

---

## **5️⃣ Delete Organization (Protected)**
```
DELETE /org/delete?organization_name=myorg
```
Requires:
```
Authorization: Bearer <token>
```

---

# 🧠 Architecture Overview

```
                    +-----------------------------+
                    |       Master Database       |
                    |  - Organizations metadata   |
                    |  - Admin credential         |
                    +-------------+---------------+
                                  |
                                  |
                   Create org     | find org
                                  |
                     +------------v------------+
                     |      FastAPI API       |
                     | - org router           |
                     | - admin router         |
                     | - JWT auth             |
                     +------------+------------+
                                  |
                                  |
                   +--------------v----------------+
                   |  Dynamic MongoDB Collections  |
                   |  org_orgname1                 |
                   |  org_orgname2                 |
                   |  org_orgname3                 |
                   +-------------------------------+
```

---

# 📌 Submission Checklist (Intern Task)
✔ Clean modular code  
✔ Multi-tenant architecture  
✔ JWT authentication  
✔ README with setup instructions  
✔ Architecture diagram  
✔ Postman Collection (included separately)  

---

# 👩‍💻 Author
**Anusaya Dahikamble**  
Backend Developer Intern — Organization Management System  

