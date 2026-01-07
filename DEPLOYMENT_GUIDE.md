# Railway Deployment Guide - Todo App

## 🚀 Quick Deployment Steps

### Option 1: Railway Web Interface (Easiest)

1. **Go to Railway**: https://railway.app/
2. **Sign up / Login** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select Repository**: `Fatimamehmoodali1/Hackathon2`
5. **Configure Services**:

#### Backend Service:
- **Root Directory**: `backend`
- **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  ```
  database_url=sqlite:///./todo_app.db
  better_auth_secret=your-32-char-secret-key-here-railway-prod
  cors_origins=https://your-frontend-url.railway.app
  app_host=0.0.0.0
  app_port=$PORT
  ```

#### Frontend Service:
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm start`
- **Environment Variables**:
  ```
  NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
  ```

6. **Deploy** both services
7. **Get URLs** from Railway dashboard

### Option 2: Railway CLI

```bash
# Login to Railway
railway login

# Link to project (creates new project)
railway link

# Deploy backend
cd backend
railway up

# Deploy frontend
cd ../frontend
railway up
```

## 📝 After Deployment

### Get Your URLs:

1. **Backend URL**: Railway will provide like `https://hackathon2-backend-production.up.railway.app`
2. **Frontend URL**: Railway will provide like `https://hackathon2-frontend-production.up.railway.app`

### Update Environment Variables:

1. **Frontend**: Add backend URL to `NEXT_PUBLIC_API_URL`
2. **Backend**: Add frontend URL to `cors_origins`

## 🗄️ Database Options

### Current: SQLite (Good for testing)
- Already configured
- Works immediately
- Limited for production

### Upgrade to Neon PostgreSQL (Production):
1. Get free Neon database: https://neon.tech/
2. Copy connection string
3. Update backend `database_url` in Railway:
   ```
   database_url=postgresql://user:pass@ep-xxx.neon.tech/dbname?sslmode=require
   ```

## ✅ Verification

After deployment, test these URLs:
- `https://your-backend-url/health` - Should return `{"status":"healthy"}`
- `https://your-frontend-url` - Should show signup/signin page
- Create account, signin, add todos!

## 🆘 Troubleshooting

### Backend won't start:
- Check logs in Railway dashboard
- Verify environment variables are set
- Check Python version (needs 3.11+)

### Frontend can't connect to backend:
- Check `NEXT_PUBLIC_API_URL` is correct
- Verify CORS settings in backend
- Check both services are running

### Database errors:
- SQLite: Check file permissions
- Neon: Verify connection string format

## 📞 Support

If you face issues:
1. Check Railway logs
2. Verify environment variables
3. Test locally first with same config

---

**Your App is Ready to Deploy!** 🎉

Just follow Option 1 (Railway Web Interface) - it's the easiest!
