# Adapted from https://github.com/DIAGNijmegen/diag-nnunet/blob/master/Dockerfile
FROM nvcr.io/nvidia/pytorch:20.12-py3

# Override at build time, e.g. --build-arg NNUNET_GIT_URL=https://github.com/You/nnUNet.git
ARG NNUNET_GIT_URL=https://github.com/DIAGNijmegen/nnUNet.git
ARG NNUNET_GIT_REF=1.7.0-3
ARG PICAI_GIT_ORG=PeterKwaterski
ARG PICAI_BASELINE_REF=main
ARG REPORT_GUIDED_ANNOTATION_GIT_URL=https://github.com/DIAGNijmegen/Report-Guided-Annotation.git
ARG REPORT_GUIDED_ANNOTATION_GIT_REF=main
ARG HIDDENLAYER_GIT_URL=https://github.com/nanohanno/hiddenlayer.git
ARG HIDDENLAYER_GIT_REF=bugfix/get_trace_graph

RUN groupadd -r user && useradd -m --no-log-init -r -g user user

# Configuration
RUN echo "PYTHONUNBUFFERED=1" >> /etc/environment && \
    echo "OMP_NUM_THREADS=1" >> /etc/environment

# Install a few dependencies that are not automatically installed, plus nnU-net
RUN apt-get update && \
    apt-get install -y --no-install-recommends graphviz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY patch_packaging_sklearn.sh /tmp/patch_packaging_sklearn.sh
COPY install_nnunet_runtime_deps.sh /tmp/install_nnunet_runtime_deps.sh
COPY pip_constraints.txt /tmp/pip_constraints.txt
ARG NNUNET_GIT_URL
ARG NNUNET_GIT_REF
ARG HIDDENLAYER_GIT_URL
ARG HIDDENLAYER_GIT_REF
RUN sed -i 's/\r$//' /tmp/patch_packaging_sklearn.sh /tmp/install_nnunet_runtime_deps.sh && \
    chmod +x /tmp/patch_packaging_sklearn.sh /tmp/install_nnunet_runtime_deps.sh && \
    git config --global advice.detachedHead false && \
    git clone "${NNUNET_GIT_URL}" /home/user/nnunet && \
    git -C /home/user/nnunet checkout "${NNUNET_GIT_REF}" && \
    /tmp/patch_packaging_sklearn.sh /home/user/nnunet && \
    chown -R user /home/user/nnunet && \
    /tmp/install_nnunet_runtime_deps.sh /tmp/pip_constraints.txt /home/user/nnunet && \
    pip3 install -c /tmp/pip_constraints.txt \
        graphviz \
        "git+${HIDDENLAYER_GIT_URL}@${HIDDENLAYER_GIT_REF}#egg=hiddenlayer" \
        carbontracker && \
    rm -rf ~/.cache/pip

# Install MSK-Tiger IO subset
COPY io.py /tmp/io.py
RUN SITE_PKG=`pip3 show nnunet | grep "Location:" | awk '{print $2}'` && \
    mv /tmp/io.py "$SITE_PKG/nnunet/utilities/io.py"


# Install PI-CAI repositories
ARG PICAI_GIT_ORG
ARG PICAI_BASELINE_REF
ARG REPORT_GUIDED_ANNOTATION_GIT_URL
ARG REPORT_GUIDED_ANNOTATION_GIT_REF
RUN pip3 install -c /tmp/pip_constraints.txt \
    picai_eval==1.4.4 \
    picai_prep==2.1.2 \
    "git+https://github.com/${PICAI_GIT_ORG}/picai_baseline.git@${PICAI_BASELINE_REF}" \
    "git+${REPORT_GUIDED_ANNOTATION_GIT_URL}@${REPORT_GUIDED_ANNOTATION_GIT_REF}" \
    mlxtend==0.19.0 && \
    rm -rf ~/.cache/pip

# copy custom files to nnUNet folder
COPY nnUNetTrainerV2_focalLoss.py /tmp/nnUNetTrainerV2_focalLoss.py
RUN SITE_PKG=`pip3 show nnunet | grep "Location:" | awk '{print $2}'` && \
    mv /tmp/nnUNetTrainerV2_focalLoss.py "$SITE_PKG/nnunet/training/network_training/nnUNet_variants/loss_function/nnUNetTrainerV2_focalLoss.py"

COPY nnUNetTrainerV2_Loss_CE_checkpoints.py /tmp/nnUNetTrainerV2_Loss_CE_checkpoints.py
RUN SITE_PKG=`pip3 show nnunet | grep "Location:" | awk '{print $2}'` && \
    mv /tmp/nnUNetTrainerV2_Loss_CE_checkpoints.py "$SITE_PKG/nnunet/training/network_training/nnUNetTrainerV2_Loss_CE_checkpoints.py"

COPY nnUNetTrainerV2_Loss_FL_and_CE.py /tmp/nnUNetTrainerV2_Loss_FL_and_CE.py
RUN SITE_PKG=`pip3 show nnunet | grep "Location:" | awk '{print $2}'` && \
    mv /tmp/nnUNetTrainerV2_Loss_FL_and_CE.py "$SITE_PKG/nnunet/training/network_training/nnUNetTrainerV2_Loss_FL_and_CE.py"

COPY run_training.py /tmp/run_training.py
RUN SITE_PKG=`pip3 show nnunet | grep "Location:" | awk '{print $2}'` && \
    mv /tmp/run_training.py "$SITE_PKG/nnunet/run/run_training.py"

# Configure entrypoint
COPY --chown=user nnunet_wrapper.py /home/user/nnunet_wrapper.py
RUN chmod +x /home/user/nnunet_wrapper.py && \
    ln -s /home/user/nnunet_wrapper.py /usr/local/bin/nnunet
