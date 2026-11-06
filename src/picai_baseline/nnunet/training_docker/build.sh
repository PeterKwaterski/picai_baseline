#!/usr/bin/env bash

docker build . \
  --build-arg PICAI_GIT_ORG=PeterKwaterski \
  --build-arg PICAI_BASELINE_REF=main \
  --tag PeterKwaterski/picai_nnunet:1.7.0-customized \
  --tag PeterKwaterski/picai_nnunet:latest \
  --tag joeranbosma/picai_nnunet:1.7.0-customized-v1.14 \
  --tag joeranbosma/picai_nnunet:latest
