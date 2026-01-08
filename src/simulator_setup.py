"""
Simulator setup utilities (Dynaphos + params.yaml).

This module is intentionally lightweight:
- load params from YAML
- generate phosphene coordinates
- instantiate Dynaphos simulator
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

import yaml

# Dynaphos imports can vary by version
try:
    from dynaphos import cortex_models
except Exception as e:
    raise ImportError("Could not import dynaphos.cortex_models. Check dynaphos installation.") from e

try:
    # common path
    from dynaphos.simulator import PhospheneSimulator
except Exception:
    try:
        # fallback: some versions expose it elsewhere
        from dynaphos import PhospheneSimulator  # type: ignore
    except Exception as e:
        raise ImportError(
            "Could not import PhospheneSimulator from dynaphos. "
            "Please check dynaphos version / module paths."
        ) from e


def load_params(params_path: str | Path) -> Dict[str, Any]:
    """Load Dynaphos params.yaml into a dict."""
    params_path = Path(params_path)
    with params_path.open("r", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    if not isinstance(params, dict):
        raise ValueError("params.yaml did not parse into a dict.")
    return params


def make_simulator(
    params: Dict[str, Any],
    n_phosphenes: int = 1000,
) -> Tuple[Any, Any]:
    """
    Create phosphene coordinates and initialize a Dynaphos simulator.

    Returns:
        simulator, phosphene_coords
    """
    phosphene_coords = cortex_models.get_visual_field_coordinates_probabilistically(
        params, n_phosphenes
    )
    simulator = PhospheneSimulator(params, phosphene_coords)
    return simulator, phosphene_coords


def get_fps_from_params(params: Dict[str, Any], default: float = 10.0) -> float:
    """Safely retrieve fps from params['run']['fps'] if present."""
    try:
        fps = float(params.get("run", {}).get("fps", default))
        if fps <= 0:
            return default
        return fps
    except Exception:
        return default
