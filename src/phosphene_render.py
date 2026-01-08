"""
Phosphene rendering helpers.

Contains:
- safe rescaling to stimulation amplitude map
- simulator stimulus sampling
- rendering to uint8 images
"""

from __future__ import annotations

from typing import Any, Optional

import numpy as np

# torch is typically used by dynaphos outputs
try:
    import torch
except Exception:
    torch = None  # type: ignore


def normalized_rescaling(img: np.ndarray, stimulus_scale: float = 100e-6) -> np.ndarray:
    """
    Normalize img and rescale into [0, stimulus_scale].
    Output represents stimulation intensity map (Amperes).
    """
    img = img.astype(np.float32)
    denom = img.max() - img.min()
    if denom < 1e-8:
        return np.zeros_like(img, dtype=np.float32)
    img_norm = (img - img.min()) / denom
    return img_norm * float(stimulus_scale)


def to_numpy(x: Any) -> np.ndarray:
    """Convert torch tensor or numpy-like into numpy array."""
    if torch is not None and isinstance(x, torch.Tensor):
        return x.detach().cpu().numpy()
    return np.asarray(x)


def to_uint8_image(img: Any) -> np.ndarray:
    """
    Convert simulator output to uint8 grayscale [0,255].
    Handles torch tensors or numpy arrays, with values possibly in [0,1].
    """
    arr = to_numpy(img).astype(np.float32)

    # If it's more than 2D, take first channel safely
    if arr.ndim == 3:
        arr = arr[..., 0]

    if arr.max() <= 1.0 + 1e-6:
        arr = arr * 255.0

    # Normalize if outside expected range
    if arr.max() > 255.0 or arr.min() < 0.0:
        denom = arr.max() - arr.min()
        if denom < 1e-8:
            arr = np.zeros_like(arr)
        else:
            arr = 255.0 * (arr - arr.min()) / denom

    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return arr


def image_to_stimulus(
    simulator: Any,
    processed_img_u8: np.ndarray,
    rescale: bool = True,
    stimulus_scale: float = 100e-6,
) -> Any:
    """
    Convert a processed image to a stimulation pattern for Dynaphos.

    If rescale=True, uses Dynaphos' sample_stimulus(..., rescale=True).
    If rescale=False, assumes you already did normalization/rescaling yourself.
    """
    if rescale:
        # Dynaphos can rescale images internally if it expects pixel intensities
        return simulator.sample_stimulus(processed_img_u8, rescale=True)

    # External rescaling path (more explicit)
    stim_map = normalized_rescaling(processed_img_u8, stimulus_scale=stimulus_scale)
    return simulator.sample_stimulus(stim_map)
