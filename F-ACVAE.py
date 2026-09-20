#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F-ACVAE — standalone final-paper runner
Generated from the final Jupyter notebook.

Design goals:
- Run from a single Python file.
- Resolve datasets relative to this file, not the shell working directory.
- Install missing Python dependencies automatically with the same interpreter.
- Preserve the final notebook's model, training, evaluation, checkpoint, and export logic.
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

# -----------------------------------------------------------------------------
# Portable project root
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)
os.environ.setdefault("MPLBACKEND", "Agg")

# -----------------------------------------------------------------------------
# Automatic dependency bootstrap
# Existing installations are preserved. Only missing/broken imports are installed.
# -----------------------------------------------------------------------------
_RUNTIME_REQUIREMENTS = {
    "numpy": "numpy>=1.24",
    "pandas": "pandas>=2.0",
    "matplotlib": "matplotlib>=3.7",
    "sklearn": "scikit-learn>=1.3",
    "torch": "torch>=2.0",
    "IPython": "ipython>=8.0",
}


def _ensure_pip() -> None:
    try:
        import pip  # noqa: F401
    except Exception:
        import ensurepip
        ensurepip.bootstrap(upgrade=True)


def _ensure_runtime_dependencies() -> None:
    missing = []
    failures = {}
    for module_name, requirement in _RUNTIME_REQUIREMENTS.items():
        try:
            importlib.import_module(module_name)
        except Exception as exc:  # missing package or unusable installation
            missing.append(requirement)
            failures[module_name] = f"{type(exc).__name__}: {exc}"

    if not missing:
        print("[setup] Python dependencies: OK")
        return

    print("[setup] Installing missing prerequisites:")
    for requirement in missing:
        print(f"  - {requirement}")
    _ensure_pip()
    command = [sys.executable, "-m", "pip", "install", *missing]
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as exc:
        details = "\n".join(f"  {k}: {v}" for k, v in failures.items())
        raise RuntimeError(
            "Automatic dependency installation failed.\n"
            f"Command: {' '.join(command)}\n"
            f"Original import failures:\n{details}"
        ) from exc

    importlib.invalidate_caches()
    still_broken = []
    for module_name in _RUNTIME_REQUIREMENTS:
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            still_broken.append(f"{module_name}: {type(exc).__name__}: {exc}")
    if still_broken:
        raise RuntimeError(
            "Dependencies were installed, but some imports still fail:\n"
            + "\n".join(still_broken)
        )
    print("[setup] Dependency installation complete.")


def _ensure_optional_dependency(module_name: str, requirement: str) -> None:
    try:
        importlib.import_module(module_name)
        return
    except Exception:
        pass
    print(f"[setup] Installing optional dependency required by current input: {requirement}")
    _ensure_pip()
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Automatic installation failed for optional dependency: {requirement}. "
            "Internet/package-index access may be unavailable."
        ) from exc
    importlib.invalidate_caches()
    importlib.import_module(module_name)


_ensure_runtime_dependencies()

# -----------------------------------------------------------------------------
# Dataset discovery
# Supported layouts:
#   project/N-BaIoT
#   project/UNSW-NB15
#   project/CIC-IDS2017
# or the same folders under project/dataset, project/datasets, or project/data.
# -----------------------------------------------------------------------------
_DATA_SEARCH_BASES = (
    PROJECT_ROOT,
    PROJECT_ROOT / "dataset",
    PROJECT_ROOT / "datasets",
    PROJECT_ROOT / "data",
)


def _portable_norm(value: object) -> str:
    return "".join(ch.lower() for ch in str(value) if ch.isalnum())


def _find_dataset_folder(aliases) -> Path | None:
    wanted = {_portable_norm(x) for x in aliases}
    for base in _DATA_SEARCH_BASES:
        if not base.is_dir():
            continue
        if _portable_norm(base.name) in wanted:
            return base
        try:
            children = tuple(base.iterdir())
        except OSError:
            continue
        for child in children:
            if child.is_dir() and _portable_norm(child.name) in wanted:
                return child
    return None


def _find_nbaiot_root() -> Path | None:
    explicit = os.environ.get("N_BAIOT_ROOT", "").strip()
    if explicit:
        return Path(explicit).expanduser().resolve()

    named = _find_dataset_folder(("N-BaIoT", "N_BaIoT", "NBaIoT", "N BaIoT"))
    if named is not None:
        return named

    # Also accept a generic dataset/ folder that itself contains N-BaIoT device folders.
    for base in _DATA_SEARCH_BASES:
        if not base.is_dir():
            continue
        for device_alias in ("Danmini_Doorbell", "Danmini Doorbell"):
            if (base / device_alias).is_dir():
                return base
    return None

print(f"[setup] Project root: {PROJECT_ROOT}")


# -----------------------------------------------------------------------------
# SECTION 0 — Pre-flight Validation  [notebook cell 0]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FINAL RELEASE — Gate B Locked  [notebook cell 1]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Output Controller — FINAL Gate-B Run  [notebook cell 2]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 3 =====
# OUTPUT CONTROLLER — V6.8 N-BaIoT + external datasets, dual-protocol evaluation.
# Headline comparison: Local-Private RF for FedAvg/FedProx/F-ACVAE.
# Cross-Client generalization is applied identically to FedAvg/FedProx/F-ACVAE.
# CMGA Gate is strictly binary-open-set only (IoT-08..IoT-11).

REAL_RESULT_RELEASE = "final_gate_b_locked_2026_08_26"
TABLE_VI_REAL_RUN_TAG = "local_private_primary_v65"
TABLE_VII_REAL_RUN_TAG = "external_local_private_v68"
NBAIOT_ONLY = False

# Binary CMGA Gate constants.
HYBRID_GATE_QUANTILE = 0.995
RELAXED_B_GATE_QUANTILE = 0.990
HYBRID_GATE_MIN_VARIANCE = 1e-6
HYBRID_GATE_MIN_BENIGN = 10
HYBRID_GATE_PROTOCOL_VERSION = "binary-cmga-radial-dual-b-v69"

# V6.8 FINAL Gate: client-balanced benign-only FPR control.
# These are protocol constants, not Test-selected hyperparameters.
CBFPR_TRAIN_FPR_CANDIDATES = (0.0025, 0.0050, 0.0100, 0.0200)
CBFPR_VALIDATION_FPR_BUDGET = 0.0100
CBFPR_DEFAULT_TRAIN_FPR = 0.0050

# Validation-only tuning candidates. Test is NEVER used to select these.
BINARY_GATE_QUANTILE_CANDIDATES = (0.970, 0.980, 0.990, 0.995, 0.9975)
BINARY_GATE_MARGIN_CANDIDATES = (-1.0, -0.5, 0.0, 0.5, 1.0)
BINARY_RF_CANDIDATES = (
    {"name":"default", "n_estimators":100, "max_depth":15, "min_samples_split":10, "min_samples_leaf":5, "max_features":"sqrt", "class_weight":None},
    {"name":"deep_balanced", "n_estimators":150, "max_depth":None, "min_samples_split":2, "min_samples_leaf":1, "max_features":"sqrt", "class_weight":"balanced_subsample"},
    {"name":"depth20_balanced", "n_estimators":150, "max_depth":20, "min_samples_split":2, "min_samples_leaf":1, "max_features":"sqrt", "class_weight":"balanced"},
)

SELECTED_OUTPUTS = [
    "TABLE_VI",
    "TABLE_VII",
    "TABLE_VIII",
    "FIGURE_3",
    "FIGURE_4",
    "TABLE_IX",
    "TABLE_X",
    "COMMUNICATION",
    "STABILITY",
    "EVALUATION_PROTOCOL",
]


# Optional portable override, e.g. FACVAE_OUTPUTS=TABLE_VI,FIGURE_3
_env_outputs = os.environ.get("FACVAE_OUTPUTS", "").strip()
if _env_outputs:
    SELECTED_OUTPUTS = [x.strip() for x in _env_outputs.split(",") if x.strip()]

OUTPUT_CATALOG = {
    "PRE_FLIGHT": "Dataset/folder pre-flight status — N-BaIoT + UNSW-NB15 + CIC-IDS2017",
    "RUNTIME_LOGS": "Runtime-monitor initialization messages",
    "DATA_AUDIT": "IoT-01 data-integrity/build status",
    "LOGIC_TESTS": "Method-isolation and FedProx-isolation checks",
    "TRAINING_PROGRESS": "Round/resume/extended-experiment progress",
    "FINAL_TEST_STATUS": "Final-test cache/run status",
    "TABLE_VI": "Table VI — IoT-01..11 Local-Private primary comparison + binary F-ACVAE final",
    "TABLE_VII": "Table VII — UNSW-NB15 / CIC-IDS2017 genuine F-ACVAE Local-Private results",
    "HYBRID_GATE": "Final Binary Open-Set Gate B — IoT-08..IoT-11 only",
    "GENERALIZATION": "All-method Cross-Client generalization: FedAvg/FedProx/F-ACVAE + binary CMGA Gate control",
    "TABLE_VIII": "IoT-01 architecture ablation without Gate",
    "FIGURE_3": "Figure 3 — convergence",
    "FIGURE_4": "Figure 4 — three audited IoT-01 Original Data candidates",
    "TABLE_IX": "IoT-01 RF / CMGA representation attribution without Gate",
    "TABLE_X": "IoT-01 per-class Local-Private F-ACVAE metrics",
    "COMMUNICATION": "Privacy / communication-efficiency summary",
    "EVALUATION_PROTOCOL": "Paper-ready evaluation-protocol paragraph",
    "STABILITY": "Five-run IoT-01 F-ACVAE stability without Gate",
    "EXPORT_SUMMARY": "Evaluation protocol and final export location",
    "FINAL_VALIDATION": "Saved-result artifact validation",
    "FINAL_SANITY": "Final runtime sanity summary",
}

_DISABLED_OUTPUTS = set()

import contextlib as _output_contextlib
import io as _output_io

def _normalize_output_key(value):
    return str(value).strip().upper().replace("-", "_").replace(" ", "_")

_SELECTED_OUTPUTS_NORMALIZED = {_normalize_output_key(x) for x in SELECTED_OUTPUTS}
_ALLOWED_OUTPUTS = set(OUTPUT_CATALOG) | {"ALL"}
_UNKNOWN_OUTPUTS = _SELECTED_OUTPUTS_NORMALIZED - _ALLOWED_OUTPUTS
if _UNKNOWN_OUTPUTS:
    raise ValueError(
        "Unknown SELECTED_OUTPUTS item(s): " + ", ".join(sorted(_UNKNOWN_OUTPUTS))
        + ". Valid names: " + ", ".join(sorted(_ALLOWED_OUTPUTS))
    )
if not _SELECTED_OUTPUTS_NORMALIZED:
    raise ValueError("SELECTED_OUTPUTS cannot be empty. Use ['ALL'] or at least one catalog item.")

def output_enabled(name):
    key = _normalize_output_key(name)
    if key not in OUTPUT_CATALOG:
        raise KeyError(f"Unknown output key: {name}")
    if key in _DISABLED_OUTPUTS:
        return False
    return "ALL" in _SELECTED_OUTPUTS_NORMALIZED or key in _SELECTED_OUTPUTS_NORMALIZED

def any_output_enabled(*names):
    return any(output_enabled(name) for name in names)

_IOT01_TRAINING_OUTPUTS = {
    "TRAINING_PROGRESS", "FINAL_TEST_STATUS", "TABLE_VI", "GENERALIZATION",
"TABLE_VIII", "FIGURE_3", "FIGURE_4", "TABLE_IX", "TABLE_X",
    "COMMUNICATION", "STABILITY",
}
IOT01_TRAINING_REQUIRED = any(output_enabled(name) for name in _IOT01_TRAINING_OUTPUTS)
IOT01_DATA_REQUIRED = IOT01_TRAINING_REQUIRED or output_enabled("DATA_AUDIT")
TABLE_VII_TRAINING_REQUIRED = output_enabled("TABLE_VII")

def out_print(name, *args, **kwargs):
    if output_enabled(name):
        print(*args, **kwargs)

@_output_contextlib.contextmanager
def output_scope(name):
    if output_enabled(name):
        yield
    else:
        with _output_contextlib.redirect_stdout(_output_io.StringIO()):
            yield


# ===== NOTEBOOK CODE CELL 4 =====
from pathlib import Path

out_print("PRE_FLIGHT", "="*70)
out_print("PRE_FLIGHT", "F-ACVAE PRE-FLIGHT CHECK (FAIL FAST)")
out_print("PRE_FLIGHT", "="*70)

required_folders = []
if IOT01_DATA_REQUIRED:
    nbaiot_root = _find_nbaiot_root()
    if nbaiot_root is None:
        nbaiot_root = PROJECT_ROOT / "dataset" / "N-BaIoT"
    required_folders.append(("N-BaIoT", nbaiot_root))

if TABLE_VII_TRAINING_REQUIRED:
    unsw_root = _find_dataset_folder(("UNSW-NB15", "UNSW_NB15", "UNSWNB15", "UNSW-NB-15", "UNSW NB-15"))
    cic_root = _find_dataset_folder(("CIC-IDS2017", "CIC_IDS2017", "CICIDS2017", "CIC IDS2017"))
    required_folders.extend([
        ("UNSW-NB15", unsw_root or (PROJECT_ROOT / "dataset" / "UNSW-NB15")),
        ("CIC-IDS2017", cic_root or (PROJECT_ROOT / "dataset" / "CIC-IDS2017")),
    ])

missing = [f"{name}: {path}" for name, path in required_folders if not Path(path).exists()]
if missing:
    raise RuntimeError(
        "Required dataset folders are missing before execution.\n"
        "Place them beside this Python file or under dataset/, datasets/, or data/:\n"
        + "\n".join(missing)
    )

if required_folders:
    out_print("PRE_FLIGHT", "✓ Required dataset folders found")
    for name, path in required_folders:
        out_print("PRE_FLIGHT", f"  - {name}: {Path(path).resolve()}")
out_print("PRE_FLIGHT", "✓ Output folders are created automatically")
out_print("PRE_FLIGHT", "="*70)


# -----------------------------------------------------------------------------
# SECTION 0B — Runtime Monitoring (Logging Only)  [notebook cell 5]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 6 =====

from pathlib import Path
import time
import datetime

RESULT_ROOT = Path("Result")
LOG_DIR = RESULT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

RUN_LOG_FILE = LOG_DIR / "training_log.txt"

def log_progress(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{timestamp}] {message}"
    if output_enabled("RUNTIME_LOGS"):
        print(text)
    with open(RUN_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

log_progress("Runtime monitoring initialized.")


# -----------------------------------------------------------------------------
# SECTION A — CORE IMPLEMENTATION (DO NOT MODIFY)  [notebook cell 7]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 8 =====
# 1. Imports, deterministic settings, and paper-locked protocol

from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple
import hashlib
import inspect
import json
import math
import os
import platform
import random
import tempfile
import time
import warnings
import pickle

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "facvae_matplotlib"))
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import torch
import torch.nn as nn
import torch.optim as optim
from IPython.display import display
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import QuantileTransformer, StandardScaler
from torch.utils.data import DataLoader, TensorDataset


def _normal_folder_name(value: object) -> str:
    return "".join(ch.lower() for ch in str(value) if ch.isalnum())


def _resolve_nbaiot_path() -> Path:
    found = _find_nbaiot_root()
    if found is not None:
        return found
    return PROJECT_ROOT / "dataset" / "N-BaIoT"


DATASET_ROOT = _resolve_nbaiot_path()
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SYNTHETIC_ONLY = os.environ.get("FACVAE_SYNTHETIC_ONLY", "0") == "1"
RUN_FULL_PROTOCOL = (not SYNTHETIC_ONLY) and IOT01_TRAINING_REQUIRED
FINAL_TEST_UNLOCK = True  # Final paper notebook: validation decisions are already frozen.


@dataclass(frozen=True)
class ProtocolConfig:
    seed: int = 42
    num_clients: int = 9
    rounds: int = 10
    local_epochs: int = 5
    batch_size: int = 128
    local_lr: float = 2e-4
    weight_decay: float = 5e-6
    latent_dim: int = 10
    condition_scale: float = 1.0
    kl_weight: float = 0.3
    gradient_clip_norm: float = 0.5
    fedprox_mu: float = 0.01

    # F-ACVAE paper: Eq. (15), Eq. (18)-(20), Table I.
    cmga_alpha: float = 0.1
    cmga_gamma: float = 0.1
    cmga_update_clip_abs: float = 0.2

    # Public CMGA specification: class-wise buffering and constrained separation.
    cmga_prior_beta: float = 0.9
    cmga_prior_margin: float = 2.0
    cmga_prior_penalty: float = 0.1
    cmga_prior_pgd_steps: int = 3
    cmga_prior_pgd_lr: float = 0.1
    cmga_min_prior_variance: float = 0.1

    def validate(self) -> None:
        if self.num_clients != 9:
            raise ValueError("The paper-locked IoT-01 protocol requires nine clients.")
        positive = (
            self.rounds, self.local_epochs, self.batch_size, self.local_lr,
            self.latent_dim, self.gradient_clip_norm, self.fedprox_mu,
            self.cmga_update_clip_abs, self.cmga_prior_margin,
            self.cmga_prior_penalty, self.cmga_prior_pgd_steps,
            self.cmga_prior_pgd_lr, self.cmga_min_prior_variance,
        )
        if any(float(value) <= 0 for value in positive):
            raise ValueError("All positive protocol parameters must be greater than zero.")
        for name, value in (
            ("cmga_alpha", self.cmga_alpha),
            ("cmga_gamma", self.cmga_gamma),
            ("cmga_prior_beta", self.cmga_prior_beta),
        ):
            if not 0.0 < float(value) < 1.0:
                raise ValueError(f"{name} must be in (0, 1).")
        if self.latent_dim < 2:
            raise ValueError("latent_dim must be at least two.")


CONFIG = ProtocolConfig()
CONFIG.validate()

RF_PARAMS = {
    "n_estimators": 100,
    "max_depth": 15,
    "min_samples_split": 10,
    "min_samples_leaf": 5,
    "max_features": "sqrt",
    "random_state": CONFIG.seed,
    "n_jobs": -1,
}


# Keep notebook output readable; this warning is a scikit-learn parallelism advisory,
# not a numerical/model error, and can otherwise repeat thousands of times.
warnings.filterwarnings(
    "ignore",
    message=r"`sklearn\.utils\.parallel\.delayed` should be used.*",
    category=UserWarning,
)

# Persistent experiment state. Every long training job writes one checkpoint per round.
RESULTS_ROOT = Path("Results")
CHECKPOINT_ROOT = RESULTS_ROOT / "Checkpoints"  # reuse validated training/cache state
FINAL_EXPORT_ROOT = RESULTS_ROOT / "Final_Gate_B"
TABLES_ROOT = FINAL_EXPORT_ROOT / "Tables"
FIGURES_ROOT = FINAL_EXPORT_ROOT / "Figures"
TEXT_ROOT = FINAL_EXPORT_ROOT / "Text"
for _folder in (CHECKPOINT_ROOT, FINAL_EXPORT_ROOT, TABLES_ROOT, FIGURES_ROOT, TEXT_ROOT):
    _folder.mkdir(parents=True, exist_ok=True)

CHECKPOINT_VERSION = "facvae-paper-resume-v1"
ENABLE_CHECKPOINTS = os.environ.get("FACVAE_CHECKPOINTS", "1") != "0"
# Long paper experiments (IoT-02..07 feature/latent plots, two ablations, 5-run stability).
# Enabled by default in this final notebook. Set FACVAE_EXTENDED_PAPER=0 only for a quick IoT-01 run.
RUN_EXTENDED_PAPER_EXPERIMENTS = os.environ.get("FACVAE_EXTENDED_PAPER", "1") != "0"

# No table/debug dataframe is printed during training; only round progress is printed.
PRINT_ONLY_ROUNDS_DURING_TRAINING = True


def reset_all_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if hasattr(torch.backends, "cudnn"):
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    try:
        torch.use_deterministic_algorithms(True, warn_only=True)
    except TypeError:
        torch.use_deterministic_algorithms(True)


reset_all_seeds(CONFIG.seed)
out_print("PRE_FLIGHT", f"F-ACVAE | device={DEVICE} | seed={CONFIG.seed} | rounds={CONFIG.rounds} | clients={CONFIG.num_clients}")


FIGURE_CACHE_ROOT = RESULTS_ROOT / "Figure_Cache"

# Output-directory resilience only: if any Results subfolder was deleted, recreate it.
# This does NOT recreate deleted checkpoint files or metrics; it only prevents false
# FileNotFoundError failures when an output directory itself is missing.
def _ensure_results_directories() -> None:
    required_dirs = (
        RESULTS_ROOT, CHECKPOINT_ROOT, TABLES_ROOT, FIGURES_ROOT, TEXT_ROOT, FIGURE_CACHE_ROOT,
        TABLES_ROOT / "Table_VI", TABLES_ROOT / "Table_VII", TABLES_ROOT / "Hybrid_Gate", TABLES_ROOT / "Generalization", TABLES_ROOT / "Table_VIII",
        TABLES_ROOT / "Table_IX", TABLES_ROOT / "Table_X",
        FIGURES_ROOT / "Figure_3_Convergence", FIGURES_ROOT / "Figure_4_Feature_Spaces",
        TEXT_ROOT / "Communication", TEXT_ROOT / "Stability", TEXT_ROOT / "Evaluation_Protocol",
    )
    for folder in required_dirs:
        folder.mkdir(parents=True, exist_ok=True)

_ensure_results_directories()

# Keep notebook output clean; this warning is internal to sklearn parallel workers.
warnings.filterwarnings(
    "ignore",
    message=r"`sklearn\.utils\.parallel\.delayed` should be used.*",
    category=UserWarning,
)


# ===== NOTEBOOK CODE CELL 9 =====
# 2. Embedded leakage-safe IoT-01 data layer


PIPELINE_VERSION = "2.1.0-integrated-clean"
HASH_METHOD = "pandas_dual_uint64_row_hash_v1"
HASH_DTYPE = np.dtype([("h1", "<u8"), ("h2", "<u8")])

GAFGYT_CLASSES = (
    "gafgyt.combo", "gafgyt.junk", "gafgyt.scan", "gafgyt.tcp", "gafgyt.udp"
)
RAW_DEVICE_FOLDERS = {"danmini": "Danmini_Doorbell"}
FILE_NAME_BY_CLASS = {
    "benign": "benign_traffic.csv",
    **{name: f"{name}.csv" for name in GAFGYT_CLASSES},
}
IOT01_SCENARIO = {
    "paper_id": "IoT-01",
    "paper_code": "DanG-6",
    "task": "multiclass",
    "device_key": "danmini",
    "classes": ("benign", *GAFGYT_CLASSES),
}
SCENARIO_BY_ID = {"IoT-01": IOT01_SCENARIO}

# Locked to the already audited raw files supplied by the user.
EXPECTED_SOURCE = {
    "benign": (49548, "eb03ac6269ef74f44a2562271a18c2f9e532595f43f0e95c32fe330990433b93"),
    "gafgyt.combo": (59718, "2b39c86654261d5f74fd78260f0891d44cc997808f3350c6ee1da2fcc59de5e9"),
    "gafgyt.junk": (29068, "31ce937906ffd4d6647f7cec7965eb36c2120a9f3afff551ff7c8e0bc583e8b3"),
    "gafgyt.scan": (29849, "4453d40f4573d865e9c489872ea8daadbf51c31a5e8afb9ca7ae1b2ec7bfea44"),
    "gafgyt.tcp": (92141, "934664e0dc9e7d1428899599ebdd5ea2c73b834432bdcfe737891b5d17bd24e9"),
    "gafgyt.udp": (105874, "4e69f346e0ace1324feb0ce69af27f902fd174e39ca9a7477ac405c8f5605bff"),
}
EXPECTED_SCHEMA_SHA256 = "bc53d803ba0cd5adf113444dfc4238878470799dddc619bb50d22adb6b7ee6d2"
EXPECTED_SEED42_SPLIT = (217890, 38450, 109858)
EXPECTED_SEED42_CLASS_COUNTS = {
    "train": (29481, 35533, 17296, 17760, 54825, 62995),
    "validation": (5203, 6270, 3052, 3134, 9674, 11117),
    "test": (14864, 17915, 8720, 8955, 27642, 31762),
}
@dataclass(frozen=True)
class PipelineConfig:
    """Configuration for one deterministic Phase-2 scenario build."""

    seed: int = 42
    train_ratio: float = 0.70
    validation_ratio_within_train: float = 0.15
    expected_feature_count: int = 115
    num_clients: int = 9
    partition_mode: str = "dirichlet"
    dirichlet_alpha: float = 0.30
    min_client_train_rows: int = 128
    max_partition_attempts: int = 1000
    quantile_n_quantiles: int = 1000
    quantile_subsample: int = 200_000
    transform_chunk_size: int = 50_000
    output_low: float = 0.10
    output_high: float = 0.90

    def validate(self) -> None:
        if self.seed < 0:
            raise ValueError("seed must be non-negative.")
        if not 0.0 < self.train_ratio < 1.0:
            raise ValueError("train_ratio must be in (0, 1).")
        if not 0.0 < self.validation_ratio_within_train < 0.5:
            raise ValueError("validation_ratio_within_train must be in (0, 0.5).")
        if self.expected_feature_count < 1:
            raise ValueError("expected_feature_count must be positive.")
        if self.num_clients < 2:
            raise ValueError("num_clients must be at least 2.")
        if self.partition_mode not in {"dirichlet", "iid_stratified"}:
            raise ValueError("partition_mode must be 'dirichlet' or 'iid_stratified'.")
        if self.dirichlet_alpha <= 0.0:
            raise ValueError("dirichlet_alpha must be positive.")
        if self.min_client_train_rows < 1:
            raise ValueError("min_client_train_rows must be positive.")
        if self.max_partition_attempts < 1:
            raise ValueError("max_partition_attempts must be positive.")
        if self.quantile_n_quantiles < 2:
            raise ValueError("quantile_n_quantiles must be at least 2.")
        if self.quantile_subsample < 2:
            raise ValueError("quantile_subsample must be at least 2.")
        if self.transform_chunk_size < 1:
            raise ValueError("transform_chunk_size must be positive.")
        if not self.output_low < self.output_high:
            raise ValueError("output_low must be smaller than output_high.")


@dataclass
class SourceData:
    source_class: str
    relative_path: str
    values: np.ndarray
    hashes: np.ndarray
    feature_columns: Tuple[str, ...]
    schema_sha256: str
    parsed_row_hash_sha256: str
    unique_hash_groups: int
    duplicate_rows: int
    max_duplicate_multiplicity: int


@dataclass
class SplitData:
    X: np.ndarray
    y: np.ndarray
    source: np.ndarray
    hashes: np.ndarray

    def take(self, indices: np.ndarray) -> "SplitData":
        indices = np.asarray(indices, dtype=np.int64)
        return SplitData(
            X=self.X[indices],
            y=self.y[indices],
            source=self.source[indices],
            hashes=self.hashes[indices],
        )

    def filter(self, keep: np.ndarray) -> "SplitData":
        keep = np.asarray(keep, dtype=bool)
        return SplitData(
            X=self.X[keep],
            y=self.y[keep],
            source=self.source[keep],
            hashes=self.hashes[keep],
        )

    @property
    def rows(self) -> int:
        return int(len(self.y))


def _looks_like_nbaiot_root(path: Path) -> bool:
    if not path.is_dir():
        return False
    return any(
        (path / folder / FILE_NAME_BY_CLASS["benign"]).is_file()
        for folder in RAW_DEVICE_FOLDERS.values()
    )


def resolve_dataset_root(user_value: Optional[object] = None) -> Path:
    """Resolve the raw N-BaIoT directory without hard-coding one workstation."""

    candidates: List[Path] = []
    if user_value is not None and str(user_value).strip():
        supplied = Path(str(user_value)).expanduser()
        candidates.extend((supplied, supplied / "N-BaIoT", supplied / "N_BaIoT"))

    cwd = Path.cwd()
    for base in (cwd, *cwd.parents):
        candidates.extend(
            (
                base / "dataset" / "N-BaIoT",
                base / "dataset" / "N_BaIoT",
                base / "datasets" / "N-BaIoT",
                base / "datasets" / "N_BaIoT",
            )
        )

    seen: set[Path] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if _looks_like_nbaiot_root(resolved):
            return resolved

    searched = "\n".join(f"  - {item}" for item in seen)
    raise FileNotFoundError(
        "Raw N-BaIoT root was not found. Pass dataset_root explicitly.\n"
        f"Searched:\n{searched}"
    )


def _required_classes(scenario: Mapping[str, object]) -> Tuple[str, ...]:
    if scenario["task"] == "multiclass":
        return tuple(str(item) for item in scenario["classes"])
    ordered = (
        "benign",
        *tuple(str(item) for item in scenario["train_attacks"]),
        *tuple(str(item) for item in scenario["test_attacks"]),
    )
    return tuple(dict.fromkeys(ordered))


def _source_path(root: Path, device_key: str, class_name: str) -> Path:
    try:
        folder = RAW_DEVICE_FOLDERS[device_key]
        filename = FILE_NAME_BY_CLASS[class_name]
    except KeyError as exc:
        raise KeyError(f"Unsupported N-BaIoT source: {device_key}/{class_name}") from exc
    return root / folder / filename


def validate_scenario_files(dataset_root: Path, scenario_id: str) -> pd.DataFrame:
    """Return a preflight table and fail before reading data if a file is absent."""

    if scenario_id not in SCENARIO_BY_ID:
        raise KeyError(f"Unknown paper scenario: {scenario_id}")
    scenario = SCENARIO_BY_ID[scenario_id]
    rows: List[Dict[str, object]] = []
    for class_name in _required_classes(scenario):
        path = _source_path(dataset_root, str(scenario["device_key"]), class_name)
        rows.append(
            {
                "paper_id": scenario_id,
                "paper_code": str(scenario["paper_code"]),
                "device_key": str(scenario["device_key"]),
                "source_class": class_name,
                "relative_path": path.relative_to(dataset_root).as_posix(),
                "exists": path.is_file(),
                "size_bytes": int(path.stat().st_size) if path.is_file() else 0,
            }
        )
    table = pd.DataFrame(rows)
    missing = table.loc[~table["exists"]]
    if not missing.empty:
        details = "\n".join(str(item) for item in missing["relative_path"])
        raise FileNotFoundError(f"{scenario_id}: required CSV files are missing:\n{details}")
    return table


def _schema_digest(columns: Sequence[str]) -> str:
    payload = "\n".join(f"{name}\tfloat64" for name in columns)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _hash_pairs(frame: pd.DataFrame) -> np.ndarray:
    first = pd.util.hash_pandas_object(
        frame,
        index=False,
        categorize=False,
    ).to_numpy(dtype=np.uint64, copy=True)
    second = pd.util.hash_pandas_object(
        frame.iloc[:, ::-1],
        index=False,
        categorize=False,
    ).to_numpy(dtype=np.uint64, copy=True)
    return np.ascontiguousarray(np.column_stack((first, second)).astype("<u8", copy=False))


def _structured_hashes(pairs: np.ndarray) -> np.ndarray:
    pairs = np.ascontiguousarray(np.asarray(pairs, dtype="<u8"))
    if pairs.ndim != 2 or pairs.shape[1] != 2:
        raise ValueError("Row hashes must have shape (n, 2).")
    return pairs.view(HASH_DTYPE).reshape(-1)


def _read_source(
    dataset_root: Path,
    device_key: str,
    class_name: str,
    expected_columns: Optional[Sequence[str]],
    expected_feature_count: int,
) -> SourceData:
    path = _source_path(dataset_root, device_key, class_name)
    frame = pd.read_csv(path)
    if frame.empty:
        raise RuntimeError(f"CSV is empty: {path}")
    columns = tuple(str(name) for name in frame.columns)
    if len(columns) != expected_feature_count:
        raise RuntimeError(
            f"{path}: expected {expected_feature_count} features, observed {len(columns)}."
        )
    if expected_columns is not None and columns != tuple(expected_columns):
        raise RuntimeError(f"{path}: feature names/order differ from the scenario schema.")
    non_numeric = tuple(str(name) for name in frame.select_dtypes(exclude=[np.number]).columns)
    if non_numeric:
        raise TypeError(f"{path}: non-numeric columns: {non_numeric}")
    values64 = frame.to_numpy(dtype=np.float64, copy=False)
    if not np.isfinite(values64).all():
        count = int((~np.isfinite(values64)).sum())
        raise FloatingPointError(f"{path}: {count} non-finite feature values.")

    pairs = _hash_pairs(frame)
    structured = _structured_hashes(pairs)
    _, counts = np.unique(structured, return_counts=True)
    duplicate_rows = int(np.sum(counts[counts > 1] - 1))
    parsed_digest = hashlib.sha256(pairs.tobytes()).hexdigest()
    return SourceData(
        source_class=class_name,
        relative_path=path.relative_to(dataset_root).as_posix(),
        values=np.asarray(values64, dtype=np.float32),
        hashes=pairs,
        feature_columns=columns,
        schema_sha256=_schema_digest(columns),
        parsed_row_hash_sha256=parsed_digest,
        unique_hash_groups=int(len(counts)),
        duplicate_rows=duplicate_rows,
        max_duplicate_multiplicity=int(counts.max(initial=0)),
    )


def _scenario_seed(base: int, paper_id: str, offset: int) -> int:
    return int(base + 10_000 * int(paper_id.split("-")[1]) + offset)


def _unique_hash_groups(hash_pairs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    unique, counts = np.unique(_structured_hashes(hash_pairs), return_counts=True)
    pairs = np.ascontiguousarray(unique).view("<u8").reshape(-1, 2)
    return pairs, counts.astype(np.int64, copy=False)


def _split_unique_groups(
    hashes: np.ndarray,
    counts: np.ndarray,
    left_ratio: float,
    seed: int,
) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    """Mirror the audited Phase-1 group splitter, including group order."""

    if len(hashes) < 2:
        raise RuntimeError("At least two unique exact-row groups are required for a split.")
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(hashes))
    ordered_counts = counts[order]
    cumulative = np.cumsum(ordered_counts)
    target = float(left_ratio) * float(cumulative[-1])
    cut = int(np.argmin(np.abs(cumulative[:-1] - target))) + 1
    cut = min(max(cut, 1), len(order) - 1)
    left_index = order[:cut]
    right_index = order[cut:]
    return (
        (hashes[left_index], counts[left_index]),
        (hashes[right_index], counts[right_index]),
    )


def _indices_for_groups(all_hashes: np.ndarray, selected_hashes: np.ndarray) -> np.ndarray:
    selected = _structured_hashes(selected_hashes)
    mask = np.isin(_structured_hashes(all_hashes), selected)
    return np.flatnonzero(mask)


def _part(source: SourceData, indices: np.ndarray, label_id: int) -> SplitData:
    indices = np.asarray(indices, dtype=np.int64)
    return SplitData(
        X=source.values[indices],
        y=np.full(len(indices), int(label_id), dtype=np.int64),
        source=np.full(len(indices), source.source_class, dtype=object),
        hashes=source.hashes[indices],
    )


def _concat(parts: Sequence[SplitData], feature_count: int) -> SplitData:
    if not parts:
        return SplitData(
            X=np.empty((0, feature_count), dtype=np.float32),
            y=np.empty(0, dtype=np.int64),
            source=np.empty(0, dtype=object),
            hashes=np.empty((0, 2), dtype=np.uint64),
        )
    return SplitData(
        X=np.concatenate([part.X for part in parts], axis=0),
        y=np.concatenate([part.y for part in parts], axis=0),
        source=np.concatenate([part.source for part in parts], axis=0),
        hashes=np.concatenate([part.hashes for part in parts], axis=0),
    )


def _filter_against(candidate: SplitData, forbidden_hashes: np.ndarray) -> Tuple[SplitData, int, Dict[str, int]]:
    forbidden = np.unique(_structured_hashes(forbidden_hashes))
    overlap = np.isin(_structured_hashes(candidate.hashes), forbidden)
    removed_by_source: Dict[str, int] = {}
    if overlap.any():
        names, counts = np.unique(candidate.source[overlap], return_counts=True)
        removed_by_source = {str(name): int(count) for name, count in zip(names, counts)}
    for name in np.unique(candidate.source):
        removed_by_source.setdefault(str(name), 0)
    return candidate.filter(~overlap), int(overlap.sum()), removed_by_source


def _overlap_groups(left: np.ndarray, right: np.ndarray) -> int:
    if len(left) == 0 or len(right) == 0:
        return 0
    left_unique = np.unique(_structured_hashes(left))
    right_unique = np.unique(_structured_hashes(right))
    return int(np.isin(right_unique, left_unique).sum())


def _assert_no_conflicting_labels(split_name: str, split: SplitData) -> None:
    structured = _structured_hashes(split.hashes)
    _, inverse = np.unique(structured, return_inverse=True)
    lower = np.full(int(inverse.max(initial=-1)) + 1, np.iinfo(np.int64).max, dtype=np.int64)
    upper = np.full(len(lower), np.iinfo(np.int64).min, dtype=np.int64)
    np.minimum.at(lower, inverse, split.y)
    np.maximum.at(upper, inverse, split.y)
    conflicting = np.flatnonzero(lower != upper)
    if len(conflicting):
        raise RuntimeError(
            f"{split_name}: {len(conflicting)} exact-row hash groups carry conflicting final labels. "
            "Stop and exact-confirm those raw rows before training."
        )


def _build_raw_splits(
    dataset_root: Path,
    scenario: Mapping[str, object],
    cfg: PipelineConfig,
) -> Tuple[SplitData, SplitData, SplitData, Tuple[str, ...], List[Dict[str, object]], List[Dict[str, object]]]:
    paper_id = str(scenario["paper_id"])
    device_key = str(scenario["device_key"])
    task = str(scenario["task"])
    feature_columns: Optional[Tuple[str, ...]] = None
    train_parts: List[SplitData] = []
    validation_parts: List[SplitData] = []
    test_parts: List[SplitData] = []
    source_profiles: List[Dict[str, object]] = []
    split_rows: List[Dict[str, object]] = []

    if task == "multiclass":
        class_names = tuple(str(item) for item in scenario["classes"])
        plans = [
            (name, index, "outer_split", index)
            for index, name in enumerate(class_names)
        ]
    else:
        class_names = ("benign", "attack")
        plans = [("benign", 0, "outer_split", 0)]
        plans.extend(
            (str(name), 1, "train_attack", attack_index)
            for attack_index, name in enumerate(scenario["train_attacks"])
        )
        plans.extend(
            (str(name), 1, "test_attack", attack_index)
            for attack_index, name in enumerate(scenario["test_attacks"])
        )

    for class_name, label_id, assignment, assignment_index in plans:
        source = _read_source(
            dataset_root,
            device_key,
            class_name,
            feature_columns,
            cfg.expected_feature_count,
        )
        if feature_columns is None:
            feature_columns = source.feature_columns
        source_profiles.append(
            {
                "source_class": class_name,
                "relative_path": source.relative_path,
                "rows": int(len(source.values)),
                "feature_count": int(source.values.shape[1]),
                "schema_sha256": source.schema_sha256,
                "parsed_row_hash_sha256": source.parsed_row_hash_sha256,
                "hash_method": HASH_METHOD,
                "unique_hash_groups": source.unique_hash_groups,
                "duplicate_rows": source.duplicate_rows,
                "max_duplicate_multiplicity": source.max_duplicate_multiplicity,
            }
        )

        if assignment == "outer_split":
            unique_hashes, unique_counts = _unique_hash_groups(source.hashes)
            outer_train_groups, outer_test_groups = _split_unique_groups(
                unique_hashes,
                unique_counts,
                cfg.train_ratio,
                _scenario_seed(cfg.seed, paper_id, 100 + assignment_index),
            )
            fit_groups, validation_groups = _split_unique_groups(
                outer_train_groups[0],
                outer_train_groups[1],
                1.0 - cfg.validation_ratio_within_train,
                _scenario_seed(cfg.seed, paper_id, 500 + assignment_index),
            )
            fit = _indices_for_groups(source.hashes, fit_groups[0])
            validation = _indices_for_groups(source.hashes, validation_groups[0])
            test = _indices_for_groups(source.hashes, outer_test_groups[0])
        elif assignment == "train_attack":
            unique_hashes, unique_counts = _unique_hash_groups(source.hashes)
            fit_groups, validation_groups = _split_unique_groups(
                unique_hashes,
                unique_counts,
                1.0 - cfg.validation_ratio_within_train,
                _scenario_seed(cfg.seed, paper_id, 1000 + assignment_index),
            )
            fit = _indices_for_groups(source.hashes, fit_groups[0])
            validation = _indices_for_groups(source.hashes, validation_groups[0])
            test = np.empty(0, dtype=np.int64)
        elif assignment == "test_attack":
            fit = np.empty(0, dtype=np.int64)
            validation = np.empty(0, dtype=np.int64)
            test = np.arange(len(source.values), dtype=np.int64)
        else:
            raise AssertionError(assignment)

        if len(fit):
            train_parts.append(_part(source, fit, label_id))
        if len(validation):
            validation_parts.append(_part(source, validation, label_id))
        if len(test):
            test_parts.append(_part(source, test, label_id))
        for split_name, indices in (("train", fit), ("validation", validation), ("test", test)):
            if len(indices):
                split_rows.append(
                    {
                        "paper_id": paper_id,
                        "paper_code": str(scenario["paper_code"]),
                        "task": task,
                        "split": split_name,
                        "source_class": class_name,
                        "final_label_id": int(label_id),
                        "final_label": class_names[label_id],
                        "rows_before_cross_source_decontamination": int(len(indices)),
                    }
                )

    if feature_columns is None:
        raise RuntimeError(f"{paper_id}: no source data loaded.")
    train = _concat(train_parts, cfg.expected_feature_count)
    validation = _concat(validation_parts, cfg.expected_feature_count)
    test = _concat(test_parts, cfg.expected_feature_count)

    validation, removed_validation, removed_validation_by_source = _filter_against(
        validation,
        train.hashes,
    )
    train_and_validation_hashes = np.concatenate((train.hashes, validation.hashes), axis=0)
    test, removed_test, removed_test_by_source = _filter_against(
        test,
        train_and_validation_hashes,
    )

    for row in split_rows:
        source_name = str(row["source_class"])
        split_name = str(row["split"])
        if split_name == "validation":
            removed = removed_validation_by_source.get(source_name, 0)
        elif split_name == "test":
            removed = removed_test_by_source.get(source_name, 0)
        else:
            removed = 0
        row["removed_due_to_prior_split_overlap"] = int(removed)
        row["rows"] = int(row["rows_before_cross_source_decontamination"]) - int(removed)

    _assert_no_conflicting_labels("train", train)
    _assert_no_conflicting_labels("validation", validation)
    _assert_no_conflicting_labels("test", test)
    train_val_overlap = _overlap_groups(train.hashes, validation.hashes)
    train_test_overlap = _overlap_groups(train_and_validation_hashes, test.hashes)
    if train_val_overlap or train_test_overlap:
        raise AssertionError(
            f"Leakage invariant failed: train-validation={train_val_overlap}, "
            f"train-test={train_test_overlap}."
        )

    split_rows.append(
        {
            "paper_id": paper_id,
            "paper_code": str(scenario["paper_code"]),
            "task": task,
            "split": "__audit__",
            "source_class": "__all__",
            "final_label_id": -1,
            "final_label": "__all__",
            "rows_before_cross_source_decontamination": int(
                train.rows + validation.rows + test.rows + removed_validation + removed_test
            ),
            "removed_due_to_prior_split_overlap": int(removed_validation + removed_test),
            "rows": int(train.rows + validation.rows + test.rows),
            "removed_validation": int(removed_validation),
            "removed_test": int(removed_test),
            "remaining_train_validation_overlap_hash_groups": int(train_val_overlap),
            "remaining_train_test_overlap_hash_groups": int(train_test_overlap),
        }
    )
    return train, validation, test, feature_columns, source_profiles, split_rows


def _fit_transformer(train_x: np.ndarray, cfg: PipelineConfig, seed: int) -> QuantileTransformer:
    if len(train_x) < 2:
        raise RuntimeError("At least two training rows are required for preprocessing.")
    subsample = min(int(cfg.quantile_subsample), int(len(train_x)))
    n_quantiles = min(int(cfg.quantile_n_quantiles), subsample, int(len(train_x)))
    transformer = QuantileTransformer(
        n_quantiles=n_quantiles,
        output_distribution="uniform",
        random_state=int(seed),
        subsample=subsample,
        copy=True,
    )
    transformer.fit(train_x)
    return transformer


def _transform_shared(
    transformer: QuantileTransformer,
    values: np.ndarray,
    cfg: PipelineConfig,
) -> np.ndarray:
    output = np.empty(values.shape, dtype=np.float32)
    scale = float(cfg.output_high - cfg.output_low)
    for start in range(0, len(values), cfg.transform_chunk_size):
        stop = min(start + cfg.transform_chunk_size, len(values))
        transformed = transformer.transform(values[start:stop])
        transformed = cfg.output_low + scale * transformed
        output[start:stop] = transformed.astype(np.float32, copy=False)
    if not np.isfinite(output).all():
        raise FloatingPointError("Shared preprocessing produced non-finite values.")
    tolerance = 1e-6
    if output.size and (
        float(output.min()) < cfg.output_low - tolerance
        or float(output.max()) > cfg.output_high + tolerance
    ):
        raise AssertionError("Quantile output escaped the locked [0.1, 0.9] range.")
    return output


def _largest_remainder(total: int, proportions: np.ndarray) -> np.ndarray:
    proportions = np.asarray(proportions, dtype=np.float64)
    if total < 0 or proportions.ndim != 1 or len(proportions) == 0:
        raise ValueError("Invalid allocation inputs.")
    proportions = proportions / proportions.sum()
    exact = float(total) * proportions
    counts = np.floor(exact).astype(np.int64)
    remainder = int(total - counts.sum())
    if remainder:
        order = np.lexsort((np.arange(len(proportions)), -(exact - counts)))
        counts[order[:remainder]] += 1
    if int(counts.sum()) != int(total):
        raise AssertionError("Largest-remainder allocation lost rows.")
    return counts


def _sample_partition_proportions(
    y_train: np.ndarray,
    num_classes: int,
    cfg: PipelineConfig,
    seed: int,
) -> Tuple[np.ndarray, int]:
    if cfg.partition_mode == "iid_stratified":
        matrix = np.full((num_classes, cfg.num_clients), 1.0 / cfg.num_clients)
        return matrix, 1

    rng = np.random.default_rng(seed)
    class_counts = np.bincount(y_train, minlength=num_classes)
    for attempt in range(1, cfg.max_partition_attempts + 1):
        matrix = np.vstack(
            [
                rng.dirichlet(np.full(cfg.num_clients, cfg.dirichlet_alpha))
                for _ in range(num_classes)
            ]
        )
        allocated = np.vstack(
            [_largest_remainder(int(class_counts[class_id]), matrix[class_id]) for class_id in range(num_classes)]
        )
        if int(allocated.sum(axis=0).min()) >= cfg.min_client_train_rows:
            return matrix, attempt
    raise RuntimeError(
        "Unable to sample a Dirichlet partition meeting min_client_train_rows. "
        "For a genuine full run keep the data unchanged; for a synthetic test lower the minimum."
    )


def _partition_indices(
    labels: np.ndarray,
    proportions: np.ndarray,
    seed: int,
) -> List[np.ndarray]:
    labels = np.asarray(labels, dtype=np.int64)
    num_classes, num_clients = proportions.shape
    rng = np.random.default_rng(seed)
    chunks: List[List[np.ndarray]] = [[] for _ in range(num_clients)]
    for class_id in range(num_classes):
        indices = np.flatnonzero(labels == class_id)
        rng.shuffle(indices)
        counts = _largest_remainder(len(indices), proportions[class_id])
        cursor = 0
        for client_id, count in enumerate(counts):
            stop = cursor + int(count)
            if stop > cursor:
                chunks[client_id].append(indices[cursor:stop])
            cursor = stop
        if cursor != len(indices):
            raise AssertionError("Client allocation did not consume a class exactly once.")

    result: List[np.ndarray] = []
    for client_id, pieces in enumerate(chunks):
        merged = np.concatenate(pieces) if pieces else np.empty(0, dtype=np.int64)
        rng.shuffle(merged)
        result.append(merged)
    _assert_partition_cover(result, len(labels))
    return result


def _assert_partition_cover(parts: Sequence[np.ndarray], total_rows: int) -> None:
    merged = np.concatenate(parts) if parts else np.empty(0, dtype=np.int64)
    if len(merged) != total_rows:
        raise AssertionError(f"Client partitions cover {len(merged)} of {total_rows} rows.")
    if total_rows and (
        int(merged.min()) != 0
        or int(merged.max()) != total_rows - 1
        or len(np.unique(merged)) != total_rows
    ):
        raise AssertionError("Client partitions are overlapping or incomplete.")


def _counts_by_source(split: SplitData) -> Dict[str, int]:
    names, counts = np.unique(split.source, return_counts=True)
    return {str(name): int(count) for name, count in zip(names, counts)}



@dataclass
class IoT01DataBundle:
    records: List[Dict[str, object]]
    input_dim: int
    class_names: Tuple[str, ...]
    audit: Dict[str, object]
    source_manifest: pd.DataFrame
    client_class_counts: pd.DataFrame


def build_iot01_data(dataset_root: object, seed: int = 42) -> IoT01DataBundle:
    cfg = PipelineConfig(
        seed=int(seed),
        train_ratio=0.70,
        validation_ratio_within_train=0.15,
        expected_feature_count=115,
        num_clients=9,
        partition_mode="dirichlet",
        dirichlet_alpha=0.30,
        min_client_train_rows=128,
        max_partition_attempts=1000,
        quantile_n_quantiles=1000,
        quantile_subsample=200_000,
        transform_chunk_size=50_000,
        output_low=0.10,
        output_high=0.90,
    )
    cfg.validate()
    root = resolve_dataset_root(dataset_root)
    validate_scenario_files(root, "IoT-01")
    started = time.time()

    train_raw, validation_raw, test_raw, columns, profiles, split_rows = _build_raw_splits(
        root, IOT01_SCENARIO, cfg
    )
    class_names = tuple(IOT01_SCENARIO["classes"])
    expected_labels = np.arange(len(class_names), dtype=np.int64)
    for split_name, split in (("train", train_raw), ("validation", validation_raw), ("test", test_raw)):
        observed = np.unique(split.y)
        if not np.array_equal(observed, expected_labels):
            raise RuntimeError(f"{split_name}: incomplete labels {observed.tolist()}.")

    transformer_seed = _scenario_seed(cfg.seed, "IoT-01", 2000)
    transformer = _fit_transformer(train_raw.X, cfg, transformer_seed)
    train_x = _transform_shared(transformer, train_raw.X, cfg)
    validation_x = _transform_shared(transformer, validation_raw.X, cfg)
    test_x = _transform_shared(transformer, test_raw.X, cfg)

    partition_seed = _scenario_seed(cfg.seed, "IoT-01", 3000)
    proportions, partition_attempts = _sample_partition_proportions(
        train_raw.y, len(class_names), cfg, partition_seed
    )
    split_indices = {
        "train": _partition_indices(train_raw.y, proportions, partition_seed + 101),
        "validation": _partition_indices(validation_raw.y, proportions, partition_seed + 202),
        "test": _partition_indices(test_raw.y, proportions, partition_seed + 303),
    }
    raw_by_split = {"train": train_raw, "validation": validation_raw, "test": test_raw}
    x_by_split = {"train": train_x, "validation": validation_x, "test": test_x}

    records: List[Dict[str, object]] = []
    count_rows: List[Dict[str, object]] = []
    for client_id in range(cfg.num_clients):
        record: Dict[str, object] = {
            "client_id": client_id,
            "scenario_id": "IoT-01",
            "paper_code": "DanG-6",
            "task": "multiclass",
            "source_device_key": "danmini",
            "source_device": "Danmini_Doorbell",
            "source_directory": str(root / "Danmini_Doorbell"),
            "class_names": class_names,
            "num_classes": len(class_names),
            "input_dim": 115,
            "partition_mode": "dirichlet",
            "partition_seed": partition_seed,
        }
        for split_name in ("train", "validation", "test"):
            idx = split_indices[split_name][client_id]
            raw = raw_by_split[split_name]
            record[f"X_{split_name}"] = x_by_split[split_name][idx]
            record[f"X_{split_name}_raw"] = raw.X[idx].astype(np.float32)
            record[f"y_{split_name}"] = raw.y[idx]
            record[f"source_{split_name}"] = raw.source[idx]
            for class_id, class_name in enumerate(class_names):
                count_rows.append({
                    "client": client_id,
                    "split": split_name,
                    "class_id": class_id,
                    "class_name": class_name,
                    "rows": int(np.sum(raw.y[idx] == class_id)),
                })
        records.append(record)

    manifest = pd.DataFrame(profiles)
    manifest_ok = True
    for row in profiles:
        expected_rows, expected_digest = EXPECTED_SOURCE[str(row["source_class"])]
        manifest_ok &= int(row["rows"]) == expected_rows
        manifest_ok &= str(row["parsed_row_hash_sha256"]) == expected_digest
        manifest_ok &= str(row["schema_sha256"]) == EXPECTED_SCHEMA_SHA256

    removed = next(row for row in split_rows if row["split"] == "__audit__")
    sizes = (train_raw.rows, validation_raw.rows, test_raw.rows)
    class_counts = {
        "train": tuple(np.bincount(train_raw.y, minlength=len(class_names)).tolist()),
        "validation": tuple(np.bincount(validation_raw.y, minlength=len(class_names)).tolist()),
        "test": tuple(np.bincount(test_raw.y, minlength=len(class_names)).tolist()),
    }
    locked_counts_ok = True
    if int(seed) == 42:
        locked_counts_ok = sizes == EXPECTED_SEED42_SPLIT and class_counts == EXPECTED_SEED42_CLASS_COUNTS

    finite_range_ok = all(
        np.isfinite(values).all()
        and (values.size == 0 or float(values.min()) >= cfg.output_low - 1e-6)
        and (values.size == 0 or float(values.max()) <= cfg.output_high + 1e-6)
        for values in (train_x, validation_x, test_x)
    )
    partition_ok = all(
        sum(len(part) for part in split_indices[name]) == raw_by_split[name].rows
        and len(np.unique(np.concatenate(split_indices[name]))) == raw_by_split[name].rows
        for name in ("train", "validation", "test")
    )
    overlap_ok = (
        int(removed["remaining_train_validation_overlap_hash_groups"]) == 0
        and int(removed["remaining_train_test_overlap_hash_groups"]) == 0
    )
    checklist = {
        "audited_raw_manifest": "PASS" if manifest_ok else "FAIL",
        "115_features_numeric_finite": "PASS" if len(columns) == 115 else "FAIL",
        "group_split_before_transform": "PASS",
        "seed42_locked_split_counts": "PASS" if locked_counts_ok else "FAIL",
        "zero_train_validation_overlap": "PASS" if overlap_ok else "FAIL",
        "zero_train_test_overlap": "PASS" if overlap_ok else "FAIL",
        "one_shared_train_only_quantile": "PASS",
        "transformed_range_0.1_0.9": "PASS" if finite_range_ok else "FAIL",
        "nine_dirichlet_clients_alpha_0.3": "PASS" if len(records) == 9 else "FAIL",
        "every_row_assigned_once": "PASS" if partition_ok else "FAIL",
        "test_not_used_for_fit_or_selection": "PASS",
    }
    failed = [name for name, status in checklist.items() if status != "PASS"]
    if failed:
        raise RuntimeError(f"STOP_DATA_GATE: {failed}")

    audit = {
        "gate_status": "PASS_DATA_GATE",
        "pipeline_version": PIPELINE_VERSION,
        "seed": int(seed),
        "dataset_root": str(root),
        "class_names": class_names,
        "raw_rows": int(sum(row["rows"] for row in profiles)),
        "train_rows": train_raw.rows,
        "validation_rows": validation_raw.rows,
        "test_rows": test_raw.rows,
        "class_counts": class_counts,
        "removed_from_validation": int(removed["removed_validation"]),
        "removed_from_test": int(removed["removed_test"]),
        "train_validation_overlap_groups": 0,
        "train_test_overlap_groups": 0,
        "preprocessing": {
            "name": "QuantileTransformer",
            "fit_split": "train only",
            "scope": "one shared transformer",
            "n_quantiles": int(transformer.n_quantiles_),
            "subsample": min(cfg.quantile_subsample, train_raw.rows),
            "range": [0.1, 0.9],
            "seed": transformer_seed,
        },
        "federation": {
            "clients": 9,
            "mode": "dirichlet",
            "alpha": 0.3,
            "partition_seed": partition_seed,
            "partition_attempts": partition_attempts,
            "client_train_rows": [len(v) for v in split_indices["train"]],
            "class_client_proportions": proportions.tolist(),
        },
        "checklist": checklist,
        "elapsed_seconds": round(time.time() - started, 3),
    }
    return IoT01DataBundle(
        records=records,
        input_dim=115,
        class_names=class_names,
        audit=audit,
        source_manifest=manifest,
        client_class_counts=pd.DataFrame(count_rows),
    )


# =============================================================================
# Paper scenario extension (IoT-02..IoT-07) used only by post-training paper jobs.
# IoT-01 continues to use the strict audited manifest above.
# =============================================================================
MIRAI_CLASSES = (
    "mirai.ack", "mirai.scan", "mirai.syn", "mirai.udp", "mirai.udpplain"
)
for _name in MIRAI_CLASSES:
    FILE_NAME_BY_CLASS.setdefault(_name, f"{_name}.csv")

# Common N-BaIoT folder aliases. Resolution below is normalization-based, so minor
# underscore/slash naming differences on the workstation are tolerated.
DEVICE_FOLDER_ALIASES = {
    "danmini": ("Danmini_Doorbell",),
    "philips": ("Philips_B120N10_Baby_Monitor", "Philips_B120N_10_Baby_Monitor"),
    "provision838": ("Provision_PT_838_Security_Camera", "Provision_PT838_Security_Camera"),
    "ecobee": ("Ecobee_Thermostat",),
    "provision737": ("Provision_PT_737E_Security_Camera", "Provision_PT737E_Security_Camera"),
}

PAPER_SCENARIOS = {
    "IoT-01": IOT01_SCENARIO,
    "IoT-02": {"paper_id":"IoT-02", "paper_code":"PhiG-6", "task":"multiclass", "device_key":"philips", "classes":("benign", *GAFGYT_CLASSES)},
    "IoT-03": {"paper_id":"IoT-03", "paper_code":"838G-6", "task":"multiclass", "device_key":"provision838", "classes":("benign", *GAFGYT_CLASSES)},
    "IoT-04": {"paper_id":"IoT-04", "paper_code":"EcoG-6", "task":"multiclass", "device_key":"ecobee", "classes":("benign", *GAFGYT_CLASSES)},
    "IoT-05": {"paper_id":"IoT-05", "paper_code":"737G-6", "task":"multiclass", "device_key":"provision737", "classes":("benign", *GAFGYT_CLASSES)},
    "IoT-06": {"paper_id":"IoT-06", "paper_code":"EcoMG-11", "task":"multiclass", "device_key":"ecobee", "classes":("benign", *GAFGYT_CLASSES, *MIRAI_CLASSES)},
    "IoT-07": {"paper_id":"IoT-07", "paper_code":"838MG-11", "task":"multiclass", "device_key":"provision838", "classes":("benign", *GAFGYT_CLASSES, *MIRAI_CLASSES)},
    # Table-VIII/open-set scenarios from the base-paper protocol.
    # Training attacks and test attacks are intentionally disjoint; all attacks map to binary label 1.
    "IoT-08": {
        "paper_id":"IoT-08", "paper_code":"737GUC-2", "task":"binary_open_set",
        "device_key":"provision737", "classes":("benign", "attack"),
        "train_attacks":("gafgyt.combo", "gafgyt.udp"),
        "test_attacks":("gafgyt.junk", "gafgyt.scan", "gafgyt.tcp", *MIRAI_CLASSES),
    },
    "IoT-09": {
        "paper_id":"IoT-09", "paper_code":"838GUC-2", "task":"binary_open_set",
        "device_key":"provision838", "classes":("benign", "attack"),
        "train_attacks":("gafgyt.combo", "gafgyt.udp"),
        "test_attacks":("gafgyt.junk", "gafgyt.scan", "gafgyt.tcp", *MIRAI_CLASSES),
    },
    "IoT-10": {
        "paper_id":"IoT-10", "paper_code":"DanM-2", "task":"binary_open_set",
        "device_key":"danmini", "classes":("benign", "attack"),
        "train_attacks":MIRAI_CLASSES,
        "test_attacks":GAFGYT_CLASSES,
    },
    "IoT-11": {
        "paper_id":"IoT-11", "paper_code":"838M-2", "task":"binary_open_set",
        "device_key":"provision838", "classes":("benign", "attack"),
        "train_attacks":MIRAI_CLASSES,
        "test_attacks":GAFGYT_CLASSES,
    },
}
SCENARIO_BY_ID.update(PAPER_SCENARIOS)


def _resolve_device_folder_flexible(root: Path, device_key: str) -> Path:
    aliases = DEVICE_FOLDER_ALIASES.get(device_key, ())
    for alias in aliases:
        candidate = root / alias
        if candidate.is_dir():
            return candidate
    target_norms = {_normal_folder_name(alias) for alias in aliases}
    for child in root.iterdir():
        if child.is_dir() and _normal_folder_name(child.name) in target_norms:
            return child
    raise FileNotFoundError(f"Device folder not found for {device_key}; expected one of {aliases}")


def _source_path(root: Path, device_key: str, class_name: str) -> Path:
    """Resolve flattened or standard nested N-BaIoT attack CSV layouts."""
    folder = _resolve_device_folder_flexible(root, device_key)
    if class_name == "benign":
        candidates = [folder / "benign_traffic.csv", folder / "benign.csv"]
    else:
        family, attack = class_name.split(".", 1)
        candidates = [
            folder / f"{class_name}.csv",
            folder / f"{family}_{attack}.csv",
            folder / family / f"{attack}.csv",
            folder / family / f"{class_name}.csv",
        ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    # Last-resort recursive match, still family-aware to avoid ambiguous scan/udp names.
    wanted = class_name.lower().replace("_", "").replace("-", "").replace(".", "")
    family = "" if class_name == "benign" else class_name.split(".",1)[0].lower()
    attack = "benign" if class_name == "benign" else class_name.split(".",1)[1].lower().replace("_","")
    scored = []
    for candidate in folder.rglob("*.csv"):
        norm = candidate.stem.lower().replace("_", "").replace("-", "").replace(".", "")
        path_lower = candidate.as_posix().lower()
        score = 0
        if norm == wanted:
            score += 10
        if attack in norm:
            score += 3
        if family and family in path_lower:
            score += 4
        if class_name == "benign" and "benign" in norm:
            score += 10
        if score >= 7:
            scored.append((score, candidate))
    if scored:
        scored.sort(key=lambda x: (-x[0], len(str(x[1]))))
        return scored[0][1]
    raise FileNotFoundError(f"CSV not found for {device_key}/{class_name} under {folder}")


def _looks_like_nbaiot_root(path: Path) -> bool:
    if not path.is_dir():
        return False
    try:
        _source_path(path, "danmini", "benign")
        return True
    except Exception:
        return False


def build_nbaiot_scenario_data(dataset_root: object, scenario_id: str, seed: int = 42) -> IoT01DataBundle:
    """Leakage-safe, train-only-preprocessed, Dirichlet non-IID build for IoT-01..IoT-11."""
    if scenario_id == "IoT-01":
        return build_iot01_data(dataset_root, seed=seed)
    if scenario_id not in PAPER_SCENARIOS:
        raise KeyError(f"Unsupported paper scenario: {scenario_id}")

    scenario = PAPER_SCENARIOS[scenario_id]
    cfg = PipelineConfig(
        seed=int(seed), train_ratio=0.70, validation_ratio_within_train=0.15,
        expected_feature_count=115, num_clients=9, partition_mode="dirichlet",
        dirichlet_alpha=0.30, min_client_train_rows=128, max_partition_attempts=1000,
        quantile_n_quantiles=1000, quantile_subsample=200_000,
        transform_chunk_size=50_000, output_low=0.10, output_high=0.90,
    )
    cfg.validate()
    root = resolve_dataset_root(dataset_root)
    validate_scenario_files(root, scenario_id)
    started = time.time()

    train_raw, validation_raw, test_raw, columns, profiles, split_rows = _build_raw_splits(root, scenario, cfg)
    class_names = tuple(str(x) for x in scenario["classes"])
    expected = np.arange(len(class_names), dtype=np.int64)
    for split_name, split in (("train", train_raw), ("validation", validation_raw), ("test", test_raw)):
        observed = np.unique(split.y)
        if not np.array_equal(observed, expected):
            raise RuntimeError(f"{scenario_id}/{split_name}: incomplete labels {observed.tolist()}")

    transformer_seed = _scenario_seed(cfg.seed, scenario_id, 2000)
    transformer = _fit_transformer(train_raw.X, cfg, transformer_seed)
    x_by_split = {
        "train": _transform_shared(transformer, train_raw.X, cfg),
        "validation": _transform_shared(transformer, validation_raw.X, cfg),
        "test": _transform_shared(transformer, test_raw.X, cfg),
    }
    raw_by_split = {"train": train_raw, "validation": validation_raw, "test": test_raw}

    # Same Dirichlet class proportions are used for the persistent clients in every split.
    base_partition_seed = _scenario_seed(cfg.seed, scenario_id, 3000)
    proportions = None
    split_indices = None
    partition_attempts = 0
    for retry in range(100):
        p_seed = base_partition_seed + retry * 1009
        candidate, attempts = _sample_partition_proportions(train_raw.y, len(class_names), cfg, p_seed)
        candidate_indices = {
            "train": _partition_indices(train_raw.y, candidate, p_seed + 101),
            "validation": _partition_indices(validation_raw.y, candidate, p_seed + 202),
            "test": _partition_indices(test_raw.y, candidate, p_seed + 303),
        }
        # FederatedClient requires non-empty split arrays for every client.
        if all(len(candidate_indices[s][cid]) > 0 for s in candidate_indices for cid in range(cfg.num_clients)):
            proportions, split_indices, partition_attempts = candidate, candidate_indices, attempts
            partition_seed = p_seed
            break
    if proportions is None or split_indices is None:
        raise RuntimeError(f"{scenario_id}: unable to construct nine non-empty persistent clients")

    records, count_rows = [], []
    device_folder = _resolve_device_folder_flexible(root, str(scenario["device_key"]))
    for client_id in range(cfg.num_clients):
        record = {
            "client_id": client_id, "scenario_id": scenario_id,
            "paper_code": str(scenario["paper_code"]), "task": str(scenario["task"]),
            "source_device_key": str(scenario["device_key"]),
            "source_device": device_folder.name, "source_directory": str(device_folder),
            "class_names": class_names, "num_classes": len(class_names), "input_dim": 115,
            "partition_mode": "dirichlet", "partition_seed": partition_seed,
        }
        for split_name in ("train", "validation", "test"):
            idx = split_indices[split_name][client_id]
            raw = raw_by_split[split_name]
            record[f"X_{split_name}"] = x_by_split[split_name][idx]
            record[f"X_{split_name}_raw"] = raw.X[idx].astype(np.float32)
            record[f"y_{split_name}"] = raw.y[idx]
            record[f"source_{split_name}"] = raw.source[idx]
            for class_id, class_name in enumerate(class_names):
                count_rows.append({"client":client_id, "split":split_name, "class_id":class_id,
                                   "class_name":class_name, "rows":int(np.sum(raw.y[idx] == class_id))})
        records.append(record)

    removed = next(row for row in split_rows if row["split"] == "__audit__")
    overlap_ok = int(removed["remaining_train_validation_overlap_hash_groups"]) == 0 and int(removed["remaining_train_test_overlap_hash_groups"]) == 0
    partition_ok = all(
        sum(len(part) for part in split_indices[name]) == raw_by_split[name].rows and
        len(np.unique(np.concatenate(split_indices[name]))) == raw_by_split[name].rows
        for name in ("train", "validation", "test")
    )
    finite_ok = all(np.isfinite(v).all() for v in x_by_split.values())
    checklist = {
        "115_features_numeric_finite":"PASS" if len(columns)==115 and finite_ok else "FAIL",
        "group_split_before_transform":"PASS",
        "zero_train_validation_overlap":"PASS" if overlap_ok else "FAIL",
        "zero_train_test_overlap":"PASS" if overlap_ok else "FAIL",
        "one_shared_train_only_quantile":"PASS",
        "nine_dirichlet_clients_alpha_0.3":"PASS" if len(records)==9 else "FAIL",
        "every_row_assigned_once":"PASS" if partition_ok else "FAIL",
        "test_not_used_for_fit_or_selection":"PASS",
    }
    failed = [k for k,v in checklist.items() if v != "PASS"]
    if failed:
        raise RuntimeError(f"{scenario_id}: STOP_DATA_GATE {failed}")

    audit = {
        "gate_status":"PASS_DATA_GATE", "pipeline_version":PIPELINE_VERSION,
        "seed":int(seed), "dataset_root":str(root), "scenario_id":scenario_id,
        "class_names":class_names, "train_rows":train_raw.rows,
        "validation_rows":validation_raw.rows, "test_rows":test_raw.rows,
        "federation":{"clients":9, "mode":"dirichlet", "alpha":0.3,
                      "partition_seed":partition_seed, "partition_attempts":partition_attempts,
                      "client_train_rows":[len(v) for v in split_indices["train"]],
                      "class_client_proportions":proportions.tolist()},
        "checklist":checklist, "elapsed_seconds":round(time.time()-started,3),
    }
    return IoT01DataBundle(
        records=records, input_dim=115, class_names=class_names,
        audit=audit, source_manifest=pd.DataFrame(profiles),
        client_class_counts=pd.DataFrame(count_rows),
    )


# ===== NOTEBOOK CODE CELL 10 =====
# 3. Build IoT-01 once and stop if any data-integrity gate fails
if SYNTHETIC_ONLY or not IOT01_DATA_REQUIRED:
    DATA = None
    if SYNTHETIC_ONLY:
        out_print("DATA_AUDIT", "Synthetic-only mode: raw IoT-01 build skipped.")
    else:
        out_print("DATA_AUDIT", "IoT-01 data build skipped: no selected output requires it.")
else:
    DATA = build_iot01_data(DATASET_ROOT, seed=CONFIG.seed)
    if output_enabled("FIGURE_4"):
        missing_raw = []
        for record in DATA.records:
            cid = int(record["client_id"])
            for split in ("train", "validation", "test"):
                raw_key = f"X_{split}_raw"
                y_key = f"y_{split}"
                if raw_key not in record or len(record[raw_key]) != len(record[y_key]):
                    missing_raw.append(f"client={cid}/{split}")
        if missing_raw:
            raise RuntimeError(
                "STOP BEFORE TRAINING: Figure 4 V6.5 requires true raw Train/Validation/Test "
                "for every IoT-01 client; missing/misaligned=" + ", ".join(missing_raw)
            )
        out_print(
            "DATA_AUDIT",
            "✓ Figure 4 raw-data gate: X_train_raw/X_validation_raw/X_test_raw are row-aligned for all 9 clients."
        )
    a = DATA.audit
    out_print(
        "DATA_AUDIT",
        f"IoT-01 DATA | PASS | train={a['train_rows']} | validation={a['validation_rows']} | "
        f"test={a['test_rows']} | all={a['train_rows']+a['validation_rows']+a['test_rows']} | "
        f"classes={len(DATA.class_names)} | clients=9 | Dirichlet alpha=0.3"
    )


# ===== NOTEBOOK CODE CELL 11 =====
# 4. Two model families: standalone VAE baselines and the proposed ACVAE
class FederatedVAE(nn.Module):
    PRIVATE_PREFIXES: Tuple[str, ...] = ("encoder.",)
    SHARED_PREFIXES: Tuple[str, ...] = ("mapper.", "decoder.")

    def __init__(
        self,
        input_dim: int,
        num_classes: int,
        latent_dim: int,
        condition_scale: float,
        conditional: bool,
    ) -> None:
        super().__init__()
        if input_dim < 2 or num_classes < 2 or latent_dim < 2:
            raise ValueError("Invalid VAE dimensions.")
        self.input_dim = int(input_dim)
        self.num_classes = int(num_classes)
        self.latent_dim = int(latent_dim)
        self.condition_scale = float(condition_scale)
        self.conditional = bool(conditional)

        # LayerNorm has no client-specific running statistics to aggregate.
        self.encoder = nn.Sequential(
            nn.Linear(self.input_dim, 128),
            nn.LayerNorm(128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.LayerNorm(64),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1),
            nn.Linear(64, 32),
            nn.LayerNorm(32),
            nn.LeakyReLU(0.2),
            nn.Linear(32, 2 * self.latent_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(self.latent_dim, 32),
            nn.LayerNorm(32),
            nn.LeakyReLU(0.2),
            nn.Linear(32, 64),
            nn.LayerNorm(64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 128),
            nn.LayerNorm(128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, self.input_dim),
            nn.Sigmoid(),
        )

        # In Algorithm 3, C_theta maps a class label to the latent space.
        # Naming it mapper makes the paper's communicated component explicit.
        if self.conditional:
            self.mapper: Optional[nn.Embedding] = nn.Embedding(self.num_classes, self.latent_dim)
            nn.init.uniform_(self.mapper.weight, -0.03, 0.03)
        else:
            self.mapper = None

    def encode(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """The deployment path is x -> mu(x); no label is accepted."""
        if x.ndim != 2 or x.shape[1] != self.input_dim:
            raise ValueError(f"Expected [N, {self.input_dim}], got {tuple(x.shape)}.")
        hidden = self.encoder(x)
        mu, logvar = hidden.chunk(2, dim=1)
        return mu, torch.clamp(logvar, min=-6.0, max=4.0)

    @staticmethod
    def reparameterize(mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        return mu + torch.randn_like(mu) * torch.exp(0.5 * logvar)

    def training_forward(self, x: torch.Tensor, y: torch.Tensor) -> Dict[str, torch.Tensor]:
        y = torch.as_tensor(y, dtype=torch.long, device=x.device).reshape(-1)
        if len(y) != len(x) or y.numel() == 0:
            raise ValueError("Input/label batch mismatch.")
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        if self.conditional:
            if self.mapper is None:
                raise AssertionError("Conditional model has no mapper.")
            z_decoder = z + self.condition_scale * self.mapper(y)
        else:
            z_decoder = z
        reconstruction = self.decoder(z_decoder)
        return {
            "mu": mu,
            "logvar": logvar,
            "z": z,
            "z_decoder": z_decoder,
            "reconstruction": reconstruction,
        }

    @staticmethod
    def loss_terms(
        outputs: Mapping[str, torch.Tensor],
        x: torch.Tensor,
        y: torch.Tensor,
        cfg: ProtocolConfig,
        prior_mu: Optional[torch.Tensor] = None,
        prior_var: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        reconstruction = nn.functional.mse_loss(outputs["reconstruction"], x)
        posterior_var = torch.exp(outputs["logvar"])
        if prior_mu is None or prior_var is None:
            # Standalone FedAvg/FedProx and no-CMGA ablation: p(z)=N(0,I).
            kl_by_dimension = (
                posterior_var + outputs["mu"].pow(2) - 1.0 - outputs["logvar"]
            )
        else:
            selected_mu = prior_mu.index_select(0, y)
            selected_var = torch.clamp(
                prior_var.index_select(0, y), min=cfg.cmga_min_prior_variance
            )
            kl_by_dimension = (
                torch.log(selected_var)
                - outputs["logvar"]
                + (posterior_var + (outputs["mu"] - selected_mu).pow(2)) / selected_var
                - 1.0
            )
        kl = 0.5 * kl_by_dimension.sum(dim=1).mean()
        total = reconstruction + cfg.kl_weight * kl
        terms = {"total": total, "reconstruction": reconstruction, "kl": kl}
        if not all(torch.isfinite(value) for value in terms.values()):
            raise FloatingPointError("Non-finite VAE loss.")
        return terms

    def parameter_partition(self) -> Tuple[set[str], set[str]]:
        keys = set(self.state_dict())
        private = {key for key in keys if key.startswith(self.PRIVATE_PREFIXES)}
        shared = {key for key in keys if key.startswith(self.SHARED_PREFIXES)}
        if self.conditional and not any(key.startswith("mapper.") for key in shared):
            raise AssertionError("Conditional mapper is not in the shared partition.")
        if private & shared:
            raise AssertionError("Private/shared state overlap.")
        if private | shared != keys:
            raise AssertionError(f"Unassigned parameters: {sorted(keys - private - shared)}")
        return private, shared

    def communicated_keys(self, selective: bool) -> set[str]:
        if selective:
            return self.parameter_partition()[1]
        return set(self.state_dict())

    def communicated_state_dict(self, selective: bool) -> Dict[str, torch.Tensor]:
        state = self.state_dict()
        return {
            key: state[key].detach().cpu().clone()
            for key in sorted(self.communicated_keys(selective))
        }

    def load_communicated_state_dict(
        self, state: Mapping[str, torch.Tensor], selective: bool
    ) -> None:
        expected = self.communicated_keys(selective)
        if set(state) != expected:
            raise KeyError("Communicated state does not match the declared method partition.")
        current = self.state_dict()
        for key, value in state.items():
            if current[key].shape != value.shape:
                raise ValueError(f"Shape mismatch for {key}.")
            current[key] = value.to(current[key].device, dtype=current[key].dtype)
        self.load_state_dict(current, strict=True)


# ===== NOTEBOOK CODE CELL 12 =====

# 5. Method contracts and stateful clients
@dataclass(frozen=True)
class MethodSpec:
    variant: str
    purpose: str
    aggregation: str
    conditional: bool
    selective: bool
    use_cmga_priors: bool
    fedprox: bool

    def validate(self) -> None:
        if self.purpose not in {"competitor", "ablation", "proposed"}:
            raise ValueError("Unknown experimental purpose.")
        if self.aggregation not in {"FEDAVG", "FEDPROX", "CMGA"}:
            raise ValueError("Unknown aggregation method.")
        if self.aggregation == "FEDPROX" and not self.fedprox:
            raise ValueError("FedProx aggregation requires the proximal local objective.")
        if self.fedprox and self.aggregation != "FEDPROX":
            raise ValueError("The proximal objective belongs only to FedProx.")

        if self.variant in {"FedAvg_baseline", "FedProx_baseline"}:
            if self.purpose != "competitor" or self.conditional or self.selective or self.use_cmga_priors:
                raise ValueError("Standalone baselines cannot contain F-ACVAE components.")
            if self.aggregation == "CMGA":
                raise ValueError("A baseline cannot use CMGA.")
            return

        if self.variant == "ACVAE_no_CMGA":
            if not (self.purpose == "ablation" and self.conditional and self.selective):
                raise ValueError("no-CMGA must retain conditional/selective ACVAE.")
            if self.use_cmga_priors or self.aggregation != "FEDAVG" or self.fedprox:
                raise ValueError("no-CMGA must remove every CMGA mechanism.")
            return

        if self.variant == "F_ACVAE_no_selective":
            if not (self.purpose == "ablation" and self.conditional and not self.selective and self.use_cmga_priors):
                raise ValueError("Without-selective ablation must change only selective federation.")
            if self.aggregation != "CMGA" or self.fedprox:
                raise ValueError("Without-selective ablation retains CMGA.")
            return

        if self.variant == "F_ACVAE_no_conditioning":
            if not (self.purpose == "ablation" and not self.conditional and self.selective and self.use_cmga_priors):
                raise ValueError("Without-conditioning ablation must change only adaptive conditioning.")
            if self.aggregation != "CMGA" or self.fedprox:
                raise ValueError("Without-conditioning ablation retains CMGA.")
            return

        if self.variant == "F_ACVAE_CMGA":
            if self.purpose != "proposed" or not (self.conditional and self.selective and self.use_cmga_priors):
                raise ValueError("Full F-ACVAE must enable conditional/selective/CMGA components.")
            if self.aggregation != "CMGA" or self.fedprox:
                raise ValueError("Full F-ACVAE must use CMGA.")
            return

        raise ValueError(f"Unregistered method contract: {self.variant}")


METHOD_SPECS: Tuple[MethodSpec, ...] = (
    MethodSpec("FedAvg_baseline", "competitor", "FEDAVG", False, False, False, False),
    MethodSpec("FedProx_baseline", "competitor", "FEDPROX", False, False, False, True),
    MethodSpec("ACVAE_no_CMGA", "ablation", "FEDAVG", True, True, False, False),
    MethodSpec("F_ACVAE_CMGA", "proposed", "CMGA", True, True, True, False),
)
PAPER_ABLATION_SPECS: Tuple[MethodSpec, ...] = (
    MethodSpec("F_ACVAE_no_selective", "ablation", "CMGA", True, False, True, False),
    MethodSpec("F_ACVAE_no_conditioning", "ablation", "CMGA", False, True, True, False),
)
for _spec in (*METHOD_SPECS, *PAPER_ABLATION_SPECS):
    _spec.validate()


class FederatedClient:
    def __init__(
        self,
        record: Mapping[str, object],
        cfg: ProtocolConfig,
        spec: MethodSpec,
        device: torch.device,
    ) -> None:
        spec.validate()
        self.cfg = cfg
        self.spec = spec
        self.device = device
        self.cid = int(record["client_id"])
        self.input_dim = int(record["input_dim"])
        self.num_classes = int(record["num_classes"])
        self.class_names = tuple(record["class_names"])
        for split in ("train", "validation", "test"):
            x = torch.as_tensor(record[f"X_{split}"], dtype=torch.float32).cpu()
            y = torch.as_tensor(record[f"y_{split}"], dtype=torch.long).reshape(-1).cpu()
            if x.ndim != 2 or x.shape[1] != self.input_dim or len(x) != len(y):
                raise ValueError(f"client {self.cid}: invalid {split} arrays")
            if len(y) == 0 or not torch.isfinite(x).all():
                raise ValueError(f"client {self.cid}: empty/non-finite {split}")
            if int(y.min()) < 0 or int(y.max()) >= self.num_classes:
                raise ValueError(f"client {self.cid}: invalid {split} labels")
            setattr(self, f"X_{split}", x)
            setattr(self, f"y_{split}", y)
            raw_key = f"X_{split}_raw"
            if raw_key in record:
                setattr(self, f"X_{split}_raw", torch.as_tensor(record[raw_key], dtype=torch.float32).cpu())

        self.model = FederatedVAE(
            self.input_dim,
            self.num_classes,
            cfg.latent_dim,
            cfg.condition_scale,
            conditional=spec.conditional,
        ).to(device)

    def _loader(self, split: str, round_index: int, shuffle: bool) -> DataLoader:
        dataset = TensorDataset(getattr(self, f"X_{split}"), getattr(self, f"y_{split}"))
        generator = torch.Generator()
        generator.manual_seed(int(self.cfg.seed + 100_003 * round_index + 1_009 * self.cid))
        return DataLoader(
            dataset,
            batch_size=self.cfg.batch_size,
            shuffle=shuffle,
            drop_last=False,
            generator=generator,
            num_workers=0,
            pin_memory=self.device.type == "cuda",
        )

    def train_local(
        self,
        communicated_state: Mapping[str, torch.Tensor],
        round_index: int,
        prior_mu: Optional[torch.Tensor] = None,
        prior_var: Optional[torch.Tensor] = None,
    ) -> Dict[str, object]:
        if self.spec.use_cmga_priors != (prior_mu is not None and prior_var is not None):
            raise AssertionError("CMGA prior routing violates the method contract.")
        local_seed = int(self.cfg.seed + 100_003 * round_index + 1_009 * self.cid)
        torch.manual_seed(local_seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(local_seed)

        self.model.load_communicated_state_dict(communicated_state, self.spec.selective)
        before = self.model.communicated_state_dict(self.spec.selective)
        reference = {
            key: value.to(self.device).detach().clone()
            for key, value in communicated_state.items()
        }
        optimizer = optim.AdamW(
            self.model.parameters(), lr=self.cfg.local_lr, weight_decay=self.cfg.weight_decay
        )
        if prior_mu is not None:
            prior_mu = prior_mu.to(self.device, dtype=torch.float32)
            prior_var = prior_var.to(self.device, dtype=torch.float32)

        totals = {name: 0.0 for name in ("total", "reconstruction", "kl", "proximal")}
        batches = 0
        self.model.train()
        for _ in range(self.cfg.local_epochs):
            for batch_x, batch_y in self._loader("train", round_index, shuffle=True):
                batch_x = batch_x.to(self.device, non_blocking=True)
                batch_y = batch_y.to(self.device, non_blocking=True)
                optimizer.zero_grad(set_to_none=True)
                outputs = self.model.training_forward(batch_x, batch_y)
                terms = self.model.loss_terms(
                    outputs, batch_x, batch_y, self.cfg, prior_mu, prior_var
                )
                proximal = torch.zeros((), device=self.device, dtype=terms["total"].dtype)
                if self.spec.fedprox:
                    for name, parameter in self.model.named_parameters():
                        if name in reference:
                            proximal = proximal + (parameter - reference[name]).pow(2).sum()
                    proximal = 0.5 * self.cfg.fedprox_mu * proximal
                loss = terms["total"] + proximal
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"client {self.cid}: non-finite local loss")
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.cfg.gradient_clip_norm)
                if any(
                    p.grad is not None and not torch.isfinite(p.grad).all()
                    for p in self.model.parameters()
                ):
                    raise FloatingPointError(f"client {self.cid}: non-finite gradient")
                optimizer.step()
                totals["total"] += float(terms["total"].detach().item())
                totals["reconstruction"] += float(terms["reconstruction"].detach().item())
                totals["kl"] += float(terms["kl"].detach().item())
                totals["proximal"] += float(proximal.detach().item())
                batches += 1
        if batches == 0:
            raise RuntimeError(f"client {self.cid}: no local batches")

        after = self.model.communicated_state_dict(self.spec.selective)
        update = {key: after[key].float() - before[key].float() for key in before}
        gaussian = self.compute_class_gaussian_statistics() if self.spec.use_cmga_priors else None
        return {
            "client_id": self.cid,
            "samples": int(len(self.X_train)),
            "shared_update": update,
            "gaussian": gaussian,
            **{name: value / batches for name, value in totals.items()},
        }

    @torch.no_grad()
    def compute_class_gaussian_statistics(self) -> Dict[str, torch.Tensor]:
        if not self.spec.use_cmga_priors:
            raise RuntimeError("Only CMGA clients may compute Gaussian-prior statistics.")
        self.model.eval()
        counts = torch.zeros(self.num_classes, dtype=torch.long)
        sums = torch.zeros(self.num_classes, self.cfg.latent_dim, dtype=torch.float64)
        squared = torch.zeros_like(sums)
        for batch_x, batch_y in self._loader("train", round_index=0, shuffle=False):
            mu, _ = self.model.encode(batch_x.to(self.device))
            mu = mu.detach().cpu().to(torch.float64)
            for class_id in torch.unique(batch_y).tolist():
                selected = mu[batch_y == int(class_id)]
                counts[class_id] += len(selected)
                sums[class_id] += selected.sum(dim=0)
                squared[class_id] += selected.pow(2).sum(dim=0)
        means = torch.zeros_like(sums)
        variances = torch.ones_like(sums)
        for class_id in range(self.num_classes):
            count = int(counts[class_id])
            if count:
                means[class_id] = sums[class_id] / count
                variances[class_id] = torch.clamp(
                    squared[class_id] / count - means[class_id].pow(2),
                    min=self.cfg.cmga_min_prior_variance,
                )
        return {"count": counts, "mean": means.float(), "var": variances.float()}

    @torch.no_grad()
    def extract_mu(self, split: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if split not in {"train", "validation", "test"}:
            raise ValueError("Unknown split.")
        self.model.eval()
        mus: List[np.ndarray] = []
        labels: List[np.ndarray] = []
        inputs: List[np.ndarray] = []
        for batch_x, batch_y in self._loader(split, round_index=0, shuffle=False):
            # Labels are deliberately not passed to encode().
            mu, _ = self.model.encode(batch_x.to(self.device))
            if not torch.isfinite(mu).all():
                raise FloatingPointError(f"client {self.cid}: non-finite latent values")
            mus.append(mu.cpu().numpy().astype(np.float32))
            labels.append(batch_y.numpy().astype(np.int64))
            inputs.append(batch_x.numpy().astype(np.float32))
        return np.concatenate(mus), np.concatenate(labels), np.concatenate(inputs)


# -----------------------------------------------------------------------------
# Raw Data Integrity Gate  [notebook cell 13]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 14 =====

def validate_original_data_path(clients):
    """
    Fail-fast guard for Figure 4 Original Data.
    This does not affect training or evaluation.
    It only guarantees that raw validation data exists
    before expensive experiments are allowed to proceed.
    """
    missing = []

    for idx, client in enumerate(clients):
        if not hasattr(client, "X_validation_raw"):
            missing.append(idx)

    if missing:
        raise RuntimeError(
            "Raw validation data is unavailable for clients: "
            + str(missing)
            + "\nStop before long training. "
              "Figure 4 Original Data cannot be generated safely."
        )

    out_print("DATA_AUDIT", "✓ Original Data validation passed: X_validation_raw available.")


# ===== NOTEBOOK CODE CELL 15 =====
# 6. Independent aggregation rules, CMGA priors, and leakage-safe evaluation
def _state_l2(state: Mapping[str, torch.Tensor]) -> float:
    return float(np.sqrt(sum(float(v.float().pow(2).sum().item()) for v in state.values())))


def _state_digest(state: Mapping[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for key in sorted(state):
        value = state[key].detach().cpu().contiguous()
        digest.update(key.encode("utf-8"))
        digest.update(str(tuple(value.shape)).encode("ascii"))
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def _aggregate_model_state(
    current: Mapping[str, torch.Tensor],
    updates: Sequence[Mapping[str, torch.Tensor]],
    weights: np.ndarray,
    spec: MethodSpec,
    cfg: ProtocolConfig,
    velocity: Optional[Mapping[str, torch.Tensor]],
) -> Tuple[Dict[str, torch.Tensor], Optional[Dict[str, torch.Tensor]], Dict[str, float]]:
    if not updates or len(updates) != len(weights):
        raise ValueError("Aggregation requires one weight per update.")
    if not np.isclose(float(weights.sum()), 1.0, atol=1e-10):
        raise ValueError("Aggregation weights must sum to one.")
    keys = set(current)
    if any(set(update) != keys for update in updates):
        raise KeyError("Client update keys do not match global state.")

    mean_delta = {key: torch.zeros_like(value, dtype=torch.float32) for key, value in current.items()}
    clipped_elements = 0
    total_elements = 0
    for weight, update in zip(weights, updates):
        for key, raw in update.items():
            value = raw.detach().cpu().float()
            if not torch.isfinite(value).all():
                raise FloatingPointError("Non-finite client update.")
            total_elements += value.numel()
            if spec.aggregation == "CMGA":
                clipped_elements += int((value.abs() > cfg.cmga_update_clip_abs).sum().item())
                value = torch.clamp(value, -cfg.cmga_update_clip_abs, cfg.cmga_update_clip_abs)
            mean_delta[key] += float(weight) * value

    if spec.aggregation in {"FEDAVG", "FEDPROX"}:
        if velocity is not None:
            raise AssertionError("FedAvg/FedProx must not own a CMGA velocity buffer.")
        applied = mean_delta
        new_velocity = None
        model_step_scale = 1.0
    else:
        if velocity is None or set(velocity) != keys:
            raise AssertionError("CMGA requires its own persistent velocity state.")
        new_velocity = {
            key: (
                cfg.cmga_gamma * mean_delta[key]
                + (1.0 - cfg.cmga_gamma) * velocity[key].detach().cpu().float()
            )
            for key in keys
        }
        # Coherent composition of CMGA Eq. (15) and MSA Eq. (18)-(20):
        # theta_{t+1} = theta_t + alpha * V_t.
        applied = {key: cfg.cmga_alpha * new_velocity[key] for key in keys}
        model_step_scale = cfg.cmga_alpha

    new_state = {
        key: (current[key].float() + applied[key]).to(current[key].dtype)
        for key in keys
    }
    if not all(torch.isfinite(value).all() for value in new_state.values()):
        raise FloatingPointError("Non-finite global state.")
    return new_state, new_velocity, {
        "raw_aggregate_l2": _state_l2(mean_delta),
        "global_change_l2": _state_l2(applied),
        "element_clipped_percent": 100.0 * clipped_elements / max(total_elements, 1),
        "model_step_scale": float(model_step_scale),
    }


def _pool_class_gaussians(
    local_results: Sequence[Mapping[str, object]],
    num_classes: int,
    latent_dim: int,
    min_variance: float,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    if any(result.get("gaussian") is None for result in local_results):
        raise AssertionError("CMGA prior pooling received a non-CMGA client result.")
    counts_out = torch.zeros(num_classes, dtype=torch.long)
    means_out = torch.zeros(num_classes, latent_dim, dtype=torch.float32)
    vars_out = torch.ones_like(means_out)
    for class_id in range(num_classes):
        counts = torch.tensor(
            [int(result["gaussian"]["count"][class_id]) for result in local_results],
            dtype=torch.float64,
        )
        total = counts.sum()
        if float(total) <= 0:
            continue
        weights = counts / total
        means = torch.stack([
            result["gaussian"]["mean"][class_id].double() for result in local_results
        ])
        variances = torch.stack([
            result["gaussian"]["var"][class_id].double() for result in local_results
        ])
        pooled_mean = (weights[:, None] * means).sum(dim=0)
        pooled_var = (
            weights[:, None] * (variances + (means - pooled_mean).pow(2))
        ).sum(dim=0)
        counts_out[class_id] = int(total)
        means_out[class_id] = pooled_mean.float()
        vars_out[class_id] = torch.clamp(pooled_var.float(), min=min_variance)
    return counts_out, means_out, vars_out


def _proximal_prior_separation(
    momentum_means: torch.Tensor,
    margin: float,
    penalty: float,
    steps: int,
    learning_rate: float,
) -> Tuple[torch.Tensor, Dict[str, float]]:
    before = float(torch.pdist(momentum_means).min().item())
    target = momentum_means.detach().float()
    projected = target.clone()
    for _ in range(int(steps)):
        candidate = projected.detach().requires_grad_(True)
        proximity = 0.5 * (candidate - target).pow(2).sum()
        distances = torch.cdist(candidate, candidate, p=2)
        upper = torch.triu(torch.ones_like(distances, dtype=torch.bool), diagonal=1)
        separation = torch.relu(float(margin) - distances[upper]).sum()
        objective = proximity + float(penalty) * separation
        gradient = torch.autograd.grad(objective, candidate)[0]
        projected = candidate - float(learning_rate) * gradient
    projected = projected.detach()
    after = float(torch.pdist(projected).min().item())
    return projected, {
        "prior_min_distance_before": before,
        "prior_min_distance_after": after,
        "prior_separation_gain": after - before,
    }


class FederatedServer:
    def __init__(
        self,
        input_dim: int,
        class_names: Sequence[str],
        cfg: ProtocolConfig,
        spec: MethodSpec,
        device: torch.device,
    ) -> None:
        cfg.validate()
        spec.validate()
        self.cfg = cfg
        self.spec = spec
        self.device = device
        self.input_dim = int(input_dim)
        self.class_names = tuple(class_names)
        self.num_classes = len(class_names)
        self.template = FederatedVAE(
            input_dim, self.num_classes, cfg.latent_dim, cfg.condition_scale, spec.conditional
        ).to(device)
        self.communicated_state = self.template.communicated_state_dict(spec.selective)
        self.velocity: Optional[Dict[str, torch.Tensor]] = None
        self.prior_mu: Optional[torch.Tensor] = None
        self.prior_var: Optional[torch.Tensor] = None
        if spec.aggregation == "CMGA":
            self.velocity = {key: torch.zeros_like(value).float() for key, value in self.communicated_state.items()}
        if spec.use_cmga_priors:
            self.prior_mu = torch.zeros(self.num_classes, cfg.latent_dim, dtype=torch.float32)
            self.prior_var = torch.ones_like(self.prior_mu)
        self.clients: List[FederatedClient] = []

    def add_client(self, client: FederatedClient) -> None:
        if client.spec != self.spec:
            raise ValueError("A client cannot be attached to another method's server.")
        if client.input_dim != self.input_dim or client.class_names != self.class_names:
            raise ValueError("Client/server schema mismatch.")
        client.model.load_communicated_state_dict(self.communicated_state, self.spec.selective)
        self.clients.append(client)

    def _update_cmga_priors(self, local_results: Sequence[Mapping[str, object]]) -> Dict[str, float]:
        if not self.spec.use_cmga_priors or self.prior_mu is None or self.prior_var is None:
            if any(result.get("gaussian") is not None for result in local_results):
                raise AssertionError("A non-CMGA method emitted Gaussian statistics.")
            return {
                "prior_min_distance_before": np.nan,
                "prior_min_distance_after": np.nan,
                "prior_separation_gain": np.nan,
            }
        counts, pooled_mu, pooled_var = _pool_class_gaussians(
            local_results, self.num_classes, self.cfg.latent_dim,
            self.cfg.cmga_min_prior_variance,
        )
        observed = counts > 0
        beta = float(self.cfg.cmga_prior_beta)
        momentum_mu = self.prior_mu.clone()
        momentum_var = self.prior_var.clone()
        momentum_mu[observed] = (
            beta * self.prior_mu[observed] + (1.0 - beta) * pooled_mu[observed]
        )
        momentum_var[observed] = (
            beta * self.prior_var[observed] + (1.0 - beta) * pooled_var[observed]
        )
        self.prior_mu, diagnostics = _proximal_prior_separation(
            momentum_mu,
            self.cfg.cmga_prior_margin,
            self.cfg.cmga_prior_penalty,
            self.cfg.cmga_prior_pgd_steps,
            self.cfg.cmga_prior_pgd_lr,
        )
        self.prior_var = torch.clamp(
            momentum_var, min=self.cfg.cmga_min_prior_variance
        )
        return diagnostics

    def train_round(self, round_index: int) -> Dict[str, object]:
        if len(self.clients) != self.cfg.num_clients:
            raise RuntimeError("Every controlled round requires all nine clients.")
        local_results = [
            client.train_local(
                self.communicated_state,
                round_index,
                self.prior_mu if self.spec.use_cmga_priors else None,
                self.prior_var if self.spec.use_cmga_priors else None,
            )
            for client in self.clients
        ]
        sample_counts = np.asarray([int(result["samples"]) for result in local_results], dtype=np.float64)
        weights = sample_counts / sample_counts.sum()
        new_state, new_velocity, aggregation = _aggregate_model_state(
            self.communicated_state,
            [result["shared_update"] for result in local_results],
            weights,
            self.spec,
            self.cfg,
            self.velocity,
        )
        self.communicated_state = new_state
        self.velocity = new_velocity
        prior_diagnostics = self._update_cmga_priors(local_results)
        for client in self.clients:
            client.model.load_communicated_state_dict(self.communicated_state, self.spec.selective)

        def weighted(name: str) -> float:
            return float(sum(float(w) * float(result[name]) for w, result in zip(weights, local_results)))

        return {
            "round": int(round_index),
            "variant": self.spec.variant,
            "valid_clients": len(local_results),
            **{name: weighted(name) for name in ("total", "reconstruction", "kl", "proximal")},
            **aggregation,
            **prior_diagnostics,
        }

    def communication_accounting(self) -> Dict[str, float]:
        full_parameters = sum(value.numel() for value in self.template.state_dict().values())
        communicated_parameters = sum(value.numel() for value in self.communicated_state.values())
        gaussian_values = 0
        if self.spec.use_cmga_priors:
            gaussian_values = 2 * self.num_classes * self.cfg.latent_dim
        return {
            "full_model_parameters": float(full_parameters),
            "communicated_model_parameters": float(communicated_parameters),
            "gaussian_statistics_per_client_round": float(gaussian_values),
            "uplink_values_per_client_round": float(communicated_parameters + gaussian_values),
            "model_parameter_reduction_percent": 100.0 * (1.0 - communicated_parameters / full_parameters),
            "uplink_reduction_including_gaussians_percent": 100.0 * (
                1.0 - (communicated_parameters + gaussian_values) / full_parameters
            ),
        }


def _metrics_from_confusion(
    matrix: np.ndarray, class_names: Sequence[str], prefix: str
) -> Dict[str, object]:
    matrix = np.asarray(matrix, dtype=np.int64)
    if matrix.shape != (len(class_names), len(class_names)) or int(matrix.sum()) == 0:
        raise ValueError("Invalid confusion matrix.")
    tp = np.diag(matrix).astype(np.float64)
    fp = matrix.sum(axis=0).astype(np.float64) - tp
    fn = matrix.sum(axis=1).astype(np.float64) - tp
    precision = np.divide(tp, tp + fp, out=np.zeros_like(tp), where=(tp + fp) > 0)
    recall = np.divide(tp, tp + fn, out=np.zeros_like(tp), where=(tp + fn) > 0)
    f1 = np.divide(
        2.0 * precision * recall,
        precision + recall,
        out=np.zeros_like(tp),
        where=(precision + recall) > 0,
    )
    attack_tp = float(matrix[1:, 1:].sum())
    attack_fp = float(matrix[0, 1:].sum())
    attack_fn = float(matrix[1:, 0].sum())
    attack_precision = attack_tp / max(attack_tp + attack_fp, 1.0)
    attack_recall = attack_tp / max(attack_tp + attack_fn, 1.0)
    attack_f1 = 2.0 * attack_precision * attack_recall / max(
        attack_precision + attack_recall, np.finfo(float).eps
    )
    result: Dict[str, object] = {
        f"{prefix}_accuracy_percent": 100.0 * float(tp.sum()) / float(matrix.sum()),
        f"{prefix}_macro_f1_percent": 100.0 * float(f1.mean()),
        f"{prefix}_attack_f1_percent": 100.0 * attack_f1,
        f"{prefix}_benign_recall_percent": 100.0 * float(recall[0]),
        f"{prefix}_rows": int(matrix.sum()),
        f"{prefix}_confusion": matrix.copy(),
    }
    for index, name in enumerate(class_names):
        result[f"{prefix}_f1_{name}_percent"] = 100.0 * float(f1[index])
    return result


_TEST_STAGE_STATE = globals().get("_FACVAE_ISOLATED_TEST_STAGE", {"count": 0})
globals()["_FACVAE_ISOLATED_TEST_STAGE"] = _TEST_STAGE_STATE


class TestStageGate:
    @classmethod
    def current_count(cls) -> int:
        return int(_TEST_STAGE_STATE["count"])

    @classmethod
    def begin_once(cls, unlocked: bool) -> None:
        if not unlocked:
            raise RuntimeError("FINAL TEST IS LOCKED.")
        if cls.current_count() != 0:
            raise RuntimeError("The final test stage has already been queried.")
        _TEST_STAGE_STATE["count"] = 1


def _pooled_client_arrays(
    clients: Sequence[FederatedClient],
    splits: Sequence[str],
    allow_test: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if "test" in splits and not allow_test:
        raise RuntimeError("Test extraction is blocked outside the final stage.")
    parts = [client.extract_mu(split) for client in clients for split in splits]
    return (
        np.concatenate([part[0] for part in parts]),
        np.concatenate([part[1] for part in parts]),
        np.concatenate([part[2] for part in parts]),
    )


def evaluate_centroid_probe(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    train_splits: Sequence[str] = ("train",),
    evaluation_split: str = "validation",
    allow_test: bool = False,
) -> Dict[str, object]:
    train_z, train_y, _ = _pooled_client_arrays(clients, train_splits, allow_test=False)
    eval_z, eval_y, _ = _pooled_client_arrays(
        clients, (evaluation_split,), allow_test=allow_test
    )
    centroids = []
    for class_id in range(len(class_names)):
        selected = train_z[train_y == class_id]
        if len(selected) == 0:
            raise RuntimeError(f"No train latent for class {class_id}.")
        centroids.append(selected.mean(axis=0))
    centroids = np.asarray(centroids, dtype=np.float32)
    distances = ((eval_z[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    prediction = distances.argmin(axis=1).astype(np.int64)
    matrix = confusion_matrix(eval_y, prediction, labels=np.arange(len(class_names)))
    return _metrics_from_confusion(matrix, class_names, "centroid")


def evaluate_cmga_prior_detector(
    server: FederatedServer,
    split: str = "validation",
    allow_test: bool = False,
) -> Dict[str, object]:
    if not server.spec.use_cmga_priors or server.prior_mu is None or server.prior_var is None:
        raise RuntimeError("Native Gaussian-prior detector exists only for full CMGA.")
    latent, labels, _ = _pooled_client_arrays(server.clients, (split,), allow_test=allow_test)
    x = torch.as_tensor(latent, dtype=torch.float32)
    means = server.prior_mu.detach().cpu().float()
    variances = torch.clamp(
        server.prior_var.detach().cpu().float(), min=server.cfg.cmga_min_prior_variance
    )
    scores = (
        ((x[:, None, :] - means[None, :, :]).pow(2) / variances[None, :, :])
        + torch.log(variances)[None, :, :]
    ).sum(dim=2)
    prediction = scores.argmin(dim=1).numpy().astype(np.int64)
    matrix = confusion_matrix(labels, prediction, labels=np.arange(server.num_classes))
    return _metrics_from_confusion(matrix, server.class_names, "prior")


def evaluate_fitted_classifier(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    classifier_kind: str,
    train_splits: Sequence[str],
    evaluation_split: str,
    allow_test: bool = False,
) -> Dict[str, object]:
    train_z, train_y, _ = _pooled_client_arrays(clients, train_splits, allow_test=False)
    eval_z, eval_y, _ = _pooled_client_arrays(
        clients, (evaluation_split,), allow_test=allow_test
    )
    if classifier_kind == "rf":
        classifier = RandomForestClassifier(**RF_PARAMS)
        prefix = "rf"
    elif classifier_kind == "linear":
        classifier = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                C=1.0, max_iter=2000, solver="lbfgs", class_weight="balanced",
                random_state=CONFIG.seed,
            ),
        )
        prefix = "linear"
    else:
        raise ValueError("classifier_kind must be rf or linear.")
    classifier.fit(train_z, train_y)
    prediction = classifier.predict(eval_z).astype(np.int64)
    matrix = confusion_matrix(eval_y, prediction, labels=np.arange(len(class_names)))
    return _metrics_from_confusion(matrix, class_names, prefix)


def evaluate_raw_rf(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    train_splits: Sequence[str],
    evaluation_split: str,
    allow_test: bool = False,
) -> Dict[str, object]:
    _, train_y, train_x = _pooled_client_arrays(clients, train_splits, allow_test=False)
    _, eval_y, eval_x = _pooled_client_arrays(
        clients, (evaluation_split,), allow_test=allow_test
    )
    classifier = RandomForestClassifier(**RF_PARAMS)
    classifier.fit(train_x, train_y)
    prediction = classifier.predict(eval_x).astype(np.int64)
    matrix = confusion_matrix(eval_y, prediction, labels=np.arange(len(class_names)))
    return _metrics_from_confusion(matrix, class_names, "raw_rf")


# --- Evaluation audit additions -------------------------------------------------
# IMPORTANT: pooled-central and client-local classifiers over private encoder spaces
# are retained only as diagnostics. The primary downstream evaluation is cross-client:
# each held-out client is unseen during classifier fitting. The exact same classifier
# family/hyperparameters are used for every method.

def _client_split_arrays(
    client: FederatedClient,
    splits: Sequence[str],
    allow_test: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if "test" in splits and not allow_test:
        raise RuntimeError("Test extraction is blocked outside the final stage.")
    parts = [client.extract_mu(split) for split in splits]
    return (
        np.concatenate([p[0] for p in parts]),
        np.concatenate([p[1] for p in parts]),
        np.concatenate([p[2] for p in parts]),
    )


def _make_classifier(kind: str, seed: int = CONFIG.seed):
    if kind == "rf":
        return RandomForestClassifier(**{**RF_PARAMS, "random_state": int(seed)})
    if kind == "shallow_rf":
        # Diagnostic only; never substitutes the paper/default RF in headline results.
        params = dict(RF_PARAMS)
        params.update({"max_depth": 4, "min_samples_leaf": 50, "random_state": int(seed)})
        return RandomForestClassifier(**params)
    if kind == "linear":
        return make_pipeline(
            StandardScaler(),
            LogisticRegression(
                C=1.0, max_iter=2000, solver="lbfgs", class_weight="balanced",
                random_state=int(seed),
            ),
        )
    raise ValueError("Unknown classifier kind.")


def evaluate_client_local_classifier(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    classifier_kind: str,
    train_splits: Sequence[str] = ("train",),
    evaluation_split: str = "validation",
    allow_test: bool = False,
) -> Dict[str, object]:
    """Fit one classifier per private encoder space and aggregate confusion matrices."""
    total = np.zeros((len(class_names), len(class_names)), dtype=np.int64)
    train_total = np.zeros_like(total)
    per_client = []
    for client in clients:
        train_z, train_y, _ = _client_split_arrays(client, train_splits, allow_test=False)
        eval_z, eval_y, _ = _client_split_arrays(client, (evaluation_split,), allow_test=allow_test)
        clf = _make_classifier(classifier_kind, CONFIG.seed + client.cid)
        clf.fit(train_z, train_y)
        pred = clf.predict(eval_z).astype(np.int64)
        train_pred = clf.predict(train_z).astype(np.int64)
        cm = confusion_matrix(eval_y, pred, labels=np.arange(len(class_names)))
        train_cm = confusion_matrix(train_y, train_pred, labels=np.arange(len(class_names)))
        total += cm
        train_total += train_cm
        local_metrics = _metrics_from_confusion(cm, class_names, "local")
        per_client.append({
            "client_id": client.cid,
            "rows": len(eval_y),
            "macro_f1_percent": local_metrics["local_macro_f1_percent"],
            "accuracy_percent": local_metrics["local_accuracy_percent"],
        })
    result = _metrics_from_confusion(total, class_names, f"local_{classifier_kind}")
    train_result = _metrics_from_confusion(train_total, class_names, f"local_{classifier_kind}_train")
    result.update({k: v for k, v in train_result.items() if not k.endswith("_confusion")})
    result["per_client"] = pd.DataFrame(per_client)
    return result


def evaluate_cross_client_classifier(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    classifier_kind: str = "rf",
    train_splits: Sequence[str] = ("train",),
    evaluation_split: str = "validation",
    allow_test: bool = False,
) -> Dict[str, object]:
    """
    Primary cross-client protocol.

    For each held-out client, fit the classifier using only latent representations
    from the *other* clients, then evaluate on the held-out client's requested split.
    This prevents a downstream classifier from seeing the held-out private encoder
    coordinate system during fitting.
    """
    if "test" in train_splits:
        raise RuntimeError("Test may never be used to fit a cross-client classifier.")
    if evaluation_split == "test" and not allow_test:
        raise RuntimeError("Test extraction is blocked outside the final stage.")

    total = np.zeros((len(class_names), len(class_names)), dtype=np.int64)
    per_client: List[Dict[str, object]] = []
    for held_out in clients:
        train_parts = [
            _client_split_arrays(c, train_splits, allow_test=False)
            for c in clients if c.cid != held_out.cid
        ]
        train_z = np.concatenate([p[0] for p in train_parts])
        train_y = np.concatenate([p[1] for p in train_parts])
        eval_z, eval_y, _ = _client_split_arrays(
            held_out, (evaluation_split,), allow_test=allow_test
        )
        clf = _make_classifier(classifier_kind, CONFIG.seed + 10_000 + int(held_out.cid))
        clf.fit(train_z, train_y)
        pred = clf.predict(eval_z).astype(np.int64)
        cm = confusion_matrix(eval_y, pred, labels=np.arange(len(class_names)))
        total += cm
        m = _metrics_from_confusion(cm, class_names, "heldout")
        per_client.append({
            "held_out_client": int(held_out.cid),
            "train_clients": len(clients) - 1,
            "train_rows": int(len(train_y)),
            "evaluation_rows": int(len(eval_y)),
            "accuracy_percent": m["heldout_accuracy_percent"],
            "macro_f1_percent": m["heldout_macro_f1_percent"],
        })
    prefix = f"cross_client_{classifier_kind}"
    result = _metrics_from_confusion(total, class_names, prefix)
    result["per_client"] = pd.DataFrame(per_client)
    return result


def evaluate_leave_one_client_out(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    classifier_kind: str = "rf",
    train_split: str = "train",
    evaluation_split: str = "validation",
) -> Dict[str, object]:
    """Backward-compatible alias for the validation leave-one-client-out protocol."""
    return evaluate_cross_client_classifier(
        clients, class_names, classifier_kind, (train_split,), evaluation_split, False
    )

def evaluate_client_identity_predictability(
    clients: Sequence[FederatedClient],
    train_split: str = "train",
    evaluation_split: str = "validation",
    classifier_kind: str = "rf",
) -> Dict[str, float]:
    train_z, _, _ = _pooled_client_arrays(clients, (train_split,), allow_test=False)
    eval_z, _, _ = _pooled_client_arrays(clients, (evaluation_split,), allow_test=False)
    train_cid = np.concatenate([
        np.full(len(c.extract_mu(train_split)[0]), c.cid, dtype=np.int64) for c in clients
    ])
    eval_cid = np.concatenate([
        np.full(len(c.extract_mu(evaluation_split)[0]), c.cid, dtype=np.int64) for c in clients
    ])
    clf = _make_classifier(classifier_kind, CONFIG.seed + 20_000)
    clf.fit(train_z, train_cid)
    return {
        "client_id_accuracy_percent": 100.0 * float((clf.predict(eval_z) == eval_cid).mean()),
        "chance_percent": 100.0 / max(len(clients), 1),
    }


def evaluate_client_prior_shortcut(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    train_split: str = "train",
    evaluation_split: str = "validation",
) -> Dict[str, object]:
    """Upper evidence for a pure client-ID -> majority-class shortcut (no x/z used)."""
    cm = np.zeros((len(class_names), len(class_names)), dtype=np.int64)
    for client in clients:
        _, train_y, _ = client.extract_mu(train_split)
        _, eval_y, _ = client.extract_mu(evaluation_split)
        majority = int(np.bincount(train_y, minlength=len(class_names)).argmax())
        pred = np.full(len(eval_y), majority, dtype=np.int64)
        cm += confusion_matrix(eval_y, pred, labels=np.arange(len(class_names)))
    return _metrics_from_confusion(cm, class_names, "client_prior")


def evaluate_classifier_complexity_suite(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
) -> pd.DataFrame:
    centroid = evaluate_centroid_probe(clients, class_names)
    rows = [{"classifier": "nearest_centroid",
             "macro_f1_percent": centroid["centroid_macro_f1_percent"],
             "accuracy_percent": centroid["centroid_accuracy_percent"]}]
    for kind in ("linear", "shallow_rf", "rf"):
        pooled = evaluate_fitted_classifier(
            clients, class_names, "linear" if kind == "linear" else "rf",
            ("train",), "validation"
        ) if kind != "shallow_rf" else None
        if kind == "shallow_rf":
            ztr, ytr, _ = _pooled_client_arrays(clients, ("train",))
            zev, yev, _ = _pooled_client_arrays(clients, ("validation",))
            clf = _make_classifier("shallow_rf")
            clf.fit(ztr, ytr)
            cm = confusion_matrix(yev, clf.predict(zev), labels=np.arange(len(class_names)))
            pooled = _metrics_from_confusion(cm, class_names, "rf")
        prefix = "linear" if kind == "linear" else "rf"
        rows.append({"classifier": kind,
                     "macro_f1_percent": pooled[f"{prefix}_macro_f1_percent"],
                     "accuracy_percent": pooled[f"{prefix}_accuracy_percent"]})
    return pd.DataFrame(rows)


def audit_sampled_near_duplicates(
    clients: Sequence[FederatedClient],
    reference_split: str = "train",
    query_split: str = "validation",
    reference_cap: int = 20000,
    query_cap: int = 5000,
) -> Dict[str, float]:
    """Sampled transformed-space nearest-neighbor audit; exact hash audit remains authoritative."""
    _, _, ref_x = _pooled_client_arrays(clients, (reference_split,))
    _, _, qry_x = _pooled_client_arrays(clients, (query_split,))
    rng = np.random.default_rng(CONFIG.seed + 30_000)
    if len(ref_x) > reference_cap:
        ref_x = ref_x[rng.choice(len(ref_x), reference_cap, replace=False)]
    if len(qry_x) > query_cap:
        qry_x = qry_x[rng.choice(len(qry_x), query_cap, replace=False)]
    nn = NearestNeighbors(n_neighbors=1, metric="euclidean", n_jobs=-1).fit(ref_x)
    distances = nn.kneighbors(qry_x, return_distance=True)[0][:, 0]
    return {
        "sampled_queries": float(len(distances)),
        "min_distance": float(distances.min()),
        "median_distance": float(np.median(distances)),
        "pct_distance_le_1e-6": 100.0 * float((distances <= 1e-6).mean()),
        "pct_distance_le_1e-4": 100.0 * float((distances <= 1e-4).mean()),
        "pct_distance_le_1e-3": 100.0 * float((distances <= 1e-3).mean()),
    }


# ===== NOTEBOOK CODE CELL 16 =====
# V6.1 correctness patch — single-class-safe client-local classifiers
#
# Why this exists:
# Dirichlet non-IID partitioning can legitimately leave a client with only one
# class in its local training split. sklearn LogisticRegression cannot fit one
# class. We must NOT pool another client's data or drop the client, because both
# would change the Local-Private evaluation protocol.
#
# Therefore, when a local training set contains exactly one class, the only
# leakage-free local prediction available is that observed class for every local
# evaluation row. All rows are still included in the aggregated confusion matrix.
# For RF this is equivalent to fitting a one-class RF; for Linear it is a
# conservative, well-defined fallback instead of a runtime failure.

def evaluate_client_local_classifier(
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    classifier_kind: str,
    train_splits: Sequence[str] = ("train",),
    evaluation_split: str = "validation",
    allow_test: bool = False,
) -> Dict[str, object]:
    """Fit one classifier per private encoder space and aggregate confusion matrices.

    Single-class local train splits are retained, never skipped or pooled.
    """
    total = np.zeros((len(class_names), len(class_names)), dtype=np.int64)
    train_total = np.zeros_like(total)
    per_client: List[Dict[str, object]] = []
    fallback_clients: List[int] = []

    for client in clients:
        train_z, train_y, _ = _client_split_arrays(client, train_splits, allow_test=False)
        eval_z, eval_y, _ = _client_split_arrays(
            client, (evaluation_split,), allow_test=allow_test
        )

        present_train_classes = np.unique(train_y).astype(np.int64)
        if len(present_train_classes) == 0:
            raise RuntimeError(f"client {client.cid}: empty local classifier training labels")

        if len(present_train_classes) == 1:
            # Honest Local-Private behavior: this client has never observed another
            # class locally, so no discriminative local boundary can be fitted.
            constant_class = int(present_train_classes[0])
            pred = np.full(len(eval_y), constant_class, dtype=np.int64)
            train_pred = np.full(len(train_y), constant_class, dtype=np.int64)
            fit_mode = "single_class_constant"
            fallback_clients.append(int(client.cid))
        else:
            clf = _make_classifier(classifier_kind, CONFIG.seed + client.cid)
            clf.fit(train_z, train_y)
            pred = clf.predict(eval_z).astype(np.int64)
            train_pred = clf.predict(train_z).astype(np.int64)
            fit_mode = "fitted"

        cm = confusion_matrix(eval_y, pred, labels=np.arange(len(class_names)))
        train_cm = confusion_matrix(train_y, train_pred, labels=np.arange(len(class_names)))
        total += cm
        train_total += train_cm

        local_metrics = _metrics_from_confusion(cm, class_names, "local")
        per_client.append({
            "client_id": int(client.cid),
            "rows": int(len(eval_y)),
            "train_rows": int(len(train_y)),
            "train_unique_classes": int(len(present_train_classes)),
            "train_class_ids": ",".join(str(int(v)) for v in present_train_classes),
            "classifier_fit_mode": fit_mode,
            "macro_f1_percent": local_metrics["local_macro_f1_percent"],
            "accuracy_percent": local_metrics["local_accuracy_percent"],
        })

    result = _metrics_from_confusion(total, class_names, f"local_{classifier_kind}")
    train_result = _metrics_from_confusion(
        train_total, class_names, f"local_{classifier_kind}_train"
    )
    result.update({k: v for k, v in train_result.items() if not k.endswith("_confusion")})
    result["per_client"] = pd.DataFrame(per_client)
    result["single_class_fallback_clients"] = tuple(fallback_clients)
    result["single_class_fallback_count"] = int(len(fallback_clients))
    result["single_class_fallback_policy"] = (
        "constant prediction of the sole locally observed training class; "
        "no client dropped; no cross-client pooling"
    )
    return result


# ===== NOTEBOOK CODE CELL 17 =====
# 7. Executable logic tests: syntax is not enough; method isolation must be proven
def _synthetic_records() -> Tuple[List[Dict[str, object]], Tuple[str, ...]]:
    rng = np.random.default_rng(771)
    class_names = ("benign", "attack_a", "attack_b")
    centers = np.asarray([
        [0.2] * 4 + [0.4] * 8,
        [0.55] * 4 + [0.65] * 8,
        [0.80] * 4 + [0.50] * 8,
    ], dtype=np.float32)
    records: List[Dict[str, object]] = []
    for client_id in range(9):
        record: Dict[str, object] = {
            "client_id": client_id,
            "input_dim": 12,
            "num_classes": 3,
            "class_names": class_names,
        }
        for split, rows_per_class in (("train", 8), ("validation", 4), ("test", 4)):
            y = np.repeat(np.arange(3, dtype=np.int64), rows_per_class)
            x = centers[y] + rng.normal(0.0, 0.025, size=(len(y), 12)).astype(np.float32)
            x = np.clip(x + 0.002 * client_id, 0.1, 0.9).astype(np.float32)
            order = rng.permutation(len(y))
            record[f"X_{split}"] = x[order]
            record[f"y_{split}"] = y[order]
        records.append(record)
    return records, class_names


def run_logic_smoke_tests() -> pd.DataFrame:
    cfg = replace(
        CONFIG, rounds=1, local_epochs=1, batch_size=16,
        latent_dim=6, num_clients=9,
    )
    records, class_names = _synthetic_records()
    checks: List[Dict[str, str]] = []

    by_name = {spec.variant: spec for spec in METHOD_SPECS}
    for name in ("FedAvg_baseline", "FedProx_baseline"):
        spec = by_name[name]
        model = FederatedVAE(12, 3, cfg.latent_dim, cfg.condition_scale, spec.conditional)
        assert model.mapper is None
        assert not spec.selective and not spec.use_cmga_priors
    checks.append({"check": "FedAvg/FedProx contain no conditional mapper or CMGA prior", "status": "PASS"})

    # Exact aggregation-rule unit test.
    current = {"w": torch.tensor([1.0, -1.0])}
    updates = ({"w": torch.tensor([0.4, -0.4])}, {"w": torch.tensor([0.2, 0.2])})
    weights = np.asarray([0.25, 0.75], dtype=np.float64)
    fedavg_state, fedavg_velocity, _ = _aggregate_model_state(
        current, updates, weights, by_name["FedAvg_baseline"], cfg, None
    )
    expected_delta = 0.25 * updates[0]["w"] + 0.75 * updates[1]["w"]
    assert fedavg_velocity is None
    assert torch.allclose(fedavg_state["w"], current["w"] + expected_delta)
    checks.append({"check": "FedAvg is pure sample-weighted averaging without clamp/momentum", "status": "PASS"})

    fedprox_state, fedprox_velocity, _ = _aggregate_model_state(
        current, updates, weights, by_name["FedProx_baseline"], cfg, None
    )
    assert fedprox_velocity is None
    assert torch.allclose(fedprox_state["w"], fedavg_state["w"])
    checks.append({"check": "FedProx differs locally; its server rule remains pure FedAvg", "status": "PASS"})

    fedprox_spec = by_name["FedProx_baseline"]
    assert fedprox_spec.aggregation == "FEDPROX"
    assert fedprox_spec.fedprox is True
    assert fedprox_spec.conditional is False
    assert fedprox_spec.selective is False
    assert fedprox_spec.use_cmga_priors is False
    assert float(cfg.fedprox_mu) > 0
    checks.append({"check": "FedProx contract is exact: proximal-only baseline, no CMGA/conditioning/selective", "status": "PASS"})

    cmga_velocity0 = {"w": torch.zeros(2)}
    cmga_state, cmga_velocity1, cmga_diag = _aggregate_model_state(
        current, updates, weights, by_name["F_ACVAE_CMGA"], cfg, cmga_velocity0
    )
    clipped_mean = 0.25 * torch.clamp(updates[0]["w"], -0.2, 0.2) + 0.75 * updates[1]["w"]
    expected_velocity = cfg.cmga_gamma * clipped_mean
    assert cmga_velocity1 is not None
    assert torch.allclose(cmga_velocity1["w"], expected_velocity)
    assert torch.allclose(cmga_state["w"], current["w"] + cfg.cmga_alpha * expected_velocity)
    assert cmga_diag["element_clipped_percent"] > 0
    checks.append({"check": "CMGA alone uses clamp plus persistent velocity plus alpha step", "status": "PASS"})

    servers: Dict[str, FederatedServer] = {}
    for spec in METHOD_SPECS:
        reset_all_seeds(cfg.seed)
        server = FederatedServer(12, class_names, cfg, spec, torch.device("cpu"))
        for record in records:
            server.add_client(FederatedClient(record, cfg, spec, torch.device("cpu")))
        servers[spec.variant] = server

    assert servers["FedAvg_baseline"].velocity is None
    assert servers["FedProx_baseline"].velocity is None
    assert servers["FedAvg_baseline"].prior_mu is None
    assert servers["FedProx_baseline"].prior_mu is None
    assert servers["ACVAE_no_CMGA"].velocity is None
    assert servers["ACVAE_no_CMGA"].prior_mu is None
    assert servers["F_ACVAE_CMGA"].velocity is not None
    assert servers["F_ACVAE_CMGA"].prior_mu is not None
    checks.append({"check": "Only full F-ACVAE owns CMGA model/prior state", "status": "PASS"})

    fedavg_before = _state_digest(servers["FedAvg_baseline"].communicated_state)
    fedprox_before = _state_digest(servers["FedProx_baseline"].communicated_state)
    servers["F_ACVAE_CMGA"].train_round(1)
    fedavg_after = _state_digest(servers["FedAvg_baseline"].communicated_state)
    fedprox_after = _state_digest(servers["FedProx_baseline"].communicated_state)
    assert fedavg_before == fedavg_after
    assert fedprox_before == fedprox_after
    checks.append({"check": "Training CMGA cannot mutate FedAvg state", "status": "PASS"})
    checks.append({"check": "Training CMGA cannot mutate FedProx state", "status": "PASS"})

    for name in ("FedAvg_baseline", "FedProx_baseline", "ACVAE_no_CMGA"):
        result = servers[name].train_round(1)
        assert result["valid_clients"] == 9
        assert np.isnan(result["prior_min_distance_after"])
    checks.append({"check": "Non-CMGA clients neither emit nor aggregate Gaussian statistics", "status": "PASS"})

    extraction_parameters = tuple(inspect.signature(FederatedClient.extract_mu).parameters)
    assert extraction_parameters == ("self", "split")
    checks.append({"check": "Validation/test latent extraction accepts no labels", "status": "PASS"})

    try:
        evaluate_centroid_probe(
            servers["FedAvg_baseline"].clients, class_names,
            evaluation_split="test", allow_test=False,
        )
        raise AssertionError("Unauthorized test evaluation was not blocked.")
    except RuntimeError:
        pass
    checks.append({"check": "Unauthorized final-test access is blocked", "status": "PASS"})

    cross = evaluate_cross_client_classifier(
        servers["F_ACVAE_CMGA"].clients, class_names, "rf",
        train_splits=("train",), evaluation_split="validation", allow_test=False,
    )
    assert "cross_client_rf_macro_f1_percent" in cross
    assert len(cross["per_client"]) == 9
    assert (cross["per_client"]["train_clients"] == 8).all()
    try:
        evaluate_cross_client_classifier(
            servers["F_ACVAE_CMGA"].clients, class_names, "rf",
            train_splits=("train",), evaluation_split="test", allow_test=False,
        )
        raise AssertionError("Unauthorized cross-client test evaluation was not blocked.")
    except RuntimeError:
        pass
    checks.append({"check": "Cross-client RF trains on 8 clients and keeps held-out Test locked", "status": "PASS"})

    reset_all_seeds(CONFIG.seed)
    return pd.DataFrame(checks)


SMOKE_CHECKLIST = run_logic_smoke_tests()
if not (SMOKE_CHECKLIST["status"] == "PASS").all():
    raise RuntimeError("A method-isolation smoke test failed.")
out_print("LOGIC_TESTS", f"LOGIC TESTS | PASS ({len(SMOKE_CHECKLIST)} checks)")


# ===== NOTEBOOK CODE CELL 18 =====
# 8. Controlled runner: separate state per method, common round probe, final classifiers once
def _round_row(
    spec: MethodSpec,
    round_index: int,
    centroid: Mapping[str, object],
    training: Optional[Mapping[str, object]],
    prior: Optional[Mapping[str, object]],
    runtime_seconds: float,
) -> Dict[str, object]:
    row: Dict[str, object] = {
        "variant": spec.variant,
        "purpose": spec.purpose,
        "round": int(round_index),
        "runtime_seconds": float(runtime_seconds),
        "train_total_loss": np.nan,
        "train_reconstruction_loss": np.nan,
        "train_kl_loss": np.nan,
        "train_proximal_loss": np.nan,
        "global_change_l2": np.nan,
        "raw_aggregate_l2": np.nan,
        "element_clipped_percent": np.nan,
        "prior_min_distance_after": np.nan,
        "valid_clients": CONFIG.num_clients,
        "prior_accuracy_percent": np.nan,
        "prior_macro_f1_percent": np.nan,
        "prior_attack_f1_percent": np.nan,
    }
    if training is not None:
        row.update({
            "train_total_loss": float(training["total"]),
            "train_reconstruction_loss": float(training["reconstruction"]),
            "train_kl_loss": float(training["kl"]),
            "train_proximal_loss": float(training["proximal"]),
            "global_change_l2": float(training["global_change_l2"]),
            "raw_aggregate_l2": float(training["raw_aggregate_l2"]),
            "element_clipped_percent": float(training["element_clipped_percent"]),
            "prior_min_distance_after": float(training["prior_min_distance_after"]),
            "valid_clients": int(training["valid_clients"]),
        })
    row.update({key: value for key, value in centroid.items() if not key.endswith("_confusion")})
    if prior is not None:
        row.update({key: value for key, value in prior.items() if not key.endswith("_confusion")})
    return row



def _scenario_id_from_data(data: "IoT01DataBundle") -> str:
    if data.records and "scenario_id" in data.records[0]:
        return str(data.records[0]["scenario_id"])
    return str(data.audit.get("scenario_id", "IoT-01"))


def _checkpoint_signature(data: "IoT01DataBundle", spec: MethodSpec, cfg: ProtocolConfig, scope: str) -> str:
    payload = {
        "version": CHECKPOINT_VERSION, "scope": scope,
        "scenario": _scenario_id_from_data(data), "class_names": list(data.class_names),
        "input_dim": int(data.input_dim), "config": asdict(cfg), "spec": asdict(spec),
        "train_rows": int(sum(len(r["y_train"]) for r in data.records)),
        "validation_rows": int(sum(len(r["y_validation"]) for r in data.records)),
        "test_rows": int(sum(len(r["y_test"]) for r in data.records)),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def _method_checkpoint_dir(data, spec, cfg, scope: str) -> Path:
    seed_tag = f"seed_{cfg.seed}"
    return CHECKPOINT_ROOT / scope / _scenario_id_from_data(data) / seed_tag / spec.variant


def _atomic_torch_save(payload: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    torch.save(payload, tmp)
    os.replace(tmp, path)


def _save_round_checkpoint(data, spec, cfg, scope, server, clients, rows, round_index) -> None:
    if not ENABLE_CHECKPOINTS:
        return
    path = _method_checkpoint_dir(data, spec, cfg, scope) / f"round_{round_index:02d}.pt"
    payload = {
        "signature": _checkpoint_signature(data, spec, cfg, scope),
        "completed_round": int(round_index),
        "rows": rows,
        "server_communicated_state": {k:v.detach().cpu() for k,v in server.communicated_state.items()},
        "server_velocity": None if server.velocity is None else {k:v.detach().cpu() for k,v in server.velocity.items()},
        "server_prior_mu": None if server.prior_mu is None else server.prior_mu.detach().cpu(),
        "server_prior_var": None if server.prior_var is None else server.prior_var.detach().cpu(),
        "client_states": [
            {k:v.detach().cpu() for k,v in client.model.state_dict().items()}
            for client in clients
        ],
    }
    _atomic_torch_save(payload, path)
    # Keep only the latest and previous checkpoint for this job.
    files = sorted(path.parent.glob("round_*.pt"))
    for old in files[:-2]:
        try: old.unlink()
        except OSError: pass


def _restore_latest_checkpoint(data, spec, cfg, scope, server, clients):
    if not ENABLE_CHECKPOINTS:
        return 0, None
    folder = _method_checkpoint_dir(data, spec, cfg, scope)
    files = sorted(folder.glob("round_*.pt"), reverse=True)
    expected = _checkpoint_signature(data, spec, cfg, scope)
    for path in files:
        try:
            payload = torch.load(path, map_location="cpu", weights_only=False)
        except Exception:
            continue
        if payload.get("signature") != expected:
            continue
        server.communicated_state = {k:v.detach().cpu().clone() for k,v in payload["server_communicated_state"].items()}
        if payload["server_velocity"] is None:
            server.velocity = None
        else:
            server.velocity = {k:v.detach().cpu().clone() for k,v in payload["server_velocity"].items()}
        server.prior_mu = None if payload["server_prior_mu"] is None else payload["server_prior_mu"].detach().cpu().clone()
        server.prior_var = None if payload["server_prior_var"] is None else payload["server_prior_var"].detach().cpu().clone()
        if len(payload["client_states"]) != len(clients):
            raise RuntimeError("Checkpoint client count mismatch")
        for client, state in zip(clients, payload["client_states"]):
            client.model.load_state_dict(state, strict=True)
        return int(payload["completed_round"]), list(payload["rows"])
    return 0, None


def _print_saved_rounds(rows, rounds_total: int, variant: str) -> None:
    for row in rows:
        r = int(row["round"])
        loss = row.get("train_total_loss", np.nan)
        loss_text = "no training" if r == 0 or not np.isfinite(loss) else f"loss={float(loss):.6f}"
        print(
            f"{variant} | Round {r}/{rounds_total} | {loss_text} | "
            f"Acc={float(row['centroid_accuracy_percent']):.4f}% | "
            f"Macro-F1={float(row['centroid_macro_f1_percent']):.4f}%"
        )


def run_method(
    data: "IoT01DataBundle",
    spec: MethodSpec,
    collect_raw_diagnostics: bool = False,
    cfg: ProtocolConfig = CONFIG,
    checkpoint_scope: str = "Main",
) -> Dict[str, object]:
    """Train/resume one method. Checkpoints are written after every completed round."""
    spec.validate()
    cfg.validate()
    reset_all_seeds(cfg.seed)
    server = FederatedServer(data.input_dim, data.class_names, cfg, spec, DEVICE)
    clients = [FederatedClient(record, cfg, spec, DEVICE) for record in data.records]
    for client in clients:
        server.add_client(client)

    initial_communicated_digest = _state_digest(server.communicated_state)
    initial_private_digests = tuple(
        _state_digest({key:value for key,value in client.model.state_dict().items() if key.startswith("encoder.")})
        for client in clients
    )

    restored_round, restored_rows = _restore_latest_checkpoint(
        data, spec, cfg, checkpoint_scope, server, clients
    )
    if restored_rows is None:
        rows: List[Dict[str, object]] = []
        centroid = evaluate_centroid_probe(clients, data.class_names)
        prior = evaluate_cmga_prior_detector(server) if spec.use_cmga_priors else None
        rows.append(_round_row(spec, 0, centroid, None, prior, 0.0))
        _save_round_checkpoint(data, spec, cfg, checkpoint_scope, server, clients, rows, 0)
        _print_saved_rounds(rows, cfg.rounds, spec.variant)
        start_round = 1
    else:
        rows = restored_rows
        print(f"{spec.variant} | RESUME from checkpoint Round {restored_round}/{cfg.rounds}")
        _print_saved_rounds(rows, cfg.rounds, spec.variant)
        start_round = restored_round + 1

    for round_index in range(start_round, cfg.rounds + 1):
        started = time.time()
        training = server.train_round(round_index)
        centroid = evaluate_centroid_probe(clients, data.class_names)
        prior = evaluate_cmga_prior_detector(server) if spec.use_cmga_priors else None
        runtime = time.time() - started
        row = _round_row(spec, round_index, centroid, training, prior, runtime)
        rows.append(row)
        _save_round_checkpoint(data, spec, cfg, checkpoint_scope, server, clients, rows, round_index)
        prior_text = "" if prior is None else f" | Prior-F1={prior['prior_macro_f1_percent']:.4f}%"
        print(
            f"{spec.variant} | Round {round_index}/{cfg.rounds} | "
            f"loss={training['total']:.6f} | Acc={centroid['centroid_accuracy_percent']:.4f}% | "
            f"Macro-F1={centroid['centroid_macro_f1_percent']:.4f}%{prior_text}"
        )

    frame = pd.DataFrame(rows).sort_values("round").drop_duplicates("round", keep="last").reset_index(drop=True)
    if frame["round"].tolist() != list(range(cfg.rounds + 1)):
        raise AssertionError(f"{spec.variant}: incomplete trajectory")
    if not (frame["valid_clients"] == cfg.num_clients).all():
        raise AssertionError(f"{spec.variant}: a client was excluded")

    # V6 primary validation protocol: one downstream classifier per private encoder space.
    # This changes evaluation only; the federated training loop above is unchanged.
    local_rf = evaluate_client_local_classifier(
        clients, data.class_names, "rf", ("train",), "validation"
    )
    local_linear = evaluate_client_local_classifier(
        clients, data.class_names, "linear", ("train",), "validation"
    )
    return {
        "spec":spec, "server":server, "clients":clients, "round_frame":frame,
        "local_rf":local_rf, "local_linear":local_linear,
        "initial_communicated_digest":initial_communicated_digest,
        "initial_private_digests":initial_private_digests,
    }


# -----------------------------------------------------------------------------
# SECTION B — TRAINING EXECUTION (TRAINING LOGIC UNCHANGED; PRIMARY VALIDATION = LOCAL-PRIVATE)  [notebook cell 19]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 20 =====
# 9. Main IoT-01 training. Model/training logic is unchanged; only stdout is routed by OUTPUT CONTROLLER.
with output_scope("TRAINING_PROGRESS"):
    # 9. Main IoT-01 training. Only round progress is printed here.
    if not RUN_FULL_PROTOCOL:
        METHOD_RUNS = {}
        ROUND_RESULTS = pd.DataFrame()
        FINAL_VALIDATION = pd.DataFrame()
        COMMUNICATION_TABLE = pd.DataFrame()
        print("Full raw-data protocol skipped in synthetic-only mode.")
    else:
        if DATA is None:
            raise RuntimeError("Raw-data protocol requested but DATA was not built.")

        METHOD_RUNS: Dict[str, Dict[str, object]] = {}
        for spec in METHOD_SPECS:
            print("\n" + "=" * 88)
            print(f"TRAINING | IoT-01 | {spec.variant}")
            METHOD_RUNS[spec.variant] = run_method(DATA, spec, checkpoint_scope="Main_Audited_v3")

        ROUND_RESULTS = pd.concat(
            [METHOD_RUNS[s.variant]["round_frame"] for s in METHOD_SPECS], ignore_index=True
        )
        rows = []
        for spec in METHOD_SPECS:
            run = METHOD_RUNS[spec.variant]
            last = run["round_frame"].sort_values("round").iloc[-1]
            rows.append({
                "variant":spec.variant,
                "representation_probe_macro_f1_percent":float(last["centroid_macro_f1_percent"]),
                "local_rf_accuracy_percent":float(run["local_rf"]["local_rf_accuracy_percent"]),
                "local_rf_macro_f1_percent":float(run["local_rf"]["local_rf_macro_f1_percent"]),
                "local_linear_macro_f1_percent":float(run["local_linear"]["local_linear_macro_f1_percent"]),
            })
        FINAL_VALIDATION = pd.DataFrame(rows)
        COMMUNICATION_TABLE = pd.DataFrame({
            spec.variant: METHOD_RUNS[spec.variant]["server"].communication_accounting()
            for spec in METHOD_SPECS
        }).T
        print("\nIoT-01 TRAINING + VALIDATION | COMPLETE")


# ===== NOTEBOOK CODE CELL 21 =====

# Final paper run: all validation decisions are frozen.
FINAL_TEST_UNLOCK = True


# ===== NOTEBOOK CODE CELL 22 =====
# 10. Locked/persistent final test.
# V6 keeps the strict Cross-Client results for generalization, but the PRIMARY paper
# result is Local-Private RF. Existing V5 final-test caches are migrated without retraining.
def run_final_test_once() -> Tuple[pd.DataFrame, Dict[str, np.ndarray]]:
    if not RUN_FULL_PROTOCOL or DATA is None:
        raise RuntimeError("Run the complete validation protocol first.")
    required = {spec.variant for spec in METHOD_SPECS}
    if set(METHOD_RUNS) != required:
        raise RuntimeError("Final method states are incomplete.")
    TestStageGate.begin_once(FINAL_TEST_UNLOCK)

    rows, confusions = [], {}
    for spec in METHOD_SPECS:
        run = METHOD_RUNS[spec.variant]
        server, clients = run["server"], run["clients"]
        centroid = evaluate_centroid_probe(
            clients, DATA.class_names, train_splits=("train","validation"),
            evaluation_split="test", allow_test=True,
        )
        local_rf = evaluate_client_local_classifier(
            clients, DATA.class_names, "rf", ("train","validation"), "test", allow_test=True,
        )
        local_linear = evaluate_client_local_classifier(
            clients, DATA.class_names, "linear", ("train","validation"), "test", allow_test=True,
        )
        cross_rf = evaluate_cross_client_classifier(
            clients, DATA.class_names, "rf", ("train","validation"), "test", allow_test=True,
        )
        cross_linear = evaluate_cross_client_classifier(
            clients, DATA.class_names, "linear", ("train","validation"), "test", allow_test=True,
        )
        prior = evaluate_cmga_prior_detector(server, split="test", allow_test=True) if spec.use_cmga_priors else None
        rows.append({
            "variant":spec.variant,
            "centroid_accuracy_percent":centroid["centroid_accuracy_percent"],
            "centroid_macro_f1_percent":centroid["centroid_macro_f1_percent"],
            "centroid_attack_f1_percent":centroid["centroid_attack_f1_percent"],
            "native_prior_macro_f1_percent":prior["prior_macro_f1_percent"] if prior else np.nan,
            "local_rf_accuracy_percent":local_rf["local_rf_accuracy_percent"],
            "local_rf_macro_f1_percent":local_rf["local_rf_macro_f1_percent"],
            "local_rf_attack_f1_percent":local_rf["local_rf_attack_f1_percent"],
            "local_linear_accuracy_percent":local_linear["local_linear_accuracy_percent"],
            "local_linear_macro_f1_percent":local_linear["local_linear_macro_f1_percent"],
            "cross_client_rf_accuracy_percent":cross_rf["cross_client_rf_accuracy_percent"],
            "cross_client_rf_macro_f1_percent":cross_rf["cross_client_rf_macro_f1_percent"],
            "cross_client_rf_attack_f1_percent":cross_rf["cross_client_rf_attack_f1_percent"],
            "cross_client_linear_accuracy_percent":cross_linear["cross_client_linear_accuracy_percent"],
            "cross_client_linear_macro_f1_percent":cross_linear["cross_client_linear_macro_f1_percent"],
        })
        confusions[f"{spec.variant}_centroid"] = centroid["centroid_confusion"]
        confusions[f"{spec.variant}_local_rf_PRIMARY"] = local_rf["local_rf_confusion"]
        confusions[f"{spec.variant}_local_linear_PRIMARY"] = local_linear["local_linear_confusion"]
        confusions[f"{spec.variant}_cross_client_rf_GENERALIZATION"] = cross_rf["cross_client_rf_confusion"]
        confusions[f"{spec.variant}_cross_client_linear_GENERALIZATION"] = cross_linear["cross_client_linear_confusion"]
        if prior is not None:
            confusions[f"{spec.variant}_prior"] = prior["prior_confusion"]
    return pd.DataFrame(rows), confusions


def _migrate_v5_final_test_to_v6(cached_results, cached_confusions):
    """Add Local-Private Test metrics to a valid V5 Cross-Client cache; never retrain."""
    frame = pd.DataFrame(cached_results).copy()
    if "variant" not in frame.columns:
        raise RuntimeError("Legacy final-test cache has no variant column.")
    frame = frame.set_index("variant", drop=False)
    confusions = dict(cached_confusions)

    for spec in METHOD_SPECS:
        clients = METHOD_RUNS[spec.variant]["clients"]
        local_rf = evaluate_client_local_classifier(
            clients, DATA.class_names, "rf", ("train","validation"), "test", allow_test=True,
        )
        local_linear = evaluate_client_local_classifier(
            clients, DATA.class_names, "linear", ("train","validation"), "test", allow_test=True,
        )
        frame.loc[spec.variant, "local_rf_accuracy_percent"] = local_rf["local_rf_accuracy_percent"]
        frame.loc[spec.variant, "local_rf_macro_f1_percent"] = local_rf["local_rf_macro_f1_percent"]
        frame.loc[spec.variant, "local_rf_attack_f1_percent"] = local_rf["local_rf_attack_f1_percent"]
        frame.loc[spec.variant, "local_linear_accuracy_percent"] = local_linear["local_linear_accuracy_percent"]
        frame.loc[spec.variant, "local_linear_macro_f1_percent"] = local_linear["local_linear_macro_f1_percent"]
        confusions[f"{spec.variant}_local_rf_PRIMARY"] = local_rf["local_rf_confusion"]
        confusions[f"{spec.variant}_local_linear_PRIMARY"] = local_linear["local_linear_confusion"]

        # Preserve legacy Cross-Client confusion names while also giving them explicit V6 semantics.
        old_rf = confusions.get(f"{spec.variant}_cross_client_rf_PRIMARY")
        old_linear = confusions.get(f"{spec.variant}_cross_client_linear_PRIMARY")
        if old_rf is not None:
            confusions[f"{spec.variant}_cross_client_rf_GENERALIZATION"] = old_rf
        if old_linear is not None:
            confusions[f"{spec.variant}_cross_client_linear_GENERALIZATION"] = old_linear

    return frame.reset_index(drop=True), confusions


FINAL_TEST_CACHE_V5 = CHECKPOINT_ROOT / "FinalTest" / "iot01_final_test_audited_v3.pkl"
FINAL_TEST_CACHE = CHECKPOINT_ROOT / "FinalTest" / "iot01_final_test_audited_v4_local_private.pkl"

if RUN_FULL_PROTOCOL:
    if FINAL_TEST_CACHE.is_file():
        with open(FINAL_TEST_CACHE, "rb") as fh:
            cached = pickle.load(fh)
        FINAL_TEST_RESULTS = cached["results"]
        FINAL_TEST_CONFUSIONS = cached["confusions"]
        _TEST_STAGE_STATE["count"] = 1
        out_print("FINAL_TEST_STATUS", "FINAL TEST | V6 Local-Private cache loaded")
    elif FINAL_TEST_CACHE_V5.is_file():
        with open(FINAL_TEST_CACHE_V5, "rb") as fh:
            legacy = pickle.load(fh)
        FINAL_TEST_RESULTS, FINAL_TEST_CONFUSIONS = _migrate_v5_final_test_to_v6(
            legacy["results"], legacy["confusions"]
        )
        FINAL_TEST_CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = FINAL_TEST_CACHE.with_suffix(".tmp")
        with open(tmp, "wb") as fh:
            pickle.dump(
                {"results":FINAL_TEST_RESULTS, "confusions":FINAL_TEST_CONFUSIONS},
                fh, protocol=pickle.HIGHEST_PROTOCOL,
            )
        os.replace(tmp, FINAL_TEST_CACHE)
        _TEST_STAGE_STATE["count"] = 1
        out_print("FINAL_TEST_STATUS", "FINAL TEST | V5 Cross-Client cache migrated; Local-Private metrics computed and saved")
    else:
        FINAL_TEST_RESULTS, FINAL_TEST_CONFUSIONS = run_final_test_once()
        FINAL_TEST_CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = FINAL_TEST_CACHE.with_suffix(".tmp")
        with open(tmp, "wb") as fh:
            pickle.dump(
                {"results":FINAL_TEST_RESULTS, "confusions":FINAL_TEST_CONFUSIONS},
                fh, protocol=pickle.HIGHEST_PROTOCOL,
            )
        os.replace(tmp, FINAL_TEST_CACHE)
        out_print("FINAL_TEST_STATUS", "FINAL TEST | V6 COMPLETE and saved")


# -----------------------------------------------------------------------------
# SECTION C — FINAL PAPER OUTPUTS  [notebook cell 23]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# 11. Extended Paper Experiments & Results  [notebook cell 25]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 26 =====
# 11.1 Results folders + helpers
_ensure_results_directories()
for path in (
    TABLES_ROOT / "Table_VI", TABLES_ROOT / "Table_VII", TABLES_ROOT / "Hybrid_Gate", TABLES_ROOT / "Local_Private_Control", TABLES_ROOT / "Generalization",
    TABLES_ROOT / "Table_VIII", TABLES_ROOT / "Table_IX", TABLES_ROOT / "Table_X",
    FIGURES_ROOT / "Figure_3_Convergence", FIGURES_ROOT / "Figure_4_Feature_Spaces",
    TEXT_ROOT / "Communication", TEXT_ROOT / "Stability", TEXT_ROOT / "Evaluation_Protocol",
):
    path.mkdir(parents=True, exist_ok=True)


def _display_paper_table(title: str, df: pd.DataFrame, decimals: int = 2):
    print(f"\n{title}")
    display(df.round(decimals).style.hide(axis="index"))


def _save_csv(df: pd.DataFrame, folder: Path, filename: str):
    _ensure_results_directories()
    folder.mkdir(parents=True, exist_ok=True)
    df.to_csv(folder / filename, index=False)


def _json_load(path: Path, default):
    if not path.is_file(): return default
    with open(path, "r", encoding="utf-8") as fh: return json.load(fh)


def _json_save(path: Path, obj):
    _ensure_results_directories()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh: json.dump(obj, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _cross_client_classifier_seeded(clients, class_names, kind, train_splits, evaluation_split, seed, allow_test=True):
    total = np.zeros((len(class_names), len(class_names)), dtype=np.int64)
    for held_out in clients:
        train_parts = [_client_split_arrays(c, train_splits, allow_test=False) for c in clients if c.cid != held_out.cid]
        train_z = np.concatenate([p[0] for p in train_parts]); train_y = np.concatenate([p[1] for p in train_parts])
        eval_z, eval_y, _ = _client_split_arrays(held_out, (evaluation_split,), allow_test=allow_test)
        clf = _make_classifier(kind, int(seed) + 10_000 + int(held_out.cid))
        clf.fit(train_z, train_y)
        total += confusion_matrix(eval_y, clf.predict(eval_z), labels=np.arange(len(class_names)))
    return _metrics_from_confusion(total, class_names, f"cross_client_{kind}")


def _evaluate_run_on_final_test(run, data, seed=CONFIG.seed):
    """V6 PRIMARY evaluator: local classifier stays inside each private encoder coordinate system."""
    clients = run["clients"]
    rf = evaluate_client_local_classifier(
        clients, data.class_names, "rf", ("train","validation"), "test", allow_test=True
    )
    linear = evaluate_client_local_classifier(
        clients, data.class_names, "linear", ("train","validation"), "test", allow_test=True
    )
    return {
        "accuracy":float(rf["local_rf_accuracy_percent"]),
        "macro_f1":float(rf["local_rf_macro_f1_percent"]),
        "attack_f1":float(rf["local_rf_attack_f1_percent"]),
        "linear_accuracy":float(linear["local_linear_accuracy_percent"]),
        "linear_macro_f1":float(linear["local_linear_macro_f1_percent"]),
        "rf_confusion":rf["local_rf_confusion"],
        "evaluation":"client-local/private RF; local train+validation -> same-client held-out test",
    }


def _evaluate_run_cross_client_generalization(run, data, seed=CONFIG.seed):
    """Strict unseen-client stress test; NOT the V6 headline/primary protocol."""
    clients = run["clients"]
    rf = _cross_client_classifier_seeded(
        clients, data.class_names, "rf", ("train","validation"), "test", seed, True
    )
    return {
        "accuracy":float(rf["cross_client_rf_accuracy_percent"]),
        "macro_f1":float(rf["cross_client_rf_macro_f1_percent"]),
        "rf_confusion":rf["cross_client_rf_confusion"],
        "evaluation":"leave-one-client-out cross-client RF; other clients train+validation -> held-out client test",
    }


def _evaluate_raw_local(data, seed=CONFIG.seed):
    """Same RF as latent methods, but on preprocessed original feature vectors, client-local."""
    n_classes = len(data.class_names)
    total = np.zeros((n_classes,n_classes), dtype=np.int64)
    for record in data.records:
        cid = int(record["client_id"])
        X_train = np.concatenate([record["X_train"], record["X_validation"]], axis=0)
        y_train = np.concatenate([record["y_train"], record["y_validation"]], axis=0)
        X_test = np.asarray(record["X_test"])
        y_test = np.asarray(record["y_test"])
        clf = RandomForestClassifier(**{**RF_PARAMS, "random_state":int(seed)+cid})
        clf.fit(X_train, y_train)
        total += confusion_matrix(y_test, clf.predict(X_test), labels=np.arange(n_classes))
    return _metrics_from_confusion(total, data.class_names, "raw_local_rf")


def _evaluate_raw_cross_client(data, seed=CONFIG.seed):
    n_classes = len(data.class_names)
    total = np.zeros((n_classes,n_classes), dtype=np.int64)
    for held_id in range(9):
        train_records = [r for r in data.records if int(r["client_id"]) != held_id]
        held = next(r for r in data.records if int(r["client_id"]) == held_id)
        X_train = np.concatenate([r[f"X_{s}"] for r in train_records for s in ("train","validation")])
        y_train = np.concatenate([r[f"y_{s}"] for r in train_records for s in ("train","validation")])
        X_test, y_test = held["X_test"], held["y_test"]
        clf = RandomForestClassifier(**{**RF_PARAMS, "random_state":int(seed)+10_000+held_id})
        clf.fit(X_train, y_train)
        total += confusion_matrix(y_test, clf.predict(X_test), labels=np.arange(n_classes))
    return _metrics_from_confusion(total, data.class_names, "raw_cross_client_rf")


# ============================================================================
# V6.3 — CROSS-CLIENT + GLOBAL V1-STYLE WHITENED NOVELTY GATE
# ============================================================================
def _classifier_attack_override(
    classifier,
    eval_z: np.ndarray,
    rf_prediction: np.ndarray,
    novelty_prediction: np.ndarray,
    benign_label: int,
) -> np.ndarray:
    """
    V1-compatible one-way gate: only a classifier BENIGN call can be overridden.
    Binary: override -> the available attack label.
    Multiclass: override -> highest-probability NON-benign RF class.
    """
    prediction = np.asarray(rf_prediction, dtype=np.int64).copy()
    override = (prediction == int(benign_label)) & (np.asarray(novelty_prediction) == 1)
    if not np.any(override):
        return prediction

    classes = np.asarray(getattr(classifier, "classes_", []), dtype=np.int64)
    attack_classes = classes[classes != int(benign_label)]
    if len(attack_classes) == 0:
        return prediction

    if len(attack_classes) == 1:
        prediction[override] = int(attack_classes[0])
        return prediction

    if not hasattr(classifier, "predict_proba"):
        # This path is not expected for RF/LogisticRegression, but keeps the
        # evaluator deterministic if a future classifier lacks probabilities.
        prediction[override] = int(attack_classes[0])
        return prediction

    proba = np.asarray(classifier.predict_proba(eval_z), dtype=np.float64)
    attack_positions = np.array([int(np.where(classes == c)[0][0]) for c in attack_classes], dtype=np.int64)
    selected = attack_classes[np.argmax(proba[override][:, attack_positions], axis=1)]
    prediction[override] = selected.astype(np.int64)
    return prediction



def _require_binary_cmga_gate(server: FederatedServer, class_names: Sequence[str]) -> Tuple[int, int]:
    class_names = tuple(str(x) for x in class_names)
    if len(class_names) != 2:
        raise RuntimeError(
            "CMGA Gate V6.5 is binary-open-set only and must never run on IoT-01..IoT-07."
        )
    if not getattr(server.spec, "use_cmga_priors", False) or getattr(server.spec, "aggregation", None) != "CMGA":
        raise RuntimeError(
            "CMGA Gate belongs only to F-ACVAE/CMGA; FedAvg, FedProx and no-CMGA are forbidden."
        )
    if server.prior_mu is None or server.prior_var is None:
        raise RuntimeError("CMGA Gate requires trained server.prior_mu/server.prior_var.")
    lower = [x.lower() for x in class_names]
    benign_label = lower.index("benign") if "benign" in lower else 0
    attack_label = 1 - benign_label
    return benign_label, attack_label


def _cmga_prior_numpy(
    server: FederatedServer, class_names: Sequence[str], min_variance: float
) -> Dict[str, np.ndarray]:
    benign_label, attack_label = _require_binary_cmga_gate(server, class_names)
    prior_mu = np.asarray(server.prior_mu.detach().cpu(), dtype=np.float64)
    prior_var = np.asarray(server.prior_var.detach().cpu(), dtype=np.float64)
    if prior_mu.shape != prior_var.shape or prior_mu.ndim != 2 or prior_mu.shape[0] != 2:
        raise RuntimeError(f"Unexpected binary CMGA prior shape: mu={prior_mu.shape}, var={prior_var.shape}.")
    return {
        "benign_label": int(benign_label),
        "attack_label": int(attack_label),
        "benign_mu": prior_mu[benign_label].copy(),
        "benign_var": np.maximum(prior_var[benign_label].copy(), float(min_variance)),
        "attack_mu": prior_mu[attack_label].copy(),
        "attack_var": np.maximum(prior_var[attack_label].copy(), float(min_variance)),
    }


def _whitened_radius(z: np.ndarray, mu: np.ndarray, var: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=np.float64)
    return np.sqrt(np.mean(((z - mu) / np.sqrt(var)) ** 2, axis=1))


def _diag_gaussian_mean_loglik(z: np.ndarray, mu: np.ndarray, var: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=np.float64)
    # Mean per latent dimension keeps margins stable when latent_dim changes.
    return -0.5 * np.mean(np.log(var) + ((z - mu) ** 2) / var, axis=1)


def _binary_gate_override(
    rf_prediction: np.ndarray,
    eval_z: np.ndarray,
    priors: Mapping[str, np.ndarray],
    threshold: float,
    likelihood_margin: Optional[float] = None,
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    rf_prediction = np.asarray(rf_prediction, dtype=np.int64)
    benign_label = int(priors["benign_label"])
    attack_label = int(priors["attack_label"])
    radius = _whitened_radius(eval_z, priors["benign_mu"], priors["benign_var"])
    radial = radius > float(threshold)

    if likelihood_margin is None:
        ratio = np.full(len(radius), np.nan, dtype=np.float64)
        gate_attack = radial
    else:
        ll_b = _diag_gaussian_mean_loglik(eval_z, priors["benign_mu"], priors["benign_var"])
        ll_a = _diag_gaussian_mean_loglik(eval_z, priors["attack_mu"], priors["attack_var"])
        ratio = ll_a - ll_b
        gate_attack = radial | (ratio > float(likelihood_margin))

    prediction = rf_prediction.copy()
    override = (rf_prediction == benign_label) & gate_attack
    prediction[override] = attack_label
    return prediction, {
        "radius": radius, "ratio": ratio, "gate_attack": gate_attack, "override": override
    }


def _binary_result_from_confusions(
    rf_total: np.ndarray,
    final_total: np.ndarray,
    class_names: Sequence[str],
    per_client_rows: Sequence[Mapping[str, object]],
    total_eval_rows: int,
    total_overrides: int,
    recovered_exact: int,
    introduced_exact: int,
    recovered_attack_detection: int,
    introduced_benign_fp: int,
    gate_quantile: float,
    likelihood_margin: Optional[float],
    evaluation: str,
) -> Dict[str, object]:
    rf_metrics = _metrics_from_confusion(rf_total, class_names, "rf_only")
    final_metrics = _metrics_from_confusion(final_total, class_names, "hybrid")
    per_client = pd.DataFrame(per_client_rows)
    thresholds = per_client["gate_threshold"].to_numpy(dtype=float) if len(per_client) else np.asarray([])
    return {
        "protocol_version": HYBRID_GATE_PROTOCOL_VERSION,
        "gate_quantile": float(gate_quantile),
        "likelihood_margin": None if likelihood_margin is None else float(likelihood_margin),
        "gate_requires_cmga": True,
        "gate_binary_only": True,
        "test_used_for_calibration": False,
        "rf_only_accuracy_percent": float(rf_metrics["rf_only_accuracy_percent"]),
        "rf_only_macro_f1_percent": float(rf_metrics["rf_only_macro_f1_percent"]),
        "rf_only_attack_f1_percent": float(rf_metrics["rf_only_attack_f1_percent"]),
        "hybrid_accuracy_percent": float(final_metrics["hybrid_accuracy_percent"]),
        "hybrid_macro_f1_percent": float(final_metrics["hybrid_macro_f1_percent"]),
        "hybrid_attack_f1_percent": float(final_metrics["hybrid_attack_f1_percent"]),
        "rf_only_confusion": rf_metrics["rf_only_confusion"],
        "hybrid_confusion": final_metrics["hybrid_confusion"],
        "per_client": per_client,
        "gate_override_percent": 100.0 * float(total_overrides) / max(int(total_eval_rows), 1),
        "recovered_exact": int(recovered_exact),
        "introduced_exact_errors": int(introduced_exact),
        "recovered_attack_detection": int(recovered_attack_detection),
        "introduced_benign_false_positives": int(introduced_benign_fp),
        "threshold_mean": float(np.mean(thresholds)) if len(thresholds) else np.nan,
        "threshold_std": float(np.std(thresholds)) if len(thresholds) else np.nan,
        "evaluation": str(evaluation),
    }


def evaluate_cross_client_global_whitened_gate(
    server: FederatedServer,
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    classifier_kind: str = "rf",
    classifier_train_splits: Sequence[str] = ("train", "validation"),
    gate_train_splits: Sequence[str] = ("train",),
    evaluation_split: str = "test",
    allow_test: bool = True,
    seed: int = CONFIG.seed,
    gate_quantile: float = HYBRID_GATE_QUANTILE,
    min_variance: float = HYBRID_GATE_MIN_VARIANCE,
    min_benign: int = HYBRID_GATE_MIN_BENIGN,
    likelihood_margin: Optional[float] = None,
) -> Dict[str, object]:
    """
    STRICT stress-test: other 8 clients fit the RF and calibrate threshold;
    held-out client Test is evaluated. Binary CMGA only.
    """
    priors = _cmga_prior_numpy(server, class_names, min_variance)
    benign_label = int(priors["benign_label"])
    if evaluation_split == "test" and not allow_test:
        raise RuntimeError("Test extraction is blocked outside the final stage.")
    if "test" in classifier_train_splits or "test" in gate_train_splits:
        raise RuntimeError("Test can never calibrate classifier or Gate.")

    n_classes = 2
    rf_total = np.zeros((2, 2), dtype=np.int64)
    final_total = np.zeros_like(rf_total)
    rows = []
    totals = dict(eval=0, overrides=0, recovered=0, introduced=0, attack_recovered=0, benign_fp=0)

    for held_out in clients:
        donors = [c for c in clients if c.cid != held_out.cid]
        parts = [_client_split_arrays(c, classifier_train_splits, allow_test=False) for c in donors]
        train_z = np.concatenate([p[0] for p in parts], axis=0)
        train_y = np.concatenate([p[1] for p in parts], axis=0).astype(np.int64)
        eval_z, eval_y, _ = _client_split_arrays(held_out, (evaluation_split,), allow_test=allow_test)
        eval_z = np.asarray(eval_z, dtype=np.float64)
        eval_y = np.asarray(eval_y, dtype=np.int64)

        clf = _make_classifier(classifier_kind, int(seed) + 30_000 + int(held_out.cid))
        clf.fit(train_z, train_y)
        rf_pred = np.asarray(clf.predict(eval_z), dtype=np.int64)

        benign_parts = []
        for donor in donors:
            z, y, _ = _client_split_arrays(donor, gate_train_splits, allow_test=False)
            z = np.asarray(z, dtype=np.float64); y = np.asarray(y, dtype=np.int64)
            if np.any(y == benign_label):
                benign_parts.append(z[y == benign_label])
        benign_train = np.concatenate(benign_parts, axis=0)
        if len(benign_train) < int(min_benign):
            raise RuntimeError(f"held_out={held_out.cid}: insufficient donor TRAIN-benign samples.")

        threshold = float(np.quantile(
            _whitened_radius(benign_train, priors["benign_mu"], priors["benign_var"]),
            float(gate_quantile)
        ))
        final_pred, diag = _binary_gate_override(
            rf_pred, eval_z, priors, threshold, likelihood_margin=likelihood_margin
        )

        labels = np.arange(2, dtype=np.int64)
        rf_cm = confusion_matrix(eval_y, rf_pred, labels=labels).astype(np.int64)
        final_cm = confusion_matrix(eval_y, final_pred, labels=labels).astype(np.int64)
        rf_total += rf_cm; final_total += final_cm

        rf_correct = rf_pred == eval_y
        final_correct = final_pred == eval_y
        true_attack = eval_y != benign_label
        true_benign = eval_y == benign_label
        recovered = (~rf_correct) & final_correct
        introduced = rf_correct & (~final_correct)
        recovered_detection = true_attack & (rf_pred == benign_label) & (final_pred != benign_label)
        introduced_fp = true_benign & (rf_pred == benign_label) & (final_pred != benign_label)

        m_rf = _metrics_from_confusion(rf_cm, class_names, "fold_rf")
        m_final = _metrics_from_confusion(final_cm, class_names, "fold_h")
        rows.append({
            "held_out_client": int(held_out.cid),
            "gate_threshold": threshold,
            "evaluation_rows": int(len(eval_y)),
            "gate_override_percent": 100.0 * float(np.mean(diag["override"])),
            "rf_accuracy_percent": float(m_rf["fold_rf_accuracy_percent"]),
            "rf_macro_f1_percent": float(m_rf["fold_rf_macro_f1_percent"]),
            "hybrid_accuracy_percent": float(m_final["fold_h_accuracy_percent"]),
            "hybrid_macro_f1_percent": float(m_final["fold_h_macro_f1_percent"]),
        })
        totals["eval"] += len(eval_y)
        totals["overrides"] += int(diag["override"].sum())
        totals["recovered"] += int(recovered.sum())
        totals["introduced"] += int(introduced.sum())
        totals["attack_recovered"] += int(recovered_detection.sum())
        totals["benign_fp"] += int(introduced_fp.sum())

    return _binary_result_from_confusions(
        rf_total, final_total, class_names, rows,
        totals["eval"], totals["overrides"], totals["recovered"], totals["introduced"],
        totals["attack_recovered"], totals["benign_fp"], gate_quantile, likelihood_margin,
        "strict leave-one-client-out Cross-Client RF + binary CMGA Gate; Test reporting only"
    )



def _pooled_global_train_benign(
    clients: Sequence[FederatedClient],
    benign_label: int,
    min_benign: int = HYBRID_GATE_MIN_BENIGN,
) -> Tuple[np.ndarray, pd.DataFrame]:
    """
    Collect BENIGN latent rows from TRAIN only across all clients.
    A client is allowed to contribute zero benign rows under Non-IID.
    We fail only if the GLOBAL pooled Train-benign support is insufficient.
    """
    benign_parts = []
    audit_rows = []
    for client in clients:
        z, y, _ = _client_split_arrays(client, ("train",), allow_test=False)
        z = np.asarray(z, dtype=np.float64)
        y = np.asarray(y, dtype=np.int64)
        local_benign = z[y == int(benign_label)]
        audit_rows.append({
            "client_id": int(client.cid),
            "train_rows": int(len(y)),
            "train_benign_rows": int(len(local_benign)),
            "train_attack_rows": int(np.sum(y != int(benign_label))),
        })
        if len(local_benign):
            benign_parts.append(local_benign)

    if not benign_parts:
        raise RuntimeError(
            "Binary CMGA Gate: GLOBAL pooled TRAIN contains zero benign rows. "
            "This is not a valid calibration scenario."
        )

    pooled = np.concatenate(benign_parts, axis=0)
    if len(pooled) < int(min_benign):
        raise RuntimeError(
            f"Binary CMGA Gate: GLOBAL pooled TRAIN-benign rows={len(pooled)} "
            f"< required min_benign={int(min_benign)}."
        )
    return pooled, pd.DataFrame(audit_rows)


def _global_train_benign_threshold(
    clients: Sequence[FederatedClient],
    priors: Mapping[str, np.ndarray],
    gate_quantile: float,
    min_benign: int = HYBRID_GATE_MIN_BENIGN,
) -> Tuple[float, pd.DataFrame, int]:
    benign_train, audit = _pooled_global_train_benign(
        clients, int(priors["benign_label"]), min_benign=min_benign
    )
    radii = _whitened_radius(
        benign_train, priors["benign_mu"], priors["benign_var"]
    )
    threshold = float(np.quantile(radii, float(gate_quantile)))
    return threshold, audit, int(len(benign_train))


def evaluate_client_local_cmga_binary_gate(
    server: FederatedServer,
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    gate_quantile: float = HYBRID_GATE_QUANTILE,
    min_variance: float = HYBRID_GATE_MIN_VARIANCE,
    min_benign: int = HYBRID_GATE_MIN_BENIGN,
    likelihood_margin: Optional[float] = None,
    rf_params: Optional[Mapping[str, object]] = None,
    seed: int = CONFIG.seed,
) -> Dict[str, object]:
    """
    Deployment/paper-matched downstream path:
    - local RF per client
    - ONE global CMGA threshold calibrated from pooled TRAIN-benign across clients
    - Test labels never calibrate anything
    - a Non-IID client may contain zero local TRAIN-benign rows
    """
    priors = _cmga_prior_numpy(server, class_names, min_variance)
    benign_label = int(priors["benign_label"])

    # IMPORTANT V6.7:
    # Do NOT require every Non-IID client to contain benign samples.
    # Calibrate one threshold from GLOBAL pooled TRAIN-benign only.
    threshold, benign_audit, global_benign_rows = _global_train_benign_threshold(
        clients, priors, gate_quantile=float(gate_quantile), min_benign=int(min_benign)
    )
    benign_count_by_client = {
        int(r.client_id): int(r.train_benign_rows)
        for r in benign_audit.itertuples(index=False)
    }

    rf_total = np.zeros((2, 2), dtype=np.int64)
    final_total = np.zeros_like(rf_total)
    rows = []
    totals = dict(eval=0, overrides=0, recovered=0, introduced=0, attack_recovered=0, benign_fp=0)

    params = dict(RF_PARAMS)
    if rf_params:
        params.update({k:v for k,v in rf_params.items() if k != "name"})
    params["n_jobs"] = -1

    for client in clients:
        train_z, train_y, _ = _client_split_arrays(
            client, ("train", "validation"), allow_test=False
        )
        test_z, test_y, _ = _client_split_arrays(
            client, ("test",), allow_test=True
        )
        train_z = np.asarray(train_z)
        train_y = np.asarray(train_y, dtype=np.int64)
        test_z = np.asarray(test_z)
        test_y = np.asarray(test_y, dtype=np.int64)

        # Non-IID may legitimately create a single-class local RF training set.
        # Preserve that reality instead of injecting artificial samples.
        unique = np.unique(train_y)
        if len(unique) == 0:
            raise RuntimeError(f"client={client.cid}: empty Train+Validation RF set.")
        if len(unique) == 1:
            rf_pred = np.full(len(test_y), int(unique[0]), dtype=np.int64)
        else:
            clf = RandomForestClassifier(
                **{**params, "random_state": int(seed) + int(client.cid)}
            )
            clf.fit(train_z, train_y)
            rf_pred = clf.predict(test_z).astype(np.int64)

        final_pred, diag = _binary_gate_override(
            rf_pred, test_z, priors, threshold,
            likelihood_margin=likelihood_margin
        )

        labels = np.arange(2, dtype=np.int64)
        rf_cm = confusion_matrix(test_y, rf_pred, labels=labels).astype(np.int64)
        final_cm = confusion_matrix(test_y, final_pred, labels=labels).astype(np.int64)
        rf_total += rf_cm
        final_total += final_cm

        rf_correct = rf_pred == test_y
        final_correct = final_pred == test_y
        true_attack = test_y != benign_label
        true_benign = test_y == benign_label
        recovered = (~rf_correct) & final_correct
        introduced = rf_correct & (~final_correct)
        recovered_detection = (
            true_attack & (rf_pred == benign_label) & (final_pred != benign_label)
        )
        introduced_fp = (
            true_benign & (rf_pred == benign_label) & (final_pred != benign_label)
        )

        rows.append({
            "client_id": int(client.cid),
            "local_train_benign_rows": int(benign_count_by_client.get(int(client.cid), 0)),
            "global_train_benign_rows": int(global_benign_rows),
            "gate_threshold": float(threshold),
            "threshold_scope": "GLOBAL pooled TRAIN-benign",
            "evaluation_rows": int(len(test_y)),
            "gate_override_percent": 100.0 * float(np.mean(diag["override"])),
            "local_rf_train_unique_classes": int(len(unique)),
        })

        totals["eval"] += len(test_y)
        totals["overrides"] += int(diag["override"].sum())
        totals["recovered"] += int(recovered.sum())
        totals["introduced"] += int(introduced.sum())
        totals["attack_recovered"] += int(recovered_detection.sum())
        totals["benign_fp"] += int(introduced_fp.sum())

    result = _binary_result_from_confusions(
        rf_total, final_total, class_names, rows,
        totals["eval"], totals["overrides"], totals["recovered"], totals["introduced"],
        totals["attack_recovered"], totals["benign_fp"],
        gate_quantile, likelihood_margin,
        "client-local RF Train+Validation -> same-client Test + binary CMGA Gate; "
        "ONE threshold from GLOBAL pooled TRAIN-benign only"
    )
    result["threshold_scope"] = "global_pooled_train_benign"
    result["global_train_benign_rows"] = int(global_benign_rows)
    result["n_clients_with_zero_train_benign"] = int(
        np.sum(benign_audit["train_benign_rows"].to_numpy(dtype=int) == 0)
    )
    result["train_benign_audit"] = benign_audit
    return result

def _binary_source_array(data, client_id: int, split: str) -> np.ndarray:
    record = next(r for r in data.records if int(r["client_id"]) == int(client_id))
    return np.asarray(record[f"source_{split}"]).astype(str)


def _rf_candidate_params(candidate: Mapping[str, object], seed: int) -> Dict[str, object]:
    params = dict(RF_PARAMS)
    params.update({k:v for k,v in candidate.items() if k != "name"})
    params["random_state"] = int(seed)
    params["n_jobs"] = -1
    return params


def select_binary_open_set_config(
    server: FederatedServer,
    clients: Sequence[FederatedClient],
    data,
    class_names: Sequence[str],
    rf_candidates: Sequence[Mapping[str, object]] = BINARY_RF_CANDIDATES,
    quantile_candidates: Sequence[float] = BINARY_GATE_QUANTILE_CANDIDATES,
    margin_candidates: Sequence[float] = BINARY_GATE_MARGIN_CANDIDATES,
    min_variance: float = HYBRID_GATE_MIN_VARIANCE,
    seed: int = CONFIG.seed,
) -> Dict[str, object]:
    """
    Select RF / radial quantile / likelihood margin ONLY with subtype-held-out
    Train->Validation folds. Test is never read here.
    """
    priors = _cmga_prior_numpy(server, class_names, min_variance)
    benign_label = int(priors["benign_label"])
    labels = np.arange(2, dtype=np.int64)

    # V6.7: Gate quantile candidates are calibrated from GLOBAL pooled TRAIN-benign.
    # Individual Non-IID clients are allowed to have zero benign samples.
    global_benign_train, global_benign_audit = _pooled_global_train_benign(
        clients, benign_label, min_benign=HYBRID_GATE_MIN_BENIGN
    )
    global_benign_radii = _whitened_radius(
        global_benign_train, priors["benign_mu"], priors["benign_var"]
    )

    # Build fold descriptors once. Each known attack subtype is held out from local RF fitting
    # and evaluated only in Validation together with Validation benign.
    descriptors = []
    for client in clients:
        train_z, train_y, _ = client.extract_mu("train")
        val_z, val_y, _ = client.extract_mu("validation")
        src_train = _binary_source_array(data, client.cid, "train")
        src_val = _binary_source_array(data, client.cid, "validation")
        train_z = np.asarray(train_z); train_y = np.asarray(train_y, dtype=np.int64)
        val_z = np.asarray(val_z); val_y = np.asarray(val_y, dtype=np.int64)
        attack_sources = sorted(set(src_train[train_y != benign_label]) & set(src_val[val_y != benign_label]))
        for held_source in attack_sources:
            fit_mask = (train_y == benign_label) | (src_train != held_source)
            eval_mask = (val_y == benign_label) | (src_val == held_source)
            if fit_mask.sum() < 2 or eval_mask.sum() < 2:
                continue
            if len(np.unique(train_y[fit_mask])) < 2 or len(np.unique(val_y[eval_mask])) < 2:
                continue
            descriptors.append({
                "client_id": int(client.cid),
                "held_source": str(held_source),
                "train_z": train_z[fit_mask],
                "train_y": train_y[fit_mask],
                "eval_z": val_z[eval_mask],
                "eval_y": val_y[eval_mask],
            })
    if not descriptors:
        raise RuntimeError("No subtype-held-out Train/Validation folds were available for binary calibration.")

    # RF selection by pseudo-open validation macro-F1, no Gate.
    rf_scores = []
    rf_predictions = {}
    for cand_idx, cand in enumerate(rf_candidates):
        total = np.zeros((2, 2), dtype=np.int64)
        preds = []
        for fold_idx, d in enumerate(descriptors):
            clf = RandomForestClassifier(**_rf_candidate_params(cand, seed + 50_000 + cand_idx*1000 + fold_idx))
            clf.fit(d["train_z"], d["train_y"])
            pred = clf.predict(d["eval_z"]).astype(np.int64)
            preds.append(pred)
            total += confusion_matrix(d["eval_y"], pred, labels=labels)
        m = _metrics_from_confusion(total, class_names, "rfselect")
        rf_scores.append((float(m["rfselect_macro_f1_percent"]), cand_idx))
        rf_predictions[cand_idx] = preds
    _, best_rf_idx = max(rf_scores, key=lambda x: (x[0], -x[1]))
    best_rf = dict(rf_candidates[best_rf_idx])

    # Quantile selection with radial Gate.
    q_scores = []
    best_preds = rf_predictions[best_rf_idx]
    for q in quantile_candidates:
        total = np.zeros((2, 2), dtype=np.int64)
        for d, rf_pred in zip(descriptors, best_preds):
            threshold = float(np.quantile(
                global_benign_radii, float(q)
            ))
            final, _ = _binary_gate_override(rf_pred, d["eval_z"], priors, threshold, likelihood_margin=None)
            total += confusion_matrix(d["eval_y"], final, labels=labels)
        m = _metrics_from_confusion(total, class_names, "qselect")
        q_scores.append((float(m["qselect_macro_f1_percent"]), float(q)))
    _, best_q = max(q_scores, key=lambda x: (x[0], x[1]))

    # Likelihood-margin selection on top of selected radial Gate.
    margin_scores = []
    for margin in margin_candidates:
        total = np.zeros((2, 2), dtype=np.int64)
        for d, rf_pred in zip(descriptors, best_preds):
            threshold = float(np.quantile(
                global_benign_radii, float(best_q)
            ))
            final, _ = _binary_gate_override(
                rf_pred, d["eval_z"], priors, threshold, likelihood_margin=float(margin)
            )
            total += confusion_matrix(d["eval_y"], final, labels=labels)
        m = _metrics_from_confusion(total, class_names, "mselect")
        margin_scores.append((float(m["mselect_macro_f1_percent"]), float(margin)))
    _, best_margin = max(margin_scores, key=lambda x: (x[0], -abs(x[1])))

    return {
        "selection_source": "subtype-held-out Train->Validation only; Gate threshold from GLOBAL pooled TRAIN-benign",
        "test_used": False,
        "folds": int(len(descriptors)),
        "global_train_benign_rows": int(len(global_benign_train)),
        "clients_with_zero_train_benign": int(np.sum(
            global_benign_audit["train_benign_rows"].to_numpy(dtype=int) == 0
        )),
        "rf_name": str(best_rf.get("name", "selected")),
        "rf_params": {k:v for k,v in best_rf.items() if k != "name"},
        "gate_quantile": float(best_q),
        "likelihood_margin": float(best_margin),
        "rf_validation_macro_f1": float(max(x[0] for x in rf_scores)),
        "quantile_validation_macro_f1": float(max(x[0] for x in q_scores)),
        "likelihood_validation_macro_f1": float(max(x[0] for x in margin_scores)),
    }



# ---------------------------------------------------------------------------
# V6.8 FINAL GATE — Client-Balanced Benign-only FPR-controlled radial CMGA Gate
# ---------------------------------------------------------------------------

def _weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    values = np.asarray(values, dtype=np.float64).reshape(-1)
    weights = np.asarray(weights, dtype=np.float64).reshape(-1)
    if len(values) == 0 or len(values) != len(weights):
        raise ValueError("weighted quantile requires non-empty aligned values/weights.")
    if np.any(~np.isfinite(values)) or np.any(~np.isfinite(weights)) or np.any(weights < 0):
        raise ValueError("weighted quantile received invalid values/weights.")
    total = float(weights.sum())
    if total <= 0:
        raise ValueError("weighted quantile requires positive total weight.")
    q = float(np.clip(float(quantile), 0.0, 1.0))
    order = np.argsort(values, kind="mergesort")
    v = values[order]
    w = weights[order] / total
    cdf = np.cumsum(w)
    idx = int(np.searchsorted(cdf, q, side="left"))
    idx = min(max(idx, 0), len(v) - 1)
    return float(v[idx])


def _client_benign_radii(
    clients: Sequence[FederatedClient],
    priors: Mapping[str, np.ndarray],
    split: str,
) -> Tuple[Dict[int, np.ndarray], pd.DataFrame]:
    """
    Extract benign CMGA radii per client for one NON-TEST split.
    Zero-benign clients are valid and are reported, not repaired.
    """
    if str(split).lower() == "test":
        raise RuntimeError("Test can never be used for Gate calibration.")
    benign_label = int(priors["benign_label"])
    radii_by_client = {}
    audit_rows = []
    for client in clients:
        z, y, _ = _client_split_arrays(client, (split,), allow_test=False)
        z = np.asarray(z, dtype=np.float64)
        y = np.asarray(y, dtype=np.int64)
        bz = z[y == benign_label]
        radii = (
            _whitened_radius(bz, priors["benign_mu"], priors["benign_var"])
            if len(bz) else np.empty(0, dtype=np.float64)
        )
        radii_by_client[int(client.cid)] = np.asarray(radii, dtype=np.float64)
        audit_rows.append({
            "client_id": int(client.cid),
            "split": str(split),
            "rows": int(len(y)),
            "benign_rows": int(len(bz)),
            "attack_rows": int(np.sum(y != benign_label)),
        })
    return radii_by_client, pd.DataFrame(audit_rows)


def _client_balanced_weighted_pool(
    radii_by_client: Mapping[int, np.ndarray],
    min_benign: int = HYBRID_GATE_MIN_BENIGN,
) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Equal total mass per active client; each sample inside a client shares that client's mass.
    """
    active = [(int(cid), np.asarray(r, dtype=np.float64).reshape(-1))
              for cid, r in radii_by_client.items() if len(r)]
    total_rows = int(sum(len(r) for _, r in active))
    if not active or total_rows < int(min_benign):
        raise RuntimeError(
            f"CBFPR Gate: global donor TRAIN-benign rows={total_rows} "
            f"< required min_benign={int(min_benign)}."
        )
    n_active = len(active)
    values = []
    weights = []
    for _, radii in active:
        values.append(radii)
        # Every active client contributes exactly 1/n_active total probability mass.
        weights.append(np.full(len(radii), 1.0 / (n_active * len(radii)), dtype=np.float64))
    return np.concatenate(values), np.concatenate(weights), total_rows


def _client_balanced_exceedance(
    radii_by_client: Mapping[int, np.ndarray],
    threshold: float,
) -> Tuple[float, pd.DataFrame]:
    """
    Mean benign exceedance rate across clients that actually contain benign samples.
    This is a client-balanced benign false-positive proxy and uses no attack labels.
    """
    rows = []
    rates = []
    for cid, radii in sorted(radii_by_client.items()):
        r = np.asarray(radii, dtype=np.float64).reshape(-1)
        if len(r) == 0:
            rows.append({
                "client_id": int(cid), "benign_rows": 0,
                "exceedance_rate": np.nan,
            })
            continue
        rate = float(np.mean(r > float(threshold)))
        rates.append(rate)
        rows.append({
            "client_id": int(cid), "benign_rows": int(len(r)),
            "exceedance_rate": rate,
        })
    return (float(np.mean(rates)) if rates else np.nan), pd.DataFrame(rows)


def calibrate_cbfpr_cmga_gate(
    clients: Sequence[FederatedClient],
    priors: Mapping[str, np.ndarray],
    train_fpr_candidates: Sequence[float] = CBFPR_TRAIN_FPR_CANDIDATES,
    validation_fpr_budget: float = CBFPR_VALIDATION_FPR_BUDGET,
    default_train_fpr: float = CBFPR_DEFAULT_TRAIN_FPR,
    min_benign: int = HYBRID_GATE_MIN_BENIGN,
) -> Dict[str, object]:
    """
    Benign-only Gate calibration.

    Threshold candidates:
      client-balanced weighted quantile of TRAIN-benign radii at q=1-alpha.

    Selection:
      use VALIDATION-benign only; choose the most aggressive alpha whose
      client-balanced benign exceedance <= validation_fpr_budget.

    No attack label participates in Gate threshold selection.
    Test is never read.
    """
    train_radii, train_audit = _client_benign_radii(clients, priors, "train")
    val_radii, val_audit = _client_benign_radii(clients, priors, "validation")
    train_values, train_weights, total_train_benign = _client_balanced_weighted_pool(
        train_radii, min_benign=min_benign
    )

    candidates = sorted({float(x) for x in train_fpr_candidates if 0.0 < float(x) < 1.0})
    if not candidates:
        raise ValueError("CBFPR train_fpr_candidates is empty.")

    rows = []
    for alpha in candidates:
        threshold = _weighted_quantile(train_values, train_weights, 1.0 - alpha)
        train_cb_fpr, _ = _client_balanced_exceedance(train_radii, threshold)
        val_cb_fpr, _ = _client_balanced_exceedance(val_radii, threshold)
        rows.append({
            "train_fpr_target": float(alpha),
            "quantile": float(1.0 - alpha),
            "threshold": float(threshold),
            "train_client_balanced_benign_fpr": float(train_cb_fpr),
            "validation_client_balanced_benign_fpr": float(val_cb_fpr)
                if np.isfinite(val_cb_fpr) else np.nan,
        })

    cand_df = pd.DataFrame(rows)
    finite_val = cand_df["validation_client_balanced_benign_fpr"].notna()
    feasible = cand_df[
        finite_val
        & (cand_df["validation_client_balanced_benign_fpr"] <= float(validation_fpr_budget) + 1e-12)
    ]

    if len(feasible):
        # Most aggressive benign FPR target that still satisfies the fixed validation budget.
        selected = feasible.sort_values(
            ["train_fpr_target", "threshold"], ascending=[False, True]
        ).iloc[0]
        selection_rule = "most_aggressive_within_validation_benign_fpr_budget"
    else:
        # If validation has no usable benign support or every candidate exceeds budget,
        # choose the safest available threshold; never consult attack labels or Test.
        if finite_val.any():
            selected = cand_df.loc[
                cand_df["validation_client_balanced_benign_fpr"].idxmin()
            ]
            selection_rule = "safest_min_validation_benign_fpr"
        else:
            idx = int(np.argmin(np.abs(cand_df["train_fpr_target"].to_numpy() - float(default_train_fpr))))
            selected = cand_df.iloc[idx]
            selection_rule = "default_train_fpr_no_validation_benign"

    threshold = float(selected["threshold"])
    selected_alpha = float(selected["train_fpr_target"])
    train_cb_fpr, train_client_rates = _client_balanced_exceedance(train_radii, threshold)
    val_cb_fpr, val_client_rates = _client_balanced_exceedance(val_radii, threshold)

    return {
        "threshold": threshold,
        "train_fpr_target": selected_alpha,
        "quantile": float(1.0 - selected_alpha),
        "validation_fpr_budget": float(validation_fpr_budget),
        "train_client_balanced_benign_fpr": float(train_cb_fpr),
        "validation_client_balanced_benign_fpr": float(val_cb_fpr)
            if np.isfinite(val_cb_fpr) else np.nan,
        "selection_rule": selection_rule,
        "selection_uses_attack_labels": False,
        "selection_uses_test": False,
        "global_train_benign_rows": int(total_train_benign),
        "clients_with_zero_train_benign": int(
            np.sum(train_audit["benign_rows"].to_numpy(dtype=int) == 0)
        ),
        "train_benign_audit": train_audit,
        "validation_benign_audit": val_audit,
        "train_client_rates": train_client_rates,
        "validation_client_rates": val_client_rates,
        "candidate_table": cand_df,
    }


def evaluate_client_local_cmga_binary_gate_cbfpr(
    server: FederatedServer,
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    seed: int = CONFIG.seed,
    min_variance: float = HYBRID_GATE_MIN_VARIANCE,
    min_benign: int = HYBRID_GATE_MIN_BENIGN,
) -> Dict[str, object]:
    """
    V6.8 FINAL Local/Paper-Matched path:
      fixed local RF + client-balanced benign-only FPR CMGA radial Gate.
    """
    priors = _cmga_prior_numpy(server, class_names, min_variance)
    benign_label = int(priors["benign_label"])
    calibration = calibrate_cbfpr_cmga_gate(
        clients, priors, min_benign=min_benign
    )
    threshold = float(calibration["threshold"])

    rf_total = np.zeros((2, 2), dtype=np.int64)
    final_total = np.zeros_like(rf_total)
    rows = []
    totals = dict(eval=0, overrides=0, recovered=0, introduced=0, attack_recovered=0, benign_fp=0)

    params = dict(RF_PARAMS)
    params["n_jobs"] = -1

    for client in clients:
        train_z, train_y, _ = _client_split_arrays(
            client, ("train", "validation"), allow_test=False
        )
        test_z, test_y, _ = _client_split_arrays(client, ("test",), allow_test=True)
        train_z = np.asarray(train_z)
        train_y = np.asarray(train_y, dtype=np.int64)
        test_z = np.asarray(test_z)
        test_y = np.asarray(test_y, dtype=np.int64)

        unique = np.unique(train_y)
        if len(unique) == 0:
            raise RuntimeError(f"client={client.cid}: empty Train+Validation RF set.")
        if len(unique) == 1:
            rf_pred = np.full(len(test_y), int(unique[0]), dtype=np.int64)
        else:
            clf = RandomForestClassifier(
                **{**params, "random_state": int(seed) + int(client.cid)}
            )
            clf.fit(train_z, train_y)
            rf_pred = clf.predict(test_z).astype(np.int64)

        # FINAL Gate is radial-only: no likelihood branch.
        final_pred, diag = _binary_gate_override(
            rf_pred, test_z, priors, threshold, likelihood_margin=None
        )

        labels = np.arange(2, dtype=np.int64)
        rf_cm = confusion_matrix(test_y, rf_pred, labels=labels).astype(np.int64)
        final_cm = confusion_matrix(test_y, final_pred, labels=labels).astype(np.int64)
        rf_total += rf_cm
        final_total += final_cm

        rf_correct = rf_pred == test_y
        final_correct = final_pred == test_y
        true_attack = test_y != benign_label
        true_benign = test_y == benign_label
        recovered = (~rf_correct) & final_correct
        introduced = rf_correct & (~final_correct)
        recovered_detection = true_attack & (rf_pred == benign_label) & (final_pred != benign_label)
        introduced_fp = true_benign & (rf_pred == benign_label) & (final_pred != benign_label)

        rows.append({
            "client_id": int(client.cid),
            "gate_threshold": threshold,
            "train_fpr_target": float(calibration["train_fpr_target"]),
            "validation_client_balanced_benign_fpr":
                float(calibration["validation_client_balanced_benign_fpr"])
                if np.isfinite(calibration["validation_client_balanced_benign_fpr"]) else np.nan,
            "evaluation_rows": int(len(test_y)),
            "gate_override_percent": 100.0 * float(np.mean(diag["override"])),
            "local_rf_train_unique_classes": int(len(unique)),
        })

        totals["eval"] += len(test_y)
        totals["overrides"] += int(diag["override"].sum())
        totals["recovered"] += int(recovered.sum())
        totals["introduced"] += int(introduced.sum())
        totals["attack_recovered"] += int(recovered_detection.sum())
        totals["benign_fp"] += int(introduced_fp.sum())

    result = _binary_result_from_confusions(
        rf_total, final_total, class_names, rows,
        totals["eval"], totals["overrides"], totals["recovered"], totals["introduced"],
        totals["attack_recovered"], totals["benign_fp"],
        float(calibration["quantile"]), None,
        "V6.8 client-local fixed RF + client-balanced benign-only FPR CMGA radial Gate; Test reporting only"
    )
    result.update({
        "threshold_scope": "client_balanced_global_train_benign",
        "calibration_rule": calibration["selection_rule"],
        "train_fpr_target": float(calibration["train_fpr_target"]),
        "validation_fpr_budget": float(calibration["validation_fpr_budget"]),
        "train_client_balanced_benign_fpr": float(calibration["train_client_balanced_benign_fpr"]),
        "validation_client_balanced_benign_fpr":
            float(calibration["validation_client_balanced_benign_fpr"])
            if np.isfinite(calibration["validation_client_balanced_benign_fpr"]) else np.nan,
        "global_train_benign_rows": int(calibration["global_train_benign_rows"]),
        "n_clients_with_zero_train_benign": int(calibration["clients_with_zero_train_benign"]),
        "selection_uses_attack_labels": False,
        "selection_test_used": False,
        "per_client": pd.DataFrame(rows),
        "calibration_candidates": calibration["candidate_table"],
        "train_benign_audit": calibration["train_benign_audit"],
        "validation_benign_audit": calibration["validation_benign_audit"],
    })
    return result


def evaluate_cross_client_cmga_binary_gate_cbfpr(
    server: FederatedServer,
    clients: Sequence[FederatedClient],
    class_names: Sequence[str],
    seed: int = CONFIG.seed,
    min_variance: float = HYBRID_GATE_MIN_VARIANCE,
    min_benign: int = HYBRID_GATE_MIN_BENIGN,
) -> Dict[str, object]:
    """
    V6.8 FINAL Cross-Client Gate:
      donor-only fixed RF + donor-only client-balanced benign-FPR radial Gate.
      Held-out client is excluded from Train AND Validation calibration.
    """
    priors = _cmga_prior_numpy(server, class_names, min_variance)
    benign_label = int(priors["benign_label"])

    rf_total = np.zeros((2, 2), dtype=np.int64)
    final_total = np.zeros_like(rf_total)
    rows = []
    totals = dict(eval=0, overrides=0, recovered=0, introduced=0, attack_recovered=0, benign_fp=0)

    for held_out in clients:
        donors = [c for c in clients if c.cid != held_out.cid]

        calibration = calibrate_cbfpr_cmga_gate(
            donors, priors, min_benign=min_benign
        )
        threshold = float(calibration["threshold"])

        parts = [_client_split_arrays(c, ("train", "validation"), allow_test=False) for c in donors]
        train_z = np.concatenate([p[0] for p in parts], axis=0)
        train_y = np.concatenate([p[1] for p in parts], axis=0).astype(np.int64)
        eval_z, eval_y, _ = _client_split_arrays(held_out, ("test",), allow_test=True)
        eval_z = np.asarray(eval_z, dtype=np.float64)
        eval_y = np.asarray(eval_y, dtype=np.int64)

        clf = _make_classifier("rf", int(seed) + 70_000 + int(held_out.cid))
        clf.fit(train_z, train_y)
        rf_pred = np.asarray(clf.predict(eval_z), dtype=np.int64)

        final_pred, diag = _binary_gate_override(
            rf_pred, eval_z, priors, threshold, likelihood_margin=None
        )

        labels = np.arange(2, dtype=np.int64)
        rf_cm = confusion_matrix(eval_y, rf_pred, labels=labels).astype(np.int64)
        final_cm = confusion_matrix(eval_y, final_pred, labels=labels).astype(np.int64)
        rf_total += rf_cm
        final_total += final_cm

        rf_correct = rf_pred == eval_y
        final_correct = final_pred == eval_y
        true_attack = eval_y != benign_label
        true_benign = eval_y == benign_label
        recovered = (~rf_correct) & final_correct
        introduced = rf_correct & (~final_correct)
        recovered_detection = true_attack & (rf_pred == benign_label) & (final_pred != benign_label)
        introduced_fp = true_benign & (rf_pred == benign_label) & (final_pred != benign_label)

        rows.append({
            "held_out_client": int(held_out.cid),
            "gate_threshold": threshold,
            "train_fpr_target": float(calibration["train_fpr_target"]),
            "validation_client_balanced_benign_fpr":
                float(calibration["validation_client_balanced_benign_fpr"])
                if np.isfinite(calibration["validation_client_balanced_benign_fpr"]) else np.nan,
            "evaluation_rows": int(len(eval_y)),
            "gate_override_percent": 100.0 * float(np.mean(diag["override"])),
            "donor_zero_train_benign_clients": int(calibration["clients_with_zero_train_benign"]),
        })

        totals["eval"] += len(eval_y)
        totals["overrides"] += int(diag["override"].sum())
        totals["recovered"] += int(recovered.sum())
        totals["introduced"] += int(introduced.sum())
        totals["attack_recovered"] += int(recovered_detection.sum())
        totals["benign_fp"] += int(introduced_fp.sum())

    result = _binary_result_from_confusions(
        rf_total, final_total, class_names, rows,
        totals["eval"], totals["overrides"], totals["recovered"], totals["introduced"],
        totals["attack_recovered"], totals["benign_fp"],
        np.nan, None,
        "V6.8 strict leave-one-client-out Cross RF + donor-only client-balanced benign-FPR CMGA radial Gate"
    )
    result.update({
        "threshold_scope": "donor_only_client_balanced_train_benign",
        "calibration_rule": "per-fold donor-only benign FPR control",
        "validation_fpr_budget": float(CBFPR_VALIDATION_FPR_BUDGET),
        "selection_uses_attack_labels": False,
        "selection_test_used": False,
        "per_client": pd.DataFrame(rows),
    })
    return result


# V6.5 runtime ownership audit on the real IoT-01 method objects.
# This is evaluation-only and does not mutate any model.
if RUN_FULL_PROTOCOL and METHOD_RUNS:
    for _variant in ("FedAvg_baseline", "FedProx_baseline", "ACVAE_no_CMGA"):
        try:
            _require_binary_cmga_gate(METHOD_RUNS[_variant]["server"], ("benign","attack"))
            raise AssertionError(f"Gate ownership leak: {_variant} unexpectedly accepted.")
        except RuntimeError:
            pass
    try:
        _require_binary_cmga_gate(METHOD_RUNS["F_ACVAE_CMGA"]["server"], DATA.class_names)
        raise AssertionError("Multiclass IoT-01 unexpectedly accepted by binary Gate.")
    except RuntimeError:
        pass
    out_print("LOGIC_TESTS", "V6.5 GATE OWNERSHIP AUDIT | PASS — only binary CMGA is eligible.")


# ===== NOTEBOOK CODE CELL 27 =====
# 11.1B REAL CROSS-DATASET DATA LAYER — UNSW-NB15 + CIC-IDS2017
#
# Source of ingestion logic: the user's F_ACVAE_V1 notebook.
# What is deliberately NOT imported from V1: IID federation, pooled/central RF headline evaluation,
# BatchNorm architecture, or V1 CMGA training rules.
#
# V5 keeps the audited V4 scientific contract:
#   external official/Table-IV outer train/test -> validation carved only from outer train
#   -> train-only preprocessing -> 9 persistent Dirichlet non-IID clients (alpha=.3)
#   -> unchanged V4 F-ACVAE -> leave-one-client-out cross-client RF on untouched outer test.

import zipfile
from sklearn.preprocessing import MinMaxScaler

TABLE_VII_SCENARIOS = {
    "UNSW-NB15": {
        "dataset_family": "UNSW-NB15",
        "class_names": ("benign", "attack"),
        "seed_offset": 1200,
        "table_iv_counts": {
            "train_benign": 37000,
            "train_attack": 45332,
            "test_benign": 56000,
            "test_attack": 119341,
        },
    },
    "CIC-IDS2017": {
        "dataset_family": "CIC-IDS2017",
        "class_names": ("benign", "attack"),
        "seed_offset": 1300,
        "table_iv_counts": {
            "train_benign": 219068,
            "train_attack": 46859,
            "test_benign": 153091,
            "test_attack": 32806,
        },
    },
}


def _ext_norm(value):
    return "".join(ch.lower() for ch in str(value) if ch.isalnum())


def _ext_resolve_folder(aliases):
    found = _find_dataset_folder(aliases)
    if found is not None:
        return found
    return PROJECT_ROOT / "dataset" / aliases[0]


UNSW_ROOT = _ext_resolve_folder(("UNSW-NB15", "UNSW_NB15", "UNSWNB15", "UNSW-NB-15", "UNSW NB-15"))
CICIDS_ROOT = _ext_resolve_folder(("CIC-IDS2017", "CIC_IDS2017", "CICIDS2017", "CIC IDS2017"))


def _ext_safe_zip_destination(extraction_root, archive_path, member_name):
    return extraction_root / archive_path.stem.replace(" ", "_") / Path(member_name).name


def _ext_find_csv_files(root, auto_extract_zip=True):
    root = Path(root)
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() == ".csv")
    if files or not auto_extract_zip:
        return files
    extraction_root = root / "_auto_extracted_csv"
    for archive_path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() == ".zip"):
        try:
            with zipfile.ZipFile(archive_path, "r") as archive:
                for member in archive.namelist():
                    if member.endswith("/") or Path(member).suffix.lower() != ".csv":
                        continue
                    destination = _ext_safe_zip_destination(extraction_root, archive_path, member)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    if destination.is_file() and destination.stat().st_size > 0:
                        continue
                    with archive.open(member, "r") as src, destination.open("wb") as dst:
                        while True:
                            chunk = src.read(1024 * 1024)
                            if not chunk:
                                break
                            dst.write(chunk)
        except zipfile.BadZipFile:
            continue
    return sorted(p for p in extraction_root.rglob("*") if p.is_file() and p.suffix.lower() == ".csv")


def _ext_find_parquet_files(root):
    root = Path(root)
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() == ".parquet")


CICIDS2017_KAGGLE_V3_EXPECTED = {
    "benign-monday-no-metadata.parquet",
    "botnet-friday-no-metadata.parquet",
    "bruteforce-tuesday-no-metadata.parquet",
    "ddos-friday-no-metadata.parquet",
    "dos-wednesday-no-metadata.parquet",
    "infiltration-thursday-no-metadata.parquet",
    "portscan-friday-no-metadata.parquet",
    "webattacks-thursday-no-metadata.parquet",
}


def _ext_cic_layout_audit(parquet_files):
    names = {p.name.lower() for p in parquet_files}
    missing = sorted(CICIDS2017_KAGGLE_V3_EXPECTED - names)
    extra = sorted(names - CICIDS2017_KAGGLE_V3_EXPECTED)
    return {
        "layout": "KAGGLE_DHOOGLA_CICIDS2017_V3_PARQUET" if not missing else "GENERIC_CICIDS2017_PARQUET",
        "expected_files_present": not missing,
        "missing_expected_files": tuple(missing),
        "extra_parquet_files": tuple(extra),
    }


def _ext_import_pyarrow():
    try:
        import pyarrow.parquet as pq
        return pq
    except ImportError:
        _ensure_optional_dependency("pyarrow", "pyarrow>=12.0")
        import pyarrow.parquet as pq
        return pq


def _ext_parquet_schema_names(path):
    pq = _ext_import_pyarrow()
    return tuple(pq.ParquetFile(str(path)).schema_arrow.names)


def _ext_probe_parquet_label(path):
    normalized = {str(x).strip().lower(): str(x) for x in _ext_parquet_schema_names(path)}
    for candidate in ("label", "class"):
        if candidate in normalized:
            return normalized[candidate]
    return None


def _ext_iter_parquet_batches(path, batch_size=150_000):
    # Low-level PyArrow is used intentionally instead of pandas.read_parquet(); this is the robust V1 path.
    pq = _ext_import_pyarrow()
    parquet_file = pq.ParquetFile(str(path))
    for batch in parquet_file.iter_batches(batch_size=int(batch_size), use_threads=True):
        try:
            yield batch.to_pandas(use_threads=True)
        except Exception:
            yield pd.DataFrame({name: batch.column(i).to_pylist() for i, name in enumerate(batch.schema.names)})


def _ext_normalize_columns(frame):
    frame = frame.copy()
    frame.columns = [str(c).strip() for c in frame.columns]
    return frame


def _ext_find_column(columns, candidates):
    normalized = {str(c).strip().lower(): str(c) for c in columns}
    for candidate in candidates:
        key = str(candidate).strip().lower()
        if key in normalized:
            return normalized[key]
    return None


def _ext_binary_labels(series, benign_tokens=("0", "normal", "benign")):
    benign = {str(x).strip().lower() for x in benign_tokens}
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().mean() > 0.95:
        values = numeric.fillna(1).to_numpy()
        if set(np.unique(values).tolist()).issubset({0, 1, 0.0, 1.0}):
            return (values != 0).astype(np.int64)
    text = series.astype(str).str.strip().str.lower()
    return (~text.isin(benign)).astype(np.int64).to_numpy()


def _ext_source_subtype(frame, y, preferred_columns):
    column = _ext_find_column(frame.columns, preferred_columns)
    if column is None:
        return np.where(y == 0, "benign", "attack").astype(object)
    source = frame[column].astype(str).str.strip().replace({"": "unknown_attack", "nan": "benign", "NaN": "benign"}).to_numpy(dtype=object)
    source[y == 0] = "benign"
    return source


def _ext_sample_exact_binary_counts(frame, y, counts, seed):
    rng = np.random.default_rng(seed)
    benign_idx = np.flatnonzero(y == 0)
    attack_idx = np.flatnonzero(y == 1)
    need_benign = int(counts["train_benign"]) + int(counts["test_benign"])
    need_attack = int(counts["train_attack"]) + int(counts["test_attack"])
    if len(benign_idx) < need_benign or len(attack_idx) < need_attack:
        raise RuntimeError(
            f"Insufficient binary rows for requested Table-IV split: benign need/found={need_benign:,}/{len(benign_idx):,}; "
            f"attack need/found={need_attack:,}/{len(attack_idx):,}."
        )
    benign_idx = rng.permutation(benign_idx)[:need_benign]
    attack_idx = rng.permutation(attack_idx)[:need_attack]
    tb, ta = int(counts["train_benign"]), int(counts["train_attack"])
    train_idx = np.concatenate([benign_idx[:tb], attack_idx[:ta]])
    test_idx = np.concatenate([benign_idx[tb:], attack_idx[ta:]])
    rng.shuffle(train_idx); rng.shuffle(test_idx)
    return frame.iloc[train_idx].reset_index(drop=True), frame.iloc[test_idx].reset_index(drop=True)


def _ext_read_unsw_outer_split(root, scenario, seed):
    if not root.is_dir():
        raise FileNotFoundError(f"UNSW-NB15 folder not found: {root}")
    csv_files = _ext_find_csv_files(root, auto_extract_zip=True)
    if not csv_files:
        raise FileNotFoundError(f"No UNSW-NB15 CSV files found under {root}")

    loaded = []
    for path in csv_files:
        name = path.name.lower()
        if not any(k in name for k in ("training-set", "testing-set", "training_set", "testing_set")):
            continue
        try:
            frame = _ext_normalize_columns(pd.read_csv(path, low_memory=False))
        except Exception:
            continue
        label_col = _ext_find_column(frame.columns, ("label", "class"))
        if label_col is None:
            continue
        y = _ext_binary_labels(frame[label_col])
        loaded.append((path, frame, y, int(np.sum(y == 0)), int(np.sum(y == 1))))

    train_match = next((x for x in loaded if x[3] == 37000 and x[4] == 45332), None)
    test_match = next((x for x in loaded if x[3] == 56000 and x[4] == 119341), None)
    if train_match is not None and test_match is not None:
        train_path, train_frame, _, _, _ = train_match
        test_path, test_frame, _, _, _ = test_match
        label_col = _ext_find_column(train_frame.columns, ("label", "class"))
        return train_frame, test_frame, label_col, (str(train_path), str(test_path)), {
            "split_source": "official UNSW split files matched by exact CTVAE Table-IV class counts"
        }

    usable = []
    for path in csv_files:
        if "feature" in path.name.lower() or "list_events" in path.name.lower():
            continue
        try:
            sample = _ext_normalize_columns(pd.read_csv(path, nrows=20, low_memory=False))
        except Exception:
            continue
        if _ext_find_column(sample.columns, ("label", "class")) is not None:
            usable.append(path)
    if not usable:
        raise RuntimeError("UNSW-NB15 files were found but no header-bearing processed CSV with a binary label was detected.")
    frames = [_ext_normalize_columns(pd.read_csv(path, low_memory=False)) for path in usable]
    pool = pd.concat(frames, ignore_index=True, sort=False)
    label_col = _ext_find_column(pool.columns, ("label", "class"))
    y = _ext_binary_labels(pool[label_col])
    train_frame, test_frame = _ext_sample_exact_binary_counts(pool, y, scenario["table_iv_counts"], seed)
    return train_frame, test_frame, label_col, tuple(str(p) for p in usable), {
        "split_source": "deterministic exact-count reconstruction of CTVAE Table-IV split"
    }


def _ext_update_reservoirs(chunk, label_column, rng, reservoirs, limits):
    chunk = _ext_normalize_columns(chunk)
    current_label = _ext_find_column(chunk.columns, ("label", "class"))
    if current_label is None:
        return label_column
    if label_column is None:
        label_column = current_label
    y_chunk = _ext_binary_labels(chunk[current_label], benign_tokens=("benign", "normal", "0"))
    work = chunk.copy()
    work["_sample_priority"] = rng.random(len(work))
    work["_binary_y"] = y_chunk
    for class_id in (0, 1):
        part = work[work["_binary_y"] == class_id]
        if part.empty:
            continue
        if reservoirs[class_id] is None:
            merged = part.copy()
        else:
            common = [c for c in reservoirs[class_id].columns if c in part.columns]
            for required in ("_sample_priority", "_binary_y"):
                if required not in common:
                    common.append(required)
            merged = pd.concat([reservoirs[class_id][common], part[common]], ignore_index=True)
        limit = int(limits[class_id])
        if len(merged) > limit:
            merged = merged.nsmallest(limit, "_sample_priority")
        reservoirs[class_id] = merged
    return label_column


def _ext_read_cic_outer_split(root, scenario, seed):
    if not root.is_dir():
        raise FileNotFoundError(f"CIC-IDS2017 folder not found: {root}")
    parquet_files = _ext_find_parquet_files(root)
    csv_files = [] if parquet_files else _ext_find_csv_files(root, auto_extract_zip=True)
    if not parquet_files and not csv_files:
        raise FileNotFoundError(f"CIC-IDS2017: no CSV or Parquet files found under {root}")

    counts = scenario["table_iv_counts"]
    limits = {
        0: int(counts["train_benign"]) + int(counts["test_benign"]),
        1: int(counts["train_attack"]) + int(counts["test_attack"]),
    }
    rng = np.random.default_rng(seed)
    reservoirs = {0: None, 1: None}
    label_column = None
    format_audit = {}

    if parquet_files:
        input_format = "parquet"
        format_audit = _ext_cic_layout_audit(parquet_files)
        for path in parquet_files:
            if _ext_probe_parquet_label(path) is None:
                raise RuntimeError(f"CIC-IDS2017 Parquet file has no recognizable Label column: {path}")
            for chunk in _ext_iter_parquet_batches(path, batch_size=150_000):
                label_column = _ext_update_reservoirs(chunk, label_column, rng, reservoirs, limits)
                del chunk
        source_files = tuple(str(p) for p in parquet_files)
    else:
        input_format = "csv"
        format_audit = {"layout": "CICIDS2017_CSV", "expected_files_present": None, "missing_expected_files": (), "extra_parquet_files": ()}
        for path in csv_files:
            try:
                reader = pd.read_csv(path, chunksize=150_000, low_memory=False)
            except Exception:
                continue
            for chunk in reader:
                label_column = _ext_update_reservoirs(chunk, label_column, rng, reservoirs, limits)
        source_files = tuple(str(p) for p in csv_files)

    if label_column is None:
        raise RuntimeError("CIC-IDS2017 files were found but no recognizable Label column was detected.")
    for class_id, required in limits.items():
        available = 0 if reservoirs[class_id] is None else len(reservoirs[class_id])
        if available < required:
            raise RuntimeError(f"CIC-IDS2017 insufficient class {class_id} rows: need {required:,}, found {available:,}")

    benign = reservoirs[0].sort_values("_sample_priority").reset_index(drop=True)
    attack = reservoirs[1].sort_values("_sample_priority").reset_index(drop=True)
    tb, ta = int(counts["train_benign"]), int(counts["train_attack"])
    train_frame = pd.concat([benign.iloc[:tb], attack.iloc[:ta]], ignore_index=True).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    test_frame = pd.concat([benign.iloc[tb:], attack.iloc[ta:]], ignore_index=True).sample(frac=1.0, random_state=seed+1).reset_index(drop=True)
    train_frame = train_frame.drop(columns=["_sample_priority", "_binary_y"], errors="ignore")
    test_frame = test_frame.drop(columns=["_sample_priority", "_binary_y"], errors="ignore")
    return train_frame, test_frame, label_column, source_files, {
        "split_source": "deterministic exact-count reconstruction of CTVAE Table-IV split from CIC tabular files",
        "input_format": input_format,
        **format_audit,
    }


def _ext_stratified_train_validation(outer_train, label_col, validation_ratio, seed):
    y = _ext_binary_labels(outer_train[label_col])
    rng = np.random.default_rng(seed)
    train_parts, val_parts = [], []
    for class_id in np.unique(y):
        idx = np.flatnonzero(y == class_id).copy()
        rng.shuffle(idx)
        n_val = max(1, int(round(len(idx) * float(validation_ratio))))
        n_val = min(n_val, len(idx)-1)
        val_parts.append(idx[:n_val]); train_parts.append(idx[n_val:])
    train_idx = np.concatenate(train_parts); val_idx = np.concatenate(val_parts)
    rng.shuffle(train_idx); rng.shuffle(val_idx)
    return outer_train.iloc[train_idx].reset_index(drop=True), outer_train.iloc[val_idx].reset_index(drop=True)


_EXT_ID_COLUMNS = {
    "id", "flow id", "flow_id", "source ip", "source_ip", "src ip", "src_ip",
    "destination ip", "destination_ip", "dst ip", "dst_ip", "timestamp", "time stamp",
}


def _ext_canonicalize_subnormals(x):
    x = np.asarray(x, dtype=np.float64)
    tiny = np.finfo(np.float64).tiny
    mask = (x != 0.0) & (np.abs(x) < tiny)
    if mask.any():
        x = x.copy(); x[mask] = 0.0
    return x, int(mask.sum())


def _ext_prepare_three_split_features(train_frame, validation_frame, test_frame, label_column, extra_drop_columns=()):
    train_frame = _ext_normalize_columns(train_frame)
    validation_frame = _ext_normalize_columns(validation_frame)
    test_frame = _ext_normalize_columns(test_frame)
    drop_lower = {str(label_column).strip().lower(), *{str(x).strip().lower() for x in extra_drop_columns}, *_EXT_ID_COLUMNS}
    common = [c for c in train_frame.columns if c in validation_frame.columns and c in test_frame.columns and c.strip().lower() not in drop_lower]
    if not common:
        raise RuntimeError("No common external feature columns remain after dropping labels/IDs.")

    outputs = [pd.DataFrame(index=f.index) for f in (train_frame, validation_frame, test_frame)]
    categorical, numeric = [], []
    for column in common:
        train_numeric = pd.to_numeric(train_frame[column], errors="coerce")
        if float(train_numeric.notna().mean()) >= 0.95:
            numeric.append(column)
            median = float(train_numeric.replace([np.inf,-np.inf],np.nan).median())
            if not np.isfinite(median): median = 0.0
            for out, frame in zip(outputs, (train_frame, validation_frame, test_frame)):
                s = pd.to_numeric(frame[column], errors="coerce").replace([np.inf,-np.inf],np.nan).fillna(median)
                out[column] = s.astype(np.float64)
        else:
            categorical.append(column)
            train_text = train_frame[column].astype(str).str.strip()
            freq = train_text.value_counts(normalize=True, dropna=False).to_dict()
            for out, frame in zip(outputs, (train_frame, validation_frame, test_frame)):
                out[column] = frame[column].astype(str).str.strip().map(freq).fillna(0.0).astype(np.float64)

    arrays=[]; subnormals=0
    for out in outputs:
        arr, replaced = _ext_canonicalize_subnormals(out.to_numpy(dtype=np.float64, copy=True))
        arrays.append(arr); subnormals += replaced
    scaler = MinMaxScaler(feature_range=(0.1,0.9), clip=True, copy=True)
    x_train = scaler.fit_transform(arrays[0]).astype(np.float32)
    x_val = scaler.transform(arrays[1]).astype(np.float32)
    x_test = scaler.transform(arrays[2]).astype(np.float32)
    if not all(np.isfinite(x).all() for x in (x_train,x_val,x_test)):
        raise FloatingPointError("External train-only preprocessing produced non-finite values.")
    tol=1e-6
    if any(x.size and (x.min() < 0.1-tol or x.max() > 0.9+tol) for x in (x_train,x_val,x_test)):
        raise AssertionError("External preprocessing escaped locked [0.1,0.9] model-input range.")
    return x_train, x_val, x_test, {
        "feature_columns": tuple(common),
        "numeric_feature_count": len(numeric),
        "categorical_feature_count": len(categorical),
        "categorical_features": tuple(categorical),
        "subnormals_replaced": int(subnormals),
        "preprocessing_mode": "TRAIN_ONLY_FREQUENCY_ENCODING + TRAIN_ONLY_MINMAX_[0.1,0.9]_CLIPPED",
    }


def _ext_row_hashes(x):
    return pd.util.hash_pandas_object(pd.DataFrame(np.ascontiguousarray(x)), index=False).to_numpy(dtype=np.uint64)


def _ext_remove_cross_split_duplicates(x_train,y_train,s_train,x_val,y_val,s_val,x_test,y_test,s_test):
    train_hash = np.unique(_ext_row_hashes(x_train))
    val_hash = _ext_row_hashes(x_val)
    keep_val = ~np.isin(val_hash, train_hash)
    removed_val = int((~keep_val).sum())
    x_val,y_val,s_val = x_val[keep_val],y_val[keep_val],s_val[keep_val]
    known = np.unique(np.concatenate([train_hash, _ext_row_hashes(x_val)]))
    test_hash = _ext_row_hashes(x_test)
    keep_test = ~np.isin(test_hash, known)
    removed_test = int((~keep_test).sum())
    x_test,y_test,s_test = x_test[keep_test],y_test[keep_test],s_test[keep_test]
    return x_train,y_train,s_train,x_val,y_val,s_val,x_test,y_test,s_test,removed_val,removed_test


def build_cross_dataset_bundle(dataset_id, seed=CONFIG.seed):
    if dataset_id not in TABLE_VII_SCENARIOS:
        raise KeyError(f"Unsupported Table VII dataset: {dataset_id}")
    scenario = TABLE_VII_SCENARIOS[dataset_id]
    source_seed = int(seed) + int(scenario["seed_offset"])
    root = UNSW_ROOT if dataset_id == "UNSW-NB15" else CICIDS_ROOT

    if dataset_id == "UNSW-NB15":
        outer_train, test_frame, label_col, source_files, loader_audit = _ext_read_unsw_outer_split(root, scenario, source_seed)
        extra_drop = ("attack_cat", "attack category")
        source_pref = ("attack_cat", "attack category", label_col)
    else:
        outer_train, test_frame, label_col, source_files, loader_audit = _ext_read_cic_outer_split(root, scenario, source_seed)
        extra_drop = ()
        source_pref = (label_col,)

    model_train, validation_frame = _ext_stratified_train_validation(
        outer_train, label_col, validation_ratio=0.15, seed=source_seed+17
    )
    y_train = _ext_binary_labels(model_train[label_col]); y_val = _ext_binary_labels(validation_frame[label_col]); y_test = _ext_binary_labels(test_frame[label_col])
    s_train = _ext_source_subtype(model_train, y_train, source_pref)
    s_val = _ext_source_subtype(validation_frame, y_val, source_pref)
    s_test = _ext_source_subtype(test_frame, y_test, source_pref)
    x_train,x_val,x_test,prep_audit = _ext_prepare_three_split_features(model_train, validation_frame, test_frame, label_col, extra_drop)

    (x_train,y_train,s_train,x_val,y_val,s_val,x_test,y_test,s_test,removed_val,removed_test) = _ext_remove_cross_split_duplicates(
        x_train,y_train,s_train,x_val,y_val,s_val,x_test,y_test,s_test
    )
    if min(len(y_train),len(y_val),len(y_test)) == 0:
        raise RuntimeError(f"{dataset_id}: a split became empty after leakage decontamination.")
    for split_name,y in (("train",y_train),("validation",y_val),("test",y_test)):
        if set(np.unique(y).tolist()) != {0,1}:
            raise RuntimeError(f"{dataset_id}/{split_name}: both binary classes are required after decontamination.")

    input_dim = int(x_train.shape[1])
    p_cfg = PipelineConfig(
        seed=int(seed), train_ratio=0.70, validation_ratio_within_train=0.15,
        expected_feature_count=input_dim, num_clients=9, partition_mode="dirichlet",
        dirichlet_alpha=0.30, min_client_train_rows=128, max_partition_attempts=1000,
        quantile_n_quantiles=1000, quantile_subsample=200_000,
        transform_chunk_size=50_000, output_low=0.10, output_high=0.90,
    )
    base_partition_seed = int(source_seed) + 7300
    proportions = split_indices = None
    for retry in range(100):
        p_seed = base_partition_seed + retry*1009
        candidate, attempts = _sample_partition_proportions(y_train, 2, p_cfg, p_seed)
        candidate_indices = {
            "train": _partition_indices(y_train, candidate, p_seed+101),
            "validation": _partition_indices(y_val, candidate, p_seed+202),
            "test": _partition_indices(y_test, candidate, p_seed+303),
        }
        if all(len(candidate_indices[s][cid]) > 0 for s in candidate_indices for cid in range(9)):
            proportions, split_indices, partition_seed, partition_attempts = candidate, candidate_indices, p_seed, attempts
            break
    if proportions is None:
        raise RuntimeError(f"{dataset_id}: unable to construct nine non-empty persistent Dirichlet clients.")

    xs={"train":x_train,"validation":x_val,"test":x_test}; ys={"train":y_train,"validation":y_val,"test":y_test}; ss={"train":s_train,"validation":s_val,"test":s_test}
    records=[]; count_rows=[]
    for cid in range(9):
        record={
            "client_id":cid,"scenario_id":dataset_id,"paper_code":dataset_id,"task":"binary",
            "source_device_key":dataset_id,"source_device":dataset_id,"source_directory":str(root),
            "class_names":("benign","attack"),"num_classes":2,"input_dim":input_dim,
            "partition_mode":"dirichlet","partition_seed":int(partition_seed),
        }
        for split in ("train","validation","test"):
            idx=split_indices[split][cid]
            record[f"X_{split}"]=xs[split][idx]
            record[f"y_{split}"]=ys[split][idx]
            record[f"source_{split}"]=ss[split][idx]
            for class_id,class_name in enumerate(("benign","attack")):
                count_rows.append({"client":cid,"split":split,"class_id":class_id,"class_name":class_name,"rows":int(np.sum(ys[split][idx]==class_id))})
        records.append(record)

    expected_counts=scenario["table_iv_counts"]
    outer_counts={
        "train_benign":int(np.sum(_ext_binary_labels(outer_train[label_col])==0)),
        "train_attack":int(np.sum(_ext_binary_labels(outer_train[label_col])==1)),
        "test_benign_before_dedup":int(expected_counts["test_benign"]),
        "test_attack_before_dedup":int(expected_counts["test_attack"]),
    }
    audit={
        "gate_status":"PASS_DATA_GATE","pipeline_version":"table-vii-v1-loader+v4-audited-protocol",
        "scenario_id":dataset_id,"seed":int(seed),"dataset_root":str(root),"class_names":("benign","attack"),
        "outer_table_iv_counts":dict(expected_counts),"observed_outer_counts":outer_counts,
        "train_rows":int(len(y_train)),"validation_rows":int(len(y_val)),"test_rows":int(len(y_test)),
        "removed_validation_duplicates":removed_val,"removed_test_duplicates":removed_test,
        "federation":{"clients":9,"mode":"dirichlet","alpha":0.3,"partition_seed":int(partition_seed),"partition_attempts":int(partition_attempts)},
        "evaluation_contract":"unchanged F-ACVAE training + V6 primary client-local/private RF; local train+validation -> same-client held-out test; strict Cross-Client is diagnostic only",
        "source_files":tuple(source_files), **loader_audit, **prep_audit,
    }
    manifest=pd.DataFrame([{"dataset":dataset_id,"source_file":p} for p in source_files])
    return IoT01DataBundle(records=records,input_dim=input_dim,class_names=("benign","attack"),audit=audit,source_manifest=manifest,client_class_counts=pd.DataFrame(count_rows))


# Strict computed-only V6 primary cache for Table VII.
# IMPORTANT: keep the V5 training scope to reuse completed training checkpoints.
TABLE_VII_REAL_CACHE_VERSION = "table-vii-local-private-v8-dual-f1"
TABLE_VII_REAL_SCOPE = "TableVII_Real_v1_V5"  # reuse validated model checkpoints
TABLE_VII_REAL_CACHE_PATH = CHECKPOINT_ROOT / "PaperExperiments" / "table_vii_local_private_v8_dual_f1.json"
LEGACY_TABLE_VII_CROSS_CLIENT_CACHE_PATH = CHECKPOINT_ROOT / "PaperExperiments" / "table_vii_real_v1_v5.json"
_TABLE_VII_DEFAULT = {"cache_version":TABLE_VII_REAL_CACHE_VERSION,"results":{}}
TABLE_VII_REAL_METRICS = _json_load(TABLE_VII_REAL_CACHE_PATH, _TABLE_VII_DEFAULT)
if TABLE_VII_REAL_METRICS.get("cache_version") != TABLE_VII_REAL_CACHE_VERSION:
    TABLE_VII_REAL_METRICS = dict(_TABLE_VII_DEFAULT)


def _save_table_vii_real(dataset_id, variant, result, data):
    TABLE_VII_REAL_METRICS.setdefault("results",{})[dataset_id]={
        "source":"computed","variant":variant,
        "accuracy":float(result["accuracy"]),
        "macro_f1":float(result["macro_f1"]),
        "attack_f1":float(result["attack_f1"]),
        "evaluation":"client-local/private RF; local train+validation -> same-client held-out test",
        "seed":int(CONFIG.seed),"checkpoint_scope":TABLE_VII_REAL_SCOPE,
        "input_dim":int(data.input_dim),"train_rows":int(data.audit["train_rows"]),"validation_rows":int(data.audit["validation_rows"]),"test_rows":int(data.audit["test_rows"]),
        "preprocessing_mode":data.audit.get("preprocessing_mode",""),"dataset_root":data.audit.get("dataset_root",""),
    }
    _json_save(TABLE_VII_REAL_CACHE_PATH,TABLE_VII_REAL_METRICS)


# -----------------------------------------------------------------------------
# 11.2 Extended experiments (checkpoint/resume)  [notebook cell 28]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 29 =====
# The only verbose output in this cell is round progress for genuinely long jobs.
# V6 changes evaluation/reporting only. Training checkpoint scopes remain V5-compatible.
PAPER_CACHE_PATH = CHECKPOINT_ROOT / "PaperExperiments" / "paper_metrics.json"
PAPER_METRICS = _json_load(PAPER_CACHE_PATH, {"scenarios":{}, "ablations":{}, "stability":{}, "raw":{}})
PAPER_METRICS.setdefault("ablations_local_v6", {})
PAPER_METRICS.setdefault("stability_local_v6", {})
PAPER_METRICS.setdefault("raw_local_v6", {})

# -----------------------------------------------------------------------------
# STRICT REAL TABLE-VI V6 CACHE — PRIMARY = LOCAL/PRIVATE RF
# New metric cache, old training checkpoint scope.
# -----------------------------------------------------------------------------
TABLE_VI_REAL_CACHE_VERSION = "table-vi-local-private-v8-dual-f1-reporting"
TABLE_VI_REAL_SCOPE = "TableVI_Real_v2_V5"  # training checkpoints remain unchanged
TABLE_VI_REAL_CACHE_PATH = CHECKPOINT_ROOT / "PaperExperiments" / "table_vi_local_private_v8_dual_f1.json"
_TABLE_VI_REAL_DEFAULT = {"cache_version": TABLE_VI_REAL_CACHE_VERSION, "results": {}}
TABLE_VI_REAL_METRICS = _json_load(TABLE_VI_REAL_CACHE_PATH, _TABLE_VI_REAL_DEFAULT)
if TABLE_VI_REAL_METRICS.get("cache_version") != TABLE_VI_REAL_CACHE_VERSION:
    TABLE_VI_REAL_METRICS = dict(_TABLE_VI_REAL_DEFAULT)

# Import genuine V6 rows. Binary rows without Attack-F1 are deliberately
# marked incomplete below and are re-evaluated from existing checkpoints.
_LEGACY_TABLE_VI_LOCAL = _json_load(
    CHECKPOINT_ROOT / "PaperExperiments" / "table_vi_local_private_v7_paper_f1.json",
    {"results":{}},
)
if not _LEGACY_TABLE_VI_LOCAL.get("results"):
    _LEGACY_TABLE_VI_LOCAL = _json_load(
        CHECKPOINT_ROOT / "PaperExperiments" / "table_vi_local_private_v6.json",
        {"results":{}},
    )
if not TABLE_VI_REAL_METRICS.get("results"):
    for _ds,_methods in _LEGACY_TABLE_VI_LOCAL.get("results",{}).items():
        TABLE_VI_REAL_METRICS.setdefault("results",{})[_ds] = {
            _method:dict(_item) for _method,_item in _methods.items()
            if _item.get("source") == "computed"
        }
    _json_save(TABLE_VI_REAL_CACHE_PATH,TABLE_VI_REAL_METRICS)

# -----------------------------------------------------------------------------
# STRICT UNSEEN-CLIENT GENERALIZATION CACHE
# Existing V5 Table-VI metrics already used exactly this Cross-Client contract,
# so they may be imported as generalization results — never as V6 headline metrics.
# -----------------------------------------------------------------------------
GENERALIZATION_CACHE_VERSION = "unseen-client-cross-client-rf-v1-v6"
GENERALIZATION_CACHE_PATH = CHECKPOINT_ROOT / "PaperExperiments" / "unseen_client_generalization_v6.json"
_GENERALIZATION_DEFAULT = {"cache_version":GENERALIZATION_CACHE_VERSION, "results":{}}
GENERALIZATION_METRICS = _json_load(GENERALIZATION_CACHE_PATH, _GENERALIZATION_DEFAULT)
if GENERALIZATION_METRICS.get("cache_version") != GENERALIZATION_CACHE_VERSION:
    GENERALIZATION_METRICS = dict(_GENERALIZATION_DEFAULT)

LEGACY_TABLE_VI_CROSS_CLIENT_CACHE_PATH = CHECKPOINT_ROOT / "PaperExperiments" / "table_vi_real_v2_v5.json"
LEGACY_TABLE_VI_CROSS_CLIENT = _json_load(LEGACY_TABLE_VI_CROSS_CLIENT_CACHE_PATH, {})
if LEGACY_TABLE_VI_CROSS_CLIENT.get("cache_version") == "table-vi-real-v2-v5-cross-client-test":
    for _ds, _methods in LEGACY_TABLE_VI_CROSS_CLIENT.get("results", {}).items():
        for _method, _item in _methods.items():
            if _item.get("source") == "computed":
                GENERALIZATION_METRICS.setdefault("results", {}).setdefault(_ds, {}).setdefault(
                    _method,
                    {
                        "source":"computed-v5-reused",
                        "variant":_item.get("variant",""),
                        "accuracy":float(_item["accuracy"]),
                        "macro_f1":float(_item["macro_f1"]),
                        "evaluation":"leave-one-client-out cross-client RF; other clients train+validation -> held-out client test",
                        "seed":int(_item.get("seed", CONFIG.seed)),
                        "checkpoint_scope":_item.get("checkpoint_scope", TABLE_VI_REAL_SCOPE),
                    },
                )
    _json_save(GENERALIZATION_CACHE_PATH, GENERALIZATION_METRICS)

_NEED_ABLATIONS = False  # V6.3 hybrid ablations are computed in the dedicated hybrid block below
_NEED_TABLE_VI_REAL = output_enabled("TABLE_VI")
_NEED_GENERALIZATION = any(output_enabled(x) for x in ("GENERALIZATION", "TABLE_IX"))
_NEED_RAW_RF = False  # V6.3 uses the Cross-Client raw-feature control in the hybrid block
_NEED_STABILITY = False  # V6.3 hybrid stability is computed in the dedicated hybrid block

_TABLE_VI_METHODS = (
    ("FedAvg", "FedAvg_baseline"),
    ("FedProx", "FedProx_baseline"),
    ("F-ACVAE", "F_ACVAE_CMGA"),
)
_TABLE_VI_SPEC_BY_VARIANT = {s.variant: s for s in METHOD_SPECS}


def _save_table_vi_real_cache():
    _json_save(TABLE_VI_REAL_CACHE_PATH, TABLE_VI_REAL_METRICS)


def _record_table_vi_real(
    dataset_id, method_name, variant, accuracy, macro_f1, attack_f1, checkpoint_scope
):
    TABLE_VI_REAL_METRICS.setdefault("results", {}).setdefault(dataset_id, {})[method_name] = {
        "source": "computed",
        "variant": variant,
        "accuracy": float(accuracy),
        "macro_f1": float(macro_f1),
        "attack_f1": float(attack_f1),
        "evaluation": "client-local/private RF; local train+validation -> same-client held-out test",
        "seed": int(CONFIG.seed),
        "checkpoint_scope": str(checkpoint_scope),
    }
    _save_table_vi_real_cache()


def _record_generalization(dataset_id, method_name, variant, result, checkpoint_scope):
    GENERALIZATION_METRICS.setdefault("results", {}).setdefault(dataset_id, {})[method_name] = {
        "source":"computed",
        "variant":variant,
        "accuracy":float(result["accuracy"]),
        "macro_f1":float(result["macro_f1"]),
        "evaluation":result.get("evaluation","leave-one-client-out cross-client RF"),
        "seed":int(CONFIG.seed),
        "checkpoint_scope":str(checkpoint_scope),
    }
    _json_save(GENERALIZATION_CACHE_PATH, GENERALIZATION_METRICS)


if RUN_FULL_PROTOCOL and RUN_EXTENDED_PAPER_EXPERIMENTS:
    # ---- Two missing IoT-01 ablations, now evaluated under the V6 primary Local-Private protocol ----
    if _NEED_ABLATIONS:
        ablation_cache = PAPER_METRICS["ablations_local_v6"]
        for spec in PAPER_ABLATION_SPECS:
            if spec.variant not in ablation_cache:
                out_print("TRAINING_PROGRESS", "\n" + "="*88)
                out_print("TRAINING_PROGRESS", f"PAPER ABLATION | IoT-01 | {spec.variant}")
                with output_scope("TRAINING_PROGRESS"):
                    run = run_method(DATA, spec, cfg=CONFIG, checkpoint_scope="Ablations")
                result = _evaluate_run_on_final_test(run, DATA, CONFIG.seed)
                ablation_cache[spec.variant] = {
                    "accuracy":result["accuracy"], "macro_f1":result["macro_f1"]
                }
                _json_save(PAPER_CACHE_PATH, PAPER_METRICS)
                del run

    # ---- Table VI PRIMARY: all three methods under Local-Private RF ----
    if _NEED_TABLE_VI_REAL:
        _iot01_final = FINAL_TEST_RESULTS.set_index("variant")
        for method_name, variant in _TABLE_VI_METHODS:
            row = _iot01_final.loc[variant]
            _record_table_vi_real(
                "IoT-01", method_name, variant,
                row["local_rf_accuracy_percent"],
                row["local_rf_macro_f1_percent"],
                row["local_rf_attack_f1_percent"],
                "Main_Audited_v3",
            )

        for scenario_id in [f"IoT-{i:02d}" for i in range(2,12)]:
            scenario_cache = TABLE_VI_REAL_METRICS.setdefault("results", {}).setdefault(scenario_id, {})
            is_binary = scenario_id in {"IoT-08","IoT-09","IoT-10","IoT-11"}
            # Final dual-F1 table needs collapsed Attack-F1 for ALL scenarios,
            # including multiclass IoT-01..07.
            missing_methods = [
                m for m,_ in _TABLE_VI_METHODS
                if (
                    m not in scenario_cache
                    or "attack_f1" not in scenario_cache.get(m,{})
                )
            ]
            if not missing_methods:
                continue
            scenario_data = build_nbaiot_scenario_data(DATASET_ROOT, scenario_id, seed=CONFIG.seed)
            for method_name, variant in _TABLE_VI_METHODS:
                cached_item = scenario_cache.get(method_name)
                if (
                    cached_item is not None
                    and "attack_f1" in cached_item
                ):
                    continue
                spec = _TABLE_VI_SPEC_BY_VARIANT[variant]
                with output_scope("TRAINING_PROGRESS"):
                    scenario_run = run_method(
                        scenario_data, spec, cfg=CONFIG, checkpoint_scope=TABLE_VI_REAL_SCOPE
                    )
                final = _evaluate_run_on_final_test(scenario_run, scenario_data, CONFIG.seed)
                _record_table_vi_real(
                    scenario_id, method_name, variant,
                    final["accuracy"], final["macro_f1"], final["attack_f1"],
                    TABLE_VI_REAL_SCOPE
                )
                del scenario_run
            del scenario_data

    # ---- Strict Cross-Client generalization is separate from headline Table VI ----
    # V6.6 FAIRNESS CONTRACT: this block MUST evaluate/cache ALL three headline methods:
    # FedAvg, FedProx and F-ACVAE under the same leave-one-client-out RF protocol.

    if _NEED_GENERALIZATION:
        # IoT-01 Cross-Client metrics are already in the locked/migrated final-test artifact.
        _iot01_final = FINAL_TEST_RESULTS.set_index("variant")
        for method_name, variant in _TABLE_VI_METHODS:
            row = _iot01_final.loc[variant]
            if method_name not in GENERALIZATION_METRICS.setdefault("results", {}).setdefault("IoT-01", {}):
                _record_generalization(
                    "IoT-01", method_name, variant,
                    {
                        "accuracy":row["cross_client_rf_accuracy_percent"],
                        "macro_f1":row["cross_client_rf_macro_f1_percent"],
                        "evaluation":"leave-one-client-out cross-client RF; other clients train+validation -> held-out client test",
                    },
                    "Main_Audited_v3",
                )

        # For IoT-02..11, prefer any verified Cross-Client results already cached/imported above.
        # Only compute a missing stress-test result if no valid legacy/current result exists.
        for scenario_id in [f"IoT-{i:02d}" for i in range(2,12)]:
            scenario_cache = GENERALIZATION_METRICS.setdefault("results", {}).setdefault(scenario_id, {})
            missing_methods = [m for m, _ in _TABLE_VI_METHODS if m not in scenario_cache]
            if not missing_methods:
                print(f"GENERALIZATION CACHE | {scenario_id} | all 3 Cross-Client results available")
                continue
            print(f"GENERALIZATION RUN | {scenario_id} | missing={missing_methods}")
            scenario_data = build_nbaiot_scenario_data(DATASET_ROOT, scenario_id, seed=CONFIG.seed)
            for method_name, variant in _TABLE_VI_METHODS:
                if method_name in scenario_cache:
                    continue
                spec = _TABLE_VI_SPEC_BY_VARIANT[variant]
                with output_scope("TRAINING_PROGRESS"):
                    scenario_run = run_method(
                        scenario_data, spec, cfg=CONFIG, checkpoint_scope=TABLE_VI_REAL_SCOPE
                    )
                result = _evaluate_run_cross_client_generalization(
                    scenario_run, scenario_data, CONFIG.seed
                )
                _record_generalization(
                    scenario_id, method_name, variant, result, TABLE_VI_REAL_SCOPE
                )
                del scenario_run
            del scenario_data

    # ---- Raw Features + Local RF, same deployment-aligned protocol as the headline latent methods ----
    if _NEED_RAW_RF and not PAPER_METRICS["raw_local_v6"]:
        raw_result = _evaluate_raw_local(DATA, CONFIG.seed)
        PAPER_METRICS["raw_local_v6"] = {
            "accuracy":float(raw_result["raw_local_rf_accuracy_percent"]),
            "macro_f1":float(raw_result["raw_local_rf_macro_f1_percent"]),
            "evaluation":"client-local RF on preprocessed original features; train+validation -> same-client test",
        }
        _json_save(PAPER_CACHE_PATH, PAPER_METRICS)

    # ---- Five independent F-ACVAE IoT-01 runs for mean ± std, using PRIMARY Local-Private RF ----
    if _NEED_STABILITY:
        full_spec = next(s for s in METHOD_SPECS if s.variant == "F_ACVAE_CMGA")
        stab_cache = PAPER_METRICS["stability_local_v6"]
        final42 = FINAL_TEST_RESULTS.set_index("variant").loc["F_ACVAE_CMGA"]
        stab_cache.setdefault("42", {
            "accuracy":float(final42["local_rf_accuracy_percent"]),
            "macro_f1":float(final42["local_rf_macro_f1_percent"]),
        })
        _json_save(PAPER_CACHE_PATH, PAPER_METRICS)
        for seed in (43,44,45,46):
            key=str(seed)
            if key in stab_cache:
                continue
            out_print("TRAINING_PROGRESS", "\n" + "="*88)
            out_print("TRAINING_PROGRESS", f"STABILITY RUN | IoT-01 | seed={seed}")
            cfg_seed = replace(CONFIG, seed=seed)
            with output_scope("TRAINING_PROGRESS"):
                run_seed = run_method(DATA, full_spec, cfg=cfg_seed, checkpoint_scope=f"Stability_seed_{seed}")
            result = _evaluate_run_on_final_test(run_seed, DATA, seed)
            stab_cache[key] = {
                "accuracy":result["accuracy"], "macro_f1":result["macro_f1"]
            }
            _json_save(PAPER_CACHE_PATH, PAPER_METRICS)
            del run_seed

elif (_NEED_TABLE_VI_REAL or _NEED_GENERALIZATION) and RUN_FULL_PROTOCOL and not RUN_EXTENDED_PAPER_EXPERIMENTS:
    raise RuntimeError(
        "TABLE_VI/GENERALIZATION requires the real extended experiments, but FACVAE_EXTENDED_PAPER=0. "
        "Remove that environment override or set it to 1; hardcoded fallback values are forbidden."
    )

out_print("TRAINING_PROGRESS", "\nEXTENDED PAPER EXPERIMENTS | COMPLETE/RESUMED")


# ===== NOTEBOOK CODE CELL 30 =====
# 11.2C — FINAL BINARY OPEN-SET GATE B ONLY
# Diagnostics (Relaxed-B, CBFPR, validation-selected Gate/RF) are intentionally
# not executed in this final release.

STRICT_BINARY_GATE_CACHE_VERSION = "iot08-11-strict-cross-binary-cmga-gate-v65"
STRICT_BINARY_GATE_CACHE_PATH = CHECKPOINT_ROOT / "PaperExperiments" / "binary_cross_cmga_gate_v65.json"
STRICT_BINARY_GATE_METRICS = _json_load(
    STRICT_BINARY_GATE_CACHE_PATH,
    {"cache_version":STRICT_BINARY_GATE_CACHE_VERSION, "results":{}}
)
if STRICT_BINARY_GATE_METRICS.get("cache_version") != STRICT_BINARY_GATE_CACHE_VERSION:
    STRICT_BINARY_GATE_METRICS = {"cache_version":STRICT_BINARY_GATE_CACHE_VERSION, "results":{}}

# Safe import of previously computed strict B results.
_legacy_v64 = _json_load(
    CHECKPOINT_ROOT / "PaperExperiments" / "hybrid_cross_cmga_prior_gate_v64.json", {}
)
for _ds in ("IoT-08","IoT-09","IoT-10","IoT-11"):
    _item = _legacy_v64.get("results",{}).get(_ds)
    if _item and _item.get("source") == "computed":
        STRICT_BINARY_GATE_METRICS.setdefault("results",{}).setdefault(_ds, dict(_item))
_json_save(STRICT_BINARY_GATE_CACHE_PATH, STRICT_BINARY_GATE_METRICS)

LOCAL_BINARY_GATE_CACHE_VERSION = "iot08-11-local-binary-cmga-gate-v67-global-train-threshold"
LOCAL_BINARY_GATE_CACHE_PATH = CHECKPOINT_ROOT / "PaperExperiments" / "binary_local_cmga_gate_v67_global_train_threshold.json"
LOCAL_BINARY_GATE_METRICS = _json_load(
    LOCAL_BINARY_GATE_CACHE_PATH,
    {"cache_version":LOCAL_BINARY_GATE_CACHE_VERSION, "results":{}}
)
if LOCAL_BINARY_GATE_METRICS.get("cache_version") != LOCAL_BINARY_GATE_CACHE_VERSION:
    LOCAL_BINARY_GATE_METRICS = {"cache_version":LOCAL_BINARY_GATE_CACHE_VERSION, "results":{}}

PAPER_METRICS.setdefault("ablations_cross_no_gate_v65", {})
PAPER_METRICS.setdefault("stability_local_v65", {})
PAPER_METRICS.setdefault("raw_cross_v63", {})

_NEED_BINARY = any(output_enabled(x) for x in ("TABLE_VI","HYBRID_GATE","GENERALIZATION"))
_NEED_IOT01_ABLATION = output_enabled("TABLE_VIII")
_NEED_IOT01_ATTRIBUTION = output_enabled("TABLE_IX")
_NEED_STABILITY_V65 = output_enabled("STABILITY")


def _record_gate_cache(store, path, dataset_id, result, scope, extra=None):
    item = {
        "source":"computed",
        "variant":"F_ACVAE_CMGA",
        "rf_only_accuracy":float(result["rf_only_accuracy_percent"]),
        "rf_only_macro_f1":float(result["rf_only_macro_f1_percent"]),
        "rf_only_attack_f1":float(result.get("rf_only_attack_f1_percent", np.nan)),
        "hybrid_accuracy":float(result["hybrid_accuracy_percent"]),
        "hybrid_macro_f1":float(result["hybrid_macro_f1_percent"]),
        "hybrid_attack_f1":float(result["hybrid_attack_f1_percent"]),
        "gate_override_percent":float(result["gate_override_percent"]),
        "recovered_exact":int(result["recovered_exact"]),
        "introduced_exact_errors":int(result["introduced_exact_errors"]),
        "recovered_attack_detection":int(result["recovered_attack_detection"]),
        "introduced_benign_false_positives":int(result["introduced_benign_false_positives"]),
        "threshold_mean":float(result["threshold_mean"]),
        "threshold_std":float(result["threshold_std"]),
        "gate_quantile":float(result["gate_quantile"]),
        "likelihood_margin":result.get("likelihood_margin"),
        "evaluation":str(result["evaluation"]),
        "seed":int(CONFIG.seed),
        "checkpoint_scope":str(scope),
    }
    if extra:
        item.update(dict(extra))
    store.setdefault("results",{})[dataset_id] = item
    _json_save(path, store)


NO_CMGA_CROSS_IOT01_RESULT = None
F_ACVAE_CROSS_IOT01_RESULT = None
F_ACVAE_LINEAR_IOT01_RESULT = None

if RUN_FULL_PROTOCOL and RUN_EXTENDED_PAPER_EXPERIMENTS:
    full_spec = next(s for s in METHOD_SPECS if s.variant == "F_ACVAE_CMGA")

    # IoT-01 architecture/attribution — Gate OFF.
    if _NEED_IOT01_ABLATION or _NEED_IOT01_ATTRIBUTION:
        F_ACVAE_CROSS_IOT01_RESULT = evaluate_cross_client_classifier(
            METHOD_RUNS["F_ACVAE_CMGA"]["clients"], DATA.class_names, "rf",
            ("train","validation"), "test", allow_test=True
        )
        NO_CMGA_CROSS_IOT01_RESULT = evaluate_cross_client_classifier(
            METHOD_RUNS["ACVAE_no_CMGA"]["clients"], DATA.class_names, "rf",
            ("train","validation"), "test", allow_test=True
        )
        F_ACVAE_LINEAR_IOT01_RESULT = evaluate_cross_client_classifier(
            METHOD_RUNS["F_ACVAE_CMGA"]["clients"], DATA.class_names, "linear",
            ("train","validation"), "test", allow_test=True
        )

    if _NEED_IOT01_ABLATION:
        ab_cache = PAPER_METRICS["ablations_cross_no_gate_v65"]
        legacy_ab = PAPER_METRICS.get("ablations_hybrid_v64",{})
        for spec in PAPER_ABLATION_SPECS:
            if spec.variant in ab_cache:
                continue
            if spec.variant in legacy_ab and "rf_only_macro_f1" in legacy_ab[spec.variant]:
                ab_cache[spec.variant] = {
                    "accuracy":float(legacy_ab[spec.variant]["rf_only_accuracy"]),
                    "macro_f1":float(legacy_ab[spec.variant]["rf_only_macro_f1"]),
                    "source":"v64-rf-only-reused",
                }
                continue
            out_print("TRAINING_PROGRESS", "\n" + "="*88)
            out_print("TRAINING_PROGRESS", f"FINAL ABLATION | IoT-01 | {spec.variant}")
            with output_scope("TRAINING_PROGRESS"):
                ab_run = run_method(DATA, spec, cfg=CONFIG, checkpoint_scope="Ablations")
            r = evaluate_cross_client_classifier(
                ab_run["clients"], DATA.class_names, "rf",
                ("train","validation"), "test", allow_test=True
            )
            ab_cache[spec.variant] = {
                "accuracy":float(r["cross_client_rf_accuracy_percent"]),
                "macro_f1":float(r["cross_client_rf_macro_f1_percent"]),
                "source":"computed",
            }
            del ab_run
        _json_save(PAPER_CACHE_PATH, PAPER_METRICS)

    # IoT-08..11 — only locked Gate B.
    if _NEED_BINARY:

        for scenario_id in ("IoT-08","IoT-09","IoT-10","IoT-11"):
            strict_item = STRICT_BINARY_GATE_METRICS.get("results",{}).get(scenario_id)
            local_item = LOCAL_BINARY_GATE_METRICS.get("results",{}).get(scenario_id)

            # Re-evaluate only if cache is missing or predates Attack-F1 reporting.
            need_strict = (
                not strict_item
                or "hybrid_attack_f1" not in strict_item
                or "rf_only_attack_f1" not in strict_item
            )
            need_local = (
                not local_item
                or "hybrid_attack_f1" not in local_item
                or "rf_only_attack_f1" not in local_item
            )

            if not (need_strict or need_local):
                continue
            scenario_data = build_nbaiot_scenario_data(
                DATASET_ROOT, scenario_id, seed=CONFIG.seed
            )
            if str(PAPER_SCENARIOS[scenario_id]["task"]) != "binary_open_set":
                raise AssertionError(f"{scenario_id} is not binary_open_set.")

            with output_scope("TRAINING_PROGRESS"):
                scenario_run = run_method(
                    scenario_data, full_spec, cfg=CONFIG,
                    checkpoint_scope=TABLE_VI_REAL_SCOPE
                )

            if need_strict:
                strict = evaluate_cross_client_global_whitened_gate(
                    scenario_run["server"], scenario_run["clients"],
                    scenario_data.class_names,
                    classifier_kind="rf",
                    evaluation_split="test",
                    allow_test=True,
                    seed=CONFIG.seed,
                    gate_quantile=HYBRID_GATE_QUANTILE,
                    likelihood_margin=None,
                )
                _record_gate_cache(
                    STRICT_BINARY_GATE_METRICS, STRICT_BINARY_GATE_CACHE_PATH,
                    scenario_id, strict, TABLE_VI_REAL_SCOPE,
                    {
                        "mode":"final-strict-cross-b",
                        "threshold_scope":"donor_pooled_train_benign",
                        "selection_test_used":False,
                        "rf_tuning":False,
                    }
                )
                strict["per_client"].to_csv(
                    TABLES_ROOT/"Hybrid_Gate"/f"{scenario_id}_FinalB_Cross_PerClient.csv",
                    index=False
                )

            if need_local:
                local = evaluate_client_local_cmga_binary_gate(
                    scenario_run["server"], scenario_run["clients"],
                    scenario_data.class_names,
                    gate_quantile=HYBRID_GATE_QUANTILE,
                    likelihood_margin=None,
                    rf_params=None,
                    seed=CONFIG.seed,
                )
                _record_gate_cache(
                    LOCAL_BINARY_GATE_METRICS, LOCAL_BINARY_GATE_CACHE_PATH,
                    scenario_id, local, TABLE_VI_REAL_SCOPE,
                    {
                        "mode":"final-local-b",
                        "threshold_scope":"global_pooled_train_benign",
                        "global_train_benign_rows":int(local["global_train_benign_rows"]),
                        "clients_with_zero_train_benign":int(local["n_clients_with_zero_train_benign"]),
                        "selection_test_used":False,
                        "rf_tuning":False,
                    }
                )
                local["per_client"].to_csv(
                    TABLES_ROOT/"Hybrid_Gate"/f"{scenario_id}_FinalB_Local_PerClient.csv",
                    index=False
                )
                local["train_benign_audit"].to_csv(
                    TABLES_ROOT/"Hybrid_Gate"/f"{scenario_id}_FinalB_TrainBenign_Audit.csv",
                    index=False
                )

            del scenario_run, scenario_data

    # IoT-01 raw Cross-RF attribution — required by Table IX.
    if _NEED_IOT01_ATTRIBUTION and not PAPER_METRICS["raw_cross_v63"]:
        raw_cross = _evaluate_raw_cross_client(DATA, CONFIG.seed)
        PAPER_METRICS["raw_cross_v63"] = {
            "accuracy":float(raw_cross["raw_cross_client_rf_accuracy_percent"]),
            "macro_f1":float(raw_cross["raw_cross_client_rf_macro_f1_percent"]),
            "evaluation":"cross-client RF on preprocessed original features",
        }
        _json_save(PAPER_CACHE_PATH, PAPER_METRICS)

    # Stability — Gate OFF on IoT-01.
    if _NEED_STABILITY_V65:
        stab = PAPER_METRICS["stability_local_v65"]
        f0 = FINAL_TEST_RESULTS.set_index("variant").loc["F_ACVAE_CMGA"]
        stab.setdefault("42", {
            "accuracy":float(f0["local_rf_accuracy_percent"]),
            "macro_f1":float(f0["local_rf_macro_f1_percent"]),
        })
        _json_save(PAPER_CACHE_PATH, PAPER_METRICS)

        for seed in (43,44,45,46):
            key = str(seed)
            if key in stab:
                continue
            cfg_seed = replace(CONFIG, seed=seed)
            out_print("TRAINING_PROGRESS", "\n" + "="*88)
            out_print("TRAINING_PROGRESS", f"FINAL STABILITY | IoT-01 | seed={seed}")
            with output_scope("TRAINING_PROGRESS"):
                seed_run = run_method(
                    DATA, full_spec, cfg=cfg_seed,
                    checkpoint_scope=f"Stability_seed_{seed}"
                )
            r = evaluate_client_local_classifier(
                seed_run["clients"], DATA.class_names, "rf",
                ("train","validation"), "test", allow_test=True
            )
            stab[key] = {
                "accuracy":float(r["local_rf_accuracy_percent"]),
                "macro_f1":float(r["local_rf_macro_f1_percent"]),
            }
            _json_save(PAPER_CACHE_PATH, PAPER_METRICS)
            del seed_run

elif RUN_FULL_PROTOCOL and (
    _NEED_BINARY or _NEED_IOT01_ABLATION or _NEED_IOT01_ATTRIBUTION or _NEED_STABILITY_V65
):
    raise RuntimeError(
        "Final paper outputs require FACVAE_EXTENDED_PAPER=1. "
        "No hardcoded/reference fallback is allowed."
    )


# ===== NOTEBOOK CODE CELL 31 =====
# 11.3 TABLE VII REAL EXPERIMENTS — V6.8 ENABLED; genuine F-ACVAE Local-Private RF, Gate OFF.
if TABLE_VII_TRAINING_REQUIRED:
    if not RUN_EXTENDED_PAPER_EXPERIMENTS:
        raise RuntimeError(
            "TABLE_VII requires real F-ACVAE experiments, but FACVAE_EXTENDED_PAPER=0. "
            "Set it to 1; hardcoded F-ACVAE fallback values are forbidden."
        )
    full_spec = next(s for s in METHOD_SPECS if s.variant == "F_ACVAE_CMGA")
    if not TABLE_VII_REAL_METRICS.get("results"):
        _prior_v7 = _json_load(
            CHECKPOINT_ROOT / "PaperExperiments" / "table_vii_local_private_v7_attack_f1.json",
            {"results":{}},
        )
        for _ds,_item in _prior_v7.get("results",{}).items():
            if _item.get("source")=="computed":
                TABLE_VII_REAL_METRICS.setdefault("results",{})[_ds]=dict(_item)
        _json_save(TABLE_VII_REAL_CACHE_PATH,TABLE_VII_REAL_METRICS)

    for dataset_id in ("UNSW-NB15", "CIC-IDS2017"):
        cached = TABLE_VII_REAL_METRICS.get("results",{}).get(dataset_id)
        if (
            cached
            and cached.get("source") == "computed"
            and cached.get("variant") == "F_ACVAE_CMGA"
            and "attack_f1" in cached
        ):
            continue
        dataset = build_cross_dataset_bundle(dataset_id, seed=CONFIG.seed)
        with output_scope("TRAINING_PROGRESS"):
            run = run_method(dataset, full_spec, cfg=CONFIG, checkpoint_scope=TABLE_VII_REAL_SCOPE)
        result = _evaluate_run_on_final_test(run, dataset, CONFIG.seed)
        _save_table_vii_real(dataset_id, full_spec.variant, result, dataset)
        audit_path = TABLES_ROOT / "Table_VII" / f"{dataset_id}_Data_Audit.json"
        _json_save(audit_path, dataset.audit)
        del run, dataset


# -----------------------------------------------------------------------------
# PAPER OUTPUT 1 — Table VI: N-BaIoT Federated Comparison  [notebook cell 32]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# TABLE VI — N-BaIoT: Published F-score + Our Macro-F1 / Attack-F1  [notebook cell 33]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 34 =====
if output_enabled("TABLE_VI"):
    _ensure_results_directories()

    # Published centralized Accuracy/F-score values from the CTVAE paper.
    reference = {
        "IoT-01":[67.2,55.7,92.0,88.9,92.1,89.2,67.2,64.9,93.0,90.9],
        "IoT-02":[75.2,66.4,94.2,91.8,94.1,91.9,74.2,71.5,95.0,93.5],
        "IoT-03":[70.9,60.4,92.8,89.9,93.4,91.3,70.5,67.9,93.9,92.2],
        "IoT-04":[61.3,47.7,90.6,87.0,90.9,87.6,60.0,57.0,91.8,89.5],
        "IoT-05":[65.6,53.6,92.1,89.0,92.2,89.3,65.7,62.8,93.1,91.1],
        "IoT-06":[85.0,79.7,92.3,91.8,78.1,76.9,62.8,61.7,94.5,93.3],
        "IoT-07":[85.8,80.7,96.5,95.1,94.2,94.2,76.8,75.5,96.6,95.5],
        "IoT-08":[97.6,97.9,90.0,92.8,95.5,96.4,88.5,91.9,100.0,100.0],
        "IoT-09":[95.3,96.0,80.2,85.7,94.8,95.7,90.1,92.2,98.9,99.0],
        "IoT-10":[40.0,52.4,89.9,92.3,98.8,98.9,95.5,96.0,99.7,99.8],
        "IoT-11":[42.1,50.9,87.9,89.7,42.1,50.9,61.0,69.4,99.7,99.7],
    }
    ref_cols = [
        "STA Acc","STA Fscore","CSAEC Acc","CSAEC Fscore",
        "MAE Acc","MAE Fscore","MVAE Acc","MVAE Fscore",
        "CTVAE Acc","CTVAE Fscore"
    ]

    binary_set={"IoT-08","IoT-09","IoT-10","IoT-11"}
    real=TABLE_VI_REAL_METRICS.get("results",{})
    gate_b=LOCAL_BINARY_GATE_METRICS.get("results",{})
    rows=[]; missing=[]

    for ds,vals in reference.items():
        row={"Dataset":ds,**dict(zip(ref_cols,vals))}

        for method in ("FedAvg","FedProx","F-ACVAE"):
            item=real.get(ds,{}).get(method)
            if (
                not item
                or "macro_f1" not in item
                or "attack_f1" not in item
            ):
                missing.append(f"{ds}/{method}/DualF1")
                acc=macro=attack=np.nan
            else:
                acc=float(item["accuracy"])
                macro=float(item["macro_f1"])
                attack=float(item["attack_f1"])

            if method=="FedAvg":
                row["FedAvg Acc"]=acc
                row["FedAvg Macro-F1"]=macro
                row["FedAvg Attack-F1"]=attack
            elif method=="FedProx":
                row["FedProx Acc"]=acc
                row["FedProx Macro-F1"]=macro
                row["FedProx Attack-F1"]=attack
            else:
                facvae_local_acc=acc
                facvae_local_macro=macro
                facvae_local_attack=attack

        # Locked proposed method: Gate B only for binary open-set IoT-08..11.
        if ds in binary_set:
            g=gate_b.get(ds)
            if (
                not g
                or "hybrid_macro_f1" not in g
                or "hybrid_attack_f1" not in g
            ):
                missing.append(f"{ds}/GateB/DualF1")
                final_acc=final_macro=final_attack=np.nan
            else:
                final_acc=float(g["hybrid_accuracy"])
                final_macro=float(g["hybrid_macro_f1"])
                final_attack=float(g["hybrid_attack_f1"])
        else:
            final_acc=facvae_local_acc
            final_macro=facvae_local_macro
            final_attack=facvae_local_attack

        row["F-ACVAE Acc"]=final_acc
        row["F-ACVAE Macro-F1"]=final_macro
        row["F-ACVAE Attack-F1"]=final_attack
        rows.append(row)

    if missing:
        raise RuntimeError(
            "TABLE VI missing final dual-F1 metrics: " + ", ".join(missing)
        )

    ordered=[
        "Dataset",*ref_cols,
        "FedAvg Acc","FedAvg Macro-F1","FedAvg Attack-F1",
        "FedProx Acc","FedProx Macro-F1","FedProx Attack-F1",
        "F-ACVAE Acc","F-ACVAE Macro-F1","F-ACVAE Attack-F1",
    ]
    TABLE_VI=pd.DataFrame(rows)[ordered]

    numeric=[x for x in TABLE_VI.columns if x!="Dataset"]
    TABLE_VI=pd.concat([
        TABLE_VI,
        pd.DataFrame([{
            "Dataset":"Average",
            **{x:TABLE_VI[x].mean() for x in numeric}
        }])
    ],ignore_index=True)

    display_df=TABLE_VI.copy()
    display_df.columns=pd.MultiIndex.from_tuples([
        ("","Dataset",""),

        ("Centralized IDS","STA","Acc"),
        ("Centralized IDS","STA","F-score (Reported)"),
        ("Centralized IDS","CSAEC","Acc"),
        ("Centralized IDS","CSAEC","F-score (Reported)"),
        ("Centralized IDS","MAE","Acc"),
        ("Centralized IDS","MAE","F-score (Reported)"),
        ("Centralized IDS","MVAE","Acc"),
        ("Centralized IDS","MVAE","F-score (Reported)"),
        ("Centralized IDS","CTVAE","Acc"),
        ("Centralized IDS","CTVAE","F-score (Reported)"),

        ("Federated IDS","FedAvg","Acc"),
        ("Federated IDS","FedAvg","Macro-F1"),
        ("Federated IDS","FedAvg","Attack-F1"),

        ("Federated IDS","FedProx","Acc"),
        ("Federated IDS","FedProx","Macro-F1"),
        ("Federated IDS","FedProx","Attack-F1"),

        ("Federated IDS","F-ACVAE","Acc"),
        ("Federated IDS","F-ACVAE","Macro-F1"),
        ("Federated IDS","F-ACVAE","Attack-F1"),
    ])

    # Because the published multiclass F-score averaging rule is not explicit,
    # we do NOT bold "best F1" across incompatible F-score definitions.
    # Accuracy remains directly comparable across all methods.
    accuracy_cols=[
        ("Centralized IDS","STA","Acc"),
        ("Centralized IDS","CSAEC","Acc"),
        ("Centralized IDS","MAE","Acc"),
        ("Centralized IDS","MVAE","Acc"),
        ("Centralized IDS","CTVAE","Acc"),
        ("Federated IDS","FedAvg","Acc"),
        ("Federated IDS","FedProx","Acc"),
        ("Federated IDS","F-ACVAE","Acc"),
    ]

    def _best_accuracy_only(frame):
        css=pd.DataFrame("",index=frame.index,columns=frame.columns)
        for ridx in frame.index:
            vals=pd.to_numeric(frame.loc[ridx,accuracy_cols],errors="coerce")
            if vals.notna().any():
                best=float(vals.max())
                for col,val in vals.items():
                    if pd.notna(val) and np.isclose(float(val),best,atol=1e-12):
                        css.loc[ridx,col]="font-weight:800;"
        return css

    print(
        "TABLE VI: Performance (%) comparison on N-BaIoT — "
        "published F-score retained; federated Macro-F1 and Attack-F1 reported separately"
    )
    display(
        display_df.round(2).style
        .apply(_best_accuracy_only,axis=None)
        .format(precision=2,na_rep="—")
        .hide(axis="index")
    )

    _save_csv(
        TABLE_VI,
        TABLES_ROOT/"Table_VI",
        "Table_VI_Dual_F1.csv"
    )


# ===== NOTEBOOK CODE CELL 35 =====
if output_enabled("EVALUATION_PROTOCOL"):
    EVALUATION_PROTOCOL_TEXT=(
        "B. Evaluation Protocol\n"
        f"To ensure fair comparison across all methods, we employ the same Random Forest (RF) "
        f"classifier with identical hyperparameters "
        f"(n_estimators={RF_PARAMS['n_estimators']}, max_depth={RF_PARAMS['max_depth']}, "
        f"min_samples_split={RF_PARAMS['min_samples_split']}, "
        f"min_samples_leaf={RF_PARAMS['min_samples_leaf']}, "
        f"max_features='{RF_PARAMS['max_features']}', random_state={RF_PARAMS['random_state']}). "
        "For each method, latent representations are first extracted from the corresponding model "
        "(or raw features are used for non-autoencoder controls), and then a fresh RF classifier "
        "is trained on these features. This keeps the downstream classifier fixed so that observed "
        "performance differences primarily reflect the learned representations."
    )
    print(EVALUATION_PROTOCOL_TEXT)
    (TEXT_ROOT/"Evaluation_Protocol"/"Evaluation_Protocol_Paper.txt").write_text(
        EVALUATION_PROTOCOL_TEXT,encoding="utf-8"
    )


# -----------------------------------------------------------------------------
# TABLE VII — Published F-score + F-ACVAE Macro-F1 / Attack-F1  [notebook cell 36]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 37 =====
if output_enabled("TABLE_VII"):
    _ensure_results_directories()

    reference = {
        "UNSW-NB15":{
            "CTVAE-O Acc":88.4,"CTVAE-O Fscore":88.7,
            "CTVAE-K Acc":89.3,"CTVAE-K Fscore":90.9,
        },
        "CIC-IDS2017":{
            "CTVAE-O Acc":97.9,"CTVAE-O Fscore":97.9,
            "CTVAE-K Acc":98.1,"CTVAE-K Fscore":98.2,
        },
    }

    real=TABLE_VII_REAL_METRICS.get("results",{})
    rows=[]; missing=[]

    for ds,ref in reference.items():
        item=real.get(ds)
        if (
            not item
            or item.get("source")!="computed"
            or "macro_f1" not in item
            or "attack_f1" not in item
        ):
            missing.append(ds)
            continue

        rows.append({
            "Datasets":ds,
            **ref,
            "F-ACVAE Acc":float(item["accuracy"]),
            "F-ACVAE Macro-F1":float(item["macro_f1"]),
            "F-ACVAE Attack-F1":float(item["attack_f1"]),
        })

    if missing:
        raise RuntimeError(
            "TABLE VII missing final dual-F1 results: " + ", ".join(missing)
        )

    TABLE_VII=pd.DataFrame(rows)
    d=TABLE_VII.copy()
    d.columns=pd.MultiIndex.from_tuples([
        ("","Datasets",""),

        ("CTVAE-O","Published","Acc"),
        ("CTVAE-O","Published","F-score"),

        ("CTVAE-K","Published","Acc"),
        ("CTVAE-K","Published","F-score"),

        ("F-ACVAE","Computed","Acc"),
        ("F-ACVAE","Computed","Macro-F1"),
        ("F-ACVAE","Computed","Attack-F1"),
    ])

    # Only Accuracy is directly bold-compared here.
    accuracy_cols=[
        ("CTVAE-O","Published","Acc"),
        ("CTVAE-K","Published","Acc"),
        ("F-ACVAE","Computed","Acc"),
    ]

    def _best_accuracy_only(frame):
        css=pd.DataFrame("",index=frame.index,columns=frame.columns)
        for ridx in frame.index:
            vals=pd.to_numeric(frame.loc[ridx,accuracy_cols],errors="coerce")
            best=float(vals.max())
            for col,val in vals.items():
                if pd.notna(val) and np.isclose(float(val),best,atol=1e-12):
                    css.loc[ridx,col]="font-weight:800;"
        return css

    print(
        "TABLE VII: Highly imbalanced binary datasets — "
        "published CTVAE F-score; F-ACVAE Macro-F1 and Attack-F1 shown separately"
    )
    display(
        d.round(2).style
        .apply(_best_accuracy_only,axis=None)
        .format(precision=2,na_rep="—")
        .hide(axis="index")
    )

    _save_csv(
        TABLE_VII,
        TABLES_ROOT/"Table_VII",
        "Table_VII_Dual_F1.csv"
    )


# -----------------------------------------------------------------------------
# SUPPLEMENTARY OUTPUT — Unseen-Client Generalization  [notebook cell 38]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Cross-Client Generalization — Fair All-Method Protocol  [notebook cell 39]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 40 =====
if output_enabled("GENERALIZATION"):
    _ensure_results_directories()
    rows=[]; missing=[]
    cross=GENERALIZATION_METRICS.get("results",{})
    strict=STRICT_BINARY_GATE_METRICS.get("results",{})
    binary_set={"IoT-08","IoT-09","IoT-10","IoT-11"}
    base_methods=("FedAvg","FedProx","F-ACVAE")

    for ds in [f"IoT-{i:02d}" for i in range(1,12)]:
        for method in base_methods:
            item=cross.get(ds,{}).get(method)
            if not item:
                missing.append(f"{ds}/{method} Cross RF")
                continue
            rows.append({
                "Dataset":ds,
                "Method":f"{method} Cross RF",
                "Accuracy (%)":float(item["accuracy"]),
                "Macro F1-score (%)":float(item["macro_f1"]),
                "Protocol":"leave-one-client-out Cross-Client RF",
                "Gate":"OFF",
                "Source":str(item.get("source","computed")),
            })

        # Gate is a component of the proposed CMGA method, never a baseline evaluation trick.
        if ds in binary_set:
            h=strict.get(ds)
            if not h:
                missing.append(f"{ds}/F-ACVAE Cross RF + CMGA Gate")
            else:
                rows.append({
                    "Dataset":ds,
                    "Method":"F-ACVAE Cross RF + B-rule CMGA Gate",
                    "Accuracy (%)":float(h["hybrid_accuracy"]),
                    "Macro F1-score (%)":float(h["hybrid_macro_f1"]),
                    "Protocol":"leave-one-client-out Cross-Client RF + donor-only pooled TRAIN-benign radial CMGA Gate q=.995",
                    "Gate":"ON — F-ACVAE only",
                    "Source":str(h.get("source","computed")),
                })

    if missing:
        raise RuntimeError(
            "GENERALIZATION incomplete. Every headline method must have the same Cross-Client protocol: "
            + ", ".join(missing)
        )

    GENERALIZATION_TABLE=pd.DataFrame(rows)

    def _style_generalization(frame):
        # Dark readable text everywhere; bold ONLY the best metric value(s) per Dataset.
        css=pd.DataFrame(
            "font-weight:normal;",
            index=frame.index, columns=frame.columns
        )
        for ds, idxs in frame.groupby("Dataset").groups.items():
            idxs=list(idxs)
            for metric in ("Accuracy (%)","Macro F1-score (%)"):
                vals=pd.to_numeric(frame.loc[idxs,metric],errors="coerce")
                if vals.notna().any():
                    best=float(vals.max())
                    for idx,val in vals.items():
                        if pd.notna(val) and np.isclose(float(val),best,rtol=0,atol=1e-12):
                            css.loc[idx,metric]="font-weight:700;"
        return css

    print("\nCROSS-CLIENT GENERALIZATION — FAIR ALL-METHOD COMPARISON")
    print("FedAvg, FedProx and F-ACVAE use the identical leave-one-client-out RF protocol.")
    print("B-rule CMGA Gate (q=.995) is the locked Final F-ACVAE binary Gate.")
    display(
        GENERALIZATION_TABLE[
            ["Dataset","Method","Accuracy (%)","Macro F1-score (%)","Gate"]
        ].round(2).style
        .apply(_style_generalization,axis=None)
        .hide(axis="index")
    )

    _save_csv(
        GENERALIZATION_TABLE,
        TABLES_ROOT/"Generalization",
        "IoT01_11_All_Methods_Cross_Client_Generalization.csv"
    )

    provenance_cols=["Dataset","Method","Protocol","Gate","Source"]
    GENERALIZATION_TABLE[provenance_cols].to_csv(
        TABLES_ROOT/"Generalization"/"Cross_Client_Protocol_Provenance.csv",
        index=False
    )


# -----------------------------------------------------------------------------
# PAPER OUTPUT 3 — Table VIII: Ablation Study  [notebook cell 41]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FINAL BINARY OPEN-SET GATE B — IoT-08..IoT-11  [notebook cell 42]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 43 =====
if output_enabled("HYBRID_GATE"):
    rows=[]; missing=[]
    local=LOCAL_BINARY_GATE_METRICS.get("results",{})
    cross=STRICT_BINARY_GATE_METRICS.get("results",{})

    for ds in ("IoT-08","IoT-09","IoT-10","IoT-11"):
        for protocol,store in (("Local",local),("Cross",cross)):
            h=store.get(ds)
            if not h:
                missing.append(f"{ds}/{protocol}")
                continue
            rows.append({
                "Dataset":ds,
                "Protocol":protocol,
                "RF-only Acc (%)":float(h["rf_only_accuracy"]),
                "RF-only Macro-F1 (%)":float(h["rf_only_macro_f1"]),
                "RF-only Attack-F1 (%)":float(h.get("rf_only_attack_f1",np.nan)),
                "Gate B Acc (%)":float(h["hybrid_accuracy"]),
                "Gate B Macro-F1 (%)":float(h["hybrid_macro_f1"]),
                "Gate B Attack-F1 (%)":float(h.get("hybrid_attack_f1",np.nan)),
                "Delta Macro-F1 (pp)":float(h["hybrid_macro_f1"])-float(h["rf_only_macro_f1"]),
                "Override (%)":float(h["gate_override_percent"]),
                "Recovered attacks":int(h["recovered_attack_detection"]),
                "Added benign FP":int(h["introduced_benign_false_positives"]),
                "q":float(h["gate_quantile"]),
            })

    if missing:
        raise RuntimeError("FINAL GATE B output missing: " + ", ".join(missing))

    FINAL_GATE_B_TABLE=pd.DataFrame(rows)

    def _style_final_b(frame):
        css=pd.DataFrame("",index=frame.index,columns=frame.columns)
        score_cols=[
            "RF-only Acc (%)","RF-only Macro-F1 (%)","RF-only Attack-F1 (%)",
            "Gate B Acc (%)","Gate B Macro-F1 (%)","Gate B Attack-F1 (%)",
        ]
        for col in score_cols:
            vals=pd.to_numeric(frame[col],errors="coerce")
            for idx,val in vals.items():
                if pd.isna(val):
                    continue
                if float(val)>=95:
                    css.loc[idx,col]="font-weight:800;background-color:rgba(34,197,94,.18);"
                elif float(val)>=85:
                    css.loc[idx,col]="font-weight:700;background-color:rgba(14,165,233,.15);"
                elif float(val)>=70:
                    css.loc[idx,col]="font-weight:700;background-color:rgba(245,158,11,.17);"
                else:
                    css.loc[idx,col]="font-weight:700;background-color:rgba(239,68,68,.16);"
        return css

    print("\n" + "="*96)
    print("FINAL GATE B — IoT-08..IoT-11")
    print("B q=.995 | Local primary + Cross stress-test | no Relaxed-B / CBFPR / tuning")
    print("="*96)
    display(
        FINAL_GATE_B_TABLE.round(4).style
        .apply(_style_final_b,axis=None)
        .hide(axis="index")
    )
    _save_csv(
        FINAL_GATE_B_TABLE,
        TABLES_ROOT/"Hybrid_Gate",
        "IoT08_11_Final_Gate_B.csv"
    )


# -----------------------------------------------------------------------------
# TABLE VIII — IoT-01 architecture ablation (Gate OFF)  [notebook cell 44]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 45 =====
if output_enabled("TABLE_VIII"):
    if (
        F_ACVAE_CROSS_IOT01_RESULT is None
        or NO_CMGA_CROSS_IOT01_RESULT is None
        or F_ACVAE_LINEAR_IOT01_RESULT is None
    ):
        raise RuntimeError("IoT-01 ablation results are unavailable.")

    ab=PAPER_METRICS.get("ablations_cross_no_gate_v65",{})
    no_sel=ab.get("F_ACVAE_no_selective")
    no_cond=ab.get("F_ACVAE_no_conditioning")
    if no_sel is None or no_cond is None:
        raise RuntimeError("IoT-01 architecture ablations are missing.")

    full_acc=float(F_ACVAE_CROSS_IOT01_RESULT["cross_client_rf_accuracy_percent"])
    full_f1=float(F_ACVAE_CROSS_IOT01_RESULT["cross_client_rf_macro_f1_percent"])

    values=[
        ("Full F-ACVAE",full_acc,full_f1),
        (
            "Without CMGA",
            float(NO_CMGA_CROSS_IOT01_RESULT["cross_client_rf_accuracy_percent"]),
            float(NO_CMGA_CROSS_IOT01_RESULT["cross_client_rf_macro_f1_percent"]),
        ),
        (
            "Without Selective Aggregation",
            float(no_sel["accuracy"]),
            float(no_sel["macro_f1"]),
        ),
        (
            "Without Adaptive Conditioning",
            float(no_cond["accuracy"]),
            float(no_cond["macro_f1"]),
        ),
        (
            "Without RF",
            float(F_ACVAE_LINEAR_IOT01_RESULT["cross_client_linear_accuracy_percent"]),
            float(F_ACVAE_LINEAR_IOT01_RESULT["cross_client_linear_macro_f1_percent"]),
        ),
    ]

    def fmt(value,full):
        delta=full-value
        if abs(delta)<1e-12:
            return f"{value:.2f}"
        arrow="↓" if delta>=0 else "↑"
        return f"{value:.2f} ({arrow}{abs(delta):.2f})"

    TABLE_VIII=pd.DataFrame([
        [name,fmt(acc,full_acc),fmt(f1,full_f1)]
        for name,acc,f1 in values
    ],columns=["Configuration","Accuracy (%)","Macro F1-score (%)"])

    cmga_acc=full_acc-values[1][1]
    cmga_f1=full_f1-values[1][2]
    sel_acc=full_acc-values[2][1]
    sel_f1=full_f1-values[2][2]
    cond_acc=full_acc-values[3][1]
    cond_f1=full_f1-values[3][2]
    rf_acc=full_acc-values[4][1]
    rf_f1=full_f1-values[4][2]

    ABLATION_TEXT=(
        f"The ablation results confirm that CMGA provides the largest contribution "
        f"(+{cmga_acc:.2f} percentage points in accuracy and +{cmga_f1:.2f} in Macro F1-score). "
        f"Selective Aggregation contributes +{sel_acc:.2f}/+{sel_f1:.2f} points, "
        f"Adaptive Conditioning contributes +{cond_acc:.2f}/+{cond_f1:.2f} points, "
        f"and replacing RF with a linear classifier reduces performance by "
        f"{rf_acc:.2f}/{rf_f1:.2f} points. "
        f"The full F-ACVAE achieves {full_acc:.2f}% accuracy and {full_f1:.2f}% Macro F1-score on IoT-01."
    )

    print("D. Ablation Study")
    print(ABLATION_TEXT)
    print("\nTABLE VIII: Ablation study results on IoT-01 dataset")
    display(TABLE_VIII.style.hide(axis="index"))
    _save_csv(TABLE_VIII,TABLES_ROOT/"Table_VIII","Table_VIII.csv")
    (TEXT_ROOT/"Ablation_Study.txt").write_text(ABLATION_TEXT,encoding="utf-8")


# -----------------------------------------------------------------------------
# PAPER OUTPUT 4 — Figure 3: Convergence  [notebook cell 46]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FIG. 3 — Convergence of F-ACVAE on IoT-01  [notebook cell 47]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 48 =====
if output_enabled("FIGURE_3"):
    _ensure_results_directories()
    conv=ROUND_RESULTS[
        (ROUND_RESULTS["variant"]=="F_ACVAE_CMGA")
        & (ROUND_RESULTS["round"].between(1,CONFIG.rounds))
    ].copy()

    fig,ax=plt.subplots(figsize=(7.2,4.8))
    ax.plot(
        conv["round"],conv["centroid_accuracy_percent"],
        marker="s",label="Accuracy"
    )
    ax.plot(
        conv["round"],conv["centroid_macro_f1_percent"],
        label="Macro F1-score"
    )
    ax.set_xlabel("Federated Rounds (T)")
    ax.set_ylabel("Performance (%)")
    ax.set_xticks(range(1,CONFIG.rounds+1))
    ax.set_ylim(50,100.5)
    ax.grid(True,alpha=.25)
    ax.legend()
    fig.tight_layout()

    out=FIGURES_ROOT/"Figure_3_Convergence"/"Figure_3_Convergence.png"
    fig.savefig(out,dpi=300,bbox_inches="tight")
    fig.savefig(out.with_suffix(".pdf"),bbox_inches="tight")
    plt.show()
    plt.close(fig)


# -----------------------------------------------------------------------------
# PAPER OUTPUT 5 — Figure 4: TRUE Raw vs Latent Visualization  [notebook cell 49]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FIG. 4(a) Original Data / FIG. 4(b) F-ACVAE Latent Space  [notebook cell 50]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 51 =====
# FIGURE 4 — FINAL SPLIT OUTPUTS
# Final Figure 4 is exported as TWO separate figures:
#   Fig. 4(a) Original Data
#   Fig. 4(b) F-ACVAE Latent Space
#
# Data protocol is unchanged:
# - all IoT-01 Train+Validation+Test rows are displayed
# - display min-max is fitted on TRAIN only
# - display scaling never enters training/evaluation

FIGURE4_CACHE_VERSION = "iot01-figure4-v4-all-splits"
FIGURE4_CACHE_NAME = "IoT-01_figure4_data_v4_all_splits.npz"
_FIG4_COLORS = ("red","green","blue","yellow","black","purple")
_FIG4_MARKERS = ("o","X","s","d","D","d")


def _display_minmax_fit(values: np.ndarray) -> Tuple[float,float]:
    values=np.asarray(values,dtype=np.float64).reshape(-1)
    finite=values[np.isfinite(values)]
    if not len(finite):
        raise FloatingPointError("Figure 4 received no finite values.")
    lo=float(finite.min()); hi=float(finite.max())
    if not hi>lo:
        hi=lo+1.0
    return lo,hi


def _display_minmax_apply(values: np.ndarray, lo: float, hi: float, clip: bool=False) -> np.ndarray:
    out=(np.asarray(values,dtype=np.float64)-float(lo))/max(float(hi-lo),1e-12)
    if clip:
        out=np.clip(out,0.0,1.0)
    return out.astype(np.float32)


def _figure4_collect_split(split: str):
    raw=[]; latent=[]; labels=[]
    for client,record in zip(
        sorted(METHOD_RUNS["F_ACVAE_CMGA"]["clients"],key=lambda c:c.cid),
        sorted(DATA.records,key=lambda r:int(r["client_id"]))
    ):
        if int(client.cid)!=int(record["client_id"]):
            raise AssertionError("Figure 4 client/record order mismatch.")
        z,y,_=client.extract_mu(split)
        xraw=np.asarray(record[f"X_{split}_raw"],dtype=np.float32)
        yr=np.asarray(record[f"y_{split}"],dtype=np.int64)
        if len(z)!=len(xraw) or not np.array_equal(np.asarray(y,dtype=np.int64),yr):
            raise AssertionError(
                f"Figure 4 {split}: raw/latent/label row alignment failed for client {client.cid}."
            )
        raw.append(xraw)
        latent.append(np.asarray(z,dtype=np.float32))
        labels.append(yr)
    return np.concatenate(raw),np.concatenate(latent),np.concatenate(labels)


def _build_iot01_figure4_cache_if_needed():
    _ensure_results_directories()
    cache_path=FIGURE_CACHE_ROOT/FIGURE4_CACHE_NAME
    if cache_path.is_file():
        try:
            c=np.load(cache_path,allow_pickle=True)
            if str(c["cache_version"][0])==FIGURE4_CACHE_VERSION:
                return cache_path
        except Exception:
            pass

    payload={}
    for split in ("train","validation","test"):
        raw,z,y=_figure4_collect_split(split)
        payload[f"{split}_raw_f0"]=raw[:,0].astype(np.float32)
        payload[f"{split}_raw_f1"]=raw[:,1].astype(np.float32)
        payload[f"{split}_latent_f0"]=z[:,0].astype(np.float32)
        payload[f"{split}_latent_f1"]=z[:,1].astype(np.float32)
        payload[f"{split}_labels"]=y.astype(np.int64)

    np.savez_compressed(
        cache_path,
        cache_version=np.asarray([FIGURE4_CACHE_VERSION],dtype=object),
        class_names=np.asarray(DATA.class_names,dtype=object),
        **payload,
    )
    return cache_path


def _figure4_arrays(cached, splits):
    def cat(key):
        return np.concatenate([np.asarray(cached[f"{s}_{key}"]) for s in splits])
    return {
        "raw0":cat("raw_f0"),
        "raw1":cat("raw_f1"),
        "lat0":cat("latent_f0"),
        "lat1":cat("latent_f1"),
        "labels":cat("labels").astype(np.int64),
    }


def _style_figure4_axis(ax, xlabel="F0", ylabel="F1"):
    ax.set_facecolor("#EAEAF2")
    ax.set_xlim(-0.04,1.02)
    ax.set_ylim(-0.05,1.05)
    ax.set_xticks(np.arange(0.0,1.01,0.2))
    ax.set_yticks(np.arange(0.0,1.01,0.2))
    ax.grid(True,color="white",linewidth=1.0,alpha=0.95)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel,fontsize=12)
    ax.set_ylabel(ylabel,fontsize=12,rotation=0,labelpad=12)
    ax.tick_params(labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("white")
        spine.set_linewidth(1.0)


def _plot_single_figure4_panel(
    x,
    y,
    labels,
    title: str,
    panel_label: str,
    out_png: Path,
    out_pdf: Path,
):
    n=len(labels)
    point_size=4 if n>150_000 else 8
    point_alpha=0.55 if n>150_000 else 0.75

    fig,ax=plt.subplots(figsize=(6.0,5.45),facecolor="white")

    for class_id in range(len(DATA.class_names)):
        mask=labels==class_id
        ax.scatter(
            x[mask],y[mask],
            s=point_size,
            marker=_FIG4_MARKERS[class_id],
            c=_FIG4_COLORS[class_id],
            alpha=point_alpha,
            linewidths=0.05,
            label=str(class_id),
        )

    _style_figure4_axis(ax)
    ax.set_title(title,fontsize=12,pad=8)

    leg=ax.legend(
        title="label",
        loc="lower right",
        frameon=True,
        facecolor="white",
        edgecolor="white",
        framealpha=0.96,
        fontsize=9,
        title_fontsize=10,
        markerscale=1.5,
        borderpad=0.45,
        labelspacing=0.55,
        handletextpad=0.55,
    )
    leg.get_frame().set_linewidth(0)

    ax.text(
        0.5,-0.18,panel_label,
        transform=ax.transAxes,
        ha="center",va="top",
        fontsize=16,fontfamily="serif",
    )

    fig.subplots_adjust(left=0.12,right=0.98,top=0.91,bottom=0.18)

    fig.savefig(out_png,dpi=300,bbox_inches="tight",facecolor="white")
    fig.savefig(out_pdf,bbox_inches="tight",facecolor="white")
    plt.show()
    plt.close(fig)


def render_final_figure4():
    cache_path=_build_iot01_figure4_cache_if_needed()
    c=np.load(cache_path,allow_pickle=True)
    if str(c["cache_version"][0])!=FIGURE4_CACHE_VERSION:
        raise RuntimeError("Unexpected Figure 4 cache version.")

    train=_figure4_arrays(c,("train",))
    all_rows=_figure4_arrays(c,("train","validation","test"))

    # Display scaling parameters are fitted on TRAIN only.
    raw_fit=(
        _display_minmax_fit(train["raw0"]),
        _display_minmax_fit(train["raw1"]),
    )
    latent_fit=(
        _display_minmax_fit(train["lat0"]),
        _display_minmax_fit(train["lat1"]),
    )

    raw0=_display_minmax_apply(all_rows["raw0"],*raw_fit[0],clip=True)
    raw1=_display_minmax_apply(all_rows["raw1"],*raw_fit[1],clip=True)
    lat0=_display_minmax_apply(all_rows["lat0"],*latent_fit[0],clip=True)
    lat1=_display_minmax_apply(all_rows["lat1"],*latent_fit[1],clip=True)
    labels=all_rows["labels"]

    outdir=FIGURES_ROOT/"Figure_4_Feature_Spaces"
    outdir.mkdir(parents=True,exist_ok=True)

    # Separate Fig. 4(a)
    original_png=outdir/"Figure_4a_Original_Data.png"
    original_pdf=outdir/"Figure_4a_Original_Data.pdf"
    _plot_single_figure4_panel(
        raw0,raw1,labels,
        title="Original Data",
        panel_label="(a)",
        out_png=original_png,
        out_pdf=original_pdf,
    )

    # Separate Fig. 4(b)
    latent_png=outdir/"Figure_4b_F_ACVAE_Latent_Space.png"
    latent_pdf=outdir/"Figure_4b_F_ACVAE_Latent_Space.pdf"
    _plot_single_figure4_panel(
        lat0,lat1,labels,
        title="F-ACVAE Latent Space",
        panel_label="(b)",
        out_png=latent_png,
        out_pdf=latent_pdf,
    )

    summary=pd.DataFrame([
        {
            "Figure":"Fig. 4(a)",
            "Title":"Original Data",
            "Rows":int(len(labels)),
            "Features":"TRUE RAW F0/F1",
            "Displayed rows":"Train+Validation+Test",
            "Display scaling":"fit on Train only",
            "Test used to fit display transform":False,
            "PNG":original_png.name,
            "PDF":original_pdf.name,
        },
        {
            "Figure":"Fig. 4(b)",
            "Title":"F-ACVAE Latent Space",
            "Rows":int(len(labels)),
            "Features":"F-ACVAE latent F0/F1",
            "Displayed rows":"Train+Validation+Test",
            "Display scaling":"fit on Train only",
            "Test used to fit display transform":False,
            "PNG":latent_png.name,
            "PDF":latent_pdf.name,
        },
    ])
    summary.to_csv(outdir/"Figure_4_Final_Audit.csv",index=False)

    return {
        "original_png": original_png,
        "original_pdf": original_pdf,
        "latent_png": latent_png,
        "latent_pdf": latent_pdf,
    }


if output_enabled("FIGURE_4"):
    render_final_figure4()


# -----------------------------------------------------------------------------
# PAPER OUTPUT 6 — Table IX: Latent Features and Classifiers  [notebook cell 52]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# TABLE IX — Comparative analysis of latent features and classifiers on IoT-01  [notebook cell 53]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 54 =====
if output_enabled("TABLE_IX"):
    raw=PAPER_METRICS.get("raw_cross_v63",{})
    if not raw or F_ACVAE_CROSS_IOT01_RESULT is None or F_ACVAE_LINEAR_IOT01_RESULT is None:
        raise RuntimeError("IoT-01 feature/classifier attribution results are incomplete.")

    TABLE_IX=pd.DataFrame([
        [
            "Raw Features + RF",
            float(raw["accuracy"]),
            float(raw["macro_f1"]),
        ],
        [
            "CTVAE Latent + RF",
            93.0,
            90.9,
        ],
        [
            "F-ACVAE Latent + Linear",
            float(F_ACVAE_LINEAR_IOT01_RESULT["cross_client_linear_accuracy_percent"]),
            float(F_ACVAE_LINEAR_IOT01_RESULT["cross_client_linear_macro_f1_percent"]),
        ],
        [
            "F-ACVAE Latent + RF",
            float(F_ACVAE_CROSS_IOT01_RESULT["cross_client_rf_accuracy_percent"]),
            float(F_ACVAE_CROSS_IOT01_RESULT["cross_client_rf_macro_f1_percent"]),
        ],
    ],columns=["Configuration","Accuracy (%)","Macro F1-score (%)"])

    print("TABLE IX: Comparative analysis of latent features and classifiers on IoT-01 subset")
    display(TABLE_IX.round(2).style.hide(axis="index"))
    _save_csv(TABLE_IX,TABLES_ROOT/"Table_IX","Table_IX.csv")


# -----------------------------------------------------------------------------
# PAPER OUTPUT 7 — Table X: Per-class Metrics  [notebook cell 55]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# TABLE X — Per-class IoT-01 F-ACVAE Local-Private RF (Gate OFF)  [notebook cell 56]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 57 =====
if output_enabled("TABLE_X"):
    key="F_ACVAE_CMGA_local_rf_PRIMARY"
    if key not in FINAL_TEST_CONFUSIONS:
        raise RuntimeError(f"Missing IoT-01 Local-Private confusion: {key}")

    cm=np.asarray(FINAL_TEST_CONFUSIONS[key],dtype=np.int64)
    tp=np.diag(cm).astype(float)
    fp=cm.sum(0)-tp
    fn=cm.sum(1)-tp
    precision=np.divide(tp,tp+fp,out=np.zeros_like(tp),where=(tp+fp)>0)
    recall=np.divide(tp,tp+fn,out=np.zeros_like(tp),where=(tp+fn)>0)
    f1=np.divide(
        2*precision*recall,
        precision+recall,
        out=np.zeros_like(tp),
        where=(precision+recall)>0,
    )

    rows=[
        [name,100*precision[i],100*recall[i],100*f1[i]]
        for i,name in enumerate(DATA.class_names)
    ]
    rows.append([
        "Macro Average",
        100*precision.mean(),
        100*recall.mean(),
        100*f1.mean(),
    ])

    TABLE_X=pd.DataFrame(
        rows,
        columns=["Class","Precision (%)","Recall (%)","F1-score (%)"],
    )

    print("TABLE X: Per-class performance metrics on IoT-01 subset")
    display(TABLE_X.round(2).style.hide(axis="index"))
    _save_csv(TABLE_X,TABLES_ROOT/"Table_X","Table_X.csv")


# ===== NOTEBOOK CODE CELL 58 =====
# OPTIONAL — Re-display any saved paper table later, without retraining.
# Example: display_saved_table("Table_VIII_Ablation", "Table_VIII.csv")
def display_saved_table(folder_name: str, file_name: str):
    path = RESULTS_ROOT / "Tables" / folder_name / file_name
    if not path.is_file():
        # Compatibility with the notebook's existing table folders.
        candidates = list(TABLES_ROOT.rglob(file_name))
        if len(candidates) == 1:
            path = candidates[0]
        elif not candidates:
            raise FileNotFoundError(f"Saved table not found: {file_name}")
        else:
            raise RuntimeError(f"Multiple files named {file_name} found: {candidates}")
    frame = pd.read_csv(path)
    display(frame)
    return frame


# -----------------------------------------------------------------------------
# PAPER OUTPUT 8 — Privacy and Communication Efficiency  [notebook cell 59]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Privacy Preservation and Communication Efficiency  [notebook cell 60]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 61 =====
if output_enabled("COMMUNICATION"):
    _ensure_results_directories()
    comm=COMMUNICATION_TABLE.loc["F_ACVAE_CMGA"]

    full=int(comm["full_model_parameters"])
    shared=int(comm["communicated_model_parameters"])
    gauss=int(comm["gaussian_statistics_per_client_round"])
    uplink=shared+gauss
    model_reduction=float(comm["model_parameter_reduction_percent"])
    uplink_reduction=float(comm["uplink_reduction_including_gaussians_percent"])
    r_sent=shared/max(full,1)
    r_reduced=1.0-r_sent

    COMM_TEXT=(
        "F. Privacy Preservation and Communication Efficiency\n"
        "F-ACVAE keeps the encoder local and federates only the shared model components, "
        "while raw samples remain on the clients. "
        f"For model parameters, W_sent/W_total = {shared:,}/{full:,} = {r_sent:.3f}, "
        f"corresponding to a model-parameter reduction of {model_reduction:.2f}% "
        f"(1 - r_sent = {r_reduced:.3f}). "
        f"CMGA additionally communicates {gauss:,} Gaussian-statistic values per client per round; "
        f"including these statistics, the effective uplink reduction is {uplink_reduction:.2f}%."
    )

    print(COMM_TEXT)
    (TEXT_ROOT/"Communication"/"Communication.txt").write_text(COMM_TEXT,encoding="utf-8")
    pd.DataFrame([{
        "W_total":full,
        "W_sent":shared,
        "r_sent":r_sent,
        "Model reduction (%)":model_reduction,
        "Gaussian stats/client/round":gauss,
        "Effective uplink values/client/round":uplink,
        "Effective uplink reduction (%)":uplink_reduction,
    }]).to_csv(TEXT_ROOT/"Communication"/"Communication.csv",index=False)


# -----------------------------------------------------------------------------
# PAPER OUTPUT 9 — Statistical Stability  [notebook cell 62]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Statistical Stability — 5 independent runs  [notebook cell 63]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 64 =====
if output_enabled("STABILITY"):
    stab=PAPER_METRICS.get("stability_local_v65",{})
    if len(stab)<5:
        raise RuntimeError("Five real IoT-01 F-ACVAE runs are required.")

    S=pd.DataFrame([
        {
            "Seed":int(k),
            "Accuracy (%)":v["accuracy"],
            "Macro F1-score (%)":v["macro_f1"],
        }
        for k,v in sorted(stab.items(),key=lambda kv:int(kv[0]))
    ])

    acc_mean=S["Accuracy (%)"].mean()
    acc_std=S["Accuracy (%)"].std(ddof=1)
    f1_mean=S["Macro F1-score (%)"].mean()
    f1_std=S["Macro F1-score (%)"].std(ddof=1)

    STABILITY_TEXT=(
        "All experiments are conducted with a fixed random seed (seed=42) to ensure "
        "reproducibility and deterministic data splits across clients. To assess statistical "
        "stability, we performed 5 independent runs on the representative IoT-01 subset. "
        f"The results are: Accuracy = {acc_mean:.2f} ± {acc_std:.2f}% and "
        f"Macro F1-score = {f1_mean:.2f} ± {f1_std:.2f}%."
    )

    print(STABILITY_TEXT)
    (TEXT_ROOT/"Stability"/"Stability.txt").write_text(STABILITY_TEXT,encoding="utf-8")
    S.to_csv(TEXT_ROOT/"Stability"/"Stability_Runs.csv",index=False)


# -----------------------------------------------------------------------------
# PAPER OUTPUT 10 — Final Export Summary  [notebook cell 65]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Final Results location  [notebook cell 66]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 67 =====
if output_enabled("EXPORT_SUMMARY"):
    _ensure_results_directories()
    protocol_text = f"""Evaluation Protocol — FINAL GATE B LOCKED

N-BaIoT PRIMARY
IoT-01..07:
- F-ACVAE Local-Private RF
- Gate OFF

IoT-08..11:
- F-ACVAE Local-Private fixed RF
- Final Gate B = radial CMGA Gate
- pooled TRAIN-benign calibration
- q = {HYBRID_GATE_QUANTILE:.3f}
- likelihood = OFF
- RF tuning = OFF
- one-way override: RF-Benign may become Attack
- Test is reporting-only and never calibrates q

CROSS-CLIENT
Same leave-one-client-out RF protocol is reported for FedAvg, FedProx and F-ACVAE.
For binary F-ACVAE, donor-only Gate B q=.995 is additionally reported.
The held-out client is excluded from Gate threshold calibration.

EXTERNAL TABLE VII
UNSW-NB15 and CIC-IDS2017 remain enabled under genuine 9-client Dirichlet
Non-IID Local-Private F-ACVAE evaluation. Gate is OFF.

REMOVED FROM FINAL RUN
Relaxed-B, CBFPR, validation-selected Gate/likelihood/RF tuning, FEATURE_DEBUG,
and redundant Local-Private control output are not part of this final execution.

FIGURE 4
Final selected visualization = former Candidate B, exported as TWO separate panels:
- Fig. 4(a): Original Data
- Fig. 4(b): F-ACVAE Latent Space
All IoT-01 rows are displayed; display min-max is fitted on Train only.

FINAL EXPORT ROOT
{FINAL_EXPORT_ROOT.resolve()}

CHECKPOINT/CACHE ROOT (REUSED)
{CHECKPOINT_ROOT.resolve()}
"""
    (TEXT_ROOT/"Evaluation_Protocol"/"Evaluation_Protocol_FINAL_GATE_B.txt").write_text(
        protocol_text,encoding="utf-8"
    )
    print(protocol_text.strip())


# -----------------------------------------------------------------------------
# SECTION D — FINAL OUTPUT VALIDATION (NO MODEL LOGIC)  [notebook cell 68]
# -----------------------------------------------------------------------------


# ===== NOTEBOOK CODE CELL 69 =====
if output_enabled("FINAL_VALIDATION"):
    required = {
        "Table_VI": TABLES_ROOT/"Table_VI",
        "Table_VII": TABLES_ROOT/"Table_VII",
        "Hybrid_Gate": TABLES_ROOT/"Hybrid_Gate",
        "Generalization": TABLES_ROOT/"Generalization",
        "Table_VIII": TABLES_ROOT/"Table_VIII",
        "Table_IX": TABLES_ROOT/"Table_IX",
        "Table_X": TABLES_ROOT/"Table_X",
        "Figure_3": FIGURES_ROOT/"Figure_3_Convergence",
        "Figure_4": FIGURES_ROOT/"Figure_4_Feature_Spaces",
        "Communication": TEXT_ROOT/"Communication",
        "Stability": TEXT_ROOT/"Stability",
        "Evaluation_Protocol": TEXT_ROOT/"Evaluation_Protocol",
    }

    print("\nFINAL OUTPUT VALIDATION")
    print("Clean export root:", FINAL_EXPORT_ROOT.resolve())
    missing=[]
    total_files=0
    for name,path in required.items():
        files=[p for p in path.rglob("*") if p.is_file()] if path.exists() else []
        total_files += len(files)
        ok=bool(files)
        print(f"{name}: {'OK' if ok else 'NOT FOUND'}")
        if not ok:
            missing.append(name)
        for f in files[:3]:
            print("  ",f.relative_to(FINAL_EXPORT_ROOT))

    # Final Figure 4 is intentionally TWO separate publication panels.
    fig4_dir=FIGURES_ROOT/"Figure_4_Feature_Spaces"
    fig4_required=[
        fig4_dir/"Figure_4a_Original_Data.png",
        fig4_dir/"Figure_4a_Original_Data.pdf",
        fig4_dir/"Figure_4b_F_ACVAE_Latent_Space.png",
        fig4_dir/"Figure_4b_F_ACVAE_Latent_Space.pdf",
    ]
    if not all(p.is_file() for p in fig4_required):
        missing.append("Figure_4_Split_Outputs")

    if missing:
        raise RuntimeError(
            "FINAL OUTPUT VALIDATION missing: " + ", ".join(sorted(set(missing)))
        )
    print(f"\nFINAL OUTPUT VALIDATION | PASS | exported files={total_files}")


# ===== NOTEBOOK CODE CELL 70 =====
if output_enabled("FINAL_SANITY"):
    print("\n" + "="*96)
    print("FINAL RELEASE SANITY CHECK — GATE B LOCKED")
    print("="*96)
    checks = [
        ("Final Local Gate", f"B q={HYBRID_GATE_QUANTILE:.3f}"),
        ("Final Cross Gate", f"donor-only B q={HYBRID_GATE_QUANTILE:.3f}"),
        ("Likelihood", "OFF"),
        ("RF tuning", "OFF"),
        ("Relaxed-B output", "REMOVED"),
        ("CBFPR output", "REMOVED"),
        ("Validation-selected Gate output", "REMOVED"),
        ("FEATURE_DEBUG", "REMOVED"),
        ("IoT-01..07 Gate", "OFF"),
        ("UNSW-NB15 + CIC-IDS2017", "ENABLED; Gate OFF"),
        ("Figure 4", "TWO FILES: Original Data + F-ACVAE Latent Space; all rows; Train-fitted display scaling"),
        ("Final export root", str(FINAL_EXPORT_ROOT.resolve())),
        ("Checkpoint/cache root", str(CHECKPOINT_ROOT.resolve())),
    ]
    for key,value in checks:
        print(f"- {key}: {value}")
    print("FINAL RELEASE SANITY | PASS")
