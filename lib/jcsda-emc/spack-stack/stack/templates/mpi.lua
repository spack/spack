help([[
]])

local pkgName    = myModuleName()
local pkgVersion = myModuleVersion()
local pkgNameVer = myModuleFullName()

family("MetaMPI")

-- conflicts
conflict("stack-intel-mpi")
conflict("stack-intel-oneapi-mpi")
conflict("stack-cray-mpich")
conflict("stack-mpich")
conflict("stack-mpt")

-- prerequisite modules
@MODULELOADS@
@MODULEPREREQS@

-- spack compiler module hierarchy
prepend_path("MODULEPATH", "@MODULEPATH@")

-- mpi wrapper environment variables
setenv("MPICC",  "@MPICC@")
setenv("MPICXX", "@MPICXX@")
setenv("MPIF77", "@MPIF77@")
setenv("MPIF90", "@MPIF90@")
setenv("MPI_CC",  "@MPICC@")
setenv("MPI_CXX", "@MPICXX@")
setenv("MPI_F77", "@MPIF77@")
setenv("MPI_F90", "@MPIF90@")

-- compiler flags and other environment variables
@COMPFLAGS@
@ENVVARS@

-- mpi root environment variable
@MPIROOT@

-- module show info
whatis("Name: " .. pkgName)
whatis("Version: " .. pkgVersion)
whatis("Category: library")
whatis("Description: " .. pkgName .. " mpi library and module access")
