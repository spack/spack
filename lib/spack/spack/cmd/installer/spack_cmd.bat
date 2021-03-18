@ECHO OFF
:: (c) 2021 Lawrence Livermore National Laboratory
pushd %~dp0
set spackinstdir=%CD%
popd

for /f "tokens=*" %%g in ('dir /b /a:d "%spackinstdir%\Python*"') do (set python_pf_ver=%%g)
set "py_path=%spackinstdir%\%python_pf_ver%"
for /f "tokens=*" %%g in ('dir /b /a:d "%spackinstdir%\spack*"') do (set spack_ver=%%g)
set "SPACK_ROOT=%spackinstdir%\%spack_ver%"

set PATH=%py_path%;%spackinstdir%\scripts\;%PATH%
"%py_path%\python.exe" "%spackinstdir%\scripts\haspywin.py"
set "EDITOR=notepad"
DOSKEY spacktivate=spack env activate $*


@echo **********************************************************************
@echo ** Spack Package Manager
@echo **********************************************************************

%comspec% /k
