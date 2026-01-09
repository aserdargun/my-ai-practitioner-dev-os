# Skill: K8s Deploy Checklist

Deploy applications to Kubernetes with production-ready configurations.

> **Note**: This skill is gated to **Advanced** learners only. It requires foundational knowledge of Docker, networking, and cloud infrastructure.

## Trigger

Use this skill when:
- Deploying services to Kubernetes (AKS, EKS, GKE)
- Setting up production workloads
- Configuring autoscaling, health checks, and resource limits
- Managing secrets and configurations

## Prerequisites

- Docker image ready and pushed to registry
- Kubernetes cluster access (`kubectl` configured)
- Basic understanding of Kubernetes concepts (pods, deployments, services)
- Familiarity with YAML

## Steps

### 1. Create Namespace (5 min)

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-service
  labels:
    app: my-service
    environment: production
```

```bash
kubectl apply -f namespace.yaml
```

### 2. ConfigMap and Secrets (15 min)

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-service-config
  namespace: my-service
data:
  LOG_LEVEL: "INFO"
  MAX_WORKERS: "4"
  CACHE_TTL: "3600"
```

```yaml
# secret.yaml (use external secrets in production!)
apiVersion: v1
kind: Secret
metadata:
  name: my-service-secrets
  namespace: my-service
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:pass@host:5432/db"
  API_KEY: "your-secret-key"
```

```bash
# Better: Use external secrets manager
kubectl create secret generic my-service-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL" \
  --namespace my-service
```

### 3. Deployment (20 min)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-service
  namespace: my-service
  labels:
    app: my-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-service
  template:
    metadata:
      labels:
        app: my-service
    spec:
      containers:
        - name: my-service
          image: myregistry/my-service:v1.0.0
          ports:
            - containerPort: 8000

          # Environment from ConfigMap and Secrets
          envFrom:
            - configMapRef:
                name: my-service-config
            - secretRef:
                name: my-service-secrets

          # Resource limits (REQUIRED for production)
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"

          # Health checks
          livenessProbe:
            httpGet:
              path: /live
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 3

          # Security context
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false

      # Pod disruption budget compliance
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: my-service
                topologyKey: kubernetes.io/hostname
```

### 4. Service (10 min)

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: my-service
spec:
  selector:
    app: my-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

### 5. Ingress (15 min)

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-service
  namespace: my-service
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: my-service-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

### 6. Horizontal Pod Autoscaler (10 min)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-service
  namespace: my-service
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### 7. Pod Disruption Budget (5 min)

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-service
  namespace: my-service
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-service
```

### 8. Network Policy (10 min)

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: my-service
  namespace: my-service
spec:
  podSelector:
    matchLabels:
      app: my-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8000
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - protocol: TCP
          port: 5432
```

### 9. Deploy and Verify (15 min)

```bash
# Apply all manifests
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
kubectl apply -f pdb.yaml

# Verify deployment
kubectl get pods -n my-service
kubectl get deployment -n my-service
kubectl describe deployment my-service -n my-service

# Check logs
kubectl logs -l app=my-service -n my-service --tail=50

# Test service
kubectl port-forward svc/my-service 8080:80 -n my-service
curl http://localhost:8080/health

# Check HPA
kubectl get hpa -n my-service
```

### 10. Rollout Strategies (10 min)

```yaml
# deployment.yaml addition for rolling updates
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

```bash
# Deploy new version
kubectl set image deployment/my-service \
  my-service=myregistry/my-service:v1.1.0 \
  -n my-service

# Watch rollout
kubectl rollout status deployment/my-service -n my-service

# Rollback if needed
kubectl rollout undo deployment/my-service -n my-service
```

## Artifacts Produced

1. **Kubernetes Manifests** — YAML files for all resources
2. **Namespace** — Isolated environment
3. **Deployment** — Running pods
4. **Service** — Internal routing
5. **HPA** — Autoscaling configuration
6. **Documentation** — Deployment runbook

## Quality Bar

Your K8s deployment is complete when:

- [ ] Namespace created and labeled
- [ ] Secrets managed externally (not in git)
- [ ] Resource requests and limits set
- [ ] Liveness and readiness probes configured
- [ ] HPA configured for scaling
- [ ] PDB ensures availability during updates
- [ ] Pods run as non-root
- [ ] Deployment rolls out successfully
- [ ] Service responds on health endpoint
- [ ] Rollback tested and working

## Pre-Deploy Checklist

```markdown
### Security
- [ ] No secrets in manifests (use external secrets)
- [ ] Pods run as non-root
- [ ] Read-only root filesystem
- [ ] Network policies restrict traffic
- [ ] Image from trusted registry

### Reliability
- [ ] Resource limits set
- [ ] Health probes configured
- [ ] Multiple replicas
- [ ] Pod anti-affinity for spread
- [ ] PDB prevents total outage

### Operations
- [ ] Logging configured
- [ ] Metrics exposed
- [ ] Alerts configured
- [ ] Rollback tested
- [ ] Documentation updated
```

## Common Pitfalls

1. **No resource limits** — Pods can starve others
2. **No health probes** — K8s can't detect failures
3. **Secrets in git** — Security breach
4. **Single replica** — No high availability
5. **No PDB** — All pods killed during node drain
