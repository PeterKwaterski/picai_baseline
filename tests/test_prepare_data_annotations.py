import numpy as np
import pytest
import SimpleITK as sitk

pytest.importorskip("picai_prep")

from picai_baseline.prepare_data import (
    annotation_preprocess_for_subdir,
    preprocess_picai_annotation_granular,
    preprocess_picai_annotation_identity,
)


def test_sparse_binary_annotations_use_identity_preprocessing():
    preprocess = annotation_preprocess_for_subdir(
        "binary_cspca_v1_sparse_p0.75"
    )
    assert preprocess is preprocess_picai_annotation_identity

    labels = np.array([[[0, 1, 2]]], dtype=np.uint8)
    result = preprocess(sitk.GetImageFromArray(labels))
    np.testing.assert_array_equal(sitk.GetArrayFromImage(result), labels)


def test_granular_annotations_still_use_granular_preprocessing():
    assert (
        annotation_preprocess_for_subdir("resampled")
        is preprocess_picai_annotation_granular
    )
