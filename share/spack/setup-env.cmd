:: Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
:: Spack Project Developers. See the top-level COPYRIGHT file for details.
::
:: SPDX-License-Identifier: (Apache-2.0 OR MIT)
::#######################################################################
::
:: This file is part of Spack and sets up the spack environment for bash,
:: zsh, and dash (sh).  This includes environment modules and lmod support,
:: and it also puts spack in your path. The script also checks that at least
:: module support exists, and provides suggestions if it doesn't. Source
:: it like this:
::
::    . /path/to/spack/share/spack/setup-env.bat
::
@echo off
setlocal enabledelayedexpansion
setlocal EnableExtensions
if defined _sp_initializing (goto :eof)
set "_sp_initializing=True"
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
set "_sp_flags="
set "_sp_args="
set "_sp_subcommand="
for %%x in (%*) do (
    set "t=%%x"
    if "!t:~0,1!" == "-" (
        if not defined _sp_flags (
            set "_sp_flags=!t!"
        ) else (
            set "_sp_flags=!_sp_flags! !t!"
            )
        ) else (
            if not defined _sp_subcommand (
                set "_sp_subcommand=!t!"
            ) else (
                set "_sp_args=!_sp_args! !t!"
            )
        )
    )
echo "SP FLAGS IS %_sp_flags%"
echo "SP COMMAND IS %_sp_subcommand%"
echo "SP ARGS IS %_sp_args%"
:: h and V flags don't require further output parsing.
:: Boolean operators do not exist for non booleans in batch
if defined _sp_flags (
    if NOT "%_sp_flags%"=="%_sp_flags:h=%" (
        ::spack %_sp_flags% %_sp_subcommand% %_sp_args%
        echo "spack %_sp_flags% %_sp_subcommand% %_sp_args%"
        exit /B 0
    )
    if NOT "%_sp_flags%"=="%_sp_flags:V=%" (
        ::spack %_sp_flags% %_sp_subcommand% %_sp_args%
        echo "spack %_sp_flags% %_sp_subcommand% %_sp_args%"
        exit /B 0
    )
)

2>nul call :case_%_sp_subcommand%
if ERRORLEVEL 1 goto :default_case
:case_cd
goto :end_switch
:case_env
goto :end_switch
:case_load
goto :end_switch
:case_unload
goto :end_switch
:default_case
echo "DEFAULT CASE"
goto :end_switch
:end_switch
goto :eof

DOSKEY spacktivate = "spack env activate"

:_spack_pathadd
_pa_varname=PATH
_pa_new_path=%~1
if NOT "%~2" == "" (
    _pa_varname=%~1
    _pa_new_path=%~2
    )
EXIT /B 0

set "_sp_initializing="