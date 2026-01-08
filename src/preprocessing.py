"""
Image preprocessing helpers.

Includes:
- center-crop to square
- grayscale conversion (from BGR frames)
- resize
- blur
- sobel edge magnitude
- canny edges
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

import cv2
import numpy as np

PreprocessMode = Literal["none", "blur", "sobel", "canny"]


@dataclass(frozen=True)
class PreprocessConfig:
    resolution: Tuple[int, int] = (256, 256)  # (width, height)
    blur_ksize: int = 21  # must be odd
    blur_sigma: float = 5.0
    canny_low: int = 70
    canny_high: int = 100
    mode: PreprocessMode = "blur"


def to_grayscale(frame_bgr: np.ndarray) -> np.ndarray:
    """Convert BGR -> grayscale uint8."""
    return cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)


def center_crop_square(gray: np.ndarray) -> np.ndarray:
    """Center-crop a 2D grayscale image to a square."""
    if gray.ndim != 2:
        raise ValueError("center_crop_square expects a 2D grayscale image.")
    h, w = gray.shape
    if h == w:
        return gray
    side = min(h, w)
    y0 = h // 2 - side // 2
    x0 = w // 2 - side // 2
    return gray[y0:y0 + side, x0:x0 + side]


def resize(gray: np.ndarray, resolution: Tuple[int, int]) -> np.ndarray:
    """Resize grayscale image to (width, height)."""
    w, h = resolution
    return cv2.resize(gray, (w, h), interpolation=cv2.INTER_AREA)


def gaussian_blur(gray: np.ndarray, ksize: int, sigma: float) -> np.ndarray:
    """Gaussian blur on grayscale image."""
    if ksize % 2 == 0 or ksize < 3:
        raise ValueError("blur_ksize must be an odd integer >= 3.")
    return cv2.GaussianBlur(gray, (ksize, ksize), sigmaX=sigma)


def sobel_processor(gray: np.ndarray) -> np.ndarray:
    """
    Sobel edge magnitude.
    Returns uint8 image in [0,255].
    """
    gray_f = gray.astype(np.float32)
    gx = cv2.Sobel(gray_f, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_f, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(gx, gy)
    mag = 255.0 * (mag / (mag.max() + 1e-8))
    return mag.astype(np.uint8)


def canny_processor(gray: np.ndarray, threshold_low: int, threshold_high: int) -> np.ndarray:
    """
    Canny edge detection.
    Returns uint8 edges in {0,255}.
    """
    edges = cv2.Canny(gray, threshold_low, threshold_high)
    return edges.astype(np.uint8)


def preprocess_frame(frame_bgr: np.ndarray, cfg: PreprocessConfig) -> np.ndarray:
    """
    Full preprocessing pipeline for a video frame:
      BGR -> gray -> center-crop square -> resize -> blur -> optional edges

    Returns:
      processed image uint8 shape (H,W) in [0,255]
    """
    gray = to_grayscale(frame_bgr)
    gray = center_crop_square(gray)
    gray = resize(gray, cfg.resolution)

    if cfg.mode == "none":
        return gray

    blurred = gaussian_blur(gray, cfg.blur_ksize, cfg.blur_sigma)

    if cfg.mode == "blur":
        return blurred
    if cfg.mode == "sobel":
        return sobel_processor(blurred)
    if cfg.mode == "canny":
        return canny_processor(blurred, cfg.canny_low, cfg.canny_high)

    raise ValueError(f"Unknown preprocess mode: {cfg.mode}")
