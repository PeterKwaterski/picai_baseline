#!/usr/bin/env bash
set -euo pipefail

docker build . \
  --build-arg NNUNET_GIT_REF=v2.8.1-picai.2 \
  --build-arg PICAI_BASELINE_GIT_REF=nnunet-v2-migration \
  --tag silverdisk/picai_nnunet_v2:2.8.1-picai.2 \
  --tag silverdisk/picai_nnunet_v2:latest
