# AWS Lightsail Container Deployment Runbook

## 1. Purpose

This runbook explains how to deploy the FastAPI Agentic RAG application from a local Docker image to an AWS Lightsail container service.

## 2. Prerequisites

- Docker Desktop installed and running
- AWS CLI installed and authenticated
- `lightsailctl` installed
- AWS Lightsail container service available
- A working Dockerfile
- Required API keys available locally in `.env`

Do not commit or upload `.env` to GitHub or Docker.

## 3. Open the project folder

```bash
cd "/Users/adhok./Desktop/Project-Enterprise-IT-Support-Agentic-RAG-Copilot/Enterprise-IT-Support-Agentic-RAG-Copilot"
```

Confirm the folder contains:

```text
Dockerfile
requirements.txt
app/
```

## 4. Build the Docker image

Build an AMD64 image for Lightsail:

```bash
docker build --platform linux/amd64 -t it-support-rag .
```

The local image name is:

```text
it-support-rag:latest
```

## 5. Test the image locally

```bash
docker run --rm --platform linux/amd64 \
  -p 8080:8080 \
  --env-file .env \
  it-support-rag
```

Verify locally:

```text
http://localhost:8080/api/health
```

Expected response:

```json
{"status":"ok","service":"Enterprise IT Support Agentic RAG Copilot"}
```

Stop the local container with `Ctrl+C` after testing.

## 6. Create the Lightsail container service

In the AWS Lightsail console:

1. Open **Containers**.
2. Choose **Create container service**.
3. Use a DNS-compatible service name, for example:

```text
it-support-rag
```

4. Select the required region, such as Mumbai (`ap-south-1`).
5. Select the plan and node count.
6. Create the service.
7. Wait until the service is ready or running.

The service must exist before an image can be pushed.

## 7. Push the image to Lightsail

Run this from the project folder:

```bash
aws lightsail push-container-image \
  --region ap-south-1 \
  --service-name it-support-rag \
  --label app \
  --image it-support-rag:latest
```

The command uploads the local image and returns a Lightsail image reference, for example:

```text
:it-support-rag.app.1
```

Copy the exact reference returned by the command.

## 8. Configure the deployment

In Lightsail, open **Deployments → Set up deployment → Specify a custom deployment**.

Use:

| Setting | Value |
|---|---|
| Container name | `app` |
| Image | The exact reference returned by `push-container-image` |
| Launch command | Leave blank; Dockerfile already defines it |
| Open port | `8080` |
| Protocol | `HTTP` |
| Public endpoint | Enabled |
| Health check path | `/api/health` |

Add the variables from the local `.env` manually in Lightsail. Typical variables include:

```text
OPENAI_API_KEY
OPENAI_MODEL
TAVILY_API_KEY
PINECONE_API_KEY
PINECONE_INDEX_NAME
PINECONE_NAMESPACE
EMBEDDING_MODEL
TOP_K
MAX_RETRIES
ADMIN_API_KEY
```

Do not add `PORT` unless your application specifically requires it.

## 9. Deploy

1. Select container `app` as the public endpoint container.
2. Review the image, port, health path, and environment variables.
3. Choose **Deploy**.
4. Wait for the deployment status to become **Active**.

## 10. Verify the public deployment

Open the Lightsail public domain and append:

```text
/api/health
```

Example:

```text
https://YOUR_PUBLIC_DOMAIN/api/health
```

The FastAPI Swagger interface is available at:

```text
https://YOUR_PUBLIC_DOMAIN/docs
```

Use `/docs` to test the chat API.

## 11. Troubleshooting

### Service error during image push

If you see:

```text
You must create a container service before retrieving container registry login credentials
```

Create the Lightsail container service first, wait until it is ready, and rerun the push command.

### Deployment is unhealthy

Check:

- Container port is `8080`.
- Health path is `/api/health`.
- Required environment variables were entered.
- Dockerfile starts Uvicorn on `0.0.0.0`.
- Open the container logs in Lightsail.

### Missing Python module

Add the missing package to `requirements.txt`, rebuild the image, push it with a new label, and deploy the new image reference.

## 12. Cleanup after a demo

To stop ongoing Lightsail container-service charges, delete the service after the demo:

```bash
aws lightsail delete-container-service \
  --region ap-south-1 \
  --service-name it-support-rag
```

Deletion removes the Lightsail service and public URL, but does not delete the local project or Docker image on your Mac.
