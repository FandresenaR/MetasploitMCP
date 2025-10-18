# Deployment Guide

This guide provides detailed deployment instructions for MetasploitMCP on various platforms.

> 📖 **Quick Start**: For a quick overview, see the [Deployment section in README.md](README.md#deployment).

## Table of Contents

- [Fly.io Deployment](#flyio-deployment)
- [Oracle Cloud Infrastructure](#oracle-cloud-infrastructure)
- [Self-Hosted / VPS](#self-hosted--vps)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)

---

## Fly.io Deployment

### Prerequisites

1. Install the Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Login to Fly.io:
   ```bash
   flyctl auth login
   ```

### Quick Deploy

1. **Initialize your Fly.io app**:
   ```bash
   flyctl launch --no-deploy
   ```
   
   - Choose a unique app name or accept the generated one
   - Select a region close to your users
   - Skip database setup (not needed)

2. **Set environment secrets**:
   ```bash
   flyctl secrets set MSFRPCD_PASSWORD=your_password_here
   flyctl secrets set OPENROUTER_API_KEY=your_api_key_here
   ```

3. **Deploy**:
   ```bash
   flyctl deploy
   ```

### Alternative: Explicit Dockerfile

```bash
flyctl deploy --dockerfile Dockerfile
```

### Troubleshooting

**Issue: mise Python installation error**
- **Solution**: The Dockerfile uses official Python image, avoiding mise entirely.

**Issue: Connection refused**
- **Solution**: Ensure app binds to `0.0.0.0`. The Dockerfile is pre-configured.

**Issue: App crashes on startup**
- **Solution**: Check logs with `flyctl logs`
- The app runs in mock mode by default (no Metasploit)

**Check deployment status**:
```bash
flyctl status
flyctl logs
flyctl open  # Open in browser
```

### Running with Real Metasploit

To connect to an actual Metasploit instance:

**Option 1: External Server**
```bash
flyctl secrets set MSFRPCD_HOST=your.server.ip
flyctl secrets set MSFRPCD_PORT=55553
flyctl secrets set MSFRPCD_PASSWORD=your_password
```

**Option 2: Install in Container** (Advanced)
- Use `Dockerfile.metasploit` for Metasploit-enabled container
- Requires more memory: `flyctl scale memory 2048`

### Scaling Resources

Edit `fly.toml` or use CLI:
```bash
flyctl scale memory 2048  # 2GB RAM
flyctl scale count 2      # 2 machines
```

---

## Oracle Cloud Infrastructure

### Prerequisites

1. Oracle Cloud account (Free Tier available)
2. VCN (Virtual Cloud Network) configured
3. SSH key pair generated

### Deployment Options

#### Option 1: Compute Instance with Docker

**1. Create Compute Instance**:
- **Shape**: VM.Standard.E2.1.Micro (Always Free) or VM.Standard.A1.Flex
- **Image**: Ubuntu 22.04 or Oracle Linux 8
- **Network**: Public subnet with internet gateway

**2. Configure Security**:
```bash
# SSH to instance
ssh ubuntu@<instance-public-ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**3. Deploy Application**:
```bash
# Clone repository
git clone https://github.com/FandresenaR/MetasploitMCP.git
cd MetasploitMCP

# Build image
docker build -t metasploit-mcp .

# Run container
docker run -d -p 8080:8080 \
  -e MSFRPCD_PASSWORD=your_password \
  -e OPENROUTER_API_KEY=your_api_key \
  --name metasploit-mcp \
  --restart unless-stopped \
  metasploit-mcp
```

**4. Configure Firewall**:
```bash
# OS firewall
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8080 -j ACCEPT
sudo netfilter-persistent save

# OR for firewalld (Oracle Linux)
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

**5. OCI Security List**:
- Navigate to VCN → Security Lists
- Add Ingress Rule:
  - Source CIDR: `0.0.0.0/0`
  - IP Protocol: TCP
  - Destination Port: 8080

**6. Optional: Setup Reverse Proxy with SSL**:
```bash
sudo apt install nginx certbot python3-certbot-nginx

# Configure Nginx
sudo nano /etc/nginx/sites-available/metasploit-mcp

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

#### Option 2: Container Instances

**1. Push to Oracle Container Registry (OCIR)**:
```bash
# Login to OCIR
docker login <region>.ocir.io
# Username: <tenancy-namespace>/<oci-username>
# Password: <auth-token>

# Tag and push
docker tag metasploit-mcp <region>.ocir.io/<namespace>/metasploit-mcp:latest
docker push <region>.ocir.io/<namespace>/metasploit-mcp:latest
```

**2. Create Container Instance**:
- OCI Console → Compute → Container Instances
- Select image from OCIR
- Configure environment variables
- Set networking and security

#### Option 3: Kubernetes (OKE)

```bash
# Install kubectl and OCI CLI
# Configure kubectl for OKE cluster

kubectl create namespace metasploit-mcp

# Create secret
kubectl create secret generic msf-secrets \
  --from-literal=password=your_password \
  --from-literal=openrouter_key=your_api_key \
  -n metasploit-mcp

# Apply deployment
kubectl apply -f k8s/deployment.yaml
```

### OCI Free Tier Resources

- **2 AMD VMs**: 1/8 OCPU, 1GB RAM each
- **Ampere A1**: 4 OCPUs, 24GB RAM (divisible)
- **Block Storage**: 200GB total
- **Outbound Transfer**: 10TB/month
- **Load Balancer**: 1 flexible LB (10 Mbps)

### OCI Best Practices

1. **Use OCI Vault** for secrets
2. **Setup monitoring** with OCI Monitoring
3. **Configure backups** with block volume backups
4. **Use Load Balancer** for SSL termination
5. **Enable OS automatic updates**
6. **Setup logging** with OCI Logging service

---

## Self-Hosted / VPS

### Requirements

- Linux server (Ubuntu 20.04+ recommended)
- Python 3.10+
- Optional: Metasploit Framework

### Installation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.10 python3-pip git -y

# Clone repository
git clone https://github.com/FandresenaR/MetasploitMCP.git
cd MetasploitMCP

# Install dependencies
pip3 install -r requirements.txt

# Configure environment
cp .env.example .env.local
nano .env.local  # Edit with your values

# Run server
python3 MetasploitMCP.py --transport http --host 0.0.0.0 --port 8080
```

### Systemd Service

Create `/etc/systemd/system/metasploit-mcp.service`:

```ini
[Unit]
Description=MetasploitMCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/MetasploitMCP
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
EnvironmentFile=/opt/MetasploitMCP/.env.local
ExecStart=/usr/bin/python3 /opt/MetasploitMCP/MetasploitMCP.py --transport http --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable metasploit-mcp
sudo systemctl start metasploit-mcp
sudo systemctl status metasploit-mcp
```

---

## Docker Deployment

### Quick Start

```bash
# Build image
docker build -t metasploit-mcp .

# Run container
docker run -d -p 8080:8080 \
  --env-file .env.local \
  --name metasploit-mcp \
  metasploit-mcp
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  metasploit-mcp:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MSFRPCD_PASSWORD=${MSFRPCD_PASSWORD}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    restart: unless-stopped
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

Run with:
```bash
docker-compose up -d
```

---

## Kubernetes Deployment

### Kubernetes Manifests

Create `k8s/deployment.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: metasploit-mcp

---
apiVersion: v1
kind: Secret
metadata:
  name: msf-secrets
  namespace: metasploit-mcp
type: Opaque
stringData:
  msfrpcd-password: your_password_here
  openrouter-api-key: your_api_key_here

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metasploit-mcp
  namespace: metasploit-mcp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: metasploit-mcp
  template:
    metadata:
      labels:
        app: metasploit-mcp
    spec:
      containers:
      - name: metasploit-mcp
        image: your-registry/metasploit-mcp:latest
        ports:
        - containerPort: 8080
        env:
        - name: MSFRPCD_PASSWORD
          valueFrom:
            secretKeyRef:
              name: msf-secrets
              key: msfrpcd-password
        - name: OPENROUTER_API_KEY
          valueFrom:
            secretKeyRef:
              name: msf-secrets
              key: openrouter-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: metasploit-mcp
  namespace: metasploit-mcp
spec:
  selector:
    app: metasploit-mcp
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: metasploit-mcp
  namespace: metasploit-mcp
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - metasploit-mcp.yourdomain.com
    secretName: metasploit-mcp-tls
  rules:
  - host: metasploit-mcp.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: metasploit-mcp
            port:
              number: 80
```

Deploy:
```bash
kubectl apply -f k8s/deployment.yaml
```

---

## Deployment Comparison

| Platform | Complexity | Cost | Best For |
|----------|-----------|------|----------|
| **Fly.io** | ⭐ Low | $5-10/mo | Quick demos, testing |
| **Oracle Cloud** | ⭐⭐ Medium | Free tier | Production, full control |
| **Self-hosted** | ⭐⭐⭐ High | VPS costs | Custom requirements |
| **Kubernetes** | ⭐⭐⭐⭐ Very High | Variable | Enterprise, scale |

## Security Checklist

- [ ] Use strong passwords (32+ characters)
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Use secrets management
- [ ] Regular security updates
- [ ] Monitor logs and access
- [ ] Implement rate limiting
- [ ] Setup backup strategy
- [ ] Use non-root user
- [ ] Enable audit logging

## Support

For issues or questions:
- Check the [README.md](README.md)
- Review [CHANGELOG.md](CHANGELOG.md)
- Open an issue on GitHub

---

**Note**: Default configuration runs in mock mode without Metasploit. For production use with real Metasploit, configure external RPC connection or install Metasploit in the deployment environment.
