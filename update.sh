#!/bin/bash

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BRANCH="main"
SERVICE_NAME="bixiviz.service"

cd "$REPO_DIR" || exit 1

git fetch origin "$BRANCH"

LOCAL=$(git rev-parse "$BRANCH")
REMOTE=$(git rev-parse "origin/$BRANCH")

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "[$(date)] New updates found. Pulling and restarting..."
  git reset --hard "origin/$BRANCH"
  $REPO_DIR/.venv/bin/pip install -r requirements
  sudo systemctl restart "$SERVICE_NAME"
  echo "Restarting done ! "
else
  echo "[$(date)] No updates. Nothing to do."
fi
