![AWS Image](aws.png)

# Deploy Any Project on AWS (and Get Free Credits)

Last verified: 2026-02-15

How to use this guide:
1. Do Section 1 first (account, credits, and budgets).
2. Do Section 3 (common prep) for your project.
3. Pick exactly one deployment recipe (Sections 4-9).
4. Add CI/CD (Section 10) after you have a working deployment.

This is a project-agnostic, step-by-step guide that takes you from:

1. "I have a project on my laptop"
2. to "my project is running on AWS with HTTPS"
3. while using AWS Free Tier credits (and other credits if you qualify)
4. with cost guardrails so you don't get surprised by a bill

It covers simple projects (static websites) and complex ones (many services and Kubernetes on EKS).

Important cost truth: AWS is pay-as-you-go. Credits reduce your bill, but you can still be charged if you use a Paid plan and go beyond credits or use services where credits don't apply. Set budgets before you deploy.

---

## 0) What You Need Before Starting

1. A project you can run locally.
2. A Git repo (recommended).
3. Docker installed (required for container recipes like App Runner/ECS/EKS).
4. An AWS account (this guide shows how).
5. Optional: a domain name (recommended for real deployments; required for the cleanest HTTPS setup).

If you do not want to install anything locally, you can use AWS CloudShell (a terminal in the AWS Console) for many CLI steps.

### Step 0.1: Pick One AWS Region (And Stick To It)

1. Pick a region close to your users (example: `us-east-1`).
2. Create most resources in that one region to keep things simpler.
3. Note two common exceptions:
   - CloudFront is global, but CloudFront TLS certificates must be in `us-east-1`.
   - Route 53 is global (DNS).

### Step 0.2: Define Your Placeholders (So Commands Make Sense)

In this guide you will see placeholders like `REGION` and `ACCOUNT_ID`. Replace them with your real values:

1. `REGION`: your AWS region (example: `us-east-1`).
2. `ACCOUNT_ID`: your 12-digit AWS account ID.
   - Get it with: `aws sts get-caller-identity`
3. `APP_NAME`: a short name for your app (example: `myapp`).
4. `DOMAIN`: your domain name (example: `example.com`).

### Step 0.3: Install Basic Tools (Once)

You will usually need:

1. Git
2. Docker
3. AWS CLI v2 (required for most CLI steps)

Helpful links:
- Git downloads: https://git-scm.com/downloads
- Docker install: https://docs.docker.com/get-docker/

Official AWS CLI install guide:
- https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Checkpoint: `aws --version` works in your terminal.

If you will use EKS (Kubernetes), you will also need:
1. kubectl
2. eksctl
3. Helm

---

## 1) Get An AWS Account + Free Credits (Do This First)

AWS Free Tier changed for new AWS accounts created after July 15, 2025. The main choice you will make at sign-up is: Free account plan vs Paid account plan.

### Step 1.1: Choose Your AWS Free Tier Plan (Free vs Paid)

1. Choose the "Free account plan" if you are learning and you want a hard safety cap:
   - It is designed so you don't incur charges while you explore.
   - It ends after 6 months or when your Free Tier credits are fully used (whichever happens first).
   - After the free plan expires, your account can close automatically and you can lose access to resources and data (AWS retains content for 90 days before permanent deletion).
   - It does not include access to some services/features (anything that could quickly deplete credits, hardware purchases, some Marketplace offers).
   - It is not eligible for other promotional credits and discounts.
2. Choose the "Paid account plan" if you want to deploy a real app (most production deployments):
   - You still receive AWS Free Tier credits (up to $200, typically $100 at sign-up + up to $100 by completing activities).
   - You can access far more AWS services and features.
   - You can be charged when credits run out or when you use services where credits don't apply.

Official docs:
- AWS Free Tier overview: https://aws.amazon.com/free/
- Choosing Free vs Paid plan: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html
- Free Tier FAQ (credits, expiry, eligibility): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-FAQ.html

Practical recommendation:
- If you are deploying something for real users, pick Paid plan and use budgets/alerts to stay safe.
- If you are only learning, pick Free plan and upgrade later if you need more services.

### Step 1.2: Create Your AWS Account

1. Go to the AWS Free Tier page: https://aws.amazon.com/free/
2. Click "Create account" / "Create a Free Account".
3. Complete identity verification (email and phone). AWS may require additional verification depending on your location and plan.
4. Sign in to the AWS Console as the root user (the email you signed up with).

Checkpoint: you can open the AWS Console at https://console.aws.amazon.com/ and see the AWS home page.

### Step 1.3: Secure The Root User (Do Not Skip)

The root user is the "master key" for your AWS account. You should almost never use it.

1. In the AWS Console, open your account menu (top right).
2. Choose "Security credentials".
3. Enable MFA for the root user (Authenticator app or hardware key).
4. Do not create access keys for the root user.

Why: if someone steals root credentials, they can do anything, including running expensive resources.

### Step 1.4: Create A Daily Admin Identity (Avoid Using Root)

Best practice for humans is IAM Identity Center (SSO), because it gives you short-lived credentials and avoids long-lived access keys.

1. In the AWS Console search bar, search for "IAM Identity Center".
2. Enable IAM Identity Center.
3. Create a user for yourself.
4. Create a permission set:
   - Use PowerUserAccess for day-to-day development, or
   - Use AdministratorAccess temporarily while learning (then reduce permissions later).
5. Assign the permission set to your user for your AWS account.

If you need to use the AWS CLI with IAM Identity Center, follow the official AWS CLI guide:
- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html

Checkpoint (CLI):
1. Run `aws configure sso`
2. Run `aws sts get-caller-identity`

If you cannot use IAM Identity Center:
1. Create an IAM user (not root).
2. Require MFA for that user.
3. Avoid long-lived access keys if you can; prefer roles and short-lived credentials.

### Step 1.5: Set Cost Guardrails (Budgets + Alerts)

This is how you avoid surprise bills.

1. Open "Billing and Cost Management" in the AWS Console.
2. Enable "Cost Explorer" (many cost features depend on it).
3. Create an AWS Budget with email alerts.
   - Example thresholds: 50%, 80%, 100% of your monthly limit.
4. Enable AWS Cost Anomaly Detection and create an email alert subscription.

Official docs:
- AWS Budgets: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- AWS Cost Anomaly Detection: https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html

Checkpoint: you have at least one budget alert configured and you can see it in AWS Budgets.

### Step 1.6: Confirm Your Credits (And How They Work)

1. Open Billing and Cost Management.
2. Go to the "Credits" page.
3. Verify you have Free Tier credits.
4. Note the expiration dates (Free Tier credits expire 12 months after their issuance date).

How credits apply:
1. Credits are automatically applied to eligible charges until they expire or are exhausted.
2. You can view remaining credits on the Credits page, and estimate remaining credits in Bills (Savings tab).

Official docs:
- Applying and viewing AWS credits: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/useconsolidatedbilling-credits.html

### Step 1.7: Get More Free Credits (Optional, If Eligible)

These are the most common ways people get extra AWS credits:

1. AWS Activate (startups).
   - Go to https://aws.amazon.com/activate/activate-landing/
   - Click "Get started" and sign in to your AWS account.
   - Create an Activate profile (basic company/startup info).
   - Apply for credits (amount depends on eligibility and program track).
   - After approval, confirm credits appear in Billing -> Credits.
   - Note: Free account plan accounts are not eligible for other promotional credits/discounts; use a Paid plan if you are trying to use Activate credits.
2. Promotional credit codes (from AWS events, partners, hackathons).
   - Redeem in Billing -> Credits.
3. Credits from your school/employer or an AWS partner.

Important details from AWS Free Tier docs:
1. Joining AWS Organizations or setting up AWS Control Tower can cause Free Tier credits to expire immediately and can upgrade a free plan to a paid plan.
2. Free plan accounts are not eligible for other promotional credits and discounts.

---

## 2) Pick The Right Deployment Path (Choose A Recipe)

There is no single best way to deploy to AWS. The goal is to pick the simplest option that meets your needs.

### Step 2.1: Inventory Your Project (Write This Down)

Write a short "deployment inventory" with:

1. What do you run?
   - frontend (static or SSR)
   - API server
   - background worker(s)
   - scheduled jobs (cron)
   - websocket server
2. What does it depend on?
   - database (Postgres/MySQL/DynamoDB/etc)
   - cache (Redis)
   - queue/stream (SQS/SNS/Kafka/MSK)
   - object storage (S3)
3. How is it packaged today?
   - runs directly (node/python/java)
   - Dockerfile exists
   - docker-compose exists
   - Kubernetes manifests/Helm exists
4. How many services?
   - 1 service (monolith)
   - 2-5 services
   - 6+ services (microservices)
5. Traffic:
   - small and steady
   - spiky
   - mostly background jobs

### Step 2.2: Choose A Recipe

Use this decision table:

1. Static website (HTML/CSS/JS or built SPA): use Recipe A (S3 + CloudFront).
2. Frontend that needs a server (SSR, API routes, websockets):
   - treat it like a backend service and use Recipe C (App Runner), Recipe D (ECS), Recipe E (EKS), or Recipe F (EC2).
   - do not use S3/CloudFront alone unless your framework can export a fully static build.
3. API or web app with spiky traffic: use Recipe B (Lambda + API Gateway).
4. One containerized web service with minimal ops: use Recipe C (App Runner).
5. Multiple containerized services without Kubernetes: use Recipe D (ECS Fargate).
6. You already use Kubernetes or need Kubernetes features: use Recipe E (EKS).
7. You need full VM control: use Recipe F (EC2).

Cost warning (very important):
1. EKS has a per-cluster cost, even with zero traffic. Check EKS pricing before choosing it: https://aws.amazon.com/eks/pricing/
2. NAT Gateways and Load Balancers can cost real money even for small apps.

---

## 3) Common Prep For All Recipes

Do these once per project. They prevent 80% of deployment failures.

### Step 3.1: Make Configuration Come From Environment Variables

1. Move settings into environment variables (examples):
   - PORT
   - DATABASE_URL
   - REDIS_URL
   - JWT_SECRET
   - PUBLIC_URL
2. Do not hardcode secrets in code or commit them to git.

Why: in AWS, you deploy the same build to dev/staging/prod and only change env vars.

### Step 3.2: Add A Health Endpoint

1. Add a fast endpoint like `/health` that returns HTTP 200 when the service is healthy.
2. Decide if it checks only the process ("shallow") or also dependencies like DB ("deep").
3. Do not leak secrets in the response.

Why: load balancers and orchestrators use health checks to route traffic and restart unhealthy containers.

### Step 3.3: Log To Stdout/Stderr

1. Log to stdout/stderr (not a local file).
2. Include request IDs/correlation IDs if you have them.

Why: ECS/EKS/App Runner/Lambda can ship stdout/stderr to CloudWatch.

### Step 3.4: Decide Your Data Stores (Do Not Run Databases In Containers For Production)

Typical managed choices:

1. Postgres/MySQL: Amazon RDS (or Aurora).
2. Serverless key/value: DynamoDB.
3. Cache: ElastiCache (Redis).
4. Files: S3.
5. Secrets: AWS Secrets Manager or SSM Parameter Store.

Why: managed data services handle backups, patching, and reliability better than "a DB container".

### Step 3.5: Containerize (If Using App Runner/ECS/EKS)

If you already have a Dockerfile, skip to Step 3.6.

If you do not have a Dockerfile:

1. Create a Dockerfile that:
   - builds your app
   - listens on a configurable port (PORT)
   - starts your app as the container command
2. Build it:
   - `docker build -t myapp:local .`
3. Run it:
   - `docker run --rm -p 8080:8080 -e PORT=8080 myapp:local`
4. Verify the app works in a browser or with curl.

Checkpoint: your container runs locally and responds to requests.

### Step 3.6: Decide How You Will Handle Secrets

1. For Lambda: use Lambda environment variables + Secrets Manager (recommended for real secrets).
2. For App Runner: use App Runner environment variables and/or Secrets Manager integration.
3. For ECS: use task definition secrets (Secrets Manager / SSM Parameter Store).
4. For EKS:
   - simplest: Kubernetes Secrets (acceptable for small projects; not ideal)
   - better: External Secrets Operator / Secrets Store CSI Driver + AWS Secrets Manager

Why: secrets should not be baked into container images or committed to git.

---

## 4) Recipe A: Static Website (S3 + CloudFront + HTTPS)

Best for: a static site or a built SPA (React/Vue/Angular) that produces static files.

### Step 4.1: Build Your Site

1. Run your build command (examples):
   - `npm run build`
   - `pnpm build`
2. Find your output folder (common names: `dist/`, `build/`, `out/`).

Checkpoint: you can open the output `index.html` locally and it looks correct.

### Step 4.2: Create An S3 Bucket

1. Open the S3 console.
2. Create a bucket with a globally unique name.
3. Keep "Block all public access" enabled (recommended).

Why: CloudFront will serve the site; the bucket stays private.

### Step 4.3: Upload Your Files

1. Upload the full contents of your build output folder into the bucket.
2. Preserve folder structure.

### Step 4.4: Create A CloudFront Distribution

1. Open CloudFront.
2. Create a distribution:
   - Origin: your S3 bucket
   - Viewer protocol policy: Redirect HTTP to HTTPS
   - Default root object: `index.html`
3. Restrict S3 access using Origin Access Control (OAC) so only CloudFront can read your bucket.

Official reference for private S3 + CloudFront:
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html

Checkpoint: CloudFront gives you a domain like `d123abc.cloudfront.net` and your site loads.

### Step 4.5: Add Your Own Domain + Free TLS (Optional But Recommended)

1. Buy or use a domain you control.
2. Request a public certificate in AWS Certificate Manager (ACM).
3. Validate via DNS.
4. Attach the certificate to CloudFront.
   - Note: CloudFront requires the certificate in region `us-east-1`.
5. Add DNS records pointing your domain to the CloudFront distribution.

### Step 4.6: Deploy Updates

1. Upload updated files to S3.
2. Create a CloudFront cache invalidation (or use versioned assets).

---

## 5) Recipe B: Serverless API (Lambda + API Gateway)

Best for: APIs, webhooks, event-driven processing, spiky traffic.

### Step 5.1: Package Your Code

Pick one packaging method:

1. Zip deployment (small projects).
2. Container image (large dependencies, native libs, consistent builds).

Checkpoint: you can run the code locally and it responds to a simple request/event.

### Step 5.2: Create An IAM Role For Lambda

1. Open IAM -> Roles -> Create role.
2. Trusted entity: Lambda.
3. Attach basic logging policy:
   - `AWSLambdaBasicExecutionRole`
4. Add only the extra permissions you need (S3, DynamoDB, etc).

Why: the Lambda role is what your code uses to talk to AWS services.

### Step 5.3: Create The Lambda Function

1. Open Lambda -> Create function.
2. Choose runtime or container image.
3. Configure:
   - memory
   - timeout
   - environment variables
4. Deploy your code.
5. Create a test event and run it.

Checkpoint: the function succeeds and logs appear in CloudWatch Logs.

### Step 5.4: Create An HTTP Endpoint (API Gateway)

1. Open API Gateway.
2. Create an HTTP API (simple) or REST API (more features).
3. Create routes (GET/POST/etc) and integrate them with your Lambda function.
4. Configure CORS if a browser frontend will call this API.
5. Deploy the API and copy the invoke URL.

Checkpoint: `curl <invoke-url>` returns the expected response.

### Step 5.5: Custom Domain + HTTPS (Optional)

1. Request/validate an ACM certificate in the same region as your API.
2. Create an API Gateway custom domain name.
3. Map the domain to your API stage.
4. Add DNS records.

### Step 5.6: Database Connections (Important Note)

If your Lambda connects to Postgres/MySQL:

1. Putting Lambda in a VPC is often required to reach a private RDS instance.
2. Too many DB connections can break small DBs.
3. Consider RDS Proxy for connection pooling.

---

## 6) Recipe C: One Container Service (App Runner)

Best for: "I have one web service in a container and want the simplest path".

### Step 6.1: Create An ECR Repo

1. Open ECR -> Create repository.
2. Choose "Private".

Checkpoint: you have a repo URI like `ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myapp`.

### Step 6.2: Build And Push Your Image To ECR

1. Authenticate Docker to ECR:
   - `aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com`
2. Build:
   - `docker build -t myapp:latest .`
3. Tag:
   - `docker tag myapp:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myapp:latest`
4. Push:
   - `docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myapp:latest`

Checkpoint: the image appears in your ECR repository.

### Step 6.3: Create The App Runner Service

1. Open App Runner -> Create service.
2. Source: ECR image.
3. Configure:
   - port (the port your app listens on)
   - health check path (`/health`)
   - environment variables
   - autoscaling (optional)
4. Create the service.

Checkpoint: App Runner gives you a public URL and your app loads.

### Step 6.4: Deploy Updates

1. Build and push a new image tag (do not overwrite `latest` in production; use version tags).
2. Update the App Runner service to the new image (or enable auto-deploy from ECR).

---

## 7) Recipe D: Multiple Containers Without Kubernetes (ECS Fargate)

Best for: production web apps and microservices without the operational cost of Kubernetes.

### Step 7.1: Decide Your Network Shape (VPC Basics)

In AWS, most "real" deployments use a VPC with:

1. Public subnets: things that must face the internet (like an Application Load Balancer).
2. Private subnets: your app containers and databases.
3. NAT Gateway: lets private subnets reach the internet (for package downloads, calling APIs).

Cost note: NAT Gateways and Load Balancers can be expensive if left running.
Cost note: public IPv4 addresses can also cost money; avoid assigning public IPs to tasks unless you need them.

### Step 7.2: Create Or Choose A VPC

You can do this via:

1. VPC console wizard (fast for learning), or
2. Infrastructure as Code (Terraform/CDK/CloudFormation) for repeatability.

If you use the VPC console wizard, a common "good default" for ECS/EKS/RDS is:

1. VPC -> "Create VPC" -> choose "VPC and more".
2. Pick:
   - 2 Availability Zones
   - 2 public subnets
   - 2 private subnets
   - 1 NAT Gateway (cheaper than 2; still not free)
3. Turn on DNS hostnames/support (usually enabled by default).
4. Create the VPC.

Checkpoint: you have VPC ID, at least 2 subnets, and security groups ready.

### Step 7.3: Push Your Images To ECR

Repeat Recipe C Step 6.2 for each service image you deploy.

### Step 7.4: Create An ECS Cluster (Fargate)

1. Open ECS -> Clusters -> Create cluster.
2. Choose a Fargate (serverless) cluster.

### Step 7.5: Create Task Definitions (One Per Service)

For each service:

1. ECS -> Task definitions -> Create.
2. Choose Fargate.
3. Configure:
   - task execution role (lets ECS pull from ECR and write logs)
   - task role (what your app code uses to access AWS services)
   - CPU and memory
   - container image (ECR)
   - container port(s)
   - environment variables
   - secrets (Secrets Manager / SSM Parameter Store)
   - CloudWatch logging

If you don't already have the roles:
1. Create the task execution role in IAM with trusted entity `ecs-tasks.amazonaws.com`.
2. Attach the managed policy `AmazonECSTaskExecutionRolePolicy`.
3. Add permissions for any secrets you reference (Secrets Manager / SSM).
4. Create a separate task role for your application (also trusted by `ecs-tasks.amazonaws.com`) and attach only the permissions your code needs.

Checkpoint: you can run a task and it starts.

### Step 7.6: Create ECS Services + Load Balancer (For Public Services)

For a public web service:

1. Create an Application Load Balancer (ALB) in public subnets.
2. Create a target group:
   - target type: IP
   - health check path: `/health`
3. ECS -> Cluster -> Create service:
   - launch type: Fargate
   - subnets: private subnets
   - security group: allow inbound only from the ALB security group
   - attach to the ALB target group

Checkpoint: the ALB DNS name returns HTTP 200 from your service.

### Step 7.7: Add HTTPS (ACM)

1. Request a public certificate in ACM (same region as the ALB).
2. Validate via DNS.
3. Add an ALB listener on port 443 using the certificate.
4. Redirect HTTP 80 -> HTTPS 443.

Checkpoint: your service works over HTTPS.

### Step 7.8: Connect Services Together (Internal Services)

For internal-only services:

1. Do not put them behind a public load balancer.
2. Keep them in private subnets.
3. Use private networking and security groups to allow only required traffic between services.

### Step 7.9: Deploy Updates

1. Build and push a new image tag to ECR.
2. Create a new task definition revision using the new tag.
3. Update the ECS service to the new task definition revision.
4. Watch the deployment until it stabilizes.

### Step 7.10: Add Background Workers (Common In Complex Projects)

If you have a worker (queue consumer, event processor, etc):

1. Create a separate task definition for the worker (often the same image, different command).
2. Create an ECS service for it with no public load balancer.
3. Put it in private subnets.
4. Give it a task role with only the permissions it needs.

Checkpoint: the worker service tasks stay Running and process jobs.

### Step 7.11: Add Scheduled Jobs (Cron)

If you need "run this every X minutes":

1. Create a task definition that runs one job and then exits.
2. Use Amazon EventBridge to schedule an ECS task run.
3. Monitor failures in CloudWatch Logs and alarms.

Checkpoint: the scheduled job runs on schedule and you can see logs for each run.

---

## 8) Recipe E: Kubernetes On AWS (EKS)

Best for: projects that already use Kubernetes (manifests/Helm) or require Kubernetes features.

This recipe uses `eksctl` because it's the most approachable way to create an EKS cluster.

### Step 8.1: Understand The Baseline Cost

EKS has a per-cluster charge, plus you pay for worker nodes, load balancers, NAT, and anything else you create.
Public IPv4 addresses can also incur charges if you assign them to workloads/nodes unnecessarily.

1. Before you choose EKS, review current EKS pricing:
   - https://aws.amazon.com/eks/pricing/
2. If your project can run on ECS Fargate, that is often cheaper and simpler.

### Step 8.2: Install Your Local Tools

You need:

1. AWS CLI v2 (`aws --version`)
2. kubectl (`kubectl version --client`)
3. eksctl (`eksctl version`)
4. Helm (`helm version`) if you deploy with Helm charts

### Step 8.3: Configure AWS Credentials

1. If you use IAM Identity Center: `aws configure sso`
2. Verify credentials: `aws sts get-caller-identity`

### Step 8.4: Create The EKS Cluster

1. Choose:
   - cluster name
   - region
   - Kubernetes version (pick a version supported by EKS today)
   - node instance type and count (this is a big cost driver)
2. Create the cluster (example):
   - `eksctl create cluster --name CLUSTER_NAME --region REGION --managed`
3. Update kubeconfig (if needed):
   - `aws eks update-kubeconfig --name CLUSTER_NAME --region REGION`

Checkpoint: `kubectl get nodes` shows Ready nodes.

### Step 8.5: Set Up Pod Permissions Without Static AWS Keys (IRSA / Pod Identity)

Do not put AWS access keys into Kubernetes secrets for production.

Common options:

1. IRSA (IAM Roles for Service Accounts): widely used, proven.
2. EKS Pod Identity Associations: a newer approach that simplifies role reuse across clusters.

References:
- eksctl IRSA guide: https://docs.aws.amazon.com/eks/latest/eksctl/iamserviceaccounts.html
- eksctl Pod Identity Associations: https://docs.aws.amazon.com/eks/latest/eksctl/pod-identity-associations.html

### Step 8.6: Push Images To ECR

1. Create ECR repos for each service.
2. Build/tag/push images (same as Recipe C).

### Step 8.7: Deploy Your App (Helm Or kubectl)

1. If you use Helm:
   - `helm upgrade --install <release> <chart> --namespace <ns> --create-namespace`
2. If you use raw YAML:
   - `kubectl apply -f k8s/`
3. Verify:
   - `kubectl get pods -A`
   - `kubectl logs <pod> -n <ns>`

Checkpoint: all pods are Running and Ready.

### Step 8.8: Expose Your App To The Internet (Two Options)

Option 1 (simplest): Service type LoadBalancer

1. Create a Service with `type: LoadBalancer`.
2. Wait for AWS to provision a load balancer.
3. Get the URL:
   - `kubectl get svc -n <ns>`

Option 2 (recommended for multiple hosts/services): AWS Load Balancer Controller + Ingress

1. Install AWS Load Balancer Controller (official AWS EKS guide):
   - https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html
2. Create an Ingress resource for your app.
3. Use ACM for TLS termination at the load balancer.

Why use the controller: it supports ALBs (Ingress) and is the recommended way to provision load balancers from Kubernetes.

### Step 8.9: Observability Basics

1. Configure CloudWatch logging (Container Insights) or another logging stack.
2. Create alarms for:
   - high CPU/memory
   - pod restarts
   - 5xx error rates on your load balancer

### Step 8.10: Deploy Updates + Rollbacks

1. Push new image tags.
2. Update your Deployment (or Helm values) to use the new tag.
3. Watch rollout:
   - `kubectl rollout status deployment/<name> -n <ns>`
4. Roll back if needed:
   - `kubectl rollout undo deployment/<name> -n <ns>`

### Step 8.11: Multi-Service Kubernetes (How Complex Projects Usually Look)

If your project has many services (frontend, API, websocket, workers, etc):

1. Deploy each service as its own Deployment (or Helm release).
2. Expose only your public entry points to the internet (usually one Ingress/ALB).
3. Keep internal services private with ClusterIP Services.
4. Put shared config in ConfigMaps and secrets in Secrets (or sync secrets from Secrets Manager).
5. Use separate namespaces for environments (example: `dev`, `staging`, `prod`) if you can.

Checkpoint: you can reach public services externally, and internal services only from within the cluster.

### Step 8.12: Workers + CronJobs

1. Background workers: Deploy as a Deployment with no Ingress and no public Service.
2. Cron: Use Kubernetes CronJob for scheduled jobs.

Checkpoint: workers stay Running; CronJobs create Jobs on schedule.

---

## 9) Recipe F: Virtual Machine On AWS (EC2)

Best for: legacy apps, custom OS needs, or when you want full control.

### Step 9.1: Launch An EC2 Instance

1. Open EC2 -> Launch instance.
2. Choose an OS (Ubuntu LTS is a common default).
3. Choose an instance type (start small).
4. Create/select a key pair (SSH).
5. Create/select a security group:
   - allow SSH (22) from your IP only
   - allow HTTP (80) and HTTPS (443) from anywhere (for web apps)
6. Launch the instance.

Checkpoint: you can see the instance running and it has a public IPv4/DNS name.

### Step 9.2: Connect To The Instance

1. Use SSH with your key pair.
2. Update packages on the server.

### Step 9.3: Deploy Your App

Two common approaches:

1. Run directly (install node/python/java and run the app).
2. Run with Docker (recommended if you already have containers).

Checkpoint: your app responds on a local port (like 8080) on the server.

### Step 9.4: Add A Reverse Proxy + HTTPS

1. Install Nginx.
2. Configure Nginx to proxy traffic to your app port.
3. Use Let's Encrypt (certbot) for HTTPS certificates.
4. Point your domain DNS to the EC2 public IP/DNS.

Checkpoint: your app loads via your domain over HTTPS.

---

## 10) CI/CD (Deploy Automatically On Every Push)

You can deploy with many tools. A secure, modern baseline is:

1. Build and test on every push.
2. Build a container image.
3. Push to ECR.
4. Deploy to ECS/EKS/App Runner.
5. Use OIDC from your CI provider (like GitHub Actions) to assume an AWS role (no long-lived AWS keys).

### Step 10.1: Set Up GitHub Actions OIDC (Recommended)

This is the safest common setup because you do not store AWS access keys in GitHub Secrets.

1. In AWS IAM, create an OpenID Connect (OIDC) provider for GitHub:
   - provider URL: `https://token.actions.githubusercontent.com`
   - audience: `sts.amazonaws.com`
2. In AWS IAM, create a role for GitHub Actions:
   - trusted entity: the OIDC provider you created
   - restrict the trust policy to your repo (and optionally a specific branch/environment)
3. Attach permissions to that role:
   - minimum for pushing images: ECR push permissions
   - plus deploy permissions (ECS/EKS/App Runner depending on your target)
4. In your GitHub workflow:
   - request OIDC token permissions (`id-token: write`)
   - assume the AWS role via an AWS credentials action
   - build and push images
   - deploy

Checkpoint: a GitHub Actions run can call `aws sts get-caller-identity` without any stored AWS keys.

Reference for GitHub OIDC role security considerations:
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html

---

## 11) Cleanup Checklist (Stop Paying)

When you're done, delete resources in this order:

1. Compute:
   - EKS clusters
   - ECS services and clusters
   - EC2 instances
   - App Runner services
   - Lambda functions (if you want to fully clean)
2. Load balancers:
   - ALB/NLB and target groups
3. Databases and streams:
   - RDS/Aurora (snapshot first if needed)
   - MSK (Kafka) clusters
4. Networking:
   - NAT Gateways (often a top cost item)
   - unused Elastic IPs
5. Container registry:
   - ECR images and repos (optional)

Final checkpoint:
1. Open Billing the next day and confirm spend is near zero.

---

## 12) Troubleshooting (Most Common Problems)

Use this checklist in order:

1. DNS issues:
   - DNS changes can take time to propagate.
   - Verify you pointed to the correct AWS DNS name.
2. 502/503 from a load balancer:
   - health check path wrong (`/health`)
   - app not listening on the port you think it is
   - security group blocks traffic
3. Container won't start:
   - check logs (CloudWatch / ECS logs / `kubectl logs`)
   - missing env vars or secrets
4. Can't pull from ECR:
   - wrong repo URI/region
   - missing IAM permissions for the task/pod role
5. Database connection timeouts:
   - DB is private but app is not in the same VPC/subnets
   - security group rules missing
   - Lambda in VPC without correct routing
6. Costs growing unexpectedly:
   - NAT Gateways, Load Balancers, EKS cluster fees, MSK, and data transfer are common causes.
   - verify budgets and anomaly detection are enabled.

---

## Official Links

Account, credits, and cost safety:
- AWS Free Tier: https://aws.amazon.com/free/
- Free Tier plans (Free vs Paid): https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html
- Free Tier FAQ: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-FAQ.html
- Viewing/applying credits: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/useconsolidatedbilling-credits.html
- AWS Budgets: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- Cost Anomaly Detection: https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html

Deployment building blocks:
- CloudFront private S3 (OAC): https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html
- AWS CLI SSO config: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html
- EKS pricing: https://aws.amazon.com/eks/pricing/
- AWS Load Balancer Controller (EKS): https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html
- GitHub OIDC trust policy guidance: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html

Extra credits:
- AWS Activate: https://aws.amazon.com/activate/activate-landing/

---

Built with precision by DanielCodeForge
