# PI-CAI nnU-Net v2 training image

This image is independent of the frozen nnU-Net v1 image. It uses:

- PyTorch 2.3.0 and CUDA 12.1
- `PeterKwaterski/nnUNet@v2.8.1-picai.1`
- `Dataset220_PICAI`
- trainer `nnUNetTrainerPICAI_FLCE`

Build after pushing the corresponding `picai_baseline` changes:

```bash
./build.sh
```

The container command is `picai-nnunet-v2` with `plan`, `train`, and `predict`
subcommands. Mount a work directory at `/workdir`.
