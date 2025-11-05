# 🚀 START HERE - Deploy Your Frontend

## Step-by-Step Instructions

### 1️⃣ SSH Into Your Server
```bash
ssh user@formations.casa
```

### 2️⃣ Pull Latest Code from GitHub
```bash
# Go to your project directory
cd /path/to/formations-casa
# (wherever you cloned the repo)

# Pull latest changes
git fetch origin
git checkout claude/formations-casa-setup-011CUphVg8YKoz3YVrmB7GVr
git pull origin claude/formations-casa-setup-011CUphVg8YKoz3YVrmB7GVr
```

### 3️⃣ Start Claude Code
```bash
# Install Claude Code (first time only)
npm install -g @anthropic-ai/claude-code

# Start Claude
claude
```

### 4️⃣ Give Claude This Message

Copy-paste this exact message to Claude:

```
Read CLAUDE_HANDOFF.md and help me deploy the Next.js frontend.

Current situation:
- Backend is running at formations.casa port 8000
- Frontend needs to be deployed with PM2 on port 3000
- Configure Nginx to show frontend at formations.casa root
- Backend API should be at /api path or api.formations.casa subdomain

Please:
1. Build the frontend (cd frontend && npm run build)
2. Start it with PM2
3. Configure Nginx
4. Update Django CORS settings
5. Test everything works

I want visitors to see the hero carousel with signup/login buttons,
not the Django API documentation.
```

### 5️⃣ Claude Will Do Everything

Claude will:
- Read the handoff document for full context
- Build your frontend
- Deploy with PM2
- Configure Nginx
- Fix any issues
- Test that it works

**Time: 10-15 minutes**

---

## That's It!

After Claude finishes, visit **https://formations.casa** and you'll see:
- ✅ Hero carousel with 8 rotating slides
- ✅ Signup button
- ✅ Login button
- ✅ Language switcher
- ✅ Professional homepage

Instead of the API documentation.

---

## If You Don't Want to Use Claude Code

You can also deploy manually:

```bash
# 1. Build frontend
cd frontend
npm install
npm run build

# 2. Start with PM2
npm install -g pm2
pm2 start npm --name "formations-frontend" -- start
pm2 save

# 3. Configure Nginx (see CLAUDE_HANDOFF.md for config)
sudo nano /etc/nginx/sites-available/formations.casa
# Add the configuration from CLAUDE_HANDOFF.md

# 4. Restart Nginx
sudo nginx -t
sudo systemctl reload nginx
```

But using Claude Code is much faster and it will handle any issues automatically!
