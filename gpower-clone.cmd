@echo off
setlocal
if defined GPOWER_HOME (set "runtime=%GPOWER_HOME%") else (set "runtime=%~dp0.run")
if not exist "%runtime%\.venv\Scripts\gpower-clone.exe" (
  echo Install first with install.ps1, or set GPOWER_HOME to the custom destination. 1>&2
  exit /b 3
)
"%runtime%\.venv\Scripts\gpower-clone.exe" %*
exit /b %errorlevel%
