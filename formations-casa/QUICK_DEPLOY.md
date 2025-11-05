# ⚡ Quick Deploy on Your Server

## 1️⃣ SSH Into Your Server
```bash
ssh user@formations.casa
```

## 2️⃣ Go to Your Project
```bash
cd /path/to/formations-casa
# (wherever you deployed the code)
```

## 3️⃣ Start Claude Code
```bash
# Install Claude Code (one time)
npm install -g @anthropic-ai/claude-code

# Start Claude
claude
```

## 4️⃣ Tell Claude:
```
I'm on my production server at formations.casa.
The backend is already running at port 8000.
I need to deploy the Next.js frontend with the hero carousel
and signup/login buttons. Can you help me set this up with
PM2 and Nginx?
```

## 5️⃣ Claude Will:
- ✅ Build the Next.js frontend
- ✅ Deploy with PM2 (keeps it running 24/7)
- ✅ Configure Nginx to serve:
  - Frontend at `https://formations.casa`
  - Backend API at `https://api.formations.casa/api`
- ✅ Set up SSL if needed
- ✅ Test everything works

**Time: 10-15 minutes total**

---

## Alternative: Manual Deployment

If you prefer to do it manually:

```bash
# 1. Build frontend
cd frontend
npm install
npm run build

# 2. Start with PM2
npm install -g pm2
pm2 start npm --name "formations-frontend" -- start
pm2 save
pm2 startup

# 3. Configure Nginx (see DEPLOYMENT.md for config)
sudo nano /etc/nginx/sites-available/formations.casa

# 4. Restart Nginx
sudo nginx -t
sudo systemctl reload nginx
```

---

## What You'll Get

After deployment, **formations.casa** will show:

✅ Hero carousel with 8 rotating slides
✅ "Commencer Gratuitement" (Start Free) button
✅ "S'inscrire" (Register) button
✅ "Connexion" (Login) button
✅ Language switcher (FR/AR/EN/ES)
✅ Full signup and login forms

Instead of the current API documentation page.

---

## Need Help?

Just run `claude` from your project directory on the server and I'll help you through it step-by-step!
