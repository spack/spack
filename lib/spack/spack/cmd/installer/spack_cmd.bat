@ECHO OFF
setlocal EnableDelayedExpansion
:: (c) 2021 Lawrence Livermore National Laboratory
:: To use this file independently of Spack's installer, please copy this file, and the
:: 'scripts' directory, to be adjacent to your spack directory. You must have python on
:: your path for Spack to locate it.
:: source_dir -------- spack
::                |--- scripts
::                |--- spack_cmd.bat
pushd %~dp0
set spackinstdir=%CD%
popd

:: Check if Python is on the PATH
(for /f "delims=" %%F in ('where python.exe') do (set python_pf_ver=%%F) ) 2> NUL

if not defined python_pf_ver (
    :: If not, look for Python from the Spack installer
    :get_builtin
    (for /f "tokens=*" %%g in ('dir /b /a:d "!spackinstdir!\Python*"') do (
        set python_ver=%%g)) 2> NUL

    if not defined python_ver (
        echo Python was not found on your system.
        echo Please install Python or add Python to your PATH.
    ) else (
        set py_path=!spackinstdir!\!python_ver!
        set py_exe=!py_path!\python.exe
    )
    goto :exitpoint
) else (
    :: Python is already on the path
    set py_exe=!python_pf_ver!
    (for /F "tokens=* USEBACKQ" %%F in (
        `!py_exe! --version`) do (set "output=%%F")) 2>NUL
    if not "!output:Microsoft Store=!"=="!output!" goto :get_builtin
    goto :exitpoint
)
:exitpoint


for /f "tokens=*" %%g in ('dir /b /a:d "%spackinstdir%\spack*"') do (set spack_ver=%%g)
set "SPACK_ROOT=%spackinstdir%\%spack_ver%"

set "PATH=%spackinstdir%\scripts\;%PATH%"
if defined py_path (
    set "PATH=%py_path%;%PATH%"
)

if defined py_exe (
    "%py_exe%" "%spackinstdir%\scripts\haspywin.py"
    "%py_exe%" "%SPACK_ROOT%\bin\spack" external find python >NUL
)

set "EDITOR=notepad"

DOSKEY spacktivate=spack env activate $*

@echo **********************************************************************
@echo ** Spack Package Manager
@echo **********************************************************************

%comspec% /k
