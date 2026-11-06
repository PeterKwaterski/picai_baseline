#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Sequence

DATASET_NAME = "Dataset220_PICAI"
TRAINER = "nnUNetTrainerPICAI_FLCE"
CONFIGURATION = "3d_fullres"
PLANNER = "nnUNetPlannerResEncM"
PLANS = "nnUNetResEncUNetMPlans"


def configure_environment(workdir: Path) -> None:
    os.environ["nnUNet_raw"] = str(workdir / "nnUNet_raw")
    os.environ["nnUNet_preprocessed"] = str(workdir / "nnUNet_preprocessed")
    os.environ["nnUNet_results"] = str(workdir / "nnUNet_results")
    for variable in ("nnUNet_raw", "nnUNet_preprocessed", "nnUNet_results"):
        Path(os.environ[variable]).mkdir(parents=True, exist_ok=True)


def dataset_id(dataset_name: str) -> str:
    if not dataset_name.startswith("Dataset") or not dataset_name[7:10].isdigit():
        raise ValueError(f"Invalid nnU-Net v2 dataset name: {dataset_name}")
    return str(int(dataset_name[7:10]))


def install_splits(workdir: Path, dataset_name: str, source: Path) -> Path:
    with source.open() as fp:
        splits = json.load(fp)
    if not isinstance(splits, list) or not all({"train", "val"} <= set(fold) for fold in splits):
        raise ValueError("Split file must be a list of objects containing train and val")

    destination = workdir / "nnUNet_preprocessed" / dataset_name / "splits_final.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return destination


def run(command: Sequence[str]) -> None:
    print("+", " ".join(map(str, command)), flush=True)
    subprocess.check_call([str(item) for item in command])


def plan(args: argparse.Namespace) -> None:
    workdir = Path(args.workdir).resolve()
    configure_environment(workdir)
    command = [
        "nnUNetv2_plan_and_preprocess",
        "-d",
        dataset_id(args.dataset),
        "-pl",
        args.planner,
    ]
    if args.verify_dataset_integrity:
        command.append("--verify_dataset_integrity")
    run(command)
    split = Path(args.splits) if args.splits else workdir / "nnUNet_raw" / args.dataset / "splits.json"
    if split.exists():
        print(f"Installed splits: {install_splits(workdir, args.dataset, split)}", flush=True)


def train(args: argparse.Namespace) -> None:
    configure_environment(Path(args.workdir).resolve())
    command = [
        "nnUNetv2_train",
        dataset_id(args.dataset),
        args.configuration,
        str(args.fold),
        "-tr",
        args.trainer,
        "-p",
        args.plans,
    ]
    if args.continue_training:
        command.append("--c")
    if args.save_probabilities:
        command.append("--npz")
    run(command)


def predict(args: argparse.Namespace) -> None:
    configure_environment(Path(args.workdir).resolve())
    command = [
        "nnUNetv2_predict",
        "-i",
        args.input,
        "-o",
        args.output,
        "-d",
        dataset_id(args.dataset),
        "-c",
        args.configuration,
        "-tr",
        args.trainer,
        "-p",
        args.plans,
        "-chk",
        args.checkpoint,
        "-f",
        *args.folds,
    ]
    if args.save_probabilities:
        command.append("--save_probabilities")
    if args.disable_tta:
        command.append("--disable_tta")
    run(command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="picai-nnunet-v2")
    subparsers = parser.add_subparsers(required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--workdir", default="/workdir")
    common.add_argument("--dataset", default=DATASET_NAME)

    plan_parser = subparsers.add_parser("plan", parents=[common])
    plan_parser.add_argument("--splits")
    plan_parser.add_argument("--planner", default=PLANNER)
    plan_parser.add_argument("--verify-dataset-integrity", action="store_true")
    plan_parser.set_defaults(func=plan)

    train_parser = subparsers.add_parser("train", parents=[common])
    train_parser.add_argument("--fold", required=True)
    train_parser.add_argument("--configuration", default=CONFIGURATION)
    train_parser.add_argument("--trainer", default=TRAINER)
    train_parser.add_argument("--plans", default=PLANS)
    train_parser.add_argument("--continue-training", action="store_true")
    train_parser.add_argument("--save-probabilities", action="store_true")
    train_parser.set_defaults(func=train)

    predict_parser = subparsers.add_parser("predict", parents=[common])
    predict_parser.add_argument("--input", required=True)
    predict_parser.add_argument("--output", required=True)
    predict_parser.add_argument("--configuration", default=CONFIGURATION)
    predict_parser.add_argument("--trainer", default=TRAINER)
    predict_parser.add_argument("--plans", default=PLANS)
    predict_parser.add_argument("--checkpoint", default="checkpoint_best.pth")
    predict_parser.add_argument("--folds", nargs="+", default=["0", "1", "2", "3", "4"])
    predict_parser.add_argument("--save-probabilities", action="store_true")
    predict_parser.add_argument("--disable-tta", action="store_true")
    predict_parser.set_defaults(func=predict)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
