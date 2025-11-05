# 🤖 Claude Code Session Handoff

**This document contains everything Claude needs to know when you start a session on your server.**

---

## Quick Context for Claude on Server

Hello Claude! The user is running you on their production server for formations.casa. Here's what you need to know:

### Current Situation:
- ✅ **Backend (Django)**: Already deployed and running at https://formations.casa
- ✅ **Code**: Fully built and ready in this directory (pulled from GitHub)
- ❌ **Frontend (Next.js)**: NOT deployed yet - currently showing Django API docs instead of the hero carousel
- 🎯 **Goal**: Deploy the Next.js frontend so users see the hero carousel, signup, and login

---

## What Was Built

### Backend (Django - Already Running):
Located in: `backend/`
- Complete REST API with Django REST Framework
- 20+ new models added:
  - **Online formations** with modules and lessons (video, PDF, quiz, live stream)
  - **Quiz system** with auto-grading and multimedia support
  - **Certificate system** with verification codes
  - **Live streaming** with chat and attendance tracking
  - **AI recommendation engine** with user interaction tracking
  - **Credit system** with transactions and platform revenue sharing
  - **Verified badge system** (replaced admin approval)
- 250 badges in database (120 original + 130 Moroccan-themed)
- Multi-language support (FR, AR, EN, ES) via next-intl
- All migrations run successfully
- Currently accessible at port 8000 (likely via Gunicorn)

### Frontend (Next.js - NEEDS DEPLOYMENT):
Located in: `frontend/`
- **Hero Carousel** with 8 auto-rotating slides (5s interval)
  - 🥐 Moroccan pastry teaching
  - 🚀 Personal development coaching
  - 🤝 Team building services
  - 🍲 Tajine & couscous classes
  - 🎨 Web design teaching
  - 🏢 Training center rentals
  - 🗣️ Darija learning
  - 💻 Tech training
- Arrow navigation + dot indicators
- **Signup/Register page** with role selection (user/coach/center)
- **Login page** with authentication
- **Dashboard page** with role-based content
- **Formations listing** and detail pages
- **Multi-language support** (FR/AR/EN/ES) with language switcher in navbar
- **Translation files**: `messages/fr.json`, `messages/ar.json`, `messages/en.json`, `messages/es.json`
- Uses Tailwind CSS with custom animations

**Dependencies installed**: All packages in package.json already installed (node_modules exists)

---

## What Needs to Be Done

### Primary Task: Deploy Frontend

The user wants visitors to **formations.casa** to see:
1. ✅ Hero carousel with 8 rotating slides
2. ✅ "Commencer Gratuitement" (Start Free) button
3. ✅ "S'inscrire" (Register) button in navbar
4. ✅ "Connexion" (Login) button in navbar
5. ✅ Language switcher (🇫🇷 🇲🇦 🇬🇧 🇪🇸)

**Instead of** the current Django API documentation page.

### Deployment Plan:

#### Option A: Same Server (Recommended)
Deploy frontend and backend on same server with Nginx routing:

**Frontend**: `formations.casa` → Next.js on port 3000
**Backend API**: `api.formations.casa` or `formations.casa/api` → Django on port 8000

**Steps:**
1. Build frontend: `cd frontend && npm run build`
2. Start with PM2: `pm2 start npm --name "formations-frontend" -- start`
3. Configure Nginx (see configuration below)
4. Update CORS in Django settings to allow frontend domain
5. Test: `curl http://localhost:3000` should show hero carousel HTML

#### Option B: Subdomain for API
**Frontend**: `formations.casa` (port 3000)
**Backend**: `api.formations.casa` (port 8000)

Update frontend `.env.production`:
```
NEXT_PUBLIC_API_URL=https://api.formations.casa/api
```

Update Django `settings.py` CORS:
```python
CORS_ALLOWED_ORIGINS = [
    "https://formations.casa",
    "https://www.formations.casa",
]
```

---

## Nginx Configuration

### Configuration A: Frontend at root, API at /api path

```nginx
server {
    listen 80;
    server_name formations.casa www.formations.casa;

    # Frontend (Next.js) - Everything except /api
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API (Django) - Only /api paths
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django admin (optional)
    location /admin {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Django static files (optional)
    location /static {
        proxy_pass http://localhost:8000;
    }
}
```

### Configuration B: Separate subdomains

```nginx
# Frontend
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

# Backend API
server {
    listen 80;
    server_name api.formations.casa;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## PM2 Commands

```bash
# Start frontend
cd frontend
pm2 start npm --name "formations-frontend" -- start

# View logs
pm2 logs formations-frontend

# Restart
pm2 restart formations-frontend

# Stop
pm2 stop formations-frontend

# Save configuration
pm2 save

# Auto-start on boot
pm2 startup
```

---

## Testing Checklist

After deployment, verify:

```bash
# 1. Frontend is running
curl http://localhost:3000 | grep "Hero"

# 2. Backend API is accessible
curl http://localhost:8000/api/

# 3. Nginx config is valid
sudo nginx -t

# 4. Services are running
pm2 list
sudo systemctl status nginx
```

Visit in browser:
- ✅ https://formations.casa → Should show hero carousel
- ✅ Click "S'inscrire" → Should show registration form
- ✅ Click "Connexion" → Should show login form
- ✅ Click language switcher → Should change to Arabic/English/Spanish
- ✅ Hero carousel → Should auto-rotate every 5 seconds
- ✅ Click arrows → Should manually navigate slides

---

## Common Issues & Solutions

### Issue: Frontend shows 404
**Solution**: Check PM2 is running: `pm2 list`

### Issue: API calls fail with CORS error
**Solution**: Update Django `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://formations.casa",
    "http://localhost:3000",
]
```

### Issue: Build fails with memory error
**Solution**: Increase Node memory:
```bash
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

### Issue: Port 3000 already in use
**Solution**:
```bash
lsof -ti:3000 | xargs kill -9
# or use different port in PM2 start command
```

### Issue: Environment variables not working
**Solution**: Check `.env.production` exists:
```bash
cat frontend/.env.production
# Should show: NEXT_PUBLIC_API_URL=https://formations.casa/api
```

---

## File Locations

**Frontend**: `./frontend/`
**Backend**: `./backend/`
**Nginx config**: `/etc/nginx/sites-available/formations.casa`
**PM2 config**: `~/.pm2/`
**Logs**:
- PM2: `pm2 logs`
- Nginx: `/var/log/nginx/error.log`
- Django: `./backend/logs/` or check Gunicorn logs

---

## Important Notes

1. **Don't touch the backend** - it's already running and working
2. **Frontend needs to connect to backend** - ensure `.env.production` has correct API URL
3. **CORS must be configured** - Django needs to allow frontend domain
4. **PM2 keeps frontend running** - better than `npm start` which stops on disconnect
5. **Nginx routes traffic** - frontend at root, API at /api or subdomain
6. **SSL/HTTPS** - If certbot is set up, it should auto-configure HTTPS

---

## Success Criteria

Deployment is successful when:
1. ✅ Visiting formations.casa shows hero carousel (not API docs)
2. ✅ Carousel auto-rotates every 5 seconds
3. ✅ "S'inscrire" button opens registration form
4. ✅ "Connexion" button opens login form
5. ✅ Language switcher works (FR→AR→EN→ES)
6. ✅ Registration form allows role selection (Apprenant/Formateur/Centre)
7. ✅ Login form connects to backend API
8. ✅ No CORS errors in browser console (F12)

---

## GitHub Branch

All code is on branch: `claude/formations-casa-setup-011CUphVg8YKoz3YVrmB7GVr`

If user hasn't pulled latest:
```bash
git fetch origin
git checkout claude/formations-casa-setup-011CUphVg8YKoz3YVrmB7GVr
git pull origin claude/formations-casa-setup-011CUphVg8YKoz3YVrmB7GVr
```

---

## Summary

**What user wants**: Deploy the Next.js frontend with hero carousel, signup, and login buttons so it shows at formations.casa instead of the Django API docs.

**What you need to do**:
1. Build frontend
2. Start with PM2
3. Configure Nginx
4. Test everything works

**Time estimate**: 10-15 minutes

Good luck! 🚀
