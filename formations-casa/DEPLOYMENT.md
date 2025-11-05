# 🚀 Formations.casa Deployment Guide

Your backend is already live at **https://formations.casa**, but the frontend needs to be deployed separately.

## Current Situation:
- ✅ **Backend (Django)**: Live at https://formations.casa
- ❌ **Frontend (Next.js)**: Not deployed yet

## Quick Deploy Options

### Option 1: Vercel (Recommended - Easiest) ⭐

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Deploy from frontend directory:**
```bash
cd formations-casa/frontend
vercel --prod
```

3. **Follow prompts:**
   - Link to your Vercel account
   - Set project name: `formations-casa`
   - Deploy!

4. **Your frontend will be live at:** `https://formations-casa.vercel.app`
   (or custom domain if you configure it)

**Advantages:**
- Free tier available
- Auto-deploys on git push
- Global CDN
- Zero configuration
- Perfect for Next.js

---

### Option 2: Netlify

1. **Install Netlify CLI:**
```bash
npm install -g netlify-cli
```

2. **Deploy:**
```bash
cd formations-casa/frontend
npm run build
netlify deploy --prod --dir=.next
```

---

### Option 3: Same Server as Backend

If you want both frontend and backend on **formations.casa**:

#### Step 1: Build Frontend
```bash
cd formations-casa/frontend
npm install
npm run build
```

#### Step 2: Serve with PM2
```bash
# Install PM2 globally
npm install -g pm2

# Start Next.js on port 3000
cd formations-casa/frontend
pm2 start npm --name "formations-frontend" -- start

# Save PM2 config
pm2 save
pm2 startup
```

#### Step 3: Configure Nginx
Add this to your Nginx config:

```nginx
# Frontend (Next.js)
server {
    listen 80;
    server_name formations.casa www.formations.casa;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Backend API (Django)
server {
    listen 80;
    server_name api.formations.casa;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

**Note:** With this setup:
- Frontend: https://formations.casa
- Backend API: https://api.formations.casa/api

Update frontend `.env.production`:
```
NEXT_PUBLIC_API_URL=https://api.formations.casa/api
```

---

## After Deployment

### Test Your Deployment:

1. **Visit your frontend URL**
2. **You should see:**
   - ✅ Hero carousel with 8 rotating slides
   - ✅ Arrow navigation buttons
   - ✅ Auto-rotation every 5 seconds
   - ✅ "Commencer Gratuitement" (Start Free) button
   - ✅ "Explorer les Formations" button
   - ✅ Language switcher (🇫🇷 🇲🇦 🇬🇧 🇪🇸)

3. **Test signup:**
   - Click "Commencer Gratuitement" or "S'inscrire"
   - Should see registration form
   - Can choose role: Apprenant, Formateur, or Centre

4. **Test login:**
   - Click "Connexion"
   - Should see login form

---

## Troubleshooting

### Frontend not connecting to backend?
Check your `.env.production` file:
```bash
cd formations-casa/frontend
cat .env.production
```

Should show:
```
NEXT_PUBLIC_API_URL=https://formations.casa/api
```

### CORS Errors?
Update Django `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://formations-casa.vercel.app",  # Your Vercel URL
    "https://formations.casa",              # Your domain
    "http://localhost:3000",                # Local dev
]
```

### Build Errors?
Make sure dependencies are installed:
```bash
cd formations-casa/frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## Custom Domain Setup

### For Vercel:
1. Go to Vercel dashboard → Project Settings → Domains
2. Add `formations.casa`
3. Update your DNS:
   - Type: CNAME
   - Name: www
   - Value: cname.vercel-dns.com

### For Netlify:
1. Go to Netlify dashboard → Domain Settings
2. Add custom domain
3. Follow DNS instructions

---

## Environment Variables

Make sure these are set in your deployment platform:

```env
NEXT_PUBLIC_API_URL=https://formations.casa/api
```

Or for Vercel/Netlify, set in their dashboard under "Environment Variables"

---

## Support

If you run into issues:
1. Check browser console for errors (F12)
2. Check frontend logs: `pm2 logs formations-frontend` (if using PM2)
3. Check backend logs for CORS errors
4. Verify API is accessible: `curl https://formations.casa/api/`

---

## Recommended Setup

**Best Practice:**
- Frontend: Vercel (free, fast, zero config)
- Backend: Your current server at formations.casa
- Database: PostgreSQL on same server as backend

This gives you:
- ✅ Lightning-fast frontend (Vercel CDN)
- ✅ Secure backend on your server
- ✅ Easy updates (git push auto-deploys)
- ✅ Free SSL certificates
- ✅ Professional setup
