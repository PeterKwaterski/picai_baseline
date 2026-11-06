import json
from pathlib import Path

import pytest

from picai_baseline.nnunet_v2.cli import dataset_id, install_splits


def test_dataset_id():
    assert dataset_id("Dataset220_PICAI") == "220"


def test_dataset_id_rejects_v1_task_name():
    with pytest.raises(ValueError):
        dataset_id("Task2201_picai_baseline")


def test_install_splits(tmp_path: Path):
    source = tmp_path / "splits.json"
    source.write_text(json.dumps([{"train": ["case_a"], "val": ["case_b"]}]))

    destination = install_splits(tmp_path, "Dataset220_PICAI", source)

    assert destination == tmp_path / "nnUNet_preprocessed/Dataset220_PICAI/splits_final.json"
    assert json.loads(destination.read_text()) == [{"train": ["case_a"], "val": ["case_b"]}]


def test_install_splits_validates_shape(tmp_path: Path):
    source = tmp_path / "splits.json"
    source.write_text(json.dumps([{"train": ["case_a"]}]))

    with pytest.raises(ValueError):
        install_splits(tmp_path, "Dataset220_PICAI", source)
