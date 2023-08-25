rmdir /s /q allureres
setlocal enabledelayedexpansion
set "datetime=%date:/=-%_%time::=-%"
set "datetime=!datetime:,=!"
call python -m pytest tests/performans.py -rA -v -k test_main_path --alluredir=allureres --html=reports/autoReport_!datetime!.html

pause 