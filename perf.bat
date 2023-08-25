rmdir /s /q allureres
call python -m pytest tests/performans.py -rA -v -k test_main_path --alluredir=allureres 
pause 