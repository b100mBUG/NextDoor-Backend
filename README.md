# NextDoor API

A location-aware house rental discovery backend. Tenants find rental properties near them, view details and images, then contact landlords directly via WhatsApp or phone — all from one platform.

Built with **FastAPI**, deployed live on **Render**, and powered by **PostgreSQL on Neon**.

📖 **Live API Docs:** [https://nextdoor-grf8.onrender.com/docs](https://nextdoor-grf8.onrender.com/docs)

---

## Features

- **Tenant & landlord accounts** — separate roles with different permissions via RBAC
- **House listings** — landlords post rental properties with images and details
- **Location-based discovery** — tenants find houses near their current location
- **Image uploads** — property photos uploaded and served via Cloudinary
- **Direct contact** — listings include landlord WhatsApp and phone number for direct communication
- **Role-Based Access Control (RBAC)** — landlords manage listings, tenants browse and enquire
- **JWT authentication** — all protected routes secured with access tokens

---

## Tech Stack

FastAPI · PostgreSQL · SQLAlchemy · Cloudinary · JWT · RBAC · Render · Neon DB

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register as a tenant or landlord |
| POST | `/auth/login` | Login and receive a JWT token |
| POST | `/houses` | List a new rental property (landlord) |
| GET | `/houses/nearby` | Find houses near current location (tenant) |
| GET | `/houses/{id}` | View full details of a listing |
| PUT | `/houses/{id}` | Update a listing (landlord only) |
| DELETE | `/houses/{id}` | Remove a listing (landlord only) |
| GET | `/houses/{id}/contact` | Get landlord contact details |

> Full interactive documentation available at the live docs link above.

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/b100mBUG/nextdoor.git
cd nextdoor

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in: DATABASE_URL, SECRET_KEY, CLOUDINARY_URL

# Run the server
uvicorn main:app --reload
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (Neon) |
| `SECRET_KEY` | JWT signing secret |
| `CLOUDINARY_URL` | Cloudinary API URL for image uploads |

---

## Author

**Were Fidel Castro** — [github.com/b100mBUG](https://github.com/b100mBUG) · [Portfolio](https://werefidelcastro.onrender.com)
