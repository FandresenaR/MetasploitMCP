# Deploying MetasploitMCP to Fly.io

## Prerequisites

1. Install the Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Login to Fly.io:
   ```bash
   flyctl auth login
   ```

## Deployment Steps

### Option 1: Quick Deploy (Recommended)

1. **Initialize your Fly.io app** (if not already done):
   ```bash
   flyctl launch --no-deploy
   ```
   
   This will detect your Dockerfile and create a `fly.toml` configuration file.
   - Choose a unique app name or accept the generated one
   - Select a region close to your users
   - Don't add a PostgreSQL or Redis database (unless you need them)

2. **Set environment variables** (if needed):
   ```bash
   flyctl secrets set MSFRPCD_PASSWORD=your_password_here
   flyctl secrets set OPENROUTER_API_KEY=your_api_key_here
   ```

3. **Deploy your application**:
   ```bash
   flyctl deploy
   ```

### Option 2: Manual Configuration

If you encounter the Python/mise error again, ensure you're using the Dockerfile:

1. **Verify Dockerfile exists**:
   ```bash
   ls -la Dockerfile
   ```

2. **Update fly.toml** to explicitly use Docker:
   The `fly.toml` file should have a `[build]` section. It's already configured in this repo.

3. **Deploy**:
   ```bash
   flyctl deploy --dockerfile Dockerfile
   ```

## Troubleshooting

### Issue: mise Python installation error

**Solution**: The Dockerfile in this repository uses the official Python Docker image, which avoids the mise Python installation entirely. Make sure you're using the Dockerfile approach.

### Issue: Connection refused

**Solution**: Ensure your app binds to `0.0.0.0` instead of `127.0.0.1`. The Dockerfile is already configured for this.

### Issue: App crashes on startup

**Solution**: Check logs:
```bash
flyctl logs
```

The app is configured to run in `--mock` mode by default on Fly.io since Metasploit won't be available in the container. To run with actual Metasploit:

1. You'd need to create a more complex Dockerfile that installs Metasploit
2. Or connect to an external Metasploit RPC server

### Check deployment status

```bash
flyctl status
```

### View logs

```bash
flyctl logs
```

### Access your app

After successful deployment:
```bash
flyctl open
```

Or visit: `https://your-app-name.fly.dev`

## Production Considerations

### Running with Real Metasploit (Advanced)

To run with actual Metasploit instead of mock mode, you'll need to:

1. Create a custom Dockerfile that installs Metasploit Framework
2. Set up persistent storage for Metasploit data
3. Configure the msfrpcd service to start within the container

Example approach:
```dockerfile
FROM kalilinux/kali-rolling

# Install Metasploit and Python
RUN apt-get update && apt-get install -y \\
    metasploit-framework \\
    python3.12 \\
    python3-pip \\
    && rm -rf /var/lib/apt/lists/*

# ... rest of your Dockerfile
```

### Environment Variables

Make sure to set these secrets in Fly.io:
```bash
flyctl secrets set MSFRPCD_HOST=127.0.0.1
flyctl secrets set MSFRPCD_PORT=55553
flyctl secrets set MSFRPCD_PASSWORD=your_secure_password
flyctl secrets set OPENROUTER_API_KEY=your_api_key
```

### Scaling

Adjust resources in `fly.toml`:
```toml
[[vm]]
  memory = '2gb'  # Increase for better performance
  cpu_kind = 'shared'
  cpus = 2
```

## Notes

- The default configuration runs in **mock mode** without Metasploit
- The app binds to port 8080 (Fly.io's internal port)
- HTTPS is automatically provided by Fly.io
- Auto-scaling is enabled with min_machines_running = 0 to reduce costs
