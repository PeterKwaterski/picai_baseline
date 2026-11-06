FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime@sha256:0279f7aa29974bf64e61d0ff6e979b41a249b3662a46e30778dbf80b8c99c361

ARG NNUNET_GIT_URL=https://github.com/PeterKwaterski/nnUNet.git
ARG NNUNET_GIT_REF=v2.8.1-picai.2
ARG PICAI_BASELINE_GIT_URL=https://github.com/PeterKwaterski/picai_baseline.git
ARG PICAI_BASELINE_GIT_REF=nnunet-v2-migration

ENV PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=1 \
    MKL_THREADING_LAYER=GNU

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY constraints.txt /tmp/constraints.txt
RUN git clone --depth 1 --branch "${NNUNET_GIT_REF}" "${NNUNET_GIT_URL}" /opt/nnUNet && \
    git clone --depth 1 --branch "${PICAI_BASELINE_GIT_REF}" "${PICAI_BASELINE_GIT_URL}" /opt/picai_baseline && \
    python -m pip install --no-cache-dir -c /tmp/constraints.txt -e /opt/nnUNet -e /opt/picai_baseline && \
    python -m pip check && \
    python -c "from nnunetv2.training.nnUNetTrainer.variants.loss.nnUNetTrainerPICAI import nnUNetTrainerPICAI_FLCE" && \
    chmod +x /opt/picai_baseline/src/picai_baseline/nnunet_v2/cli.py && \
    ln -s /opt/picai_baseline/src/picai_baseline/nnunet_v2/cli.py /usr/local/bin/picai-nnunet-v2

CMD ["picai-nnunet-v2", "--help"]
