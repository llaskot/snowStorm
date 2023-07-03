python --version
if %errorlevel% neq 0 (
	echo WAIT....
	start /wait python-3.9.7.exe /quiet InstallAllUsers=0 PrependPath=1 TargetDir="%~dp0Python"
	
)
timeout /t 3
refreshenv
start cmd /c instLibs.bat


