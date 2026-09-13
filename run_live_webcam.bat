@echo off
title BioMechAI Dual-Timescale Live Webcam
echo ======================================================================
echo           BioMechAI Dual-Timescale Live Webcam Testing
echo ======================================================================
echo 1. Stand back so the camera sees your hips, knees, and ankles.
echo 2. Perform 1 or 2 clean squats.
echo 3. Watch the skeleton HUD track your angles and increment your Reps.
echo 4. Press 'q' or 'ESC' on the video window when finished.
echo ======================================================================
echo.
python tools/test_live_camera_dual_pipeline.py --source 0
pause
