# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys
from copy import deepcopy

from spack.package import *


def xsdk_depends_on_accl(accl_name, accl_var, *args, **kwargs):
    if accl_name == "cuda":
        accl_arch_name = "cuda_arch"
        accl_arch_values = list(deepcopy(CudaPackage.cuda_arch_values))
    elif accl_name == "rocm":
        accl_arch_name = "amdgpu_target"
        accl_arch_values = list(deepcopy(ROCmPackage.amdgpu_targets))
    # require ~cuda when xsdk~cuda (and '?cuda' not used)
    usedep = 1
    args_new = list(deepcopy(args))
    if not isinstance(accl_var, list):
        accl_var = [accl_var]
    for idx, var in enumerate(accl_var):
        # skip variants starting with '?' so that
        # that that they are left unspecified by xsdk
        if not var.startswith("?"):
            args_new[0] += " ~%s" % var
        else:
            accl_var[idx] = var.replace("?", "")
        # if '?cuda' skip adding '~cuda' dep
        if var == "?" + accl_name:
            usedep = 0
    kwargs_new = deepcopy(kwargs)
    if "when" in kwargs_new:
        kwargs_new["when"] += " ~" + accl_name
    else:
        kwargs_new["when"] = "~" + accl_name
    if usedep:
        depends_on(*args_new, **kwargs_new)

    # require +cuda when xsdk+cuda, and match the arch
    for arch in accl_arch_values:
        args_new = list(deepcopy(args))
        kwargs_new = deepcopy(kwargs)
        args_new[0] += "+%s %s=%s" % ("+".join(accl_var), accl_arch_name, str(arch))
        if "when" in kwargs_new:
            kwargs_new["when"] += " +%s %s=%s" % (accl_name, accl_arch_name, str(arch))
        else:
            kwargs_new["when"] = "+%s %s=%s" % (accl_name, accl_arch_name, str(arch))
        depends_on(*args_new, **kwargs_new)


def xsdk_depends_on(spec, cuda_var="", rocm_var="", **kwargs):
    """
    Wrapper for depends_on which can handle propagating cuda and rocm
    variants.

    Currently, it propagates +cuda_var when xsdk+cuda and rocm_var
    when xsdk+rocm. When xsdk~[cuda|rocm], then ~[cuda|rocm]_var is
    selected unless the variant string is prefixed with a '?'
    (see the tasmanian use below). When '?' prefix is used, then
    the variant is left unspecified.

    [cuda|rocm]_var can be an array of variant strings or just a single
    variant string. The spack '+' and '~' symbols should not appear
    in the strings.
    """
    if bool(cuda_var):
        xsdk_depends_on_accl("cuda", cuda_var, spec, **kwargs)
    if bool(rocm_var):
        xsdk_depends_on_accl("rocm", rocm_var, spec, **kwargs)
    if not bool(cuda_var) and not bool(rocm_var):
        depends_on(spec, **kwargs)


class Xsdk(BundlePackage, CudaPackage, ROCmPackage):
    """Xsdk is a suite of Department of Energy (DOE) packages for numerical
    simulation. This is a Spack bundle package that installs the xSDK
    packages
    """

    homepage = "https://xsdk.info"
    maintainers("balay", "luszczek", "balos1", "shuds13", "v-dobrev")

    version("develop")
    version("0.8.0")
    version("0.7.0")
    version("0.6.0", deprecated=True)

    variant("trilinos", default=True, sticky=True, description="Enable trilinos package build")
    variant("datatransferkit", default=True, description="Enable datatransferkit package build")
    variant("omega-h", default=True, description="Enable omega-h package build")
    variant("strumpack", default=True, description="Enable strumpack package build")
    variant("dealii", default=True, description="Enable dealii package build")
    variant("alquimia", default=True, description="Enable alquimia package build")
    variant("phist", default=True, description="Enable phist package build")
    variant("ginkgo", default=True, description="Enable ginkgo package build")
    variant("libensemble", default=True, description="Enable py-libensemble package build")
    variant(
        "precice", default=(sys.platform != "darwin"), description="Enable precice package build"
    )
    variant("butterflypack", default=True, description="Enable butterflypack package build")
    variant("heffte", default=True, description="Enable heffte package build")
    variant("slate", default=(sys.platform != "darwin"), description="Enable slate package build")
    variant("arborx", default=True, description="Enable ArborX build")
    variant("exago", default=True, description="Enable exago build")
    variant("hiop", default=True, description="Enable hiop build")
    variant("raja", default=(sys.platform != "darwin"), description="Enable raja for hiop, exago")

    xsdk_depends_on("hypre@develop+superlu-dist+shared", when="@develop", cuda_var="cuda")
    xsdk_depends_on("hypre@2.26.0+superlu-dist+shared", when="@0.8.0", cuda_var="cuda")
    xsdk_depends_on("hypre@2.23.0+superlu-dist+shared", when="@0.7.0", cuda_var="cuda")
    xsdk_depends_on("hypre@2.20.0+superlu-dist+shared", when="@0.6.0")

    xsdk_depends_on(
        "mfem@develop+shared+mpi+superlu-dist+petsc+sundials+examples+miniapps",
        when="@develop",
        cuda_var="cuda",
        rocm_var="rocm",
    )
    xsdk_depends_on(
        "mfem@4.5.0+shared+mpi+superlu-dist+petsc+sundials+examples+miniapps",
        when="@0.8.0",
        cuda_var="cuda",
        rocm_var="rocm",
    )
    xsdk_depends_on(
        "mfem@4.3.0+mpi+superlu-dist+petsc+sundials+examples+miniapps",
        when="@0.7.0",
        cuda_var="cuda",
        rocm_var="rocm",
    )
    xsdk_depends_on(
        "mfem@4.2.0+mpi+superlu-dist+petsc+sundials+examples+miniapps",
        when="@0.6.0",
        cuda_var="cuda",
    )

    xsdk_depends_on("superlu-dist@develop", when="@develop")
    xsdk_depends_on("superlu-dist@8.1.2", when="@0.8.0")
    xsdk_depends_on("superlu-dist@7.1.1", when="@0.7.0")
    xsdk_depends_on("superlu-dist@6.4.0", when="@0.6.0")
    xsdk_depends_on(
        "trilinos@develop+hypre+superlu-dist+hdf5~mumps+boost"
        + "~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2"
        + "~exodus~dtk+intrepid2+shards+stratimikos gotype=int"
        + " cxxstd=14",
        when="@develop +trilinos",
    )
    xsdk_depends_on(
        "trilinos@13.4.1+hypre+superlu-dist+hdf5~mumps+boost"
        + "~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2"
        + "~exodus~dtk+intrepid2+shards+stratimikos gotype=int"
        + " cxxstd=14",
        when="@0.8.0 +trilinos",
    )
    xsdk_depends_on(
        "trilinos@13.2.0+hypre+superlu-dist+hdf5~mumps+boost"
        + "~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2"
        + "~exodus~dtk+intrepid2+shards+stratimikos gotype=int"
        + " cxxstd=14",
        when="@0.7.0 +trilinos",
    )
    xsdk_depends_on(
        "trilinos@13.0.1+hypre+superlu-dist+hdf5~mumps+boost"
        + "~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2"
        + "~exodus~dtk+intrepid2+shards gotype=int"
        + " cxxstd=11",
        when="@0.6.0 +trilinos",
    )

    xsdk_depends_on("datatransferkit@master", when="@develop +trilinos +datatransferkit")
    dtk7ver = "3.1-rc2" if sys.platform == "darwin" else "3.1-rc3"
    xsdk_depends_on("datatransferkit@" + dtk7ver, when="@0.8.0 +trilinos +datatransferkit")
    xsdk_depends_on("datatransferkit@" + dtk7ver, when="@0.7.0 +trilinos +datatransferkit")
    xsdk_depends_on("datatransferkit@3.1-rc2", when="@0.6.0 +trilinos +datatransferkit")

    xsdk_depends_on("petsc +trilinos", when="+trilinos @:0.6.0")
    xsdk_depends_on("petsc +batch", when="@0.6.0: ^cray-mpich")
    xsdk_depends_on(
        "petsc@main+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64",
        when="@develop",
        cuda_var="cuda",
        rocm_var="rocm",
    )
    xsdk_depends_on(
        "petsc@3.18.1+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64",
        when="@0.8.0",
        cuda_var="cuda",
        rocm_var="rocm",
    )
    xsdk_depends_on(
        "petsc@3.16.1+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64",
        when="@0.7.0",
        cuda_var="cuda",
    )
    xsdk_depends_on(
        "petsc@3.14.1+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64",
        when="@0.6.0",
        cuda_var="cuda",
    )

    xsdk_depends_on("dealii +trilinos~adol-c", when="+trilinos +dealii")
    xsdk_depends_on("dealii ~trilinos", when="~trilinos +dealii")
    xsdk_depends_on(
        "dealii@master~assimp~python~doc~gmsh+petsc+slepc+mpi~int64"
        + "~netcdf+metis+sundials~ginkgo~symengine~nanoflann~simplex~arborx~cgal",
        when="@develop +dealii",
    )
    xsdk_depends_on(
        "dealii@9.4.0~assimp~python~doc~gmsh+petsc+slepc+mpi~int64"
        + "~netcdf+metis+sundials~ginkgo~symengine~simplex~arborx~cgal",
        when="@0.8.0 +dealii",
    )
    xsdk_depends_on(
        "dealii@9.3.2~assimp~python~doc~gmsh+petsc+slepc+mpi~int64+hdf5"
        + "~netcdf+metis~sundials~ginkgo~symengine~simplex~arborx",
        when="@0.7.0 +dealii",
    )
    xsdk_depends_on(
        "dealii@9.2.0~assimp~python~doc~gmsh+petsc+slepc+mpi~int64+hdf5"
        + "~netcdf+metis~sundials~ginkgo~symengine~simplex~arborx",
        when="@0.6.0 +dealii",
    )

    xsdk_depends_on("pflotran@develop", when="@develop")
    xsdk_depends_on("pflotran@4.0.1", when="@0.8.0")
    xsdk_depends_on("pflotran@3.0.2", when="@0.7.0")
    xsdk_depends_on("pflotran@xsdk-0.6.0", when="@0.6.0")

    xsdk_depends_on("alquimia@develop", when="@develop +alquimia")
    xsdk_depends_on("alquimia@1.0.10", when="@0.8.0 +alquimia")
    xsdk_depends_on("alquimia@1.0.9", when="@0.7.0 +alquimia")
    xsdk_depends_on("alquimia@xsdk-0.6.0", when="@0.6.0 +alquimia")

    xsdk_depends_on("sundials +trilinos", when="+trilinos @0.6.0:")
    xsdk_depends_on("sundials +ginkgo", when="+ginkgo @0.8.0:")
    xsdk_depends_on(
        "sundials@develop~int64+hypre+petsc+superlu-dist",
        when="@develop",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )
    xsdk_depends_on(
        "sundials@6.4.1~int64+hypre+petsc+superlu-dist",
        when="@0.8.0",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )
    xsdk_depends_on(
        "sundials@5.8.0~int64+hypre+petsc+superlu-dist",
        when="@0.7.0",
        cuda_var="cuda",
        rocm_var="rocm",
    )
    xsdk_depends_on(
        "sundials@5.5.0~int64+hypre+petsc+superlu-dist", when="@0.6.0", cuda_var="cuda"
    )

    xsdk_depends_on("plasma@develop:", when="@develop %gcc@6.0:")
    xsdk_depends_on("plasma@22.9.29:", when="@0.8.0 %gcc@6.0:")
    xsdk_depends_on("plasma@21.8.29:", when="@0.7.0 %gcc@6.0:")
    xsdk_depends_on("plasma@20.9.20:", when="@0.6.0 %gcc@6.0:")

    xsdk_depends_on("magma@master", when="@develop", cuda_var="?cuda", rocm_var="?rocm")
    xsdk_depends_on("magma@2.7.0", when="@0.8.0", cuda_var="?cuda", rocm_var="?rocm")
    xsdk_depends_on("magma@2.6.1", when="@0.7.0", cuda_var="?cuda", rocm_var="?rocm")
    xsdk_depends_on("magma@2.5.4", when="@0.6.0", cuda_var="?cuda")

    xsdk_depends_on(
        "amrex@develop+sundials", when="@develop %intel", cuda_var="cuda", rocm_var="rocm"
    )
    xsdk_depends_on(
        "amrex@develop+sundials", when="@develop %gcc", cuda_var="cuda", rocm_var="rocm"
    )
    xsdk_depends_on(
        "amrex@develop+sundials", when="@develop %cce", cuda_var="cuda", rocm_var="rocm"
    )
    xsdk_depends_on("amrex@22.09+sundials", when="@0.8.0 %intel", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("amrex@22.09+sundials", when="@0.8.0 %gcc", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("amrex@22.09+sundials", when="@0.8.0 %cce", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("amrex@21.10+sundials", when="@0.7.0 %intel", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("amrex@21.10+sundials", when="@0.7.0 %gcc", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("amrex@21.10+sundials", when="@0.7.0 %cce", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("amrex@20.10", when="@0.6.0 %intel")
    xsdk_depends_on("amrex@20.10", when="@0.6.0 %gcc")

    xsdk_depends_on("slepc@main", when="@develop")
    xsdk_depends_on("slepc@3.18.1", when="@0.8.0", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("slepc@3.16.0", when="@0.7.0")
    xsdk_depends_on("slepc@3.14.0", when="@0.6.0")

    xsdk_depends_on("omega-h +trilinos", when="+trilinos +omega-h")
    xsdk_depends_on("omega-h ~trilinos", when="~trilinos +omega-h")
    xsdk_depends_on("omega-h@main", when="@develop +omega-h")
    xsdk_depends_on("omega-h@9.34.13", when="@0.8.0 +omega-h")
    xsdk_depends_on("omega-h@9.34.1", when="@0.7.0 +omega-h")
    xsdk_depends_on("omega-h@9.32.5", when="@0.6.0 +omega-h")

    xsdk_depends_on("strumpack ~cuda", when="~cuda @0.6.0: +strumpack")
    xsdk_depends_on("strumpack ~slate~openmp", when="~slate @0.8.0: +strumpack")
    xsdk_depends_on("strumpack@master", when="@develop +strumpack", cuda_var=["cuda"])
    xsdk_depends_on("strumpack@7.0.1", when="@0.8.0 +strumpack", cuda_var=["cuda"])
    xsdk_depends_on("strumpack@6.1.0~slate~openmp", when="@0.7.0 +strumpack")
    xsdk_depends_on("strumpack@5.0.0~slate~openmp", when="@0.6.0 +strumpack")

    xsdk_depends_on("pumi@master+shared", when="@develop")
    xsdk_depends_on("pumi@2.2.7+shared", when="@0.8.0")
    xsdk_depends_on("pumi@2.2.6", when="@0.7.0")
    xsdk_depends_on("pumi@2.2.5", when="@0.6.0")

    tasmanian_openmp = "~openmp" if sys.platform == "darwin" else "+openmp"
    xsdk_depends_on(
        "tasmanian@develop+xsdkflags+blas" + tasmanian_openmp,
        when="@develop",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )
    xsdk_depends_on(
        "tasmanian@7.9+xsdkflags+mpi+blas" + tasmanian_openmp,
        when="@0.8.0",
        cuda_var=["cuda", "?magma"],
    )
    xsdk_depends_on(
        "tasmanian@7.7+xsdkflags+mpi+blas" + tasmanian_openmp,
        when="@0.7.0",
        cuda_var=["cuda", "?magma"],
    )
    xsdk_depends_on(
        "tasmanian@7.3+xsdkflags+mpi+blas" + tasmanian_openmp,
        when="@0.6.0",
        cuda_var=["cuda", "?magma"],
    )

    xsdk_depends_on("arborx@master", when="@develop +arborx")
    xsdk_depends_on("arborx@1.2", when="@0.8.0 +arborx")
    xsdk_depends_on("arborx@1.1", when="@0.7.0 +arborx")

    # the Fortran 2003 bindings of phist require python@3:, but this
    # creates a conflict with other packages like petsc@main. Actually
    # these are type='build' dependencies, but spack reports a conflict anyway.
    # This will be fixed once the new concretizer becomes available
    # (says @adamjstewart)

    xsdk_depends_on("phist kernel_lib=tpetra", when="+trilinos +phist")
    xsdk_depends_on("phist kernel_lib=petsc", when="~trilinos +phist")
    xsdk_depends_on("phist@develop ~fortran ~scamac ~openmp ~host ~int64", when="@develop +phist")
    xsdk_depends_on("phist@1.11.2 ~fortran ~scamac ~openmp ~host ~int64", when="@0.8.0 +phist")
    xsdk_depends_on("phist@1.9.5 ~fortran ~scamac ~openmp ~host ~int64", when="@0.7.0 +phist")
    xsdk_depends_on("phist@1.9.3 ~fortran ~scamac ~openmp ~host ~int64", when="@0.6.0 +phist")

    xsdk_depends_on(
        "ginkgo@develop +mpi ~openmp", when="@develop +ginkgo", cuda_var="cuda", rocm_var="rocm"
    )
    xsdk_depends_on(
        "ginkgo@1.5.0 +mpi ~openmp", when="@0.8.0 +ginkgo", cuda_var="cuda", rocm_var="rocm"
    )
    xsdk_depends_on(
        "ginkgo@1.4.0 ~openmp", when="@0.7.0 +ginkgo", cuda_var="cuda", rocm_var="rocm"
    )
    xsdk_depends_on("ginkgo@1.3.0 ~openmp", when="@0.6.0 +ginkgo", cuda_var="cuda")

    xsdk_depends_on("py-libensemble@develop+petsc4py", when="@develop +libensemble")
    xsdk_depends_on("py-petsc4py@main", when="@develop +libensemble")
    xsdk_depends_on("py-libensemble@0.9.3+petsc4py", when="@0.8.0 +libensemble")
    xsdk_depends_on("py-petsc4py@3.18.1", when="@0.8.0 +libensemble")
    xsdk_depends_on("py-libensemble@0.8.0+petsc4py", when="@0.7.0 +libensemble")
    xsdk_depends_on("py-petsc4py@3.16.1", when="@0.7.0 +libensemble")
    xsdk_depends_on("py-libensemble@0.7.1+petsc4py", when="@0.6.0 +libensemble")
    xsdk_depends_on("py-petsc4py@3.14.0", when="@0.6.0 +libensemble")

    xsdk_depends_on("precice ~petsc", when="+precice ^cray-mpich")
    xsdk_depends_on("precice@develop", when="@develop +precice")
    xsdk_depends_on("precice@2.5.0", when="@0.8.0 +precice")
    xsdk_depends_on("precice@2.3.0", when="@0.7.0 +precice")
    xsdk_depends_on("precice@2.1.1", when="@0.6.0 +precice")

    bfpk_openmp = "~openmp" if sys.platform == "darwin" else "+openmp"
    xsdk_depends_on("butterflypack@master", when="@develop +butterflypack")
    xsdk_depends_on("butterflypack@2.2.2" + bfpk_openmp, when="@0.8.0 +butterflypack")
    xsdk_depends_on("butterflypack@2.0.0", when="@0.7.0 +butterflypack")
    xsdk_depends_on("butterflypack@1.2.1", when="@0.6.0 +butterflypack")

    xsdk_depends_on(
        "heffte@develop+fftw",
        when="@develop +heffte",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )
    xsdk_depends_on(
        "heffte@2.3.0+fftw",
        when="@0.8.0 +heffte",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )
    xsdk_depends_on(
        "heffte@2.2.0+fftw",
        when="@0.7.0 +heffte",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )
    xsdk_depends_on("heffte@2.0.0+fftw", when="@0.6.0 +heffte", cuda_var=["cuda", "?magma"])

    xsdk_depends_on("slate@master", when="@develop +slate", cuda_var="cuda")
    xsdk_depends_on("slate@2022.07.00", when="@0.8.0 +slate", cuda_var="cuda")
    xsdk_depends_on("slate@2021.05.02", when="@0.7.0 +slate %gcc@6.0:", cuda_var="cuda")
    xsdk_depends_on("slate@2020.10.00", when="@0.6.0 +slate %gcc@6.0:", cuda_var="cuda")

    xsdk_depends_on("exago@develop~ipopt~hiop~python", when="@develop +exago ~raja")
    xsdk_depends_on("exago@develop~ipopt+hiop+raja", when="@develop +exago +raja", cuda_var="cuda")
    xsdk_depends_on("exago@1.5.0~ipopt~hiop~python", when="@0.8.0 +exago ~raja")
    xsdk_depends_on("exago@1.5.0~ipopt+hiop+raja", when="@0.8.0 +exago +raja", cuda_var="cuda")

    xsdk_depends_on("hiop@develop", when="@develop +hiop ~raja")
    xsdk_depends_on("hiop@develop+raja", when="@develop +hiop +raja", cuda_var="cuda")
    xsdk_depends_on("hiop@0.7.1", when="@0.8.0 +hiop ~raja")
    xsdk_depends_on("hiop@0.7.1+raja", when="@0.8.0 +hiop +raja", cuda_var="cuda")
