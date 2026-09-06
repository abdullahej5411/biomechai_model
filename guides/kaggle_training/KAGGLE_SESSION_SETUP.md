# BioMechAI — Kaggle Session Setup Cell
### Run this FIRST in every new Kaggle session, before any phase-specific task — no exceptions

## Why this exists

Kaggle sessions do not persist installed packages, cloned repositories, or patched files
between sessions — a new session (or a restarted kernel) starts from a clean base image every
time. The original production training run and Q11 verification already solved every
environment problem this project has, but that work only lasted for the session it was done
in. **Do not assume anything is "already installed" just because it worked in a previous
session — always run this cell fresh, even if you think nothing has changed.**

## Do NOT do this instead

Do not rediscover these fixes one at a time through trial and error (installing a package,
hitting the next error, installing another, patching a file, hitting a different error, and
so on). That is exactly what happened once already and cost significant time solving already-
solved problems. Every fix below is already known — apply them as a complete block, in order.

---

## The setup cell

```python
# ============================================================
# BioMechAI Kaggle Session Setup
# Run this complete cell first, every new session.
# ============================================================

# Step 1: Core dependencies, matching the already-verified working versions
# (PyTorch 2.10.0+cu128, CUDA 12.8, MMEngine 0.10.7, MMCV 2.2.0, MMAction2 v1.2.0,
#  Python 3.12.13 — confirmed working in the original production run)
!pip install -q mmengine==0.10.7
!pip install -q openmim
!mim install -q mmcv==2.2.0

# Step 2: Clone the REAL MMAction2 repo from GitHub.
# Do NOT `pip install mmaction` from PyPI — that package (version 0.5.0) is a deprecated,
# unrelated legacy package, not the framework this project uses. This was already
# discovered once; do not rediscover it.
!git clone --depth 1 https://github.com/open-mmlab/mmaction2.git /kaggle/working/mmaction2

# Step 3: Additional dependencies already confirmed necessary
!pip install -q einops timm

# Step 4: Apply the compatibility patches already documented from the original production
# run's "Technical Obstacles Encountered" section (in CLAUDE_FINAL_AUDIT_RESOLUTION.md or
# CLAUDE_FINAL_PRODUCTION_UPDATE.md). READ THAT SECTION NOW and apply every listed patch to
# this freshly-cloned copy, exactly as it was successfully applied before. At minimum this
# includes:
#   - The mmcv_maximum_version ceiling string patch in mmaction/__init__.py
#   - np.Inf -> np.inf replacements (NumPy 2.0 removed this alias) in whichever files were
#     identified before
#   - Disabling the conflicting multimodal Pillow/HuggingFace module import
#   - Any other patch listed in that section
# Do NOT skip reading that section and do NOT guess at these patches from scratch — they are
# already solved. If that document is not accessible in this environment, STOP and ask the
# user for it rather than rediscovering the patches through trial and error.

# Step 5: Editable install of the patched local copy
!pip install -q -e /kaggle/working/mmaction2 --no-deps

# Step 6: The PyTorch 2.6+ weights_only default-change patch — needed every session, since
# this patches torch.load's behavior at runtime, not a file on disk.
import functools, torch
_orig_torch_load = torch.load
torch.load = functools.partial(_orig_torch_load, weights_only=False)

# Step 7: Verify everything imports cleanly BEFORE running any phase-specific command
import sys
sys.path.insert(0, '/kaggle/working/mmaction2')
import mmengine, mmcv, mmaction

print("PyTorch:", torch.__version__, "| CUDA available:", torch.cuda.is_available())
print("MMEngine:", mmengine.__version__)
print("MMCV:", mmcv.__version__)
print("MMAction2:", mmaction.__version__)
print("Setup complete — safe to proceed to the phase-specific task.")
```

## If this cell errors

Apply the same Rule 1 as every phase: **stop, print the exact error, do not troubleshoot on
your own initiative.** If Step 4's referenced document isn't accessible, that's the most
likely failure point — report that specifically rather than guessing at the patches.

## What does NOT need this cell

Any phase whose task is pure Python with no MMAction2/GPU dependency (checking a `.pkl` file
with plain `pickle`, editing text in a config file without validating it loads) does not need
this full setup — only phases that actually run `test.py`/`train.py` or import `mmaction` do.
