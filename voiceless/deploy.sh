#!/usr/bin/env bash
set -euo pipefail

# ── Configuration ──────────────────────────────────────────────
PROJECT_ID="${GCP_PROJECT_ID:?Set GCP_PROJECT_ID}"
REGION="${GCP_REGION:-us-central1}"
REPO="voiceless"
API_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/api"
WORKER_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/worker"

echo "==> Deploying Voiceless to GCP project: ${PROJECT_ID} (${REGION})"

# ── 1. Create Artifact Registry repo (first time only) ────────
gcloud artifacts repositories describe "$REPO" \
  --project="$PROJECT_ID" --location="$REGION" 2>/dev/null || \
gcloud artifacts repositories create "$REPO" \
  --project="$PROJECT_ID" --location="$REGION" \
  --repository-format=docker --description="Voiceless containers"

# ── 2. Build & push images ────────────────────────────────────
echo "==> Building API image..."
gcloud builds submit backend/ \
  --project="$PROJECT_ID" \
  --tag="${API_IMAGE}:latest"

echo "==> Building Worker image..."
gcloud builds submit backend/ \
  --project="$PROJECT_ID" \
  --tag="${WORKER_IMAGE}:latest" \
  --gcs-log-dir="gs://${PROJECT_ID}_cloudbuild/logs" \
  2>/dev/null || \
docker build -t "${WORKER_IMAGE}:latest" -f backend/Dockerfile.worker backend/ && \
docker push "${WORKER_IMAGE}:latest"

# ── 3. Deploy API to Cloud Run ────────────────────────────────
echo "==> Deploying API service..."
gcloud run deploy voiceless-api \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --image="${API_IMAGE}:latest" \
  --platform=managed \
  --allow-unauthenticated \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=3 \
  --timeout=300 \
  --set-env-vars="^||^$(grep -v '^#' backend/.env | grep -v '^$' | grep -v 'GCS_KEY_FILE' | tr '\n' '||')" \
  --update-env-vars="GCS_KEY_FILE="

# ── 4. Deploy Celery Worker to Cloud Run ──────────────────────
echo "==> Deploying Worker service..."
gcloud run deploy voiceless-worker \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --image="${WORKER_IMAGE}:latest" \
  --platform=managed \
  --no-allow-unauthenticated \
  --memory=1Gi \
  --cpu=1 \
  --min-instances=1 \
  --max-instances=2 \
  --no-cpu-throttling \
  --timeout=900 \
  --set-env-vars="^||^$(grep -v '^#' backend/.env | grep -v '^$' | grep -v 'GCS_KEY_FILE' | tr '\n' '||')" \
  --update-env-vars="GCS_KEY_FILE="

# ── 5. Print URLs ─────────────────────────────────────────────
API_URL=$(gcloud run services describe voiceless-api \
  --project="$PROJECT_ID" --region="$REGION" \
  --format="value(status.url)")

echo ""
echo "==> Deployment complete!"
echo "    API: ${API_URL}"
echo "    Set NEXT_PUBLIC_API_URL=${API_URL}/api in Vercel"
echo ""
echo "==> Next steps:"
echo "    1. Grant Cloud Run service account 'Storage Object Admin' on bucket voiceless-audio-prod"
echo "    2. Deploy frontend to Vercel: cd frontend && vercel --prod"
echo "    3. Update FRONTEND_URL env var on Cloud Run to your Vercel domain"
