:: Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
:: Spack Project Developers. See the top-level COPYRIGHT file for details.
::
:: SPDX-License-Identifier: (Apache-2.0 OR MIT)
::#######################################################################
::
:: This file is part of Spack and sets up the spack environment for batch,
:: This includes environment modules and lmod support,
:: and it also puts spack in your path. The script also checks that at least
:: module support exists, and provides suggestions if it doesn't. Source
:: it like this:
::
::    . /path/to/spack/install/spack_cmd.bat
::
@echo off
set spack=%SPACK_ROOT%\bin\spack
::#######################################################################
:: This is a wrapper around the spack command that forwards calls to
:: 'spack load' and 'spack unload' to shell functions.  This in turn
:: allows them to be used to invoke environment modules functions.
::
:: 'spack load' is smarter than just 'load' because it converts its
:: arguments into a unique Spack spec that is then passed to module
:: commands.  This allows the user to use packages without knowing all
:: their installation details.
::
:: e.g., rather than requiring a full spec for libelf, the user can type:
::
::     spack load libelf
::
:: This will first find the available libelf module file and use a
:: matching one.  If there are two versions of libelf, the user would
:: need to be more specific, e.g.:
::
::     spack load libelf@0.8.13
::
:: This is very similar to how regular spack commands work and it
:: avoids the need to come up with a user-friendly naming scheme for
:: spack module files.
::#######################################################################

:_sp_shell_wrapper
set "_sp_flags="
set "_sp_args="
set "_sp_subcommand="
setlocal enabledelayedexpansion
for %%x in (%*) do (
    set "t=%%x"
    if "!t:~0,1!" == "-" (
        if not defined _sp_flags (
            set "_sp_flags=!t!"
            shift
        ) else (
            set "_sp_flags=!_sp_flags! !t!"
            shift
            )
        ) else (
            if not defined _sp_subcommand (
                set "_sp_subcommand=!t!"
                shift
            ) else (
                set "_sp_args=!_sp_args! !t!"
            )
        )
    )
:: h and V flags don't require further output parsing.
:: If we encounter, execute and exit
if defined _sp_flags (
    if NOT "%_sp_flags%"=="%_sp_flags:-h=%" (
        if not defined _sp_subcommand (
            python "%spack%" %_sp_flags% %_sp_subcommand% %_sp_args%
            exit /B 0
        ) else (
            python "%spack%" %_sp_subcommand% %_sp_flags% %_sp_args%
            exit /B 0 )
    )
    if NOT "%_sp_flags%"=="%_sp_flags:-V=%" (
        python "%spack%" %_sp_flags% %_sp_subcommand% %_sp_args%
        exit /B 0
    )
)
:: pass parsed variables outside of local scope. Need to do
:: this because delayedexpansion can only be set by setlocal
echo %_sp_flags%>flags
echo %_sp_args%>args
echo %_sp_subcommand%>subcmd
endlocal
set /p _sp_subcommand=<subcmd
set /p _sp_flags=<flags
set /p _sp_args=<args
if "%_sp_subcommand%"=="ECHO is off." (set "_sp_subcommand=")
if "%_sp_flags%"=="ECHO is off." (set "_sp_flags=")
if "%_sp_args%"=="ECHO is off." (set "_sp_args=")
del subcmd
del flags
del args

:: Filter out environment commands. For any others, just run the command.
if "%_sp_subcommand%" == "cd" (
    goto :case_cd
) else if "%_sp_subcommand%" == "env" (
    goto :case_env
) else if "%_sp_subcommand%" == "load" (
    goto :case_load
) else if "%_sp_subcommand%" == "unload" (
    goto :case_load
) else (
    python "%spack%" %_sp_subcommand% %_sp_flags% %_sp_args%
    goto :end_switch
)
::#######################################################################

:case_cd
 for /F "tokens=* USEBACKQ" %%F in (
`python "%spack%" location %_sp_flags% %_sp_args%`) do (
    set "LOC=%%F"
)
for %%Z In ("%LOC%") do if EXIST %%~sZ\NUL (cd /d "%LOC%")
goto :end_switch

:case_env
if NOT "%_sp_args%"=="%_sp_args:deactivate=%" (
    if "%_sp_flags%" == "" (
        for /f "tokens=* USEBACKQ" %%I in (
            `call python "%spack%" env deactivate %_sp_flags% --bat %_sp_args:deactivate=%`
            ) do %%I
    ) else if NOT "%_sp_flags%"=="%_sp_flags:--bat=%" (
            call python "%spack%" env deactivate %_sp_flags% %_sp_args:deactivate=%
    ) else (
        for /f "tokens=* USEBACKQ" %%I in (
            `call python "%spack%" env deactivate %_sp_flags% --bat %_sp_args:deactivate=%`
        ) do %%I
    )
) else if NOT "%_sp_args%"=="%_sp_args:activate=%" (
    if "%_sp_flags%" == "" (
        for /f "tokens=* USEBACKQ" %%I in (
            `call python "%spack%" env activate %_sp_flags% --bat %_sp_args:activate=%`
        ) do %%I
    ) else if NOT "%_sp_flags%"=="%_sp_flags:--bat=%" (
            call python "%spack%" env activate %_sp_flags% %_sp_args:activate=%
    ) else (
        for /f "tokens=* USEBACKQ" %%I in (
            `call python "%spack%" env activate %_sp_flags% --bat %_sp_args:activate=%`
        ) do %%I
    )
) else (
    python "%spack%" %_sp_subcommand% %_sp_flags% %_sp_args%
)
goto :end_switch

:case_load
if "%_sp_flags%" == "" (
    for /f "tokens=* USEBACKQ" %%I in (
    `python "%spack%" %_sp_subcommand% %_sp_flags% --bat %_sp_args%`) do %%I
) else if NOT "%_sp_flags%"=="%_sp_flags:--bat=%" (
     python "%spack%" %_sp_subcommand% %_sp_flags% %_sp_args%
) else if NOT "%_sp_flags%"=="%_sp_flags:--help=%" (
    :: Note: Should never get here, --help should already be handled
    python "%spack%" %_sp_subcommand% %_sp_flags% --bat %_sp_args%
) else (
    for /f "tokens=* USEBACKQ" %%I in (
    `python "%spack%" %_sp_subcommand% %_sp_flags% --bat %_sp_args%`) do %%I
)
goto :end_switch

:case_unload
goto :case_load

:end_switch
exit /B 0

::########################################################################
:: Prepends directories to path, if they exist.
::      pathadd /path/to/dir            # add to PATH
:: or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
::########################################################################

:_spack_pathadd
set "_pa_varname=PATH"
set "_pa_new_path=%~1"
if NOT "%~2" == "" (
    set "_pa_varname=%~1"
    set "_pa_new_path=%~2"
    )
set "_pa_oldvalue=%_pa_varname%"
for %%Z in ("%_pa_new_path%") do if EXIST %%~sZ\NUL (
    if defined %_pa_oldvalue% (
        set "_pa_varname=%_pa_new_path%:%_pa_oldvalue%"
    ) else (
        set "_pa_varname=%_pa_new_path%"
    )
)
exit /b 0

:: set module system roots
:_sp_multi_pathadd 
for %%I in (%~2) do (
    for %%Z in (%_sp_compatible_sys_types%) do (
        :pathadd "%~1" "%%I\%%Z"
    )
)
exit /B 0