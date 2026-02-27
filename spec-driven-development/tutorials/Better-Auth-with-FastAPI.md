# 🛡️ Better Auth + FastAPI: The Ultimate Beginner's Guide

This guide walks you through building a **"Hello World"** project that connects a **Next.js** frontend (using Better Auth) to a **FastAPI** backend.

---

## 1. The Core Concept (The "Why")

In modern web apps, we often separate the **Frontend** (Next.js) from the **Backend** (FastAPI). 
- **Next.js** handles the "Front Door" (Login, Signup, User Sessions).
- **FastAPI** handles the "Vault" (Data, Logic, Database).

**The Problem:** How does the Vault (FastAPI) know that the person asking for data is actually logged in at the Front Door (Next.js)?

**The Solution:** A **JWT (JSON Web Token)**. It's like a digital "signed badge." Next.js issues the badge, and FastAPI inspects the signature to verify it.

---

## 2. Prerequisites & Setup

### Environment Variables (`.env`)
You must have the **exact same secret** in both projects. This is the "Key" used to sign and verify badges.

**In `frontend/.env` AND `backend/.env`:**
```env
BETTER_AUTH_SECRET=your_super_secret_key_123
```

---

## 3. Step 1: The Frontend (The Badge Maker)

### 1.1 Better Auth Configuration
In `frontend/src/lib/auth.ts`, enable the **JWT Plugin**.

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
    secret: process.env.BETTER_AUTH_SECRET,
    plugins: [
        jwt({
            jwt: { expirationTime: "7d" } // Badge lasts 7 days
        }),
    ],
});
```

### 1.2 The Token "Exposer"
Next.js needs an endpoint to give the badge to your browser.
Create `frontend/app/api/token/route.ts`:

```typescript
import { auth } from "@/src/lib/auth";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
    const token = await auth.api.getToken({ headers: request.headers });
    if (!token) return NextResponse.json({ error: "No session" }, { status: 401 });
    
    return NextResponse.json({ token: token.token });
}
```

---

## 4. Step 2: The Backend (The Badge Inspector)

### 2.1 The Verification Logic
In `backend/auth_utils.py`, we create the logic to "check the signature."

```python
import jwt
import os
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Load the secret we shared with Next.js
SHARED_SECRET = os.getenv("BETTER_AUTH_SECRET")
security = HTTPBearer()

def get_current_user(res: HTTPAuthorizationCredentials = Security(security)):
    token = res.credentials # The badge sent from frontend
    try:
        # Check if the badge is authentic and not expired
        payload = jwt.decode(token, SHARED_SECRET, algorithms=["HS256"])
        return payload # Returns user info (id, email)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Badge!")
```

### 2.2 The "Hello World" Route
Now, create a route that only logged-in users can see.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/api/hello-world")
async def hello_world(user = Depends(get_current_user)):
    return {
        "message": "Hello World! You are authorized.",
        "your_user_id": user.get("sub"), # 'sub' is the User ID in JWTs
        "your_email": user.get("email")
    }
```

---

## 5. Step 3: Connecting the Two (The "Flow")

Finally, in your Next.js frontend, call the FastAPI route.

```typescript
// frontend/components/HelloWorld.tsx
"use client";

async function fetchHello() {
    // 1. Ask Next.js for our Badge (JWT)
    const tokenRes = await fetch("/api/token");
    const { token } = await tokenRes.json();

    // 2. Send the badge to FastAPI
    const response = await fetch("http://localhost:8000/api/hello-world", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();
    console.log(data.message); // "Hello World! You are authorized."
}

export default function HelloWorld() {
    return <button onClick={fetchHello}>Click Me for Hello World</button>;
}
```

---

## 🎯 Summary of the Process

1.  **Identity:** User logs into Next.js.
2.  **Badge:** Next.js generates a **JWT** using the `BETTER_AUTH_SECRET`.
3.  **Request:** The Frontend fetches that JWT and puts it in a suitcase (`Authorization` header).
4.  **Verification:** FastAPI opens the suitcase, sees the JWT, and checks it using the same `BETTER_AUTH_SECRET`.
5.  **Access:** If the secret matches, FastAPI says "Welcome!" and processes the request.

### 💡 Pro Tip
If you ever get an **"Invalid Token"** error, 99% of the time it means your `BETTER_AUTH_SECRET` in the Frontend doesn't match the one in the Backend!

---
*Authored with precision by **DanielCodeForge***
