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

setlocal enabledelayedexpansion
setlocal EnableExtensions
if NOT defined SPACK_ROOT (
:: this file is located in %SPACK_ROOT%\lib\spack\spack\cmd\installer
    pushd %~dp0
    cd ../../../../../
    set SPACK_ROOT=%CD%
    popd
)
if defined _sp_initializing (goto :eof)
set "_sp_initializing=True"
DOSKEY spacktivate = "spack env activate"
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
:: Boolean operators do not exist for non integers in batch
if defined _sp_flags (
    if NOT "%_sp_flags%"=="%_sp_flags:-h=%" (
        if not defined _sp_subcommand (
            python %spack% %_sp_flags% %_sp_subcommand% %_sp_args%
            exit /B 0
        ) else (
            python %spack% %_sp_subcommand% %_sp_flags% %_sp_args%
            exit /B 0 )
    )
    if NOT "%_sp_flags%"=="%_sp_flags:-V=%" (
        python %spack% %_sp_flags% %_sp_subcommand% %_sp_args%
        exit /B 0
    )
)


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
if "%_sp_flags%" == "" (
) else (
    if NOT "%_sp_flags%"=="%_sp_flags:-h=%" (
        python %spack% cd -h
    ) else (
        if NOT "%_sp_flags%"=="%_sp_flags:--help=%" (
            python %spack% cd -h
        )
    )
)
FOR /F "tokens=* USEBACKQ" %%F IN ('call spack location %_sp_args%') DO (
set "LOC=%%F"
)
for %%Z In ("%LOC%") do if "%%~aZ" GEq "d" (cd "%LOC%")
goto :end_switch

:case_env
if NOT "%_sp_args%"=="%_sp_args:deactivate=%" (
    if "%_sp_flags%" == "" (
        @echo "HERE"
        @echo python %spack% env deactivate %_sp_flags% --bat %_sp_args:deactivate=%
        for /f "tokens=*" %%I in (
            'call python %spack% env deactivate %_sp_flags% --bat %_sp_args:deactivate=%'
            ) do %%I
    ) else (
        if NOT "%_sp_flags%"=="%_sp_flags:--bat=%" (
            call python %spack% env deactivate %_sp_flags% %_sp_args:deactivate=%
        ) else (
            for /f "tokens=*" %%I in (
            'call python %spack% env deactivate %_sp_flags% --bat %_sp_args:deactivate=%'
            ) do %%I
        )
    )
) else (
    if NOT "%_sp_args%"=="%_sp_args:activate=%" (
        if "%_sp_flags%" == "" (
            for /f "tokens=*" %%I in (
                'call python %spack% env activate %_sp_flags% --bat %_sp_args:activate=%'
                ) do %%I
        ) else (
            if NOT "%_sp_flags%"=="%_sp_flags:--bat=%" (
                call python %spack% env activate %_sp_flags% %_sp_args:activate=%
            ) else (
                for /f "tokens=*" %%I in (
                'call python %spack% env activate %_sp_flags% --bat %_sp_args:activate=%'
                ) do %%I
            )
        )
    ) else (
        python %spack% env -h
    )
)
goto :end_switch

:case_load
if "%_sp_flags%" == "" (
    for /f "tokens=*" %%I in ('python "%spack%" %_sp_subcommand% %_sp_flags% --bat %_sp_args%') do %%I
) else (
  if NOT "%_sp_flags%"=="%_sp_flags:--bat=%" (
     python "%spack%" %_sp_subcommand% %_sp_flags% %_sp_args%
  ) else (
      if NOT "%_sp_flags%"=="%_sp_flags:--help=%" (
          :: Note: Should never get here, --help should already be handled
          python "%spack%" %_sp_subcommand% %_sp_flags% --bat %_sp_args%
      ) else (
          for /f "tokens=*" %%I in ('python "%spack%" %_sp_subcommand% %_sp_flags% --bat %_sp_args%') do %%I
      )
  )
)
goto :end_switch

:end_switch
set "_sp_initializing="
exit /B 0

::#######################################################################

:_spack_pathadd
_pa_varname=PATH
_pa_new_path=%~1
if NOT "%~2" == "" (
    _pa_varname=%~1
    _pa_new_path=%~2
    )

set "_sp_initializing="
EXIT /B 0
