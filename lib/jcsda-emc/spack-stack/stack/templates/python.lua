help([[
]])

local pkgName    = myModuleName()
local pkgVersion = myModuleVersion()
local pkgNameVer = myModuleFullName()

family("MetaPython")

-- conflicts
conflict("stack-python")

-- prerequisite modules
@MODULELOADS@
@MODULEPREREQS@

-- compiler flags and other environment variables
@COMPFLAGS@
@ENVVARS@

-- python root environment variable
@PYTHONROOT@

-- module show info
whatis("Name: " .. pkgName)
whatis("Version: " .. pkgVersion)
whatis("Category: interpreter")
whatis("Description: " .. pkgName .. " interpreter and module access")
