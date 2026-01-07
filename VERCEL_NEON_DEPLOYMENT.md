# Vercel + Neon Deployment Guide

## 🎯 Quick Steps

### Step 1: Create Neon Database (2 minutes)

1. Go to: **https://neon.tech**
2. **Sign up** with GitHub (free tier)
3. Click **"Create Project"**
4. Name: `hackathon-todo-db`
5. **Copy Connection String** - looks like:
   ```
   postgresql://user:password@ep-xxx-123.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
6. **Save this URL** - you'll need it!

### Step 2: Deploy Backend to Vercel (3 minutes)

1. Go to: **https://vercel.com**
2. **Sign up / Login** with GitHub
3. Click **"Add New"** → **"Project"**
4. **Import** your repo: `Fatimamehmoodali1/Hackathon2`
5. **Root Directory**: Select `backend`
6. **Framework Preset**: Other
7. **Build Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: (leave empty)
8. **Environment Variables** - Add these:
   ```
   database_url = postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require
   better_auth_secret = your-32-character-secret-key-here-production
   cors_origins = https://your-frontend-url.vercel.app
   app_host = 0.0.0.0
   app_port = 8000
   ```
9. Click **Deploy**
10. **Copy Backend URL**: `https://hackathon2-backend.vercel.app`

### Step 3: Deploy Frontend to Vercel (2 minutes)

1. In Vercel, click **"Add New"** → **"Project"** again
2. **Import** same repo: `Fatimamehmoodali1/Hackathon2`
3. **Root Directory**: Select `frontend`
4. **Framework Preset**: Next.js (auto-detected)
5. **Build Settings**: (auto-filled)
6. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL = https://your-backend-url.vercel.app
   ```
7. Click **Deploy**
8. **Copy Frontend URL**: `https://hackathon2-frontend.vercel.app`

### Step 4: Update CORS (1 minute)

1. Go back to **Backend project** in Vercel
2. **Settings** → **Environment Variables**
3. Update `cors_origins` with your frontend URL
4. **Redeploy** backend

## ✅ Done! Your URLs:

- **Frontend**: `https://your-frontend.vercel.app`
- **Backend API**: `https://your-backend.vercel.app`
- **Database**: Neon PostgreSQL

## 🔧 Environment Variables Summary

### Backend (Vercel):
```
database_url=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
better_auth_secret=min-32-chars-secret-production-key
cors_origins=https://your-frontend.vercel.app
app_host=0.0.0.0
app_port=8000
```

### Frontend (Vercel):
```
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

## 📝 Where to Get Values:

1. **database_url**: From Neon dashboard (https://neon.tech)
2. **better_auth_secret**: Generate random 32+ character string
3. **cors_origins**: Your Vercel frontend URL
4. **NEXT_PUBLIC_API_URL**: Your Vercel backend URL

## 🧪 Testing After Deployment:

1. Open: `https://your-frontend.vercel.app`
2. Click **Sign Up**
3. Create account with email/password
4. **Sign In**
5. Add todos, test all features!

## 🆘 Troubleshooting:

### Backend Errors:
- Check Vercel logs: Project → Deployments → Latest → Logs
- Verify Neon connection string is correct
- Ensure all environment variables are set

### Frontend Can't Connect:
- Check `NEXT_PUBLIC_API_URL` is correct
- Verify CORS settings in backend
- Check browser console for errors

### Database Connection Failed:
- Verify Neon database is active
- Check connection string format
- Ensure `sslmode=require` is in URL

## 🎉 Success Checklist:

- ✅ Neon database created
- ✅ Backend deployed to Vercel
- ✅ Frontend deployed to Vercel
- ✅ Environment variables configured
- ✅ CORS updated
- ✅ Can sign up new users
- ✅ Can sign in
- ✅ Can create/view/edit/delete todos

---

**Total Time: ~10 minutes**

Your full-stack todo app is now LIVE on Vercel + Neon! 🚀
