# 🖥️ Running Claude Code on Your Server

This guide will help you run Claude Code directly on your server where formations.casa is deployed.

## Prerequisites

Your server should have:
- ✅ Node.js installed
- ✅ formations.casa code deployed
- ✅ Backend already running
- ✅ SSH access

---

## Step 1: Install Claude Code on Server

SSH into your server and run:

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Or using npx (no installation needed)
npx @anthropic-ai/claude-code
```

---

## Step 2: Navigate to Your Project

```bash
# Go to where your formations.casa code is deployed
cd /path/to/formations-casa

# For example, it might be:
cd /var/www/formations-casa
# or
cd ~/formations-casa
# or
cd /home/yourusername/formations-casa
```

**Important:** Make sure you're in the directory that contains:
- `backend/` folder
- `frontend/` folder
- `DEPLOYMENT.md`
- `deploy-frontend.sh`

---

## Step 3: Start Claude Code Session

From the project root directory, run:

```bash
claude
```

Or if you used npx:

```bash
npx @anthropic-ai/claude-code
```

This will open an interactive session where you can talk to me (Claude) and I'll have direct access to your server files.

---

## Step 4: Tell Claude What You Need

Once Claude Code starts, you can say:

**Example 1 - Deploy Frontend:**
```
I need help deploying the Next.js frontend on this server.
The backend is already running at formations.casa on port 8000.
Can you deploy the frontend and configure Nginx?
```

**Example 2 - Fix Issues:**
```
The frontend isn't showing signup buttons. Can you check
what's running on the server and help me deploy the correct frontend?
```

**Example 3 - Complete Setup:**
```
I'm on my production server. Can you:
1. Build and deploy the Next.js frontend
2. Set up PM2 to keep it running
3. Configure Nginx to serve frontend at formations.casa
4. Move the backend API to api.formations.casa
```

---

## What Claude Can Do on Your Server

When you run Claude Code on the server, I can:

✅ **Check what's currently running:**
```bash
pm2 list
sudo systemctl status nginx
netstat -tlnp
```

✅ **Deploy the frontend:**
```bash
cd frontend
npm install
npm run build
pm2 start npm --name "formations-frontend" -- start
```

✅ **Configure Nginx:**
- Edit `/etc/nginx/sites-available/formations.casa`
- Set up frontend at root domain
- Set up backend API at subdomain
- Reload Nginx

✅ **Set up environment variables:**
- Create `.env.production`
- Set API URLs
- Configure CORS

✅ **Troubleshoot issues:**
- Check logs: `pm2 logs`
- Test API connectivity
- Fix CORS errors
- Debug build issues

✅ **Set up SSL/HTTPS:**
- Install certbot
- Generate SSL certificates
- Configure HTTPS redirect

---

## Tips for Server Session

### 1. Give Context
Tell me about your server setup:
```
"I'm running Ubuntu 22.04. The backend is in /var/www/formations-casa/backend
and runs on port 8000 with Gunicorn. Nginx is already configured for the backend."
```

### 2. Show Me Current State
I can run commands to see what's happening:
```bash
# What's running?
pm2 list
sudo systemctl status nginx

# What ports are in use?
sudo netstat -tlnp | grep LISTEN

# Current Nginx config
cat /etc/nginx/sites-available/formations.casa
```

### 3. Let Me Test
After changes, I can verify:
```bash
# Test Nginx config
sudo nginx -t

# Test frontend build
cd frontend && npm run build

# Check if frontend is accessible
curl http://localhost:3000
```

---

## Common Server Deployment Workflow

Here's what I'll typically do when you start a session:

### Phase 1: Discovery (2 minutes)
```bash
# Check current setup
pwd
ls -la
pm2 list
sudo systemctl status nginx
cat /etc/nginx/sites-available/*
```

### Phase 2: Build Frontend (3-5 minutes)
```bash
cd frontend
npm install
npm run build
```

### Phase 3: Deploy with PM2 (1 minute)
```bash
pm2 start npm --name "formations-frontend" -- start
pm2 save
pm2 startup  # Set up auto-start
```

### Phase 4: Configure Nginx (2 minutes)
```nginx
# I'll create/update Nginx config for:
# - Frontend at formations.casa (port 3000)
# - Backend API at api.formations.casa (port 8000)
# - SSL/HTTPS support
```

### Phase 5: Test & Verify (1 minute)
```bash
# Test frontend
curl http://localhost:3000

# Test API
curl http://localhost:8000/api/

# Check Nginx
sudo nginx -t
sudo systemctl reload nginx
```

**Total time: 10-15 minutes for complete deployment!**

---

## Security Note

When running Claude Code on your production server:

✅ **Safe:**
- Reading files
- Building code
- Installing dependencies
- Configuring services
- Checking logs

⚠️ **Review First:**
- Any `sudo` commands
- Nginx/system configuration changes
- Firewall modifications
- Database operations

I'll always show you commands before running them and explain what they do.

---

## Example Session Transcript

```bash
you@server:~/formations-casa$ claude

Claude Code v1.0
Connected to your project at /home/you/formations-casa

You: I need to deploy the Next.js frontend. Backend is already running.

Claude: I'll help you deploy the frontend! Let me first check your current setup.

[Running commands to check pm2, nginx, etc.]

Claude: I can see your backend is running on port 8000. Here's my deployment plan:
1. Build the Next.js frontend
2. Start it with PM2 on port 3000
3. Configure Nginx to serve frontend at formations.casa
4. Move backend API to api.formations.casa subdomain

Should I proceed? (yes/no)

You: yes

Claude: Starting deployment...
[Builds frontend, configures services, tests everything]

Claude: ✅ Deployment complete!
- Frontend: https://formations.casa
- Backend API: https://api.formations.casa/api
- Hero carousel is now live with signup buttons!

Let me test the signup flow...
[Tests registration, login, etc.]

Claude: All working! Your site is now live with the hero carousel,
signup, and login functionality.
```

---

## Alternative: Share Your Screen

If you prefer, you can also:

1. SSH into your server
2. Share your screen with me via this chat
3. Tell me what you see and what you want to do
4. I'll give you step-by-step commands to run

But using Claude Code directly on the server is much faster since I can:
- Run commands automatically
- Check outputs
- Fix issues in real-time
- Verify everything works

---

## Getting Started Now

1. **SSH into your server:**
```bash
ssh user@formations.casa
```

2. **Navigate to your project:**
```bash
cd /path/to/formations-casa
```

3. **Start Claude Code:**
```bash
npx @anthropic-ai/claude-code
```

4. **Tell me:** "I'm ready to deploy the frontend on my production server.
The backend is already running at formations.casa. Can you help me set everything up?"

Then I'll take it from there and get your frontend deployed! 🚀

---

## Questions?

Common questions when running Claude Code on server:

**Q: Will this affect my running backend?**
A: No, we'll deploy frontend separately on port 3000. Backend stays on 8000.

**Q: Do I need to stop Nginx?**
A: No, we'll just update the configuration and reload it.

**Q: What if something goes wrong?**
A: I can rollback changes. We'll also keep backups of configs.

**Q: Can you access my database?**
A: Only if you explicitly ask me to. I'll always ask permission first.

**Q: How long will deployment take?**
A: 10-15 minutes for complete frontend deployment with Nginx config.

---

Ready to get started? Just SSH into your server and run `claude` from your project directory!
