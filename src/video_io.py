"""
Video pipeline:
- load video
- preprocess each frame
- generate stimulus + phosphenes
- concatenate and write output MP4 (GitHub-friendly)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import cv2
import numpy as np

from .preprocessing import PreprocessConfig, preprocess_frame
from .phosphene_render import image_to_stimulus, to_uint8_image


def _get_video_fps(cap: cv2.VideoCapture, fallback: float = 10.0) -> float:
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps is None or fps <= 0:
        return fallback
    return float(fps)


def write_video_gray_mp4(frames: list[np.ndarray], output_path: Path, fps: float) -> None:
    """
    Write grayscale frames (uint8, HxW) to MP4.
    """
    if not frames:
        raise ValueError("No frames to write.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    h, w = frames[0].shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (w, h), isColor=False)

    try:
        for fr in frames:
            if fr.shape[:2] != (h, w):
                raise ValueError("Frame size mismatch while writing output video.")
            writer.write(fr)
    finally:
        writer.release()


def generate_phosphene_video(
    input_video_path: str | Path,
    output_video_path: str | Path,
    simulator: Any,
    preprocess_cfg: Optional[PreprocessConfig] = None,
    max_seconds: float = 10.0,
    concat_processed_and_phosphenes: bool = True,
) -> None:
    """
    Generate a phosphene simulation video from an input video.

    Output is grayscale MP4.
    If concat_processed_and_phosphenes=True:
      output frame is [processed | phosphenes] side-by-side (width doubles).
    """
    input_video_path = Path(input_video_path)
    output_video_path = Path(output_video_path)

    preprocess_cfg = preprocess_cfg or PreprocessConfig()

    cap = cv2.VideoCapture(str(input_video_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Unable to open input video: {input_video_path}")

    fps = _get_video_fps(cap, fallback=10.0)
    max_frames = int(max_seconds * fps)

    frames_out: list[np.ndarray] = []
    frame_nr = 0

    try:
        while frame_nr < max_frames:
            ret, frame_bgr = cap.read()
            if not ret:
                break
            frame_nr += 1

            processed = preprocess_frame(frame_bgr, preprocess_cfg)  # uint8 (256,256)

            stim_pattern = image_to_stimulus(simulator, processed, rescale=True)

            # Generate phosphenes
            simulator.reset()
            phs = simulator(stim_pattern)

            # Clamp if torch-like
            try:
                phs = phs.clamp(0, 1)
            except Exception:
                pass

            phs_u8 = to_uint8_image(phs)

            if concat_processed_and_phosphenes:
                cat = np.concatenate([processed, phs_u8], axis=1).astype(np.uint8)
                frames_out.append(cat)
            else:
                frames_out.append(phs_u8)

    finally:
        cap.release()

    write_video_gray_mp4(frames_out, output_video_path, fps=fps)
