@echo off
:: Copyright Spack Project Developers. See COPYRIGHT file for details.
:: SPDX-License-Identifier: (Apache-2.0 OR MIT)

if "%~1"=="" (
    doskey _separator_exists=call "%~f0" _separator_exists $*
    doskey _spack_env_varname_is_empty=call "%~f0" _spack_env_varname_is_empty $*
    doskey _spack_env_set=call "%~f0" _spack_env_set $*
    doskey _spack_env_unset=call "%~f0" _spack_env_unset $*
    doskey _spack_env_append=call "%~f0" _spack_env_append $*
    doskey _spack_env_prepend=call "%~f0" _spack_env_prepend $*
    doskey _spack_env_remove_value=call "%~f0" _spack_env_remove_value $*
    doskey _spack_env_remove_first=call "%~f0" _spack_env_remove_first $*
    doskey _spack_env_remove_last=call "%~f0" _spack_env_remove_last $*
    doskey _spack_env_prune_duplicates=call "%~f0" _spack_env_prune_duplicates $*
    echo Spack environment functions loaded into the current shell context.
    exit /b 0
)

:: Dispatcher: Route to the requested "function" label
:: Interpret initial script arg as function
goto :%~1

:: -----------------------------------------------------------------------------
:: FUNCTIONS
:: Note: Arguments start at %2 because %1 is the function name routed by DOSKEY
:: -----------------------------------------------------------------------------

:_separator_exists
if "%~2"=="" (
    echo Missing argument: separator
    exit /b 1
)
exit /b 0

:_spack_env_varname_is_empty
call set "val=%%%~2%%"
if not defined val exit /b 0
exit /b 1

:_spack_env_set
set "%~2=%~3"
exit /b 0

:_spack_env_unset
set "%~2="
exit /b 0

:_spack_env_append
set "varname=%~2"
set "value=%~3"
set "sep=%~4"
call :_separator_exists "" "%sep%" || exit /b 1

call set "current=%%%varname%%%"
if not defined current (
    set "%varname%=%value%"
) else (
    set "%varname%=%current%%sep%%value%"
)
exit /b 0

:_spack_env_prepend
set "varname=%~2"
set "value=%~3"
set "sep=%~4"
call :_separator_exists "" "%sep%" || exit /b 1

call set "current=%%%varname%%%"
if not defined current (
    set "%varname%=%value%"
) else (
    set "%varname%=%value%%sep%%current%"
)
exit /b 0

:_spack_env_remove_value
set "varname=%~2"
set "value=%~3"
set "sep=%~4"
call :_separator_exists "" "%sep%" || exit /b 1

call set "current=%%%varname%%%"
if not defined current exit /b 0

setlocal EnableDelayedExpansion
:: CMD hack: replace dynamic separators with " " to iterate over the list natively
set "work=!current:%sep%=" "!"
set "work="!work!""
set "accum="

for %%A in (!work!) do (
    set "item=%%~A"
    :: Strict case-sensitive match like Bash
    if not "!item!"=="%value%" (
        if not defined accum (
            set "accum=!item!"
        ) else (
            set "accum=!accum!%sep%!item!"
        )
    )
)
goto :export_and_exit

:_spack_env_remove_first
set "varname=%~2"
set "value=%~3"
set "sep=%~4"
call :_separator_exists "" "%sep%" || exit /b 1

call set "current=%%%varname%%%"
if not defined current exit /b 0

setlocal EnableDelayedExpansion
set "work=!current:%sep%=" "!"
set "work="!work!""
set "accum="
set "done=0"

for %%A in (!work!) do (
    set "item=%%~A"
    set "match=0"
    if "!done!"=="0" if "!item!"=="%value%" (
        set "done=1"
        set "match=1"
    )
    if "!match!"=="0" (
        if not defined accum (
            set "accum=!item!"
        ) else (
            set "accum=!accum!%sep%!item!"
        )
    )
)
goto :export_and_exit

:_spack_env_remove_last
set "varname=%~2"
set "value=%~3"
set "sep=%~4"
call :_separator_exists "" "%sep%" || exit /b 1

call set "current=%%%varname%%%"
if not defined current exit /b 0

setlocal EnableDelayedExpansion
set "work=!current:%sep%=" "!"
set "work="!work!""

set "index=0"
set "last_match=-1"
for %%A in (!work!) do (
    set "item=%%~A"
    if "!item!"=="%value%" set "last_match=!index!"
    set /a index+=1
)

set "accum="
set "index=0"
for %%A in (!work!) do (
    set "item=%%~A"
    set "skip=0"
    if "!index!"=="!last_match!" set "skip=1"
    if "!skip!"=="0" (
        if not defined accum (
            set "accum=!item!"
        ) else (
            set "accum=!accum!%sep%!item!"
        )
    )
    set /a index+=1
)
goto :export_and_exit

:_spack_env_prune_duplicates
set "varname=%~2"
set "sep=%~3"
call :_separator_exists "" "%sep%" || exit /b 1

call set "current=%%%varname%%%"
if not defined current exit /b 0

setlocal EnableDelayedExpansion
set "work=!current:%sep%=" "!"
set "work="!work!""
set "accum="

for %%A in (!work!) do (
    set "item=%%~A"
    if not defined accum (
        set "accum=!item!"
    ) else (
        set "check=%sep%!accum!%sep%"
        set "search=%sep%!item!%sep%"
        set "found=0"
        
        for /f "delims=" %%S in ("!search!") do (
            if not "!check!"=="!check:%%S=!" set "found=1"
        )
        
        if "!found!"=="0" (
            set "accum=!accum!%sep%!item!"
        )
    )
)
goto :export_and_exit

:export_and_exit
if not defined accum (
    endlocal
    set "%varname%="
    exit /b 0
)
for /f "delims=" %%V in ("!accum!") do (
    endlocal
    set "%varname%=%%V"
)
exit /b 0
