# ☁️ Free Hosting Summary - MetasploitMCP

> 🌐 **Currently Hosted**: https://metasploitmcp.onrender.com on Render.com (free tier)

## Quick Answer: Best Free Options

We're currently using **Render.com** for free hosting with 750 hours/month!

---

## 🏆 CURRENT DEPLOYMENT

### ✅ Render.com (Currently In Use) ⭐⭐⭐⭐⭐

**Live URL**: https://metasploitmcp.onrender.com

**Why we chose it**:
- ✅ **750 hours/month FREE** (enough for 24/7 running)
- ✅ One-click deployment with GitHub
- ✅ Automatic HTTPS with SSL
- ✅ Auto-deploy on every push
- ✅ No credit card required for free tier
- ✅ Built-in monitoring and logs
- ✅ Zero configuration needed

**Quick Deploy**:
```bash
# 1. Fork repository on GitHub
# 2. Go to https://render.com
# 3. Click "New" → "Blueprint"
# 4. Connect your forked repo
# 5. Set environment variables (MSF_SERVER, MSF_PASSWORD, etc.)
# 6. Click "Apply" - Done!
```

**Complete Guide**: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

---

## 🏆 ALTERNATIVE RECOMMENDATIONS

### Option 1: Oracle Cloud (You Already Have This!) ⭐⭐⭐⭐

**Your existing server**: `168.110.55.210`

**Why it's perfect**:
- ✅ **FREE FOREVER** (Always Free tier never expires)
- ✅ You already have it running
- ✅ Generous resources (24GB RAM available)
- ✅ No cold starts
- ✅ Static IP

**Setup with Cloudflare Tunnel** (Free HTTPS, No Domain Needed):

```bash
# 1. SSH to your server
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210

# 2. Install Cloudflare Tunnel
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# 3. Authenticate with Cloudflare (free account)
cloudflared tunnel login

# 4. Create tunnel
cloudflared tunnel create metasploit-mcp

# 5. Get your tunnel ID
cloudflared tunnel list

# 6. Configure tunnel
mkdir -p ~/.cloudflared
cat > ~/.cloudflared/config.yml << 'EOF'
tunnel: YOUR-TUNNEL-ID
credentials-file: /home/ubuntu/.cloudflared/YOUR-TUNNEL-ID.json

ingress:
  - hostname: metasploit-mcp-YOUR-SUBDOMAIN.trycloudflare.com
    service: http://localhost:8085
  - service: http_status:404
EOF

# 7. Run tunnel (test first)
cloudflared tunnel run metasploit-mcp

# 8. If working, install as service
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared

# 9. Get your public URL
cloudflared tunnel route dns metasploit-mcp
```

**Result**: Free HTTPS URL like `https://metasploit-mcp-xyz.trycloudflare.com`

**Time to setup**: 15 minutes  
**Cost**: $0 forever  
**Reliability**: ⭐⭐⭐⭐⭐

---

## 🥈 BACKUP OPTIONS

### Option 2: Railway ⭐⭐⭐⭐

**Free Tier**: $5 credit/month (renewable)  
**Sustainability**: Very good (credits renew monthly)

```bash
# Install CLI
npm i -g @railway/cli

# Deploy
cd /path/to/MetasploitMCP
railway login
railway init
railway up
```

**Time**: 5 minutes  
**Cost**: $0 (with monthly credit)

---

### Option 3: Render ⭐⭐⭐⭐

**Free Tier**: 750 hours/month  
**Sustainability**: Good (permanent free tier)

```bash
# Create render.yaml
cat > render.yaml << 'EOF'
services:
  - type: web
    name: metasploitmcp
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python MetasploitMCP.py --transport http --host 0.0.0.0 --port 10000
EOF

# Push to GitHub, then connect on render.com
```

**Time**: 5 minutes  
**Cost**: $0 forever  
**Note**: Spins down after 15 min (cold starts)

---

### Option 4: Koyeb ⭐⭐⭐⭐

**Free Tier**: 1 web service + 1 database  
**Sustainability**: Excellent (permanent)

```bash
# Install CLI
curl -fsSL https://cli.koyeb.com/install.sh | sh

# Deploy
koyeb login
koyeb app init metasploitmcp --git github.com/FandresenaR/MetasploitMCP
```

**Time**: 10 minutes  
**Cost**: $0 forever

---

## 📊 Quick Comparison

| Platform | Free? | Forever? | Cold Starts? | HTTPS? | Recommended? |
|----------|-------|----------|--------------|--------|--------------|
| **Render** | ✅ | ✅ | ✅ (minimal) | ✅ | ⭐⭐⭐⭐⭐ (IN USE) |
| **Oracle Cloud** | ✅ | ✅ | ❌ | ✅ (w/ tunnel) | ⭐⭐⭐⭐ |
| **Railway** | ✅ | ✅ (credit) | ❌ | ✅ | ⭐⭐⭐⭐ |
| **Koyeb** | ✅ | ✅ | ❌ | ✅ | ⭐⭐⭐⭐ |

---

## 🎯 Recommended Strategy

### Current Setup (Render.com):

1. **Primary**: Render.com (https://metasploitmcp.onrender.com)
   - Free 750 hours/month
   - Auto-deploy from GitHub
   - HTTPS automatic
   - Zero maintenance

2. **Backup**: Oracle Cloud
   - Free forever
   - No cold starts
   - Full Metasploit installation possible

---

## 📝 Step-by-Step for Oracle Cloud

Since you already have the server, here's the complete setup:

### 1. Make MetasploitMCP Start on Boot

```bash
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210

# Create systemd service
sudo tee /etc/systemd/system/metasploitmcp.service << 'EOF'
[Unit]
Description=MetasploitMCP Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/MetasploitMCP
Environment="PATH=/home/ubuntu/MetasploitMCP/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/ubuntu/MetasploitMCP/venv/bin/python MetasploitMCP.py --transport http --host 127.0.0.1 --port 8085
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable metasploitmcp
sudo systemctl start metasploitmcp

# Check status
sudo systemctl status metasploitmcp
```

### 2. Setup Cloudflare Tunnel (Already shown above)

### 3. Done!

Your API will be available at: `https://metasploit-mcp-xyz.trycloudflare.com`

---

## 🔒 Security Reminder

Don't forget to add authentication:

```python
# In MetasploitMCP.py
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("MCP_API_KEY", "your-secret-key")
api_key_header = APIKeyHeader(name="X-API-Key")

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path not in ["/health", "/docs"]:
        api_key = request.headers.get("X-API-Key")
        if api_key != API_KEY:
            return JSONResponse(status_code=403, content={"error": "Invalid API key"})
    return await call_next(request)
```

Set in `.env.local`:
```bash
MCP_API_KEY=$(openssl rand -base64 32)
```

---

## 📚 Full Documentation

See **[FREE_HOSTING_ALTERNATIVES.md](FREE_HOSTING_ALTERNATIVES.md)** for:
- Complete setup guides for all platforms
- Security recommendations
- Troubleshooting guides
- Advanced configurations

---

## ✅ Action Items

1. [ ] Setup Cloudflare Tunnel on Oracle Cloud (15 min)
2. [ ] Make MetasploitMCP a systemd service (5 min)
3. [ ] Add API key authentication (10 min)
4. [ ] Test the public URL
5. [ ] Optional: Setup Railway as backup (5 min)

**Total time**: 35-45 minutes for production-ready setup!

---

*Need help? All detailed instructions are in FREE_HOSTING_ALTERNATIVES.md* 🚀
