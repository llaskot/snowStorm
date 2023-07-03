python --version
if %errorlevel% neq 0 (
	start /wait cmd /c "python-3.9.7-amd64.exe /quiet InstallAllUsers=0 PrependPath=1 TargetDir="%~dp0Python""
)
timeout /t 5
start /b cmd /c instLibs.bat