#!/usr/bin/env bash

docker build . \
  --build-arg NNUNET_GIT_URL=https://github.com/DIAGNijmegen/nnUNet.git \
  --build-arg NNUNET_GIT_REF=1.7.0-3 \
  --build-arg PICAI_GIT_ORG=PeterKwaterski \
  --build-arg PICAI_BASELINE_REF=main \
  --build-arg REPORT_GUIDED_ANNOTATION_GIT_URL=https://github.com/PeterKwaterski/Report-Guided-Annotation.git \
  --build-arg REPORT_GUIDED_ANNOTATION_GIT_REF=main \
  -t silverdisk/picai_nnunet:latest
