:: Copyright Spack Project Developers. See COPYRIGHT file for details.
::
:: SPDX-License-Identifier: (Apache-2.0 OR MIT)
::
:: Regenerate the checked-in PE/COFF fixtures used by
:: lib/spack/spack/test/relocate_windows.py
::
:: Usage (from a Visual Studio Developer Command Prompt):
::
::     generate_fixtures.bat [path-to-msvc-wrapper-repo]
::
:: The MSVC wrapper lives in its own repository, outside this one, so there is no
:: sensible default for where it is: pass the repo path as the first argument, or
:: set SPACK_MSVC_WRAPPER_ROOT. Either way it must already have a built
:: install\cl.exe -- `nmake cl.exe` in the wrapper repo produces it.
::
:: The fixtures produced here are deliberately tiny. Each PE is linked with
:: /NODEFAULTLIB and a custom entry point so nothing from the CRT is pulled in.
::
:: After running, `git status` should show updated .dll/.exe/.lib files in this
:: directory. The reported "resource" and "DLL:" values are what the test module's
:: expectation constants must match.

@echo off
setlocal enabledelayedexpansion

set "FIXTURE_DIR=%~dp0"
if "%FIXTURE_DIR:~-1%"=="\" set "FIXTURE_DIR=%FIXTURE_DIR:~0,-1%"
set "SRC_DIR=%FIXTURE_DIR%\src"

:: The wrapper pads every path it records to exactly this width (MAX_NAME_LEN in
:: the wrapper's src/utils.h, WRAPPER_NAME_LEN in relocate_windows.py). A path that
:: fits is recorded verbatim; a longer one falls back to its 8.3 short form. The
:: fixtures need one of each, so the staging layout is checked against this below
:: rather than assumed to work out.
set "NAME_LEN=143"

set "WRAPPER_ROOT=%~1"
if "%WRAPPER_ROOT%"=="" set "WRAPPER_ROOT=%SPACK_MSVC_WRAPPER_ROOT%"

if "%WRAPPER_ROOT%"=="" (
    echo ERROR: no MSVC wrapper repo given.
    echo Pass its path as the first argument, or set SPACK_MSVC_WRAPPER_ROOT.
    exit /b 1
)

if not exist "%WRAPPER_ROOT%\install\cl.exe" (
    echo ERROR: no built wrapper at "%WRAPPER_ROOT%\install\cl.exe"
    echo Build it first with `nmake cl.exe` in the wrapper repo.
    exit /b 1
)

where cl.exe >nul 2>&1 || (
    echo ERROR: cl.exe not on PATH. Run this from a VS Developer Command Prompt.
    exit /b 1
)

:: ---------------------------------------------------------------------------
:: Stage the wrapper. Its mode is selected by argv[0]'s basename, so cl / link /
:: relocate must each be a copy of the same binary under the right name.
:: ---------------------------------------------------------------------------
:: Stage at a fixed, neutral location rather than %TEMP%. The absolute staging
:: path is baked into every PE built here (as the spack resource) and recorded in
:: fixtures.txt, so using %TEMP% would embed whoever ran this last into the repo.
:: A literal C: keeps the recorded paths identical for everyone who regenerates.
:: Overriding this is supported but changes those recorded paths, so the
:: regenerated fixtures.txt must be committed along with the binaries.
set "STAGE=%SPACK_PE_FIXTURE_STAGE%"
if "%STAGE%"=="" set "STAGE=C:\spack-pe-fixtures"

call :strlen PLAIN_LEN "%STAGE%\build\tester.exe"
if %PLAIN_LEN% GTR %NAME_LEN% (
    echo ERROR: staging path is too long: %STAGE%
    echo   %STAGE%\build\tester.exe is %PLAIN_LEN% characters, over the wrapper's %NAME_LEN%.
    echo   calc.dll and tester.exe have to be recorded verbatim rather than as 8.3
    echo   short paths, or fixtures.txt will not match what the wrapper stored.
    echo   Use a shorter SPACK_PE_FIXTURE_STAGE.
    exit /b 1
)
if exist "%STAGE%" rmdir /s /q "%STAGE%"
mkdir "%STAGE%\bin" || exit /b 1
mkdir "%STAGE%\build" || exit /b 1

copy /y "%WRAPPER_ROOT%\install\cl.exe" "%STAGE%\bin\cl.exe" >nul || exit /b 1
copy /y "%WRAPPER_ROOT%\install\cl.exe" "%STAGE%\bin\link.exe" >nul || exit /b 1
copy /y "%WRAPPER_ROOT%\install\cl.exe" "%STAGE%\bin\relocate.exe" >nul || exit /b 1

:: Remember the real toolchain before we shadow it with the wrapper.
for /f "tokens=* usebackq" %%F in (`where cl.exe`) do (
    if not defined REAL_CL set "REAL_CL=%%F"
)
for /f "tokens=* usebackq" %%F in (`where link.exe`) do (
    if not defined REAL_LINK set "REAL_LINK=%%F"
)
for /f "tokens=* usebackq" %%F in (`where lib.exe`) do (
    if not defined REAL_LIB set "REAL_LIB=%%F"
)

:: The wrapper aborts with INVALID_ENVIRONMENT unless all of these are set.
set "SPACK_CC=%REAL_CL%"
set "SPACK_CXX=%REAL_CL%"
set "SPACK_LD=%REAL_LINK%"
set "SPACK_COMPILER_WRAPPER_PATH=%STAGE%\bin"
set "SPACK_DEBUG_LOG_DIR=%STAGE%"
set "SPACK_DEBUG_LOG_ID=FIXTURES"
set "SPACK_SHORT_SPEC=spack-pe-fixtures%%msvc"
set "SPACK_SYSTEM_DIRS=%PATH%"
set "SPACK_MANAGED_DIRS=%STAGE%"

set "WRAP_CL=%STAGE%\bin\cl.exe"
set "WRAP_LINK=%STAGE%\bin\link.exe"
set "RELOCATE=%STAGE%\bin\relocate.exe"

:: Keep the PEs minimal: no CRT, no default libs, custom entry points.
set "CFLAGS=/nologo /c /EHsc /GS- /Gs9999999 /O1 /I "%SRC_DIR%""
set "DLLFLAGS=/nologo /DLL /NODEFAULTLIB /ENTRY:DllEntry /OPT:REF /OPT:ICF /INCREMENTAL:NO"
set "EXEFLAGS=/nologo /NODEFAULTLIB /ENTRY:ExeEntry /OPT:REF /OPT:ICF /INCREMENTAL:NO"

pushd "%STAGE%\build" || exit /b 1

:: ---------------------------------------------------------------------------
:: calc.dll / calc.lib / tester.exe -- built through the wrapper, so calc.dll and
:: tester.exe carry the spack/SPACKRESOURCE resource and calc.lib records the
:: padded absolute path to calc.dll in its name field.
:: ---------------------------------------------------------------------------
echo === building calc.dll / calc.lib (wrapper) ===
"%WRAP_CL%" %CFLAGS% /DCALC_EXPORTS "%SRC_DIR%\calc.cxx" /Fo:calc.obj || goto :fail
"%WRAP_CL%" %CFLAGS% "%SRC_DIR%\entry.cxx" /Fo:entry.obj || goto :fail
"%WRAP_LINK%" %DLLFLAGS% calc.obj entry.obj /OUT:calc.dll /IMPLIB:calc.lib || goto :fail

echo === building tester.exe (wrapper) ===
"%WRAP_CL%" %CFLAGS% "%SRC_DIR%\main.cxx" /Fo:main.obj || goto :fail
"%WRAP_CL%" %CFLAGS% "%SRC_DIR%\exe_entry.cxx" /Fo:exe_entry.obj || goto :fail
"%WRAP_LINK%" %EXEFLAGS% main.obj exe_entry.obj calc.lib /OUT:tester.exe || goto :fail

:: ---------------------------------------------------------------------------
:: plain.dll -- stock link.exe, no wrapper. Must have NO spack resource.
:: ---------------------------------------------------------------------------
echo === building plain.dll (stock link.exe) ===
"%REAL_CL%" %CFLAGS% /DCALC_EXPORTS "%SRC_DIR%\calc.cxx" /Fo:plain_calc.obj || goto :fail
"%REAL_CL%" %CFLAGS% "%SRC_DIR%\entry.cxx" /Fo:plain_entry.obj || goto :fail
"%REAL_LINK%" %DLLFLAGS% plain_calc.obj plain_entry.obj /OUT:plain.dll /IMPLIB:plain.lib || goto :fail

:: ---------------------------------------------------------------------------
:: static.lib -- a genuine static archive, not an import library.
:: ---------------------------------------------------------------------------
echo === building static.lib (lib.exe) ===
"%REAL_CL%" %CFLAGS% "%SRC_DIR%\static_only.cxx" /Fo:static_only.obj || goto :fail
"%REAL_LIB%" /nologo static_only.obj /OUT:static.lib || goto :fail

popd

:: ---------------------------------------------------------------------------
:: sfn_calc.dll / sfn_calc.lib -- built from a staging directory whose absolute
:: path exceeds the wrapper's 143 character name limit, which is the only case in
:: which the wrapper falls back to GetShortPathName. Requires 8.3 name creation to
:: be enabled on the volume (`fsutil 8dot3name set 0`, elevated).
:: ---------------------------------------------------------------------------
set "LONGSEG=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
set "LONGDIR=%STAGE%"
:grow_long_dir
call :strlen SFN_LEN "%LONGDIR%\sfn_calc.dll"
if %SFN_LEN% LEQ %NAME_LEN% (
    set "LONGDIR=%LONGDIR%\%LONGSEG%"
    goto :grow_long_dir
)
if %SFN_LEN% GTR 250 (
    echo ERROR: the long staging path reached %SFN_LEN% characters, at MAX_PATH.
    echo   Use a shorter SPACK_PE_FIXTURE_STAGE.
    exit /b 1
)
mkdir "%LONGDIR%" 2>nul

echo === checking 8.3 short name support ===
for %%D in ("%LONGDIR%") do set "SHORTDIR=%%~sD"
if /i "%SHORTDIR%"=="%LONGDIR%" (
    echo.
    echo WARNING: 8.3 short filename creation is disabled for this volume, so the
    echo          SFN fixtures cannot be generated. Run `fsutil 8dot3name set 0`
    echo          from an elevated prompt and re-run, or stage on a volume where
    echo          8.3 creation is enabled.
    echo          sfn_calc.dll / sfn_calc.lib will be SKIPPED.
    echo.
    set "SKIP_SFN=1"
) else (
    echo   long : %LONGDIR%
    echo   short: %SHORTDIR%
)

if not defined SKIP_SFN (
    echo === building sfn_calc.dll / sfn_calc.lib (wrapper, long path) ===
    pushd "%LONGDIR%" || goto :fail
    "%WRAP_CL%" %CFLAGS% /DCALC_EXPORTS "%SRC_DIR%\calc.cxx" /Fo:sfn_calc.obj || goto :fail
    "%WRAP_CL%" %CFLAGS% "%SRC_DIR%\entry.cxx" /Fo:sfn_entry.obj || goto :fail
    "%WRAP_LINK%" %DLLFLAGS% sfn_calc.obj sfn_entry.obj /OUT:sfn_calc.dll /IMPLIB:sfn_calc.lib || goto :fail
    popd
)

:: ---------------------------------------------------------------------------
:: Collect
:: ---------------------------------------------------------------------------
echo.
echo === installing fixtures into %FIXTURE_DIR% ===
for %%F in (calc.dll calc.lib tester.exe plain.dll static.lib) do (
    copy /y "%STAGE%\build\%%F" "%FIXTURE_DIR%\%%F" >nul || goto :fail
)
if not defined SKIP_SFN (
    for %%F in (sfn_calc.dll sfn_calc.lib) do (
        copy /y "%LONGDIR%\%%F" "%FIXTURE_DIR%\%%F" >nul || goto :fail
    )
)

:: The absolute paths the PEs were linked at are baked into each PE as the
:: spack/SPACKRESOURCE resource and into each import library's name field. They are
:: machine specific, so record them here rather than hard coding them in the tests.
echo.
echo === writing fixtures.txt manifest ===
> "%FIXTURE_DIR%\fixtures.txt" (
    echo # Generated by generate_fixtures.bat -- do not edit by hand.
    echo # Absolute path each fixture PE was linked at. This is what the compiler
    echo # wrapper stores, padded, in the PE's spack/SPACKRESOURCE resource and in
    echo # the name field of the corresponding import library.
    echo calc.dll=%STAGE%\build\calc.dll
    echo tester.exe=%STAGE%\build\tester.exe
    if not defined SKIP_SFN echo sfn_calc.dll=%SHORTDIR%\sfn_calc.dll
)
type "%FIXTURE_DIR%\fixtures.txt"

echo.
echo === fixture sizes ===
for %%F in ("%FIXTURE_DIR%\*.dll" "%FIXTURE_DIR%\*.exe" "%FIXTURE_DIR%\*.lib") do (
    echo   %%~nxF  %%~zF bytes
)

echo.
echo === relocate --report output (paste into relocate_windows.py) ===
"%RELOCATE%" --coff "%FIXTURE_DIR%\calc.lib" --report
if not defined SKIP_SFN "%RELOCATE%" --coff "%FIXTURE_DIR%\sfn_calc.lib" --report

echo.
echo === relocate --verify exit codes (0 import, 1 static, 2 unparsable) ===
"%RELOCATE%" --coff "%FIXTURE_DIR%\calc.lib" --verify
echo   calc.lib   -^> !errorlevel!
"%RELOCATE%" --coff "%FIXTURE_DIR%\static.lib" --verify
echo   static.lib -^> !errorlevel!

echo.
echo Done.
exit /b 0

:: Length of %~2, into the variable named by %~1. Batch has no strlen.
:strlen
setlocal enabledelayedexpansion
set "s=%~2"
set "n=0"
:strlen_loop
if defined s (
    set "s=!s:~1!"
    set /a n+=1
    goto :strlen_loop
)
endlocal & set "%~1=%n%"
goto :eof

:fail
echo.
echo FAILED with errorlevel %errorlevel%
popd 2>nul
exit /b 1
