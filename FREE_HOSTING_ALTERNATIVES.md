# Free Hosting Alternatives for MetasploitMCP API

> 🌐 **Currently Hosted On**: [Render.com](https://metasploitmcp.onrender.com) - Free tier with 750 hours/month and auto-deploy from GitHub!

## Overview

This guide covers **free, long-term hosting options** for MetasploitMCP's HTTP/SSE API endpoint. Unlike Fly.io's 7-day trial, these alternatives offer sustainable free tiers.

**Current Status**: MetasploitMCP is successfully deployed on Render.com. See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for details.

---

## Comparison Table

| Platform | Free Tier | Always-On | SSL | Cold Starts | Best For | Status |
|----------|-----------|-----------|-----|-------------|----------|--------|
| **Render** | 750 hours/month | Limited | ✅ | Yes (15min) | Simple setup | ✅ **IN USE** |
| **Railway** | $5 credit/month | Yes | ✅ | No | Best overall | Alternative |
| **Koyeb** | Free tier | Yes | ✅ | Minimal | Docker-friendly | Alternative |
| **Oracle Cloud** | Always Free | Yes | Manual | No | Full control | Alternative |
| **Deta Space** | Unlimited | Yes | ✅ | No | Easiest setup | Alternative |
| **Cyclic** | Unlimited | Yes | ✅ | No | Node.js focused | Alternative |
| **Vercel** | Unlimited | No | ✅ | Yes | Serverless only | Not suitable |
| **Netlify** | Unlimited | No | ✅ | Yes | Static + functions | Not suitable |

---

## 🌟 Recommended Free Alternatives

### 1. Render (⭐ Currently In Use)

> ✅ **Live at**: https://metasploitmcp.onrender.com

**Free Tier**: 750 hours/month  
**Sustainability**: Permanent free tier  
**Cold Starts**: Yes (spins down after 15 min inactivity)  
**Always On**: Limited (needs pings to stay warm)

#### Pros:
- ✅ **Currently hosting MetasploitMCP successfully**
- ✅ Truly free tier (no credit card required)
- ✅ GitHub auto-deploy on push
- ✅ Automatic HTTPS with SSL
- ✅ Simple setup with `render.yaml`
- ✅ Built-in monitoring and logs
- ✅ Custom domains supported
- ✅ PostgreSQL, Redis available
- ✅ No manual server management

#### Cons:
- ⚠️ Spins down after 15 minutes inactivity
- ⚠️ First request after sleep takes ~30 seconds
- ⚠️ 750 hours/month limit (enough for continuous running)
- ⚠️ No persistent disk on free tier

#### Why We Chose Render:
1. **One-click deployment** with `render.yaml` blueprint
2. **Auto-deploy from GitHub** - push to deploy
3. **Free and reliable** - 750 hours is enough for 24/7 running
4. **No credit card required** for free tier
5. **Great documentation** and support

#### Deployment:

**Method 1: Blueprint (Recommended)**
```bash
# 1. Fork repository on GitHub
# 2. Go to https://render.com
# 3. New → Blueprint
# 4. Connect GitHub repo
# 5. Set environment variables
# 6. Deploy!
```

**Method 2: Manual**
```bash
# 1. Sign up at render.com
# 2. New Web Service
# 3. Connect GitHub repo
# 4. Configure:
Name: metasploitmcp
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python MetasploitMCP.py --transport http --host 0.0.0.0 --port $PORT

# 5. Environment Variables:
MSF_SERVER=your.server.ip
MSF_PORT=55553
MSF_PASSWORD=your_password
MSF_SSL=true
OPENROUTER_API_KEY=your_key

# 6. Create Web Service
```

**Complete Guide**: See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

**URL**: `https://metasploitmcp.onrender.com` (or your custom name)

---

### 2. Railway (⭐ Best for Always-On)

**Free Tier**: $5 credit/month (covers ~500 hours of small instance)  
**Sustainability**: Renewable monthly credit  
**Cold Starts**: No  
**Always On**: Yes

#### Pros:
- ✅ GitHub integration (auto-deploy)
- ✅ Built-in PostgreSQL, Redis (if needed)
- ✅ No credit card required initially
- ✅ Easy environment variable management
- ✅ Custom domains with SSL
- ✅ Real-time logs and monitoring

#### Cons:
- ⚠️ Credits expire monthly (need to monitor usage)
- ⚠️ May need credit card after trial

#### Deployment Steps:

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd /path/to/MetasploitMCP
railway init

# 4. Set environment variables
railway variables set MSF_SERVER=your.server.ip
railway variables set MSF_PORT=55553
railway variables set MSF_PASSWORD=your_password
railway variables set MSF_SSL=true
railway variables set OPENROUTER_API_KEY=your_key

# 5. Deploy
railway up

# 6. Get URL
railway domain
```

#### Configuration:

Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python MetasploitMCP.py --transport http --host 0.0.0.0 --port 8080",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**URL**: `https://metasploitmcp.up.railway.app`

---

### 3. Koyeb (Great Alternative)

**Free Tier**: 750 hours/month  
**Sustainability**: Permanent free tier  
**Cold Starts**: Yes (spins down after 15 min inactivity)  
**Always On**: Limited (needs pings to stay warm)

#### Pros:
- ✅ Truly free tier (no credit card)
- ✅ GitHub auto-deploy
- ✅ Free SSL certificates
- ✅ PostgreSQL free tier available
- ✅ Easy to use dashboard

#### Cons:
- ⚠️ Cold starts (15 sec delay)
- ⚠️ Spins down after 15 min inactivity
- ⚠️ 750 hours = ~31 days if always on

#### Deployment Steps:

```bash
# 1. Create render.yaml
cat > render.yaml << 'EOF'
services:
  - type: web
    name: metasploitmcp
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python MetasploitMCP.py --transport http --host 0.0.0.0 --port 10000
    envVars:
      - key: MSF_SERVER
        value: your.server.ip
      - key: MSF_PORT
        value: 55553
      - key: MSF_PASSWORD
        sync: false
      - key: MSF_SSL
        value: true
      - key: PYTHON_VERSION
        value: 3.10.0
EOF

# 2. Push to GitHub
git add render.yaml
git commit -m "Add Render deployment config"
git push

# 3. Connect on Render.com
# - Sign in with GitHub
# - New → Web Service
# - Connect repository
# - Auto-deploys!
```

#### Keep Alive (Optional):

To prevent cold starts, use a free ping service:

```bash
# Use UptimeRobot (free)
# Add your Render URL: https://metasploitmcp.onrender.com
# Ping interval: 5 minutes
```

Or create a GitHub Action:

```yaml
# .github/workflows/keep-alive.yml
name: Keep Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping server
        run: curl https://metasploitmcp.onrender.com/health
```

**URL**: `https://metasploitmcp.onrender.com`

---

### 3. Koyeb (⭐ Docker-Friendly)

**Free Tier**: 1 web service, 1 database  
**Sustainability**: Permanent free tier  
**Cold Starts**: Minimal  
**Always On**: Yes

#### Pros:
- ✅ Permanent free tier
- ✅ Docker support
- ✅ Auto-scaling
- ✅ Global CDN
- ✅ No credit card required

#### Cons:
- ⚠️ Limited to 1 service on free tier
- ⚠️ Smaller community

#### Deployment Steps:

```bash
# 1. Install Koyeb CLI
curl -fsSL https://cli.koyeb.com/install.sh | sh

# 2. Login
koyeb login

# 3. Create app from GitHub
koyeb app init metasploitmcp \
  --git github.com/FandresenaR/MetasploitMCP \
  --git-branch main \
  --ports 8080:http \
  --routes /:8080 \
  --env MSF_SERVER=your.server.ip \
  --env MSF_PORT=55553 \
  --env MSF_SSL=true

# 4. Deploy
koyeb app deploy metasploitmcp
```

Or use their web interface:
1. Go to https://app.koyeb.com/
2. New App → From GitHub
3. Select MetasploitMCP repository
4. Set environment variables
5. Deploy!

**URL**: `https://metasploitmcp-yourname.koyeb.app`

---

### 4. Oracle Cloud Always Free (⭐ Best for Full Control)

**Free Tier**: 2 AMD VMs + 4 Arm VMs (24GB RAM total)  
**Sustainability**: **ALWAYS FREE** (no expiration)  
**Cold Starts**: No  
**Always On**: Yes

#### Pros:
- ✅ **Always free** (never expires)
- ✅ Generous resources (24GB RAM!)
- ✅ Full VM control
- ✅ Can run Metasploit directly
- ✅ No cold starts
- ✅ Static IP

#### Cons:
- ⚠️ More setup required
- ⚠️ You manage OS/security
- ⚠️ Need to configure SSL manually

#### Deployment Steps:

**You already have this!** Your current server at `168.110.55.210` is Oracle Cloud.

To expose MetasploitMCP publicly:

```bash
# SSH to your Oracle server
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210

# Install Nginx (reverse proxy)
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y

# Configure Nginx
sudo tee /etc/nginx/sites-available/metasploitmcp << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # Or use IP

    location / {
        proxy_pass http://127.0.0.1:8085;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/metasploitmcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Open firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Get free SSL certificate (if you have domain)
sudo certbot --nginx -d your-domain.com

# Start MetasploitMCP
cd /path/to/MetasploitMCP
source venv/bin/activate
nohup python MetasploitMCP.py --transport http --host 127.0.0.1 --port 8085 > mcp.log 2>&1 &
```

#### Optional: Use Cloudflare Tunnel (No Domain Needed!)

```bash
# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Login to Cloudflare
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create metasploitmcp

# Route traffic
cloudflared tunnel route dns metasploitmcp metasploitmcp.yourdomain.com

# Run tunnel
cloudflared tunnel run metasploitmcp
```

**URL**: `http://168.110.55.210` or `https://your-domain.com`

---

### 5. Deta Space (⭐ Easiest Setup)

**Free Tier**: Unlimited apps  
**Sustainability**: Permanent free tier  
**Cold Starts**: No  
**Always On**: Yes

#### Pros:
- ✅ Completely free
- ✅ Instant HTTPS
- ✅ No cold starts
- ✅ Simple CLI
- ✅ Personal cloud

#### Cons:
- ⚠️ Python 3.9 only (need to adjust)
- ⚠️ Limited to Deta's ecosystem

#### Deployment Steps:

```bash
# 1. Install Space CLI
curl -fsSL https://get.deta.dev/space-cli.sh | sh

# 2. Login
space login

# 3. Create Spacefile
cat > Spacefile << 'EOF'
v: 0
micros:
  - name: metasploitmcp
    src: .
    engine: python3.9
    run: python MetasploitMCP.py --transport http --host 0.0.0.0 --port 8080
    presets:
      env:
        - name: MSF_SERVER
          description: Metasploit server IP
        - name: MSF_PORT
          default: "55553"
        - name: MSF_PASSWORD
          description: msfrpcd password
        - name: MSF_SSL
          default: "true"
EOF

# 4. Push to Space
space push

# 5. Release
space release
```

**URL**: `https://metasploitmcp-yourinstance.deta.space`

---

### 6. Cyclic (⭐ Good for Node.js Wrapper)

**Free Tier**: Unlimited deployments  
**Sustainability**: Permanent free tier  
**Cold Starts**: No  
**Always On**: Yes

#### Pros:
- ✅ Truly unlimited free tier
- ✅ No cold starts
- ✅ GitHub auto-deploy
- ✅ Custom domains

#### Cons:
- ⚠️ Focused on Node.js (need wrapper)

#### Deployment Steps:

Create Node.js wrapper:

```javascript
// server.js
const { spawn } = require('child_process');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

// Start Python MCP server
const python = spawn('python', ['MetasploitMCP.py', '--transport', 'http', '--port', '8085']);

// Proxy requests
app.use((req, res) => {
  // Forward to Python server
  const proxy = require('http-proxy').createProxyServer({});
  proxy.web(req, res, { target: 'http://localhost:8085' });
});

app.listen(PORT, () => console.log(`Proxy listening on ${PORT}`));
```

```bash
# Deploy
npm init -y
npm install express http-proxy
git add .
git commit -m "Add Cyclic deployment"
git push

# Connect on cyclic.sh
# Deploy from GitHub
```

---

### 7. Glitch (🎨 Quick Prototyping)

**Free Tier**: Unlimited projects  
**Sustainability**: Permanent free tier  
**Cold Starts**: Yes (5 min inactivity)  
**Always On**: No

#### Pros:
- ✅ No credit card
- ✅ Live code editor
- ✅ Instant deployment
- ✅ Great for demos

#### Cons:
- ⚠️ Sleeps after 5 min
- ⚠️ Limited resources

#### Deployment Steps:

1. Go to https://glitch.com/
2. New Project → Import from GitHub
3. Paste: `https://github.com/FandresenaR/MetasploitMCP`
4. Set environment variables in `.env`
5. Done!

**URL**: `https://metasploitmcp.glitch.me`

---

## 🏆 Best Choice for Each Use Case

### For Production Use
**Oracle Cloud Always Free** (you already have this!)
- Best resources
- No expiration
- Full control
- Static IP

### For Public Demo
**Railway** or **Render**
- Easy setup
- Good uptime
- Professional URLs

### For Quick Testing
**Deta Space** or **Glitch**
- Instant deployment
- No configuration

### For Docker Deployment
**Koyeb** or **Railway**
- Native Docker support
- Easy scaling

---

## 💡 Recommended Setup

Since you already have **Oracle Cloud** (168.110.55.210), here's the best free solution:

### Option A: Oracle Cloud + Cloudflare Tunnel (FREE, HTTPS, NO DOMAIN)

```bash
# 1. Install cloudflared on your Oracle server
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# 2. Authenticate
cloudflared tunnel login

# 3. Create tunnel
cloudflared tunnel create metasploit-mcp

# 4. Configure tunnel
mkdir -p ~/.cloudflared
cat > ~/.cloudflared/config.yml << 'EOF'
tunnel: metasploit-mcp
credentials-file: /home/ubuntu/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: metasploit-mcp.yourusername.workers.dev
    service: http://localhost:8085
  - service: http_status:404
EOF

# 5. Run tunnel (test)
cloudflared tunnel run metasploit-mcp

# 6. Install as service (always on)
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

**Benefits**:
- ✅ **100% FREE** (no costs)
- ✅ **Automatic HTTPS**
- ✅ **No domain required**
- ✅ **No cold starts**
- ✅ **DDoS protection**
- ✅ **Always on**

**URL**: `https://metasploit-mcp.yourusername.workers.dev`

### Option B: Oracle Cloud + Nginx + Let's Encrypt (FREE, Custom Domain)

If you have a domain:

```bash
# Already shown above in Oracle Cloud section
# Gives you: https://your-domain.com
```

### Option C: Railway as Backup (FREE $5/month)

Use Railway for redundancy or if Oracle has issues:

```bash
railway init
railway up
```

---

## 🔒 Security Recommendations

Regardless of platform, implement:

### 1. API Key Authentication

```python
# Add to MetasploitMCP.py
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("MCP_API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path not in ["/health", "/docs"]:
        api_key = request.headers.get("X-API-Key")
        if api_key != API_KEY:
            return JSONResponse(status_code=403, content={"error": "Invalid API key"})
    return await call_next(request)
```

### 2. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/sse")
@limiter.limit("10/minute")
async def sse_endpoint():
    pass
```

### 3. IP Whitelisting

Set environment variable:
```bash
ALLOWED_IPS=192.168.1.0/24,10.0.0.1
```

---

## 📊 Cost Comparison

| Platform | Cost | Sustainability | Setup Time |
|----------|------|----------------|------------|
| **Oracle Cloud** | $0 forever | ⭐⭐⭐⭐⭐ | 30 min |
| **Railway** | $0 ($5/month credit) | ⭐⭐⭐⭐ | 5 min |
| **Render** | $0 (750h/month) | ⭐⭐⭐⭐ | 5 min |
| **Koyeb** | $0 forever | ⭐⭐⭐⭐⭐ | 10 min |
| **Deta Space** | $0 forever | ⭐⭐⭐⭐⭐ | 5 min |
| **Fly.io** | $0 (7 days only) | ⭐ | 5 min |

---

## 🎯 Final Recommendation

**Use your existing Oracle Cloud server with Cloudflare Tunnel:**

```bash
# One-time setup (15 minutes)
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210

# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Create tunnel
cloudflared tunnel login
cloudflared tunnel create metasploit-mcp

# Configure and install as service
# (follow Option A above)
```

**Result**: 
- ✅ Free forever
- ✅ HTTPS automatic
- ✅ No domain needed
- ✅ Professional URL
- ✅ Always on
- ✅ DDoS protection

**Plus**, keep **Railway** as a backup for $0 additional cost!

---

*Need help with any of these setups? All detailed instructions are included above!* 🚀
