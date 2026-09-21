# Built by .github/workflows/deploy.yml and pushed to Artifact Registry.
#
# Adapted from the fleet's python stack pack. Differences, and why:
#   - CMD names THIS app's entrypoint (app.main:app) rather than the pack's
#     hardcoded guess, which is only right for a FastAPI repo shaped like this.
#   - uvicorn comes from requirements.txt, so it is not installed a second time.
#
# BASE_PATH is deliberately NOT baked in: the app reads it from the environment
# at startup (app/base_path.py), so one image serves at the host root in k8s and
# under /direct/<agent>:<port> when an agent runs it.
FROM python:3.12-slim AS build
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
COPY requirements.txt ./
RUN python -m venv /venv && /venv/bin/pip install -r requirements.txt

FROM python:3.12-slim AS runtime
ARG BUILD_ID=""
WORKDIR /app
ENV PATH=/venv/bin:$PATH PYTHONUNBUFFERED=1 PORT=8000 BUILD_ID=$BUILD_ID
RUN useradd -r -u 10001 app
COPY --from=build /venv /venv
COPY --chown=app:app . .
USER app
EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
