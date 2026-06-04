# StatEdge Pro Deployment Guide

## Overview

This guide provides instructions for deploying StatEdge Pro in various environments. StatEdge Pro is designed for both development and production use with containerization for easy deployment.

## Prerequisites

Before deploying StatEdge Pro, ensure you have the following:

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows 10/11
- **CPU**: 4+ cores (8+ recommended for production)
- **RAM**: 8GB minimum (16GB+ recommended for production)
- **Storage**: 50GB+ free space (SSD recommended)
- **Network**: Stable internet connection

### Software Requirements

- **Docker**: Version 20.10+
- **Docker Compose**: Version 1.29+
- **Git**: Version 2.30+
- **Python**: Version 3.10+
- **Make**: Version 4.3+

## Development Environment

### Local Setup

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/statedge-pro.git
cd statedge-pro
```

2. **Create environment variables**:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Application
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
APP_SECRET_KEY=your-super-secret-key-here

# Database
DB_HOST=db
DB_PORT=5432
DB_NAME=statedge_pro
DB_USER=postgres
DB_PASSWORD=your-postgres-password-here

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password-here

# AI Models
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-email-password-here
```

3. **Build and start the services**:

```bash
make up
```

This will:
- Build the StatEdge Pro Docker image
- Start the PostgreSQL database
- Start the Redis cache
- Start the ChromaDB vector database
- Start the StatEdge Pro application

4. **Verify the deployment**:

Open your browser and navigate to `http://localhost:8000/health` to verify the API is running:

```json
{
  "status": "healthy",
  "service": "StatEdge Pro API",
  "version": "1.0.0",
  "environment": "development"
}
```

5. **Access the API documentation**:

Navigate to `http://localhost:8000/docs` to access the interactive Swagger UI documentation.

### Development Workflow

For development, use the following commands:

```bash
# Start the application in development mode
make run

# Run tests
make test

# Run tests with coverage
make test-coverage

# Lint the code
make lint

# Format the code
make format

# Type check the code
make type-check

# Build the Docker image
make build

# Run with Docker
make run-docker

# Stop all services
make down
```

## Production Deployment

### Cloud Provider Options

StatEdge Pro can be deployed on any cloud provider that supports Docker containers:

- **AWS**: Amazon ECS, EKS, or EC2
- **Google Cloud**: Google Kubernetes Engine (GKE)
- **Azure**: Azure Kubernetes Service (AKS)
- **DigitalOcean**: Kubernetes Service
- **Vercel**: For the frontend (if using a web interface)

### Production Architecture

The production architecture consists of:

- **Application**: StatEdge Pro API (containerized)
- **Database**: PostgreSQL (managed service recommended)
- **Cache**: Redis (managed service recommended)
- **Vector Database**: ChromaDB (self-hosted or managed)
- **Load Balancer**: For traffic distribution
- **Reverse Proxy**: Nginx or Traefik for SSL termination
- **Monitoring**: Prometheus and Grafana
- **Logging**: ELK Stack or similar
- **Backup**: Automated database backups

### Deployment Steps

1. **Set up your cloud infrastructure**:

   - Create a Kubernetes cluster or container service
   - Set up a managed PostgreSQL database
   - Set up a managed Redis instance
   - Configure DNS records for your domain

2. **Configure environment variables**:

   Create a `.env.prod` file with production settings:

   ```env
   # Application
   APP_ENV=production
   APP_HOST=0.0.0.0
   APP_PORT=8000
   APP_SECRET_KEY=your-production-secret-key-here
   
   # Database
   DB_HOST=your-postgres-host
   DB_PORT=5432
   DB_NAME=statedge_pro
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   
   # Redis
   REDIS_HOST=your-redis-host
   REDIS_PORT=6379
   REDIS_PASSWORD=your-redis-password
   
   # AI Models
   OPENAI_API_KEY=your-openai-api-key-here
   ANTHROPIC_API_KEY=your-anthropic-api-key-here
   
   # Logging
   LOG_LEVEL=INFO
   LOG_FORMAT=json
   
   # CORS
   CORS_ORIGINS=https://statedge-pro.com
   
   # Email
   EMAIL_HOST=smtp.your-email-provider.com
   EMAIL_PORT=587
   EMAIL_USER=your-email@your-domain.com
   EMAIL_PASSWORD=your-email-password
   
   # Security
   SSL_CERTIFICATE_PATH=/etc/ssl/certs/your-cert.pem
   SSL_KEY_PATH=/etc/ssl/private/your-key.pem
   ```

3. **Build the production Docker image**:

   ```bash
   docker build -t statedge-pro:latest .
   ```

4. **Push the image to your container registry**:

   ```bash
   # For AWS ECR
   aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
   docker tag statedge-pro:latest your-account-id.dkr.ecr.your-region.amazonaws.com/statedge-pro:latest
   docker push your-account-id.dkr.ecr.your-region.amazonaws.com/statedge-pro:latest
   
   # For Google Container Registry
   docker tag statedge-pro:latest gcr.io/your-project-id/statedge-pro:latest
   docker push gcr.io/your-project-id/statedge-pro:latest
   
   # For Azure Container Registry
   docker tag statedge-pro:latest your-registry-name.azurecr.io/statedge-pro:latest
   docker push your-registry-name.azurecr.io/statedge-pro:latest
   ```

5. **Deploy to Kubernetes**:

   Create a `kubernetes-deployment.yaml` file:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: statedge-pro
     labels:
       app: statedge-pro
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: statedge-pro
     template:
       metadata:
         labels:
           app: statedge-pro
       spec:
         containers:
         - name: statedge-pro
           image: your-registry-name.azurecr.io/statedge-pro:latest
           ports:
           - containerPort: 8000
           env:
           - name: APP_ENV
             value: "production"
           - name: APP_HOST
             value: "0.0.0.0"
           - name: APP_PORT
             value: "8000"
           - name: APP_SECRET_KEY
             valueFrom:
               secretKeyRef:
                 name: statedge-pro-secrets
                 key: APP_SECRET_KEY
           - name: DB_HOST
             value: "your-postgres-host"
           - name: DB_PORT
             value: "5432"
           - name: DB_NAME
             value: "statedge_pro"
           - name: DB_USER
             valueFrom:
               secretKeyRef:
                 name: statedge-pro-secrets
                 key: DB_USER
           - name: DB_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: statedge-pro-secrets
                 key: DB_PASSWORD
           - name: REDIS_HOST
             value: "your-redis-host"
           - name: REDIS_PORT
             value: "6379"
           - name: REDIS_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: statedge-pro-secrets
                 key: REDIS_PASSWORD
           - name: OPENAI_API_KEY
             valueFrom:
               secretKeyRef:
                 name: statedge-pro-secrets
                 key: OPENAI_API_KEY
           - name: ANTHROPIC_API_KEY
             valueFrom:
               secretKeyRef:
                 name: statedge-pro-secrets
                 key: ANTHROPIC_API_KEY
           - name: LOG_LEVEL
             value: "INFO"
           - name: LOG_FORMAT
             value: "json"
           - name: CORS_ORIGINS
             value: "https://statedge-pro.com"
           resources:
             requests:
               memory: "512Mi"
               cpu: "250m"
             limits:
               memory: "1Gi"
               cpu: "500m"
           readinessProbe:
             httpGet:
               path: /health
               port: 8000
             initialDelaySeconds: 30
             periodSeconds: 10
           livenessProbe:
             httpGet:
               path: /health
               port: 8000
             initialDelaySeconds: 60
             periodSeconds: 15
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: statedge-pro
     labels:
       app: statedge-pro
   spec:
     selector:
       app: statedge-pro
     ports:
       - protocol: TCP
         port: 80
         targetPort: 8000
     type: LoadBalancer
   ---
   apiVersion: v1
   kind: Secret
   metadata:
     name: statedge-pro-secrets
   type: Opaque
   data:
     APP_SECRET_KEY: eW91ci1wcm9kdWN0aW9uLXNlY3JldC1rZXktaGVyZQ==
     DB_USER: eW91ci1kYi11c2Vy
     DB_PASSWORD: eW91ci1kYi1wYXNzd29yZA==
     REDIS_PASSWORD: eW91ci1yZWRpcy1wYXNzd29yZA==
     OPENAI_API_KEY: eW91ci1vcGVuYWlpLWFwaS1rZXktaGVyZQ==
     ANTHROPIC_API_KEY: eW91ci1hbnRocm9waWMtYXBpLWtleS1oZXJl
   ```

   Apply the deployment:

   ```bash
   kubectl apply -f kubernetes-deployment.yaml
   ```

6. **Set up a reverse proxy**:

   Create an Nginx configuration file (`nginx.conf`):

   ```nginx
   upstream statedge_pro {
       server statedge-pro:8000;
   }
   
   server {
       listen 80;
       server_name statedge-pro.com www.statedge-pro.com;
       
       # Redirect HTTP to HTTPS
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl http2;
       server_name statedge-pro.com www.statedge-pro.com;
       
       # SSL certificates
       ssl_certificate /etc/ssl/certs/statedge-pro.com.crt;
       ssl_certificate_key /etc/ssl/private/statedge-pro.com.key;
       
       # SSL settings
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
       ssl_prefer_server_ciphers off;
       ssl_session_cache shared:SSL:10m;
       ssl_session_timeout 10m;
       
       # Security headers
       add_header X-Frame-Options "SAMEORIGIN" always;
       add_header X-XSS-Protection "1; mode=block" always;
       add_header X-Content-Type-Options "nosniff" always;
       add_header Referrer-Policy "strict-origin-when-cross-origin" always;
       add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
       
       # Rate limiting
       limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
       
       location / {
           proxy_pass http://statedge_pro;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           
           # Increase timeout for long-running requests
           proxy_read_timeout 300s;
           proxy_connect_timeout 300s;
           proxy_send_timeout 300s;
       }
       
       # API rate limiting
       location /api/ {
           limit_req zone=api burst=20 nodelay;
           proxy_pass http://statedge_pro;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Deploy the Nginx configuration:

   ```bash
   docker run -d --name nginx-proxy \
     -p 80:80 \
     -p 443:443 \
     -v /path/to/nginx.conf:/etc/nginx/nginx.conf:ro \
     -v /path/to/certs:/etc/ssl/certs:ro \
     -v /path/to/private:/etc/ssl/private:ro \
     nginx:latest
   ```

7. **Set up monitoring and logging**:

   Create a `monitoring.yaml` file for Prometheus and Grafana:

   ```yaml
   # Prometheus configuration
   global:
     scrape_interval: 15s
     evaluation_interval: 15s
   
   scrape_configs:
     - job_name: 'statedge-pro'
       static_configs:
         - targets: ['statedge-pro:8000']
       metrics_path: '/metrics'
   
   # Grafana configuration (in Grafana UI)
   # Add Prometheus as a data source
   # Create dashboards for:
   # - API request rates
   # - Error rates
   # - Response times
   # - Memory and CPU usage
   # - Database connections
   # - Redis usage
   ```

   Deploy the monitoring stack:

   ```bash
   # Prometheus
   docker run -d --name=prometheus \
     -p 9090:9090 \
     -v /path/to/prometheus.yaml:/etc/prometheus/prometheus.yml \
     prom/prometheus
   
   # Grafana
   docker run -d --name=grafana \
     -p 3000:3000 \
     grafana/grafana
   ```

## Scaling

### Horizontal Scaling

To scale StatEdge Pro horizontally:

1. **Increase API gateway replicas**:

   ```bash
   kubectl scale deployment/statedge-pro --replicas=5
   ```

2. **Scale the analytics engine**:

   - Add more replicas of the API service
   - Use a load balancer to distribute traffic
   - Consider adding read replicas for the database

3. **Database scaling**:

   - Use a managed database service with automatic scaling
   - Implement connection pooling
   - Use read replicas for read-heavy operations

### Vertical Scaling

To scale vertically:

1. **Increase CPU and memory**:

   - Update the resource limits in the deployment configuration
   - Restart the containers with new resource limits

2. **Storage scaling**:

   - Increase storage volume size for the database
   - Add more storage for logs and backups

## Backup and Recovery

### Database Backup

Set up automated backups for PostgreSQL:

```bash
# Daily backup script
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/postgres"
DB_NAME="statedge_pro"
DB_USER="postgres"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create backup
pg_dump -h your-postgres-host -U $DB_USER $DB_NAME > $BACKUP_DIR/${DB_NAME}_${DATE}.sql

# Compress backup
gzip $BACKUP_DIR/${DB_NAME}_${DATE}.sql

# Keep only the last 7 days of backups
find $BACKUP_DIR -name "${DB_NAME}_*.sql.gz" -mtime +7 -delete
```

Schedule the backup with cron:

```bash
# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

### Redis Backup

Redis persistence is enabled by default, but you should also set up periodic snapshots:

```bash
# Create a snapshot
redis-cli save

# Copy the RDB file
cp /var/lib/redis/dump.rdb /backups/redis/dump_${DATE}.rdb
```

### ChromaDB Backup

ChromaDB uses SQLite by default, so backup the database file:

```bash
# Copy the ChromaDB database file
cp /app/data/chroma/chroma.sqlite3 /backups/chromadb/chroma_${DATE}.sqlite3
```

### Recovery Procedure

1. **Stop all services**
2. **Restore the database**:
   - PostgreSQL: `psql -h your-postgres-host -U postgres statedge_pro < backup.sql`
   - Redis: Copy the RDB file back to `/var/lib/redis/`
   - ChromaDB: Copy the SQLite file back to `/app/data/chroma/`
3. **Restart all services**
4. **Verify data integrity**

## Security Hardening

### Network Security

- Use a firewall to restrict access to only necessary ports
- Implement network policies in Kubernetes
- Use private subnets for databases
- Use a WAF (Web Application Firewall) for the API

### Authentication and Authorization

- Use strong, randomly generated API keys
- Implement rate limiting
- Use HTTPS exclusively
- Implement CORS policies

### Data Security

- Encrypt data at rest (database files, backups)
- Use TLS 1.3 for data in transit
- Implement data retention policies
- Use secure key management for secrets

### Monitoring and Alerting

- Set up alerts for:
  - High CPU or memory usage
  - High error rates
  - Database connection issues
  - Failed authentication attempts
  - Unexpected traffic spikes

### Regular Security Audits

- Perform regular vulnerability scans
- Update dependencies regularly
- Monitor for security advisories
- Conduct penetration testing

## Maintenance

### Updates

1. **Update the application**:
   - Pull the latest code
   - Build a new Docker image
   - Push to your container registry
   - Deploy the new version

2. **Update dependencies**:
   - Regularly update Python packages
   - Update Docker base images
   - Update system packages

### Performance Monitoring

- Monitor API response times
- Track database query performance
- Monitor Redis cache hit rates
- Track AI model inference times
- Monitor system resource usage

### Log Management

- Aggregate logs from all services
- Set up log rotation
- Implement log retention policies
- Search and analyze logs for issues

## Troubleshooting

### Common Issues

**Issue**: API returns 502 Bad Gateway
- **Solution**: Check if the StatEdge Pro container is running
- **Solution**: Check if the database is accessible
- **Solution**: Check network connectivity between services

**Issue**: High CPU usage
- **Solution**: Check for infinite loops in AI models
- **Solution**: Check for excessive API calls
- **Solution**: Scale up resources

**Issue**: Database connection errors
- **Solution**: Check database credentials
- **Solution**: Check database availability
- **Solution**: Check network connectivity

**Issue**: AI model not generating predictions
- **Solution**: Check AI model training status
- **Solution**: Check data feed connectivity
- **Solution**: Check API key permissions

### Debugging Commands

```bash
# Check container status
kubectl get pods

# View container logs
kubectl logs statedge-pro-xxxxx

# Get detailed pod information
kubectl describe pod statedge-pro-xxxxx

# Execute command in container
kubectl exec -it statedge-pro-xxxxx -- /bin/bash

# Check database connections
kubectl exec -it statedge-pro-xxxxx -- psql -h your-postgres-host -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Check Redis connection
kubectl exec -it statedge-pro-xxxxx -- redis-cli ping

# Check ChromaDB connection
kubectl exec -it statedge-pro-xxxxx -- curl http://chromadb:8000/health
```

## Support

For support, please contact us at sahjonycapitalllc@outlook.com.