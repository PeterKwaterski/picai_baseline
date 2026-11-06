#!/usr/bin/env bash
# Install nnUNet install_requires with pinned constraints, then nnUNet itself without
# re-resolving deps (avoids PyPI python-gdcm source builds on Python 3.8).
set -euo pipefail

CONSTRAINTS="${1:?constraints file path}"
NNUNET_ROOT="${2:?nnUNet checkout path}"

pip3 install -c "${CONSTRAINTS}" \
    tqdm \
    'dicom2nifti==2.3.2' \
    'pydicom>=2.3.0,<3.0' \
    'scikit-image>=0.17.0,<0.19.0' \
    'medpy==0.5.2' \
    'batchgenerators==0.25.6' \
    'scikit-learn>=1.0.2,<1.3' \
    'SimpleITK>=2.0.0,<2.2.0' \
    pandas \
    requests \
    nibabel \
    tifffile

pip3 install -c "${CONSTRAINTS}" --no-deps -e "${NNUNET_ROOT}"
