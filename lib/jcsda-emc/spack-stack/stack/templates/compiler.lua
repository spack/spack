help([[
]])

local pkgName    = myModuleName()
local pkgVersion = myModuleVersion()
local pkgNameVer = myModuleFullName()

family("MetaCompiler")

-- conflicts
conflict("stack-apple-clang")
conflict("stack-clang")
conflict("stack-gnu")
conflict("stack-intel")
conflict("stack-intel-oneapi-compilers")

-- prerequisite modules
@MODULELOADS@
@MODULEPREREQS@

-- spack compiler module hierarchy
prepend_path("MODULEPATH", "@MODULEPATH@")

-- compiler environment variables
setenv("F77", "@F77@")
setenv("FC",  "@FC@")
setenv("CC",  "@CC@")
setenv("CXX", "@CXX@")
setenv("SERIAL_F77", "@F77@")
setenv("SERIAL_FC",  "@FC@")
setenv("SERIAL_CC",  "@CC@")
setenv("SERIAL_CXX", "@CXX@")

-- compiler flags and other environment variables
@COMPFLAGS@
@ENVVARS@

-- module show info
whatis("Name: " .. pkgName)
whatis("Version: " .. pkgVersion)
whatis("Category: compiler")
whatis("Description: " .. pkgName .. " compiler family and module access")
