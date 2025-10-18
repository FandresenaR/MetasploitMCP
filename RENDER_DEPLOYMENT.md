# Render.com Deployment Guide

MetasploitMCP is now deployed on Render.com, offering a free and reliable hosting solution with automatic deployments from GitHub.

## Live Deployment

**URL**: https://metasploitmcp.onrender.com

This deployment provides:
- ✅ Free hosting with 750 hours/month
- ✅ Automatic HTTPS with SSL certificates
- ✅ Automatic deployments from GitHub
- ✅ Environment variables management
- ✅ Built-in logging and monitoring
- ✅ No cold starts on free tier (unlike Fly.io)

## Features

- **API Documentation**: https://metasploitmcp.onrender.com/docs
- **SSE Endpoint**: https://metasploitmcp.onrender.com/sse
- **Health Check**: https://metasploitmcp.onrender.com/
- **13 Metasploit Tools**: Full MCP integration
- **AI Analysis**: OpenRouter integration with Grok-4-Fast

## Deployment Configuration

### render.yaml

The project includes a `render.yaml` file for infrastructure as code:

```yaml
services:
  - type: web
    name: metasploitmcp
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python MetasploitMCP.py --transport http --host 0.0.0.0 --port $PORT
```

### Environment Variables

The following environment variables are configured in Render dashboard:

- `MSF_SERVER`: Your Metasploit RPC server IP (168.110.55.210)
- `MSF_PORT`: Metasploit RPC port (55553)
- `MSF_PASSWORD`: Secure password for msfrpcd authentication
- `MSF_SSL`: Enable SSL for RPC connection (true)
- `OPENROUTER_API_KEY`: OpenRouter API key for AI features
- `OPENROUTER_BASE_URL`: https://openrouter.ai/api/v1
- `OPENROUTER_MODEL`: x-ai/grok-4-fast:free
- `PAYLOAD_SAVE_DIR`: /tmp/payloads (Render temporary storage)

## Deploying to Your Own Render Account

### Prerequisites

1. Render.com account (free tier available)
2. GitHub account with your MetasploitMCP fork
3. Metasploit RPC server (or use mock mode)

### Method 1: Using render.yaml (Recommended)

1. **Fork the repository** to your GitHub account

2. **Connect to Render**:
   - Go to https://dashboard.render.com
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the MetasploitMCP repository

3. **Configure environment variables**:
   Render will automatically detect `render.yaml` and prompt for:
   - `MSF_SERVER` (your server IP)
   - `MSF_PASSWORD` (your secure password)
   - `OPENROUTER_API_KEY` (optional, for AI features)

4. **Deploy**:
   - Click "Apply"
   - Render will automatically build and deploy
   - Your app will be available at `https://your-app-name.onrender.com`

### Method 2: Manual Setup

1. **Create new Web Service**:
   - Go to https://dashboard.render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure build settings**:
   - **Name**: metasploitmcp
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python MetasploitMCP.py --transport http --host 0.0.0.0 --port $PORT`

3. **Set environment variables**:
   ```
   MSF_SERVER=your.server.ip
   MSF_PORT=55553
   MSF_PASSWORD=your_secure_password
   MSF_SSL=true
   OPENROUTER_API_KEY=your_api_key
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   OPENROUTER_MODEL=x-ai/grok-4-fast:free
   PAYLOAD_SAVE_DIR=/tmp/payloads
   ```

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete

## Connecting to External Metasploit

### Option 1: VPS with Public IP (Recommended)

If you have a VPS with Metasploit (like Oracle Cloud):

```bash
# On your VPS, start msfrpcd with your secure password
msfrpcd -P your_password -S -a 0.0.0.0 -p 55553

# Configure firewall to allow Render.com IPs
sudo ufw allow from any to any port 55553
```

In Render dashboard, set:
```
MSF_SERVER=your.vps.ip
MSF_PORT=55553
MSF_PASSWORD=your_password
MSF_SSL=true
```

### Option 2: Mock Mode (Testing)

For testing without Metasploit, the app runs in mock mode automatically when it cannot connect to a real server.

## Render.com Features

### Automatic Deployments

- **Auto-deploy on push**: Render automatically deploys when you push to main branch
- **Preview deployments**: Create preview environments for pull requests
- **Rollback**: Easy rollback to previous deployments

### Monitoring & Logs

- **Live logs**: View real-time logs in dashboard
- **Metrics**: CPU, memory, and request metrics
- **Health checks**: Automatic health monitoring
- **Alerts**: Email notifications for failures

### Custom Domain

To use a custom domain:

1. Go to your service settings
2. Click "Custom Domain"
3. Add your domain (e.g., `metasploit.yourdomain.com`)
4. Update DNS records as instructed
5. Render automatically provisions SSL certificate

## Render.com Free Tier Limits

- **750 hours/month**: Service hours (enough for continuous running)
- **512 MB RAM**: Memory limit
- **0.1 CPU**: CPU allocation
- **Disk**: Temporary storage only (ephemeral)
- **Bandwidth**: 100 GB/month
- **Sleep after inactivity**: No automatic sleep (unlike Fly.io)

### Important Notes

1. **Persistent Storage**: Render free tier doesn't provide persistent disk. Generated payloads are saved to `/tmp/payloads` and will be lost on restart.

2. **Cold Starts**: Free tier services may experience cold starts after 15 minutes of inactivity (but stay running).

3. **Database**: Not needed for this project, but Render offers free PostgreSQL (90 days).

## Scaling to Paid Plans

When you need more resources:

- **Starter ($7/month)**: 512 MB RAM, always on
- **Standard ($25/month)**: 2 GB RAM, better performance
- **Pro ($85/month)**: 4 GB RAM, SLA support

## Troubleshooting

### Service won't start

**Check logs**:
```bash
# In Render dashboard, go to Logs tab
# Look for Python errors or missing dependencies
```

**Common issues**:
- Missing environment variables
- Incorrect MSF_SERVER address
- Firewall blocking Metasploit RPC port

### Cannot connect to Metasploit

**Verify connection**:
1. Check MSF_SERVER is accessible from internet
2. Verify msfrpcd is running: `ps aux | grep msfrpcd`
3. Test connection: `telnet your.server.ip 55553`

### API endpoints not responding

**Check health endpoint**:
```bash
curl https://metasploitmcp.onrender.com/
```

Should return:
```json
{
  "status": "ok",
  "service": "MetasploitMCP",
  "version": "1.0.0"
}
```

## Security Best Practices

1. **Strong Passwords**: Use 32+ character random passwords
2. **Environment Variables**: Never commit secrets to Git
3. **SSL/TLS**: Always use `MSF_SSL=true`
4. **Firewall**: Restrict Metasploit RPC to known IPs
5. **API Keys**: Rotate OpenRouter keys regularly
6. **Monitoring**: Enable Render notifications

## Comparison: Render vs Fly.io

| Feature | Render.com | Fly.io |
|---------|------------|--------|
| **Free Tier** | 750 hours/month | 7-day trial only |
| **Setup** | Very easy | Easy |
| **Auto-deploy** | ✅ Yes | ✅ Yes |
| **HTTPS** | ✅ Automatic | ✅ Automatic |
| **Cold starts** | Minimal | Auto-stop (free) |
| **Persistent disk** | ❌ No (free tier) | ✅ Yes (paid) |
| **Regions** | Limited choice | Many regions |
| **Logging** | ✅ Built-in | ✅ Built-in |
| **Cost (basic)** | Free → $7/mo | $5-10/mo |

## MCP Client Configuration

### Claude Desktop

Update `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "metasploit": {
      "url": "https://metasploitmcp.onrender.com/sse"
    }
  }
}
```

### Custom MCP Client

Connect to SSE endpoint:

```python
import requests

# SSE endpoint
sse_url = "https://metasploitmcp.onrender.com/sse"

# Connect and stream events
response = requests.get(sse_url, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

## Support

For issues or questions:
- **GitHub Issues**: https://github.com/FandresenaR/MetasploitMCP/issues
- **Documentation**: https://github.com/FandresenaR/MetasploitMCP
- **Render Status**: https://status.render.com

## License

Apache 2.0 - See [LICENSE](LICENSE)
