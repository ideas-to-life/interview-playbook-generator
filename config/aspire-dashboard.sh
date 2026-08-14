#!/usr/bin/env bash

set -a
export OTEL_SERVICE_NAME="antigravity-cli"

# Explicitly direct OpenTelemetry SDK to use OTLP exporter
export OTEL_TRACES_EXPORTER="otlp"
export OTEL_METRICS_EXPORTER="otlp"
export OTEL_LOGS_EXPORTER="otlp"

# Use OTLP HTTP/protobuf on port 4318 (mapped to Aspire 18890)
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"

# Set payload capture mode
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="true"
set +a

# Reuse existing container if running/stopped; create with persistent volume if not present
if docker inspect aspire-dashboard >/dev/null 2>&1; then
  if [ "$(docker inspect -f '{{.State.Running}}' aspire-dashboard)" != "true" ]; then
    echo "🔄 Starting existing Aspire Dashboard container..."
    docker start aspire-dashboard >/dev/null
  fi
else
  echo "🚀 Creating persistent Aspire Dashboard container..."
  docker run -d \
    -p 18888:18888 \
    -p 4317:18889 \
    -p 4318:18890 \
    -v aspire-dashboard-data:/app/data \
    -e DOTNET_DASHBOARD_UNAUTHENTICATED_ALLOW_ANONYMOUS=true \
    -e DOTNET_DASHBOARD_UNSECURED_ALLOW_ANONYMOUS=true \
    --name aspire-dashboard \
    mcr.microsoft.com/dotnet/aspire-dashboard:latest >/dev/null
fi

# Confirm the dashboard is ready before launching the service
if ! curl -fsS http://localhost:18888 > /dev/null 2>&1; then
  echo "⚠️  Aspire Dashboard did not become ready on http://localhost:18888" >&2
fi

echo "✅ Aspire Dashboard is running at http://localhost:18888"
echo "💡 To apply OTEL settings to your current shell and launch the service, run:"
echo "   source config/aspire-dashboard.sh && agy"
