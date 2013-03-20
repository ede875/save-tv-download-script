@rem Run Save.TV Download Script, producing a log file.
@setlocal enableextensions
@echo off

@rem Customize the following two directories:
set _LOCK_DIR=L:\share\save.tv
set _LOG_DIR=L:\share\save.tv

set _LOCK_FILE=%_LOCK_DIR%\download.lock
set _LOG_FILE=%_LOG_DIR%\download.log

if exist %_LOCK_FILE% goto lockexists

echo exists >%_LOCK_FILE%
set _STVDLD_FILE=%~d0%~p0stvDld.py
echo Running "%_STVDLD_FILE%" with log file %_LOG_FILE% ...
python "%_STVDLD_FILE%" >>%_LOG_FILE% 2>&1
del %_LOCK_FILE%
goto end

:lockexists
echo Error: Duplicate invocation; Lock file already exists: %_LOCK_FILE%

:end
