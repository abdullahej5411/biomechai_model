# BioMechAI Tools & Utilities

## Overview
This directory contains reusable utility scripts, automated data downloaders, extraction runners, and Google Drive cloud synchronization tools.

---

## File Inventory & Descriptions

### 1. Cloud & Google Drive Synchronization Tools
| File | Purpose |
|---|---|
| `get_drive_token.py` | Initiates the local OAuth2 browser consent flow with Google Cloud, generating the authorized `token.json` for Drive API access. |
| `verify_headless_oauth.py` | Validates silent token refresh in headless environments (e.g., Kaggle container) without requiring a browser window. |
| `clear_drive_test_checkpoints.py` | Utility script to clean up temporary test checkpoints from the Google Drive `BioMechAI_Checkpoints` folder. |
| `client_secret.json` | Google Cloud OAuth 2.0 client credentials (Client ID and secret). |
| `token.json` | Authorized OAuth user token (access token, refresh token, and scopes). |

### 2. Video & Landmark Processing Tools
| File | Purpose |
|---|---|
| `download_videos.py` | Utility to fetch video files from online sources / URLs for dataset construction. |
| `extract_landmarks.py` | Standalone script using MediaPipe Pose Landmarker Lite to extract 33 3D body keypoints from `.mp4` video files. |
| `pose_landmarker_lite.task` | Pre-trained MediaPipe Pose Landmarker model binary. |
| `cleanup_pipeline.py` | Master procedural pipeline runner coordinating multi-step processing and file management. |
| `train_model.py` | Standalone baseline model training script. |
