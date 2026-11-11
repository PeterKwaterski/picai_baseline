import json
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Union

from picai_baseline.prepare_data import prepare_data


DATASET_NAME = "Dataset220_PICAI"
CHANNEL_NAMES = {"0": "T2W", "1": "ADC", "2": "HBV"}
LABELS = {"background": 0, "csPCa": 1}


def write_v2_dataset_json(dataset_dir: Path) -> None:
    labels_dir = dataset_dir / "labelsTr"
    metadata = {
        "channel_names": CHANNEL_NAMES,
        "labels": LABELS,
        "numTraining": len(list(labels_dir.glob("*.nii.gz"))),
        "file_ending": ".nii.gz",
    }
    with (dataset_dir / "dataset.json").open("w") as fp:
        json.dump(metadata, fp, indent=2)


def prepare_data_v2(
    workdir: Union[Path, str] = "/workdir",
    inputdir: Union[Path, str] = "/input",
    imagesdir: str = "images",
    labelsdir: str = "picai_labels",
    spacing: Optional[Iterable[float]] = None,
    matrix_size: Optional[Iterable[int]] = None,
    preprocessing_kwargs: Optional[Dict[str, Any]] = None,
    splits: str = "picai_pub_nnunet",
    task: str = DATASET_NAME,
    annotations_subdir: str = "resampled",
):
    """Prepare PI-CAI using nnU-Net v2's DatasetXXX directory and metadata schema."""
    if not task.startswith("Dataset") or not task[7:10].isdigit():
        raise ValueError("nnU-Net v2 dataset names must start with DatasetXXX")

    workdir = Path(workdir)
    destination = workdir / "nnUNet_raw" / task
    staging = workdir / "nnUNet_raw_data" / task

    if not destination.exists():
        prepare_data(
            workdir=workdir,
            inputdir=inputdir,
            imagesdir=imagesdir,
            labelsdir=labelsdir,
            spacing=spacing,
            matrix_size=matrix_size,
            preprocessing_kwargs=preprocessing_kwargs,
            splits=splits,
            task=task,
            annotations_subdir=annotations_subdir,
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(staging), str(destination))

    write_v2_dataset_json(destination)
    return destination
