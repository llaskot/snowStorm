rmdir /s /q allureres
setlocal enabledelayedexpansion
set "datetime=%date:/=-%_%time::=-%"
set "datetime=!datetime:,=!"
call python -m pytest tests/performansProd.py -rA -v -k test_main_path --alluredir=allureres --html=reportsProd/autoReport_!datetime!.html

pause 