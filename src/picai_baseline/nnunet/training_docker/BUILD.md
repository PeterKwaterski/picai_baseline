# Building the nnU-Net training image

## Prerequisites

1. Push your `picai_baseline` fork (`PeterKwaterski/picai_baseline`) so the Docker build can `pip install` it from GitHub.
2. Build on Linux/WSL (same as PI-CAI organizers).

## Default build

```bash
./build.sh
```

This applies `patch_packaging_sklearn.sh` to nnUNet after clone (fixes deprecated `sklearn` PyPI package), installs runtime deps via **`install_nnunet_runtime_deps.sh`** (pinned **`pip_constraints.txt`**, then `pip install --no-deps -e nnUNet` to avoid broken PyPI `python-gdcm` source builds), and does **not** upgrade pip.

## Custom forks / refs

```bash
docker build . \
  --build-arg NNUNET_GIT_URL=https://github.com/You/nnUNet.git \
  --build-arg NNUNET_GIT_REF=1.7.0-3-picai.1 \
  --build-arg PICAI_GIT_ORG=PeterKwaterski \
  --build-arg PICAI_BASELINE_REF=main \
  -t your/picai_nnunet:latest
```

| Build arg | Default |
|-----------|---------|
| `NNUNET_GIT_URL` | `https://github.com/DIAGNijmegen/nnUNet.git` |
| `NNUNET_GIT_REF` | `1.7.0-3` |
| `PICAI_GIT_ORG` | `PeterKwaterski` |
| `PICAI_BASELINE_REF` | `main` |
| `REPORT_GUIDED_ANNOTATION_GIT_URL` | DIAGNijmegen Report-Guided-Annotation |
| `HIDDENLAYER_GIT_URL` | nanohanno/hiddenlayer |

After you merge PI-CAI trainer patches into your nnUNet fork, point `NNUNET_GIT_URL` at your repo and drop the redundant `COPY` overlay steps if you prefer.
