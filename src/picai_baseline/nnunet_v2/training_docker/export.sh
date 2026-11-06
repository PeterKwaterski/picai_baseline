#!/usr/bin/env bash
set -euo pipefail

docker save silverdisk/picai_nnunet_v2:2.8.1-picai.1 |
  gzip > picai_nnunet_v2_2.8.1-picai.1.tar.gz
