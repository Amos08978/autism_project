@echo off
echo 執行測試...
python -m pytest tests || echo 測試失敗或尚未建立測試
pause