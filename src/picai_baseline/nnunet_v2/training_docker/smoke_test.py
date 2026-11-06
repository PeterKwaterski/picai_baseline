"""Create a tiny synthetic dataset and run a short nnU-Net v2 CPU fold."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import SimpleITK as sitk


def run(*command: str) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.check_call(command)


def main() -> None:
    root = Path(tempfile.mkdtemp(prefix="picai-nnunet-v2-smoke-"))
    raw = root / "nnUNet_raw"
    preprocessed = root / "nnUNet_preprocessed"
    results = root / "nnUNet_results"
    dataset = raw / "Dataset999_Smoke"
    images = dataset / "imagesTr"
    labels = dataset / "labelsTr"
    images.mkdir(parents=True)
    labels.mkdir()

    for case_index in range(2):
        case_id = f"smoke_{case_index:03d}"
        rng = np.random.default_rng(case_index)
        for channel in range(3):
            array = rng.normal(size=(32, 32, 32)).astype(np.float32)
            image = sitk.GetImageFromArray(array)
            image.SetSpacing((1.5, 1.5, 1.5))
            sitk.WriteImage(image, str(images / f"{case_id}_{channel:04d}.nii.gz"))
        segmentation = np.zeros((32, 32, 32), dtype=np.uint8)
        segmentation[12:20, 12:20, 12:20] = 1
        label = sitk.GetImageFromArray(segmentation)
        label.SetSpacing((1.5, 1.5, 1.5))
        sitk.WriteImage(label, str(labels / f"{case_id}.nii.gz"))

    (dataset / "dataset.json").write_text(
        json.dumps(
            {
                "channel_names": {"0": "T2W", "1": "ADC", "2": "HBV"},
                "labels": {"background": 0, "csPCa": 1},
                "numTraining": 2,
                "file_ending": ".nii.gz",
            },
            indent=2,
        )
    )
    os.environ.update(
        nnUNet_raw=str(raw),
        nnUNet_preprocessed=str(preprocessed),
        nnUNet_results=str(results),
        nnUNet_n_proc_DA="1",
        MKL_THREADING_LAYER="GNU",
    )

    run(
        "nnUNetv2_plan_and_preprocess",
        "-d",
        "999",
        "-c",
        "3d_fullres",
        "-npfp",
        "1",
        "-np",
        "1",
        "--verify_dataset_integrity",
    )
    (preprocessed / "Dataset999_Smoke" / "splits_final.json").write_text(
        json.dumps([{"train": ["smoke_000"], "val": ["smoke_001"]}], indent=2)
    )
    run(
        "nnUNetv2_train",
        "999",
        "3d_fullres",
        "0",
        "-tr",
        "nnUNetTrainerPICAI_FLCE_5epochs",
        "-device",
        "cpu",
    )
    checkpoints = list(results.rglob("checkpoint_final.pth"))
    if len(checkpoints) != 1:
        raise RuntimeError(f"Expected one final checkpoint, found {checkpoints}")
    print(f"Smoke checkpoint: {checkpoints[0]}")

    prediction_dir = root / "predictions"
    run(
        "nnUNetv2_predict",
        "-i",
        str(images),
        "-o",
        str(prediction_dir),
        "-d",
        "999",
        "-c",
        "3d_fullres",
        "-tr",
        "nnUNetTrainerPICAI_FLCE_5epochs",
        "-f",
        "0",
        "-chk",
        "checkpoint_final.pth",
        "--save_probabilities",
        "-device",
        "cpu",
        "-npp",
        "1",
        "-nps",
        "1",
    )
    probabilities = np.load(prediction_dir / "smoke_000.npz")["probabilities"]
    if probabilities.shape != (2, 32, 32, 32):
        raise RuntimeError(f"Unexpected probability shape: {probabilities.shape}")
    print("Synthetic train/predict smoke test passed")


if __name__ == "__main__":
    main()
