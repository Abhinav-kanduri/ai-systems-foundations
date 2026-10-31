# Deployment Guide

## Local Development

### Prerequisites
- Python 3.10+
- SQLite (included with Python)
- Optional: PostgreSQL for development

### Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd reliable-multi-agent-loan-underwriting

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env with your settings

# 5. Run application
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 6. Access API
# - Interactive docs: http://localhost:8000/docs
# - API: http://localhost:8000/api/v1/applications
```

## Docker Compose (Full Stack)

### Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd reliable-multi-agent-loan-underwriting

# 2. Create .env file
cp .env.example .env
# Set OPENAI_API_KEY and other secrets

# 3. Build and start
docker-compose up --build

# 4. Access services
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - UI Dashboard: http://localhost:8501
# - Jaeger Traces: http://localhost:16686
# - Database: localhost:5432 (postgres:underwriting)
# - Redis: localhost:6379

# 5. Run migrations (if needed)
docker-compose exec api alembic upgrade head

# 6. View logs
docker-compose logs -f api
```

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

## Kubernetes Deployment (Production)

### Prerequisites
- Kubernetes cluster 1.24+
- kubectl configured
- Helm 3.0+ (optional, for templating)
- Container registry (Docker Hub, ECR, GCR, etc.)

### Build and Push Docker Image

```bash
# 1. Build image
docker build -t your-registry/loan-underwriting:v1.0.0 .

# 2. Push to registry
docker push your-registry/loan-underwriting:v1.0.0

# 3. Build UI image (optional)
docker build -f Dockerfile.ui -t your-registry/loan-underwriting-ui:v1.0.0 .
docker push your-registry/loan-underwriting-ui:v1.0.0
```

### ConfigMap and Secrets

```yaml
# config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: loan-underwriting-config
  namespace: default
data:
  APP_ENV: production
  LOG_LEVEL: INFO
  MAX_AGENT_STEPS: "12"
  MAX_TOOL_RETRIES: "3"

---
apiVersion: v1
kind: Secret
metadata:
  name: loan-underwriting-secrets
  namespace: default
type: Opaque
stringData:
  DATABASE_URL: postgresql://user:password@postgres:5432/underwriting
  REDIS_URL: redis://redis:6379/0
  OPENAI_API_KEY: your-api-key-here
```

Apply:
```bash
kubectl apply -f config.yaml
```

### API Deployment

```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-underwriting-api
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: loan-underwriting-api
  template:
    metadata:
      labels:
        app: loan-underwriting-api
    spec:
      containers:
      - name: api
        image: your-registry/loan-underwriting:v1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        
        envFrom:
        - configMapRef:
            name: loan-underwriting-config
        - secretRef:
            name: loan-underwriting-secrets
        
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2Gi
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL

---
apiVersion: v1
kind: Service
metadata:
  name: loan-underwriting-api
  namespace: default
spec:
  type: LoadBalancer
  selector:
    app: loan-underwriting-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

Apply:
```bash
kubectl apply -f api-deployment.yaml
```

### Database (PostgreSQL)

```yaml
# postgres-statefulset.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 10Gi

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: default
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        
        env:
        - name: POSTGRES_USER
          value: underwriting
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: POSTGRES_DB
          value: underwriting
        
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
          subPath: postgres
        
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 1000m
            memory: 1Gi
      
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: default
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

### Redis (Caching)

```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi

---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: default
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

### Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: loan-underwriting-ingress
  namespace: default
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.yourdomain.com
    secretName: loan-underwriting-tls
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: loan-underwriting-api
            port:
              number: 80
```

### Deploy All

```bash
# Create namespace
kubectl create namespace underwriting

# Create secrets
kubectl create secret generic postgres-secret \
  --from-literal=password=$(openssl rand -base64 32) \
  -n underwriting

kubectl create secret generic loan-underwriting-secrets \
  --from-literal=OPENAI_API_KEY=your-key-here \
  -n underwriting

# Apply manifests
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f config.yaml
kubectl apply -f api-deployment.yaml
kubectl apply -f ingress.yaml

# Verify deployment
kubectl get pods -n underwriting
kubectl get svc -n underwriting
kubectl logs -f deployment/loan-underwriting-api -n underwriting
```

## AWS Deployment

### Using ECS (Elastic Container Service)

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name loan-underwriting --region us-east-1

# 2. Build and push
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag loan-underwriting:v1.0.0 <account-id>.dkr.ecr.us-east-1.amazonaws.com/loan-underwriting:v1.0.0
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/loan-underwriting:v1.0.0

# 3. Create ECS task definition (task-definition.json)
# See AWS documentation for full template

# 4. Create ECS service
aws ecs create-service --cluster underwriting --service-name api --task-definition loan-underwriting:1 --desired-count 3 --region us-east-1
```

### Using RDS for PostgreSQL

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier loan-underwriting \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password <password> \
  --allocated-storage 20 \
  --region us-east-1
```

### Using ElastiCache for Redis

```bash
# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id loan-underwriting \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1 \
  --region us-east-1
```

## Environment Variables (Production)

```bash
# Application
APP_ENV=production
DEBUG=false

# API Server
API_HOST=0.0.0.0
API_PORT=8000

# Database (RDS)
DATABASE_URL=postgresql://user:password@loan-underwriting.us-east-1.rds.amazonaws.com:5432/underwriting

# Redis (ElastiCache)
REDIS_URL=redis://loan-underwriting.xxxxxxxxx.ng.0001.use1.cache.amazonaws.com:6379/0

# LLM
OPENAI_API_KEY=sk-xxx

# Workflow
MAX_AGENT_STEPS=12
MAX_TOOL_RETRIES=3
HUMAN_REVIEW_CONFIDENCE_THRESHOLD=0.75

# Observability
TRACE_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
LOG_LEVEL=INFO

# Security
ENABLE_CORS=false
CORS_ORIGINS=["https://yourdomain.com"]
API_KEY_REQUIRED=true
```

## Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database connectivity
curl -X GET http://localhost:8000/health

# Workflow status
curl http://localhost:8000/api/v1/status/applications/{app_id}/status
```

## Monitoring Setup

### Prometheus Scrape Config

```yaml
scrape_configs:
  - job_name: 'loan-underwriting'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboard

Create dashboard with panels:
- Workflow duration (histogram)
- Decision distribution (pie chart)
- Error rate (graph)
- Human review queue (gauge)
- Agent execution times (bar chart)

## Troubleshooting

### API not responding
```bash
# Check logs
kubectl logs deployment/loan-underwriting-api

# Check resources
kubectl describe pod <pod-name>

# Restart
kubectl rollout restart deployment/loan-underwriting-api
```

### Database connection issues
```bash
# Check database is running
kubectl exec -it postgres-0 -- psql -U underwriting -d underwriting -c "SELECT 1"

# Check connection string
echo $DATABASE_URL
```

### High latency
- Check agent logs for slowdowns
- Monitor external API latencies
- Review database query performance
- Consider caching agent responses

## Rollback

```bash
# Kubernetes rollback
kubectl rollout undo deployment/loan-underwriting-api

# AWS ECS rollback
aws ecs update-service --cluster underwriting --service api --task-definition loan-underwriting:1
```

## Security Checklist

- [ ] Enable HTTPS/TLS
- [ ] Restrict API access with API keys
- [ ] Use secrets manager for credentials
- [ ] Enable audit logging
- [ ] Set up VPC and security groups
- [ ] Enable database encryption
- [ ] Configure backup strategy
- [ ] Set up firewall rules
- [ ] Enable WAF (Web Application Firewall)
- [ ] Perform security scanning
