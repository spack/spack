# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.build_environment import dso_suffix
from spack.error import NoHeadersError
from spack.operating_systems.mac_os import macos_version
from spack.package import *
from spack.pkg.builtin.kokkos import Kokkos

# Trilinos is complicated to build, as an inspiration a couple of links to
# other repositories which build it:
# https://github.com/hpcugent/easybuild-easyblocks/blob/master/easybuild/easyblocks/t/trilinos.py#L111
# https://github.com/koecher/candi/blob/master/deal.II-toolchain/packages/trilinos.package
# https://gitlab.com/configurations/cluster-config/blob/master/trilinos.sh
# https://github.com/Homebrew/homebrew-science/blob/master/trilinos.rb and some
# relevant documentation/examples:
# https://github.com/trilinos/Trilinos/issues/175

# Hints and tips on installation:
# ------------------------------------------------------------------------------
# Trilinos contains a large number of packages, so installing Trilinos directly
# as a spec needs to have some intention of the packages required.
# For instance, `spack install trilinos` will install Trilinos with no packages. 
# However, `spack install trilinos+muelu` will install Trilinos along with all
# packages needed to build MueLu in Trilinos. If you are installing the 
# Trilinos spec directly, this is probably all that you will need for choosing 
# packages in Trilinos that you want to enable (along with optional packages that
# those packages rely on). 
#
# tldr; only use +variant for Trilinos packages that you know you NEED (you don't have to
# worry about their other required package dependencies, it will be handled for you), and 
# do NOT use ~variant to indicate not installing a package, as the package would have 
# only been installed if it was needed.

class Trilinos(CMakePackage, CudaPackage, ROCmPackage):
    """The Trilinos Project is an effort to develop algorithms and enabling
    technologies within an object-oriented software framework for the solution
    of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """

    homepage = "https://trilinos.org/"
    url = "https://github.com/trilinos/Trilinos/archive/refs/tags/trilinos-release-12-12-1.tar.gz"
    git = "https://github.com/trilinos/Trilinos.git"

    maintainers = ["keitat", "sethrj", "kuberry"]

    tags = ["e4s"]

    # ###################### Versions ##########################

    version("master", branch="master")
    version("develop", branch="develop")
    version("13.4.0", sha256="39550006e059043b7e2177f10467ae2f77fe639901aee91cbc1e359516ff8d3e")
    version("13.2.0", sha256="0ddb47784ba7b8a6b9a07a4822b33be508feb4ccd54301b2a5d10c9e54524b90")
    version(
        "13.0.1",
        sha256="0bce7066c27e83085bc189bf524e535e5225636c9ee4b16291a38849d6c2216d",
        preferred=True,
    )
    version("13.0.0", sha256="d44e8181b3ef5eae4e90aad40a33486f0b2ae6ba1c34b419ce8cbc70fd5dd6bd")
    version(
        "12.18.1", commit="55a75997332636a28afc9db1aee4ae46fe8d93e7"
    )  # tag trilinos-release-12-8-1
    version("12.14.1", sha256="52a4406cca2241f5eea8e166c2950471dd9478ad6741cbb2a7fc8225814616f0")
    version("12.12.1", sha256="5474c5329c6309224a7e1726cf6f0d855025b2042959e4e2be2748bd6bb49e18")
    version("12.10.1", sha256="ab81d917196ffbc21c4927d42df079dd94c83c1a08bda43fef2dd34d0c1a5512")
    version("12.8.1", sha256="d20fe60e31e3ba1ef36edecd88226240a518f50a4d6edcc195b88ee9dda5b4a1")
    version("12.6.4", sha256="1c7104ba60ee8cc4ec0458a1c4f6a26130616bae7580a7b15f2771a955818b73")
    version("12.6.3", sha256="4d28298bb4074eef522db6cd1626f1a934e3d80f292caf669b8846c0a458fe81")
    version("12.6.2", sha256="8be7e3e1166cc05aea7f856cc8033182e8114aeb8f87184cb38873bfb2061779")
    version("12.6.1", sha256="4b38ede471bed0036dcb81a116fba8194f7bf1a9330da4e29c3eb507d2db18db")
    version("12.4.2", sha256="fd2c12e87a7cedc058bcb8357107ffa2474997aa7b17b8e37225a1f7c32e6f0e")
    version("12.2.1", sha256="088f303e0dc00fb4072b895c6ecb4e2a3ad9a2687b9c62153de05832cf242098")
    version("12.0.1", sha256="eee7c19ca108538fa1c77a6651b084e06f59d7c3307dae77144136639ab55980")
    version("11.14.3", sha256="e37fa5f69103576c89300e14d43ba77ad75998a54731008b25890d39892e6e60")
    version("11.14.2", sha256="f22b2b0df7b88e28b992e19044ba72b845292b93cbbb3a948488199647381119")
    version("11.14.1", sha256="f10fc0a496bf49427eb6871c80816d6e26822a39177d850cc62cf1484e4eec07")

    # ###################### Variants ##########################

    # Build options
    variant("complex", default=False, description="Enable complex numbers in Trilinos")
    variant("cuda_rdc", default=False, description="Turn on RDC for CUDA build")
    variant("rocm_rdc", default=False, description="Turn on RDC for ROCm build")
    variant("cxxstd", default="14", values=["11", "14", "17"], multi=False)
    variant("debug", default=False, description="Enable runtime safety and debug checks")
    variant(
        "explicit_template_instantiation",
        default=True,
        description="Enable explicit template instantiation (ETI)",
    )
    variant(
        "float", default=False, description="Enable single precision (float) numbers in Trilinos"
    )
    variant("fortran", default=True, description="Compile with Fortran support")
    variant(
        "gotype",
        default="long_long",
        values=("int", "long", "long_long", "all"),
        multi=False,
        description="global ordinal type for Tpetra",
    )
    variant("openmp", default=False, description="Enable OpenMP")
    variant("python", default=False, description="Build PyTrilinos wrappers")
    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("uvm", default=False, when="@13.2: +cuda", description="Turn on UVM for CUDA build")
    variant("wrapper", default=False, description="Use nvcc-wrapper for CUDA build")

    # TPLs (alphabet order)
    variant("adios2", default=False, description="Enable ADIOS2")
    variant("boost", default=False, description="Compile with Boost")
    variant("hdf5", default=False, description="Compile with HDF5")
    variant("hypre", default=False, description="Compile with Hypre preconditioner")
    variant("mpi", default=True, description="Compile with MPI parallelism")
    variant("mumps", default=False, description="Compile with support for MUMPS solvers")
    variant("suite-sparse", default=False, description="Compile with SuiteSparse solvers")
    variant("superlu-dist", default=False, description="Compile with SuperluDist solvers")
    variant("superlu", default=False, description="Compile with SuperLU solvers")
    variant("strumpack", default=False, description="Compile with STRUMPACK solvers")
    variant("x11", default=False, description="Compile with X11 when +exodus")

    # Package options (alphabet order)
    variant("exodus", default=False, description="Compile with Exodus from SEACAS")
    variant('all_optional_packages', default=False, description ='Enable optional dependencies of packages \
            (CMake equivalent of Trilinos_ENABLE_ALL_OPTIONAL_PACKAGES)')


    # Spack logic auto-generated from Tribits BEGINS here (no manual modifications)
    # Trilinos parent packages
    variant('trilinosframeworktests', default=False, description='Enable Trilinos package TrilinosFrameworkTests')
    variant('trilinosatdmconfigtests', default=False, description='Enable Trilinos package TrilinosATDMConfigTests')
    variant('gtest', default=False, description='Enable Trilinos package Gtest')
    variant('kokkos', default=False, description='Enable Trilinos package Kokkos')
    variant('teuchos', default=False, description='Enable Trilinos package Teuchos')
    variant('kokkoskernels', default=False, description='Enable Trilinos package KokkosKernels')
    variant('rtop', default=False, description='Enable Trilinos package RTOp')
    variant('sacado', default=False, description='Enable Trilinos package Sacado')
    variant('minitensor', default=False, description='Enable Trilinos package MiniTensor')
    variant('epetra', default=False, description='Enable Trilinos package Epetra')
    variant('zoltan', default=False, description='Enable Trilinos package Zoltan')
    variant('shards', default=False, description='Enable Trilinos package Shards')
    variant('triutils', default=False, description='Enable Trilinos package Triutils')
    variant('epetraext', default=False, description='Enable Trilinos package EpetraExt')
    variant('tpetra', default=False, description='Enable Trilinos package Tpetra')
    variant('trilinosss', default=False, description='Enable Trilinos package TrilinosSS')
    variant('domi', default=False, description='Enable Trilinos package Domi')
    variant('thyra', default=False, description='Enable Trilinos package Thyra')
    variant('xpetra', default=False, description='Enable Trilinos package Xpetra')
    variant('isorropia', default=False, description='Enable Trilinos package Isorropia')
    variant('pliris', default=False, description='Enable Trilinos package Pliris')
    variant('aztec', default=False, description='Enable Trilinos package AztecOO')
    variant('galeri', default=False, description='Enable Trilinos package Galeri')
    variant('amesos', default=False, description='Enable Trilinos package Amesos')
    variant('pamgen', default=False, description='Enable Trilinos package Pamgen')
    variant('zoltan2core', default=False, description='Enable Trilinos package Zoltan2Core')
    variant('ifpack', default=False, description='Enable Trilinos package Ifpack')
    variant('ml', default=False, description='Enable Trilinos package ML')
    variant('belos', default=False, description='Enable Trilinos package Belos')
    variant('shylu_node', default=False, description='Enable Trilinos package ShyLU_Node')
    variant('amesos2', default=False, description='Enable Trilinos package Amesos2')
    variant('seacas', default=False, description='Enable Trilinos package SEACAS')
    variant('komplex', default=False, description='Enable Trilinos package Komplex')
    variant('anasazi', default=False, description='Enable Trilinos package Anasazi')
    variant('ifpack2', default=False, description='Enable Trilinos package Ifpack2')
    variant('stratimikos', default=False, description='Enable Trilinos package Stratimikos')
    variant('fei', default=False, description='Enable Trilinos package FEI')
    variant('teko', default=False, description='Enable Trilinos package Teko')
    variant('trikota', default=False, description='Enable Trilinos package TriKota')
    variant('intrepid', default=False, description='Enable Trilinos package Intrepid')
    variant('intrepid2', default=False, description='Enable Trilinos package Intrepid2')
    variant('compadre', default=False, description='Enable Trilinos package Compadre')
    variant('stk', default=False, description='Enable Trilinos package STK')
    variant('percept', default=False, description='Enable Trilinos package Percept')
    variant('krino', default=False, description='Enable Trilinos package Krino')
    variant('phalanx', default=False, description='Enable Trilinos package Phalanx')
    variant('nox', default=False, description='Enable Trilinos package NOX')
    variant('moertel', default=False, description='Enable Trilinos package Moertel')
    variant('muelu', default=False, description='Enable Trilinos package MueLu')
    variant('zoltan2sphynx', default=False, description='Enable Trilinos package Zoltan2Sphynx')
    variant('zoltan2', default=False, description='Enable Trilinos package Zoltan2')
    variant('shylu_dd', default=False, description='Enable Trilinos package ShyLU_DD')
    variant('shylu', default=False, description='Enable Trilinos package ShyLU')
    variant('rythmos', default=False, description='Enable Trilinos package Rythmos')
    variant('tempus', default=False, description='Enable Trilinos package Tempus')
    variant('stokhos', default=False, description='Enable Trilinos package Stokhos')
    variant('rol', default=False, description='Enable Trilinos package ROL')
    variant('piro', default=False, description='Enable Trilinos package Piro')
    variant('panzer', default=False, description='Enable Trilinos package Panzer')
    variant('pytrilinos', default=False, description='Enable Trilinos package PyTrilinos')
    variant('adelus', default=False, description='Enable Trilinos package Adelus')
    variant('trilinoscouplings', default=False, description='Enable Trilinos package TrilinosCouplings')
    variant('pike', default=False, description='Enable Trilinos package Pike')
    variant('trilinosbuildstats', default=False, description='Enable Trilinos package TrilinosBuildStats')
    variant('trilinosinstalltests', default=False, description='Enable Trilinos package TrilinosInstallTests')
    
    # Trilinos subpackages
    variant('kokkoscore', default=False, description='Enable Trilinos subpackage KokkosCore')
    variant('kokkoscontainers', default=False, description='Enable Trilinos subpackage KokkosContainers')
    variant('kokkosalgorithms', default=False, description='Enable Trilinos subpackage KokkosAlgorithms')
    variant('teuchoscore', default=False, description='Enable Trilinos subpackage TeuchosCore')
    variant('teuchosparser', default=False, description='Enable Trilinos subpackage TeuchosParser')
    variant('teuchosparameterlist', default=False, description='Enable Trilinos subpackage TeuchosParameterList')
    variant('teuchoscomm', default=False, description='Enable Trilinos subpackage TeuchosComm')
    variant('teuchosnumerics', default=False, description='Enable Trilinos subpackage TeuchosNumerics')
    variant('teuchosremainder', default=False, description='Enable Trilinos subpackage TeuchosRemainder')
    variant('teuchoskokkoscompat', default=False, description='Enable Trilinos subpackage TeuchosKokkosCompat')
    variant('teuchoskokkoscomm', default=False, description='Enable Trilinos subpackage TeuchosKokkosComm')
    variant('tpetratsqr', default=False, description='Enable Trilinos subpackage TpetraTSQR')
    variant('tpetracore', default=False, description='Enable Trilinos subpackage TpetraCore')
    variant('thyracore', default=False, description='Enable Trilinos subpackage ThyraCore')
    variant('thyraepetraadapters', default=False, description='Enable Trilinos subpackage ThyraEpetraAdapters')
    variant('thyraepetraextadapters', default=False, description='Enable Trilinos subpackage ThyraEpetraExtAdapters')
    variant('thyratpetraadapters', default=False, description='Enable Trilinos subpackage ThyraTpetraAdapters')
    variant('shylu_nodehts', default=False, description='Enable Trilinos subpackage ShyLU_NodeHTS')
    variant('shylu_nodetacho', default=False, description='Enable Trilinos subpackage ShyLU_NodeTacho')
    variant('seacasexodus', default=False, description='Enable Trilinos subpackage SEACASExodus')
    variant('seacasexodus_for', default=False, description='Enable Trilinos subpackage SEACASExodus_for')
    variant('seacasexoiiv2for32', default=False, description='Enable Trilinos subpackage SEACASExoIIv2for32')
    variant('seacasnemesis', default=False, description='Enable Trilinos subpackage SEACASNemesis')
    variant('seacasioss', default=False, description='Enable Trilinos subpackage SEACASIoss')
    variant('seacaschaco', default=False, description='Enable Trilinos subpackage SEACASChaco')
    variant('seacasaprepro_lib', default=False, description='Enable Trilinos subpackage SEACASAprepro_lib')
    variant('seacassupes', default=False, description='Enable Trilinos subpackage SEACASSupes')
    variant('seacassuplib', default=False, description='Enable Trilinos subpackage SEACASSuplib')
    variant('seacassuplibc', default=False, description='Enable Trilinos subpackage SEACASSuplibC')
    variant('seacassuplibcpp', default=False, description='Enable Trilinos subpackage SEACASSuplibCpp')
    variant('seacassvdi', default=False, description='Enable Trilinos subpackage SEACASSVDI')
    variant('seacasplt', default=False, description='Enable Trilinos subpackage SEACASPLT')
    variant('seacasalgebra', default=False, description='Enable Trilinos subpackage SEACASAlgebra')
    variant('seacasaprepro', default=False, description='Enable Trilinos subpackage SEACASAprepro')
    variant('seacasblot', default=False, description='Enable Trilinos subpackage SEACASBlot')
    variant('seacasconjoin', default=False, description='Enable Trilinos subpackage SEACASConjoin')
    variant('seacasejoin', default=False, description='Enable Trilinos subpackage SEACASEjoin')
    variant('seacasepu', default=False, description='Enable Trilinos subpackage SEACASEpu')
    variant('seacascpup', default=False, description='Enable Trilinos subpackage SEACASCpup')
    variant('seacasexo2mat', default=False, description='Enable Trilinos subpackage SEACASExo2mat')
    variant('seacasexodiff', default=False, description='Enable Trilinos subpackage SEACASExodiff')
    variant('seacasexomatlab', default=False, description='Enable Trilinos subpackage SEACASExomatlab')
    variant('seacasexotxt', default=False, description='Enable Trilinos subpackage SEACASExotxt')
    variant('seacasexo_format', default=False, description='Enable Trilinos subpackage SEACASExo_format')
    variant('seacasex1ex2v2', default=False, description='Enable Trilinos subpackage SEACASEx1ex2v2')
    variant('seacasfastq', default=False, description='Enable Trilinos subpackage SEACASFastq')
    variant('seacasgjoin', default=False, description='Enable Trilinos subpackage SEACASGjoin')
    variant('seacasgen3d', default=False, description='Enable Trilinos subpackage SEACASGen3D')
    variant('seacasgenshell', default=False, description='Enable Trilinos subpackage SEACASGenshell')
    variant('seacasgrepos', default=False, description='Enable Trilinos subpackage SEACASGrepos')
    variant('seacasexplore', default=False, description='Enable Trilinos subpackage SEACASExplore')
    variant('seacasmapvarlib', default=False, description='Enable Trilinos subpackage SEACASMapvarlib')
    variant('seacasmapvar', default=False, description='Enable Trilinos subpackage SEACASMapvar')
    variant('seacasmapvar-kd', default=False, description='Enable Trilinos subpackage SEACASMapvar-kd')
    variant('seacasmat2exo', default=False, description='Enable Trilinos subpackage SEACASMat2exo')
    variant('seacasnas2exo', default=False, description='Enable Trilinos subpackage SEACASNas2exo')
    variant('seacaszellij', default=False, description='Enable Trilinos subpackage SEACASZellij')
    variant('seacasnemslice', default=False, description='Enable Trilinos subpackage SEACASNemslice')
    variant('seacasnemspread', default=False, description='Enable Trilinos subpackage SEACASNemspread')
    variant('seacasnumbers', default=False, description='Enable Trilinos subpackage SEACASNumbers')
    variant('seacasslice', default=False, description='Enable Trilinos subpackage SEACASSlice')
    variant('seacastxtexo', default=False, description='Enable Trilinos subpackage SEACASTxtexo')
    variant('seacasex2ex1v2', default=False, description='Enable Trilinos subpackage SEACASEx2ex1v2')
    variant('stkutil', default=False, description='Enable Trilinos subpackage STKUtil')
    variant('stkemend', default=False, description='Enable Trilinos subpackage STKEmend')
    variant('stkcoupling', default=False, description='Enable Trilinos subpackage STKCoupling')
    variant('stkmath', default=False, description='Enable Trilinos subpackage STKMath')
    variant('stksimd', default=False, description='Enable Trilinos subpackage STKSimd')
    variant('stkngp_test', default=False, description='Enable Trilinos subpackage STKNGP_TEST')
    variant('stktopology', default=False, description='Enable Trilinos subpackage STKTopology')
    variant('stkmesh', default=False, description='Enable Trilinos subpackage STKMesh')
    variant('stkio', default=False, description='Enable Trilinos subpackage STKIO')
    variant('stksearch', default=False, description='Enable Trilinos subpackage STKSearch')
    variant('stktransfer', default=False, description='Enable Trilinos subpackage STKTransfer')
    variant('stktools', default=False, description='Enable Trilinos subpackage STKTools')
    variant('stkbalance', default=False, description='Enable Trilinos subpackage STKBalance')
    variant('stkunit_test_utils', default=False, description='Enable Trilinos subpackage STKUnit_test_utils')
    variant('stksearchutil', default=False, description='Enable Trilinos subpackage STKSearchUtil')
    variant('stkunit_tests', default=False, description='Enable Trilinos subpackage STKUnit_tests')
    variant('stkdoc_tests', default=False, description='Enable Trilinos subpackage STKDoc_tests')
    variant('stkexpreval', default=False, description='Enable Trilinos subpackage STKExprEval')
    variant('shylu_ddfrosch', default=False, description='Enable Trilinos subpackage ShyLU_DDFROSch')
    variant('shylu_ddcommon', default=False, description='Enable Trilinos subpackage ShyLU_DDCommon')
    variant('panzercore', default=False, description='Enable Trilinos subpackage PanzerCore')
    variant('panzerdofmgr', default=False, description='Enable Trilinos subpackage PanzerDofMgr')
    variant('panzerdiscfe', default=False, description='Enable Trilinos subpackage PanzerDiscFE')
    variant('panzeradaptersstk', default=False, description='Enable Trilinos subpackage PanzerAdaptersSTK')
    variant('panzerminiem', default=False, description='Enable Trilinos subpackage PanzerMiniEM')
    variant('pikeblackbox', default=False, description='Enable Trilinos subpackage PikeBlackBox')
    variant('pikeimplicit', default=False, description='Enable Trilinos subpackage PikeImplicit')
    
    # parent packages (if enabled) enable all subpackages
    conflicts('~kokkoscore', when='+kokkos')
    conflicts('~kokkoscontainers', when='+kokkos')
    conflicts('~kokkosalgorithms', when='+kokkos')
    conflicts('~teuchoscore', when='+teuchos')
    conflicts('~teuchosparser', when='+teuchos')
    conflicts('~teuchosparameterlist', when='+teuchos')
    conflicts('~teuchoscomm', when='+teuchos')
    conflicts('~teuchosnumerics', when='+teuchos')
    conflicts('~teuchosremainder', when='+teuchos')
    conflicts('~teuchoskokkoscompat', when='+teuchos')
    conflicts('~teuchoskokkoscomm', when='+teuchos')
    conflicts('~tpetratsqr', when='+tpetra')
    conflicts('~tpetracore', when='+tpetra')
    conflicts('~thyracore', when='+thyra')
    conflicts('~thyraepetraadapters', when='+thyra')
    conflicts('~thyraepetraextadapters', when='+thyra')
    conflicts('~thyratpetraadapters', when='+thyra')
    conflicts('~shylu_nodehts', when='+shylu_node')
    conflicts('~shylu_nodetacho', when='+shylu_node')
    conflicts('~seacasexodus', when='+seacas')
    conflicts('~seacasexodus_for', when='+seacas')
    conflicts('~seacasexoiiv2for32', when='+seacas')
    conflicts('~seacasnemesis', when='+seacas')
    conflicts('~seacasioss', when='+seacas')
    conflicts('~seacaschaco', when='+seacas')
    conflicts('~seacasaprepro_lib', when='+seacas')
    conflicts('~seacassupes', when='+seacas')
    conflicts('~seacassuplib', when='+seacas')
    conflicts('~seacassuplibc', when='+seacas')
    conflicts('~seacassuplibcpp', when='+seacas')
    conflicts('~seacassvdi', when='+seacas')
    conflicts('~seacasplt', when='+seacas')
    conflicts('~seacasalgebra', when='+seacas')
    conflicts('~seacasaprepro', when='+seacas')
    conflicts('~seacasblot', when='+seacas')
    conflicts('~seacasconjoin', when='+seacas')
    conflicts('~seacasejoin', when='+seacas')
    conflicts('~seacasepu', when='+seacas')
    conflicts('~seacascpup', when='+seacas')
    conflicts('~seacasexo2mat', when='+seacas')
    conflicts('~seacasexodiff', when='+seacas')
    conflicts('~seacasexomatlab', when='+seacas')
    conflicts('~seacasexotxt', when='+seacas')
    conflicts('~seacasexo_format', when='+seacas')
    conflicts('~seacasex1ex2v2', when='+seacas')
    conflicts('~seacasfastq', when='+seacas')
    conflicts('~seacasgjoin', when='+seacas')
    conflicts('~seacasgen3d', when='+seacas')
    conflicts('~seacasgenshell', when='+seacas')
    conflicts('~seacasgrepos', when='+seacas')
    conflicts('~seacasexplore', when='+seacas')
    conflicts('~seacasmapvarlib', when='+seacas')
    conflicts('~seacasmapvar', when='+seacas')
    conflicts('~seacasmapvar-kd', when='+seacas')
    conflicts('~seacasmat2exo', when='+seacas')
    conflicts('~seacasnas2exo', when='+seacas')
    conflicts('~seacaszellij', when='+seacas')
    conflicts('~seacasnemslice', when='+seacas')
    conflicts('~seacasnemspread', when='+seacas')
    conflicts('~seacasnumbers', when='+seacas')
    conflicts('~seacasslice', when='+seacas')
    conflicts('~seacastxtexo', when='+seacas')
    conflicts('~seacasex2ex1v2', when='+seacas')
    conflicts('~stkutil', when='+stk')
    conflicts('~stkemend', when='+stk')
    conflicts('~stkcoupling', when='+stk')
    conflicts('~stkmath', when='+stk')
    conflicts('~stksimd', when='+stk')
    conflicts('~stkngp_test', when='+stk')
    conflicts('~stktopology', when='+stk')
    conflicts('~stkmesh', when='+stk')
    conflicts('~stkio', when='+stk')
    conflicts('~stksearch', when='+stk')
    conflicts('~stktransfer', when='+stk')
    conflicts('~stktools', when='+stk')
    conflicts('~stkbalance', when='+stk')
    conflicts('~stkunit_test_utils', when='+stk')
    conflicts('~stksearchutil', when='+stk')
    conflicts('~stkunit_tests', when='+stk')
    conflicts('~stkdoc_tests', when='+stk')
    conflicts('~stkexpreval', when='+stk')
    conflicts('~shylu_ddfrosch', when='+shylu_dd')
    conflicts('~shylu_ddcommon', when='+shylu_dd')
    conflicts('~panzercore', when='+panzer')
    conflicts('~panzerdofmgr', when='+panzer')
    conflicts('~panzerdiscfe', when='+panzer')
    conflicts('~panzeradaptersstk', when='+panzer')
    conflicts('~panzerminiem', when='+panzer')
    conflicts('~pikeblackbox', when='+pike')
    conflicts('~pikeimplicit', when='+pike')
    
    # register required package dependencies
    conflicts('~kokkoscore', when='+kokkoscontainers')
    conflicts('~kokkoscore', when='+kokkosalgorithms')
    conflicts('~kokkoscontainers', when='+kokkosalgorithms')
    conflicts('~kokkoscore', when='+kokkos')
    conflicts('~teuchoscore', when='+teuchosparser')
    conflicts('~teuchoscore', when='+teuchosparameterlist')
    conflicts('~teuchosparser', when='+teuchosparameterlist')
    conflicts('~teuchoscore', when='+teuchoscomm')
    conflicts('~teuchosparameterlist', when='+teuchoscomm')
    conflicts('~teuchoscore', when='+teuchosnumerics')
    conflicts('~teuchoscomm', when='+teuchosnumerics')
    conflicts('~teuchoscore', when='+teuchosremainder')
    conflicts('~kokkoscore', when='+teuchoskokkoscompat')
    conflicts('~teuchoscore', when='+teuchoskokkoscompat')
    conflicts('~teuchosparameterlist', when='+teuchoskokkoscompat')
    conflicts('~kokkoscore', when='+teuchoskokkoscomm')
    conflicts('~teuchoskokkoscompat', when='+teuchoskokkoscomm')
    conflicts('~teuchoscomm', when='+teuchoskokkoscomm')
    conflicts('~teuchoscore', when='+teuchos')
    conflicts('~teuchosparser', when='+teuchos')
    conflicts('~teuchosparameterlist', when='+teuchos')
    conflicts('~teuchoscomm', when='+teuchos')
    conflicts('~teuchosnumerics', when='+teuchos')
    conflicts('~teuchosremainder', when='+teuchos')
    conflicts('~kokkoscore', when='+kokkoskernels')
    conflicts('~kokkoscontainers', when='+kokkoskernels')
    conflicts('~kokkosalgorithms', when='+kokkoskernels')
    conflicts('~teuchoscore', when='+rtop')
    conflicts('~teuchoscomm', when='+rtop')
    conflicts('~teuchosnumerics', when='+rtop')
    conflicts('~teuchoscore', when='+minitensor')
    conflicts('~kokkoscore', when='+minitensor')
    conflicts('~kokkoskernels', when='+minitensor')
    conflicts('~sacado', when='+minitensor')
    conflicts('~gtest', when='+minitensor')
    conflicts('~teuchoscore', when='+triutils')
    conflicts('~teuchos', when='+epetraext')
    conflicts('~epetra', when='+epetraext')
    conflicts('~teuchos', when='+tpetratsqr')
    conflicts('~kokkoscore', when='+tpetratsqr')
    conflicts('~kokkoskernels', when='+tpetratsqr')
    conflicts('~teuchos', when='+tpetracore')
    conflicts('~kokkoscore', when='+tpetracore')
    conflicts('~kokkoscontainers', when='+tpetracore')
    conflicts('~kokkosalgorithms', when='+tpetracore')
    conflicts('~teuchoskokkoscompat', when='+tpetracore')
    conflicts('~teuchoskokkoscomm', when='+tpetracore')
    conflicts('~kokkoskernels', when='+tpetracore')
    conflicts('~tpetracore', when='+tpetra')
    conflicts('~teuchos', when='+domi')
    conflicts('~kokkos', when='+domi')
    conflicts('~teuchoskokkoscompat', when='+domi')
    conflicts('~teuchoscore', when='+thyracore')
    conflicts('~teuchosparameterlist', when='+thyracore')
    conflicts('~teuchoscomm', when='+thyracore')
    conflicts('~teuchosnumerics', when='+thyracore')
    conflicts('~rtop', when='+thyracore')
    conflicts('~thyracore', when='+thyraepetraadapters')
    conflicts('~epetra', when='+thyraepetraadapters')
    conflicts('~triutils', when='+thyraepetraadapters')
    conflicts('~thyracore', when='+thyraepetraextadapters')
    conflicts('~thyraepetraadapters', when='+thyraepetraextadapters')
    conflicts('~epetra', when='+thyraepetraextadapters')
    conflicts('~epetraext', when='+thyraepetraextadapters')
    conflicts('~thyracore', when='+thyratpetraadapters')
    conflicts('~tpetra', when='+thyratpetraadapters')
    conflicts('~thyracore', when='+thyra')
    conflicts('~teuchos', when='+xpetra')
    conflicts('~kokkoscore', when='+xpetra')
    conflicts('~kokkoscontainers', when='+xpetra')
    conflicts('~teuchos', when='+isorropia')
    conflicts('~epetra', when='+isorropia')
    conflicts('~epetraext', when='+isorropia')
    conflicts('~zoltan', when='+isorropia')
    conflicts('~epetra', when='+pliris')
    conflicts('~epetra', when='+aztec')
    conflicts('~triutils', when='+aztec')
    conflicts('~teuchos', when='+galeri')
    conflicts('~teuchos', when='+amesos')
    conflicts('~epetra', when='+amesos')
    conflicts('~trilinosss', when='+amesos')
    conflicts('~tpetra', when='+zoltan2core')
    conflicts('~teuchoscore', when='+zoltan2core')
    conflicts('~teuchoscomm', when='+zoltan2core')
    conflicts('~teuchosparameterlist', when='+zoltan2core')
    conflicts('~xpetra', when='+zoltan2core')
    conflicts('~zoltan', when='+zoltan2core')
    conflicts('~tpetra', when='+zoltan2core')
    conflicts('~teuchoscore', when='+zoltan2core')
    conflicts('~teuchoscomm', when='+zoltan2core')
    conflicts('~teuchosparameterlist', when='+zoltan2core')
    conflicts('~xpetra', when='+zoltan2core')
    conflicts('~zoltan', when='+zoltan2core')
    conflicts('~teuchos', when='+ifpack')
    conflicts('~epetra', when='+ifpack')
    conflicts('~teuchos', when='+belos')
    conflicts('~kokkos', when='+shylu_nodetacho')
    conflicts('~kokkos', when='+shylu_nodetacho')
    conflicts('~kokkosalgorithms', when='+shylu_nodetacho')
    conflicts('~teuchos', when='+amesos2')
    conflicts('~tpetra', when='+amesos2')
    conflicts('~trilinosss', when='+amesos2')
    conflicts('~kokkos', when='+amesos2')
    conflicts('~seacasexodus', when='+seacasexodus_for')
    conflicts('~seacasexodus', when='+seacasexoiiv2for32')
    conflicts('~seacasexodus', when='+seacasnemesis')
    conflicts('~seacassupes', when='+seacassuplib')
    conflicts('~seacassvdi', when='+seacasplt')
    conflicts('~seacassupes', when='+seacasalgebra')
    conflicts('~seacassuplib', when='+seacasalgebra')
    conflicts('~seacasexodus_for', when='+seacasalgebra')
    conflicts('~seacasaprepro_lib', when='+seacasaprepro')
    conflicts('~seacassupes', when='+seacasblot')
    conflicts('~seacassuplib', when='+seacasblot')
    conflicts('~seacasexodus_for', when='+seacasblot')
    conflicts('~seacasplt', when='+seacasblot')
    conflicts('~seacasexodus', when='+seacasconjoin')
    conflicts('~seacassuplibc', when='+seacasconjoin')
    conflicts('~seacassuplibcpp', when='+seacasconjoin')
    conflicts('~seacasexodus', when='+seacasejoin')
    conflicts('~seacasioss', when='+seacasejoin')
    conflicts('~seacassuplibc', when='+seacasejoin')
    conflicts('~seacassuplibcpp', when='+seacasejoin')
    conflicts('~seacasexodus', when='+seacasepu')
    conflicts('~seacassuplibc', when='+seacasepu')
    conflicts('~seacassuplibcpp', when='+seacasepu')
    conflicts('~seacasexodus', when='+seacascpup')
    conflicts('~seacasioss', when='+seacascpup')
    conflicts('~seacassuplibc', when='+seacascpup')
    conflicts('~seacassuplibcpp', when='+seacascpup')
    conflicts('~seacasexodus', when='+seacasexo2mat')
    conflicts('~seacassuplibc', when='+seacasexo2mat')
    conflicts('~seacassuplibcpp', when='+seacasexo2mat')
    conflicts('~seacasexodus', when='+seacasexodiff')
    conflicts('~seacassuplibc', when='+seacasexodiff')
    conflicts('~seacassuplibcpp', when='+seacasexodiff')
    conflicts('~seacasioss', when='+seacasexomatlab')
    conflicts('~seacassuplibc', when='+seacasexomatlab')
    conflicts('~seacassuplibcpp', when='+seacasexomatlab')
    conflicts('~seacassupes', when='+seacasexotxt')
    conflicts('~seacassuplib', when='+seacasexotxt')
    conflicts('~seacasexodus_for', when='+seacasexotxt')
    conflicts('~seacasexodus', when='+seacasexo_format')
    conflicts('~seacassupes', when='+seacasex1ex2v2')
    conflicts('~seacassuplib', when='+seacasex1ex2v2')
    conflicts('~seacasexodus_for', when='+seacasex1ex2v2')
    conflicts('~seacassupes', when='+seacasfastq')
    conflicts('~seacassuplib', when='+seacasfastq')
    conflicts('~seacasexodus_for', when='+seacasfastq')
    conflicts('~seacasplt', when='+seacasfastq')
    conflicts('~seacassupes', when='+seacasgjoin')
    conflicts('~seacassuplib', when='+seacasgjoin')
    conflicts('~seacasexodus_for', when='+seacasgjoin')
    conflicts('~seacassupes', when='+seacasgen3d')
    conflicts('~seacassuplib', when='+seacasgen3d')
    conflicts('~seacasexodus_for', when='+seacasgen3d')
    conflicts('~seacassupes', when='+seacasgenshell')
    conflicts('~seacassuplib', when='+seacasgenshell')
    conflicts('~seacasexodus_for', when='+seacasgenshell')
    conflicts('~seacassupes', when='+seacasgrepos')
    conflicts('~seacassuplib', when='+seacasgrepos')
    conflicts('~seacasexodus_for', when='+seacasgrepos')
    conflicts('~seacassupes', when='+seacasexplore')
    conflicts('~seacassuplib', when='+seacasexplore')
    conflicts('~seacasexodus_for', when='+seacasexplore')
    conflicts('~seacassupes', when='+seacasmapvarlib')
    conflicts('~seacassuplib', when='+seacasmapvarlib')
    conflicts('~seacasexodus_for', when='+seacasmapvarlib')
    conflicts('~seacassupes', when='+seacasmapvar')
    conflicts('~seacassuplib', when='+seacasmapvar')
    conflicts('~seacasexodus_for', when='+seacasmapvar')
    conflicts('~seacasmapvarlib', when='+seacasmapvar')
    conflicts('~seacassupes', when='+seacasmapvar-kd')
    conflicts('~seacassuplib', when='+seacasmapvar-kd')
    conflicts('~seacasexodus_for', when='+seacasmapvar-kd')
    conflicts('~seacasmapvarlib', when='+seacasmapvar-kd')
    conflicts('~seacasexodus', when='+seacasmat2exo')
    conflicts('~seacassuplibc', when='+seacasmat2exo')
    conflicts('~seacassuplibcpp', when='+seacasmat2exo')
    conflicts('~seacasexodus', when='+seacasnas2exo')
    conflicts('~seacassuplibc', when='+seacasnas2exo')
    conflicts('~seacassuplibcpp', when='+seacasnas2exo')
    conflicts('~seacasexodus', when='+seacaszellij')
    conflicts('~seacasioss', when='+seacaszellij')
    conflicts('~seacassuplibc', when='+seacaszellij')
    conflicts('~seacassuplibcpp', when='+seacaszellij')
    conflicts('~seacasexodus', when='+seacasnemslice')
    conflicts('~seacaschaco', when='+seacasnemslice')
    conflicts('~seacassuplibc', when='+seacasnemslice')
    conflicts('~seacassuplibcpp', when='+seacasnemslice')
    conflicts('~seacasexodus', when='+seacasnemspread')
    conflicts('~seacassuplibc', when='+seacasnemspread')
    conflicts('~seacassuplibcpp', when='+seacasnemspread')
    conflicts('~seacassupes', when='+seacasnumbers')
    conflicts('~seacassuplib', when='+seacasnumbers')
    conflicts('~seacasexodus_for', when='+seacasnumbers')
    conflicts('~seacasexodus', when='+seacasslice')
    conflicts('~seacasioss', when='+seacasslice')
    conflicts('~seacassuplibc', when='+seacasslice')
    conflicts('~seacassuplibcpp', when='+seacasslice')
    conflicts('~seacassupes', when='+seacastxtexo')
    conflicts('~seacassuplib', when='+seacastxtexo')
    conflicts('~seacasexodus_for', when='+seacastxtexo')
    conflicts('~seacassupes', when='+seacasex2ex1v2')
    conflicts('~seacassuplib', when='+seacasex2ex1v2')
    conflicts('~seacasexodus_for', when='+seacasex2ex1v2')
    conflicts('~seacasexodus', when='+seacas')
    conflicts('~seacasioss', when='+seacas')
    conflicts('~teuchos', when='+komplex')
    conflicts('~epetra', when='+komplex')
    conflicts('~aztec', when='+komplex')
    conflicts('~teuchos', when='+anasazi')
    conflicts('~belos', when='+ifpack2')
    conflicts('~teuchos', when='+ifpack2')
    conflicts('~tpetra', when='+ifpack2')
    conflicts('~kokkoskernels', when='+ifpack2')
    conflicts('~belos', when='+ifpack2')
    conflicts('~galeri', when='+ifpack2')
    conflicts('~thyracore', when='+stratimikos')
    conflicts('~thyraepetraadapters', when='+stratimikos')
    conflicts('~teuchos', when='+fei')
    conflicts('~epetra', when='+fei')
    conflicts('~teuchos', when='+teko')
    conflicts('~thyra', when='+teko')
    conflicts('~thyraepetraadapters', when='+teko')
    conflicts('~thyraepetraextadapters', when='+teko')
    conflicts('~stratimikos', when='+teko')
    conflicts('~aztec', when='+teko')
    conflicts('~anasazi', when='+teko')
    conflicts('~ml', when='+teko')
    conflicts('~ifpack', when='+teko')
    conflicts('~amesos', when='+teko')
    conflicts('~tpetra', when='+teko')
    conflicts('~thyratpetraadapters', when='+teko')
    conflicts('~ifpack2', when='+teko')
    conflicts('~teuchos', when='+trikota')
    conflicts('~epetra', when='+trikota')
    conflicts('~epetraext', when='+trikota')
    conflicts('~thyra', when='+trikota')
    conflicts('~teuchos', when='+intrepid')
    conflicts('~shards', when='+intrepid')
    conflicts('~sacado', when='+intrepid')
    conflicts('~gtest', when='+intrepid')
    conflicts('~teuchoscore', when='+intrepid2')
    conflicts('~teuchosnumerics', when='+intrepid2')
    conflicts('~shards', when='+intrepid2')
    conflicts('~kokkoscore', when='+intrepid2')
    conflicts('~kokkoscontainers', when='+intrepid2')
    conflicts('~kokkosalgorithms', when='+intrepid2')
    conflicts('~kokkoscore', when='+compadre')
    conflicts('~kokkoscontainers', when='+compadre')
    conflicts('~kokkosalgorithms', when='+compadre')
    conflicts('~kokkoskernels', when='+compadre')
    conflicts('~teuchoscore', when='+stkutil')
    conflicts('~kokkoscore', when='+stkutil')
    conflicts('~gtest', when='+stkutil')
    conflicts('~stkutil', when='+stkemend')
    conflicts('~teuchoscore', when='+stkcoupling')
    conflicts('~stkutil', when='+stkcoupling')
    conflicts('~gtest', when='+stkcoupling')
    conflicts('~kokkoscore', when='+stkmath')
    conflicts('~stkutil', when='+stkmath')
    conflicts('~gtest', when='+stkmath')
    conflicts('~kokkoscore', when='+stksimd')
    conflicts('~stkmath', when='+stksimd')
    conflicts('~gtest', when='+stksimd')
    conflicts('~gtest', when='+stkngp_test')
    conflicts('~kokkos', when='+stkngp_test')
    conflicts('~kokkoscore', when='+stkngp_test')
    conflicts('~kokkoscontainers', when='+stkngp_test')
    conflicts('~stkutil', when='+stktopology')
    conflicts('~teuchoscore', when='+stkmesh')
    conflicts('~shards', when='+stkmesh')
    conflicts('~stktopology', when='+stkmesh')
    conflicts('~stkutil', when='+stkmesh')
    conflicts('~kokkos', when='+stkmesh')
    conflicts('~kokkoscore', when='+stkmesh')
    conflicts('~teuchoscore', when='+stkio')
    conflicts('~seacasioss', when='+stkio')
    conflicts('~stkutil', when='+stkio')
    conflicts('~stkmesh', when='+stkio')
    conflicts('~gtest', when='+stkio')
    conflicts('~stkutil', when='+stksearch')
    conflicts('~kokkos', when='+stksearch')
    conflicts('~kokkoskernels', when='+stksearch')
    conflicts('~stkmath', when='+stksearch')
    conflicts('~stkutil', when='+stktransfer')
    conflicts('~stksearch', when='+stktransfer')
    conflicts('~stkio', when='+stktools')
    conflicts('~stkmesh', when='+stktools')
    conflicts('~stkutil', when='+stktools')
    conflicts('~stktransfer', when='+stktools')
    conflicts('~stktopology', when='+stktools')
    conflicts('~gtest', when='+stktools')
    conflicts('~teuchoscore', when='+stkbalance')
    conflicts('~teuchosparameterlist', when='+stkbalance')
    conflicts('~seacasnemesis', when='+stkbalance')
    conflicts('~seacasexodus', when='+stkbalance')
    conflicts('~seacasioss', when='+stkbalance')
    conflicts('~zoltan2core', when='+stkbalance')
    conflicts('~stkutil', when='+stkbalance')
    conflicts('~stksearch', when='+stkbalance')
    conflicts('~stkmesh', when='+stkbalance')
    conflicts('~stkio', when='+stkbalance')
    conflicts('~stktools', when='+stkbalance')
    conflicts('~stktopology', when='+stkbalance')
    conflicts('~gtest', when='+stkbalance')
    conflicts('~stkutil', when='+stkunit_test_utils')
    conflicts('~stkngp_test', when='+stkunit_test_utils')
    conflicts('~stktopology', when='+stkunit_test_utils')
    conflicts('~gtest', when='+stkunit_test_utils')
    conflicts('~stksearch', when='+stksearchutil')
    conflicts('~stkmesh', when='+stksearchutil')
    conflicts('~stkutil', when='+stksearchutil')
    conflicts('~gtest', when='+stksearchutil')
    conflicts('~stkunit_test_utils', when='+stksearchutil')
    conflicts('~gtest', when='+stkunit_tests')
    conflicts('~stkutil', when='+stkunit_tests')
    conflicts('~stkunit_test_utils', when='+stkunit_tests')
    conflicts('~gtest', when='+stkdoc_tests')
    conflicts('~stkutil', when='+stkdoc_tests')
    conflicts('~stkngp_test', when='+stkdoc_tests')
    conflicts('~stkunit_test_utils', when='+stkdoc_tests')
    conflicts('~stkutil', when='+stkexpreval')
    conflicts('~stkmath', when='+stkexpreval')
    conflicts('~kokkoscontainers', when='+stkexpreval')
    conflicts('~gtest', when='+stkexpreval')
    conflicts('~stkunit_test_utils', when='+stkexpreval')
    conflicts('~seacasioss', when='+percept')
    conflicts('~stkutil', when='+percept')
    conflicts('~stkio', when='+percept')
    conflicts('~stkmesh', when='+percept')
    conflicts('~stkexpreval', when='+percept')
    conflicts('~stksearch', when='+percept')
    conflicts('~stktransfer', when='+percept')
    conflicts('~intrepid', when='+percept')
    conflicts('~seacasioss', when='+krino')
    conflicts('~seacasexodus', when='+krino')
    conflicts('~seacasaprepro', when='+krino')
    conflicts('~stkbalance', when='+krino')
    conflicts('~stkmath', when='+krino')
    conflicts('~stkio', when='+krino')
    conflicts('~stksearch', when='+krino')
    conflicts('~stktopology', when='+krino')
    conflicts('~stkutil', when='+krino')
    conflicts('~stktools', when='+krino')
    conflicts('~stkemend', when='+krino')
    conflicts('~percept', when='+krino')
    conflicts('~intrepid', when='+krino')
    conflicts('~gtest', when='+krino')
    conflicts('~stkunit_test_utils', when='+krino')
    conflicts('~teuchoscore', when='+phalanx')
    conflicts('~teuchosparameterlist', when='+phalanx')
    conflicts('~teuchoscomm', when='+phalanx')
    conflicts('~kokkoscore', when='+phalanx')
    conflicts('~kokkoscontainers', when='+phalanx')
    conflicts('~sacado', when='+phalanx')
    conflicts('~kokkoskernels', when='+phalanx')
    conflicts('~teuchos', when='+nox')
    conflicts('~teuchos', when='+moertel')
    conflicts('~epetra', when='+moertel')
    conflicts('~epetraext', when='+moertel')
    conflicts('~amesos', when='+moertel')
    conflicts('~aztec', when='+moertel')
    conflicts('~ifpack', when='+moertel')
    conflicts('~ml', when='+moertel')
    conflicts('~galeri', when='+moertel')
    conflicts('~teuchos', when='+muelu')
    conflicts('~xpetra', when='+muelu')
    conflicts('~kokkoscore', when='+muelu')
    conflicts('~kokkoscontainers', when='+muelu')
    conflicts('~kokkoskernels', when='+muelu')
    conflicts('~galeri', when='+muelu')
    conflicts('~anasazi', when='+zoltan2sphynx')
    conflicts('~belos', when='+zoltan2sphynx')
    conflicts('~ifpack2', when='+zoltan2sphynx')
    conflicts('~zoltan2core', when='+zoltan2sphynx')
    conflicts('~anasazi', when='+zoltan2sphynx')
    conflicts('~belos', when='+zoltan2sphynx')
    conflicts('~ifpack2', when='+zoltan2sphynx')
    conflicts('~zoltan2core', when='+zoltan2sphynx')
    conflicts('~zoltan2core', when='+zoltan2')
    conflicts('~tpetra', when='+zoltan2')
    conflicts('~teuchoscore', when='+zoltan2')
    conflicts('~teuchoscomm', when='+zoltan2')
    conflicts('~teuchosparameterlist', when='+zoltan2')
    conflicts('~xpetra', when='+zoltan2')
    conflicts('~zoltan', when='+zoltan2')
    conflicts('~amesos2', when='+shylu_ddfrosch')
    conflicts('~teuchos', when='+shylu_ddfrosch')
    conflicts('~tpetra', when='+shylu_ddfrosch')
    conflicts('~xpetra', when='+shylu_ddfrosch')
    conflicts('~galeri', when='+shylu_ddfrosch')
    conflicts('~shylu_ddfrosch', when='+shylu_dd')
    conflicts('~shylu_dd', when='+shylu')
    conflicts('~shylu_node', when='+shylu')
    conflicts('~teuchos', when='+rythmos')
    conflicts('~thyracore', when='+rythmos')
    conflicts('~teuchoscore', when='+tempus')
    conflicts('~teuchosparameterlist', when='+tempus')
    conflicts('~teuchoscomm', when='+tempus')
    conflicts('~thyracore', when='+tempus')
    conflicts('~nox', when='+tempus')
    conflicts('~epetra', when='+tempus')
    conflicts('~thyraepetraadapters', when='+tempus')
    conflicts('~belos', when='+tempus')
    conflicts('~stratimikos', when='+tempus')
    conflicts('~teuchos', when='+stokhos')
    conflicts('~kokkoscore', when='+stokhos')
    conflicts('~teuchos', when='+rol')
    conflicts('~teuchos', when='+piro')
    conflicts('~stratimikos', when='+piro')
    conflicts('~thyracore', when='+piro')
    conflicts('~teuchoscore', when='+panzercore')
    conflicts('~teuchoscomm', when='+panzercore')
    conflicts('~teuchosparameterlist', when='+panzercore')
    conflicts('~tpetracore', when='+panzercore')
    conflicts('~shards', when='+panzerdofmgr')
    conflicts('~intrepid2', when='+panzerdofmgr')
    conflicts('~teuchoscore', when='+panzerdofmgr')
    conflicts('~teuchoscomm', when='+panzerdofmgr')
    conflicts('~tpetra', when='+panzerdofmgr')
    conflicts('~phalanx', when='+panzerdofmgr')
    conflicts('~panzercore', when='+panzerdofmgr')
    conflicts('~teuchoscore', when='+panzerdiscfe')
    conflicts('~teuchosparameterlist', when='+panzerdiscfe')
    conflicts('~teuchoscomm', when='+panzerdiscfe')
    conflicts('~kokkoscore', when='+panzerdiscfe')
    conflicts('~sacado', when='+panzerdiscfe')
    conflicts('~phalanx', when='+panzerdiscfe')
    conflicts('~intrepid2', when='+panzerdiscfe')
    conflicts('~thyracore', when='+panzerdiscfe')
    conflicts('~thyratpetraadapters', when='+panzerdiscfe')
    conflicts('~tpetra', when='+panzerdiscfe')
    conflicts('~zoltan', when='+panzerdiscfe')
    conflicts('~panzercore', when='+panzerdiscfe')
    conflicts('~panzerdofmgr', when='+panzerdiscfe')
    conflicts('~stkutil', when='+panzeradaptersstk')
    conflicts('~stktopology', when='+panzeradaptersstk')
    conflicts('~stkmesh', when='+panzeradaptersstk')
    conflicts('~stkio', when='+panzeradaptersstk')
    conflicts('~zoltan', when='+panzeradaptersstk')
    conflicts('~stratimikos', when='+panzeradaptersstk')
    conflicts('~piro', when='+panzeradaptersstk')
    conflicts('~nox', when='+panzeradaptersstk')
    conflicts('~rythmos', when='+panzeradaptersstk')
    conflicts('~panzercore', when='+panzeradaptersstk')
    conflicts('~panzerdiscfe', when='+panzeradaptersstk')
    conflicts('~seacasioss', when='+panzeradaptersstk')
    conflicts('~seacasexodus', when='+panzeradaptersstk')
    conflicts('~teko', when='+panzeradaptersstk')
    conflicts('~muelu', when='+panzeradaptersstk')
    conflicts('~ifpack2', when='+panzeradaptersstk')
    conflicts('~panzercore', when='+panzerminiem')
    conflicts('~panzerdofmgr', when='+panzerminiem')
    conflicts('~panzerdiscfe', when='+panzerminiem')
    conflicts('~panzeradaptersstk', when='+panzerminiem')
    conflicts('~phalanx', when='+panzerminiem')
    conflicts('~belos', when='+panzerminiem')
    conflicts('~teko', when='+panzerminiem')
    conflicts('~muelu', when='+panzerminiem')
    conflicts('~panzercore', when='+panzer')
    conflicts('~teuchos', when='+pytrilinos')
    conflicts('~kokkos', when='+adelus')
    conflicts('~kokkoskernels', when='+adelus')
    conflicts('~teuchoscore', when='+pikeblackbox')
    conflicts('~teuchoscomm', when='+pikeblackbox')
    conflicts('~teuchosparameterlist', when='+pikeblackbox')
    conflicts('~teuchoscore', when='+pikeimplicit')
    conflicts('~teuchoscomm', when='+pikeimplicit')
    conflicts('~teuchosparameterlist', when='+pikeimplicit')
    conflicts('~thyra', when='+pikeimplicit')
    conflicts('~pikeblackbox', when='+pikeimplicit')
    
    # register OPTIONAL package dependencies
    with when('+all_optional_packages'):
    
        conflicts('~kokkoscontainers', when='+kokkos')
        conflicts('~kokkosalgorithms', when='+kokkos')
        conflicts('~kokkoscore', when='+teuchoscore')
        conflicts('~teuchoskokkoscompat', when='+teuchos')
        conflicts('~teuchoskokkoscomm', when='+teuchos')
        conflicts('~kokkoscore', when='+sacado')
        conflicts('~teuchoscore', when='+sacado')
        conflicts('~teuchosnumerics', when='+sacado')
        conflicts('~teuchoscomm', when='+sacado')
        conflicts('~teuchoskokkoscomm', when='+sacado')
        conflicts('~kokkoscontainers', when='+sacado')
        conflicts('~teuchos', when='+epetra')
        conflicts('~teuchos', when='+shards')
        conflicts('~epetra', when='+triutils')
        conflicts('~triutils', when='+epetraext')
        conflicts('~epetra', when='+tpetracore')
        conflicts('~tpetratsqr', when='+tpetracore')
        conflicts('~teuchosnumerics', when='+tpetracore')
        conflicts('~tpetratsqr', when='+tpetra')
        conflicts('~epetra', when='+domi')
        conflicts('~tpetracore', when='+domi')
        conflicts('~thyraepetraadapters', when='+thyratpetraadapters')
        conflicts('~thyraepetraadapters', when='+thyra')
        conflicts('~thyraepetraextadapters', when='+thyra')
        conflicts('~thyratpetraadapters', when='+thyra')
        conflicts('~epetra', when='+xpetra')
        conflicts('~epetraext', when='+xpetra')
        conflicts('~tpetra', when='+xpetra')
        conflicts('~kokkoskernels', when='+xpetra')
        conflicts('~thyra', when='+xpetra')
        conflicts('~epetra', when='+xpetra')
        conflicts('~epetraext', when='+xpetra')
        conflicts('~tpetra', when='+xpetra')
        conflicts('~kokkoskernels', when='+xpetra')
        conflicts('~thyra', when='+xpetra')
        conflicts('~teuchos', when='+aztec')
        conflicts('~epetra', when='+galeri')
        conflicts('~epetraext', when='+galeri')
        conflicts('~xpetra', when='+galeri')
        conflicts('~tpetra', when='+galeri')
        conflicts('~triutils', when='+galeri')
        conflicts('~epetraext', when='+amesos')
        conflicts('~triutils', when='+amesos')
        conflicts('~galeri', when='+amesos')
        conflicts('~epetra', when='+zoltan2core')
        conflicts('~epetra', when='+zoltan2core')
        conflicts('~galeri', when='+zoltan2core')
        conflicts('~pamgen', when='+zoltan2core')
        conflicts('~amesos', when='+ifpack')
        conflicts('~epetraext', when='+ifpack')
        conflicts('~aztec', when='+ifpack')
        conflicts('~galeri', when='+ifpack')
        conflicts('~teuchos', when='+ml')
        conflicts('~epetra', when='+ml')
        conflicts('~zoltan', when='+ml')
        conflicts('~galeri', when='+ml')
        conflicts('~amesos', when='+ml')
        conflicts('~ifpack', when='+ml')
        conflicts('~aztec', when='+ml')
        conflicts('~epetraext', when='+ml')
        conflicts('~isorropia', when='+ml')
        conflicts('~epetra', when='+belos')
        conflicts('~tpetra', when='+belos')
        conflicts('~xpetra', when='+belos')
        conflicts('~thyra', when='+belos')
        conflicts('~aztec', when='+belos')
        conflicts('~triutils', when='+belos')
        conflicts('~kokkoskernels', when='+belos')
        conflicts('~galeri', when='+belos')
        conflicts('~triutils', when='+belos')
        conflicts('~epetraext', when='+belos')
        conflicts('~ifpack', when='+belos')
        conflicts('~ml', when='+belos')
        conflicts('~aztec', when='+belos')
        conflicts('~kokkoskernels', when='+shylu_nodehts')
        conflicts('~shylu_nodehts', when='+shylu_node')
        conflicts('~shylu_nodetacho', when='+shylu_node')
        conflicts('~epetra', when='+amesos2')
        conflicts('~epetraext', when='+amesos2')
        conflicts('~shylu_nodetacho', when='+amesos2')
        conflicts('~shylu_nodetacho', when='+amesos2')
        conflicts('~kokkos', when='+amesos2')
        conflicts('~trilinosss', when='+amesos2')
        conflicts('~seacasexodus', when='+seacasioss')
        conflicts('~pamgen', when='+seacasioss')
        conflicts('~zoltan', when='+seacasioss')
        conflicts('~kokkos', when='+seacasioss')
        conflicts('~seacasexodus', when='+seacasaprepro_lib')
        conflicts('~zoltan', when='+seacaszellij')
        conflicts('~zoltan', when='+seacasnemslice')
        conflicts('~seacasexodus_for', when='+seacas')
        conflicts('~seacasexoiiv2for32', when='+seacas')
        conflicts('~seacasnemesis', when='+seacas')
        conflicts('~seacaschaco', when='+seacas')
        conflicts('~seacasaprepro_lib', when='+seacas')
        conflicts('~seacassupes', when='+seacas')
        conflicts('~seacassuplib', when='+seacas')
        conflicts('~seacassuplibc', when='+seacas')
        conflicts('~seacassuplibcpp', when='+seacas')
        conflicts('~seacassvdi', when='+seacas')
        conflicts('~seacasplt', when='+seacas')
        conflicts('~seacasalgebra', when='+seacas')
        conflicts('~seacasaprepro', when='+seacas')
        conflicts('~seacasblot', when='+seacas')
        conflicts('~seacasconjoin', when='+seacas')
        conflicts('~seacasejoin', when='+seacas')
        conflicts('~seacasepu', when='+seacas')
        conflicts('~seacascpup', when='+seacas')
        conflicts('~seacasexo2mat', when='+seacas')
        conflicts('~seacasexodiff', when='+seacas')
        conflicts('~seacasexomatlab', when='+seacas')
        conflicts('~seacasexotxt', when='+seacas')
        conflicts('~seacasexo_format', when='+seacas')
        conflicts('~seacasex1ex2v2', when='+seacas')
        conflicts('~seacasfastq', when='+seacas')
        conflicts('~seacasgjoin', when='+seacas')
        conflicts('~seacasgen3d', when='+seacas')
        conflicts('~seacasgenshell', when='+seacas')
        conflicts('~seacasgrepos', when='+seacas')
        conflicts('~seacasexplore', when='+seacas')
        conflicts('~seacasmapvarlib', when='+seacas')
        conflicts('~seacasmapvar', when='+seacas')
        conflicts('~seacasmapvar-kd', when='+seacas')
        conflicts('~seacasmat2exo', when='+seacas')
        conflicts('~seacasnas2exo', when='+seacas')
        conflicts('~seacaszellij', when='+seacas')
        conflicts('~seacasnemslice', when='+seacas')
        conflicts('~seacasnemspread', when='+seacas')
        conflicts('~seacasnumbers', when='+seacas')
        conflicts('~seacasslice', when='+seacas')
        conflicts('~seacastxtexo', when='+seacas')
        conflicts('~seacasex2ex1v2', when='+seacas')
        conflicts('~tpetra', when='+anasazi')
        conflicts('~epetra', when='+anasazi')
        conflicts('~epetraext', when='+anasazi')
        conflicts('~thyracore', when='+anasazi')
        conflicts('~thyraepetraadapters', when='+anasazi')
        conflicts('~belos', when='+anasazi')
        conflicts('~amesos', when='+anasazi')
        conflicts('~aztec', when='+anasazi')
        conflicts('~belos', when='+anasazi')
        conflicts('~epetraext', when='+anasazi')
        conflicts('~galeri', when='+anasazi')
        conflicts('~ifpack', when='+anasazi')
        conflicts('~triutils', when='+anasazi')
        conflicts('~xpetra', when='+ifpack2')
        conflicts('~zoltan2core', when='+ifpack2')
        conflicts('~thyratpetraadapters', when='+ifpack2')
        conflicts('~amesos2', when='+ifpack2')
        conflicts('~shylu_nodehts', when='+ifpack2')
        conflicts('~amesos2', when='+ifpack2')
        conflicts('~shylu_nodehts', when='+ifpack2')
        conflicts('~ml', when='+ifpack2')
        conflicts('~aztec', when='+ifpack2')
        conflicts('~epetra', when='+ifpack2')
        conflicts('~amesos', when='+stratimikos')
        conflicts('~amesos2', when='+stratimikos')
        conflicts('~aztec', when='+stratimikos')
        conflicts('~belos', when='+stratimikos')
        conflicts('~ifpack', when='+stratimikos')
        conflicts('~ml', when='+stratimikos')
        conflicts('~epetraext', when='+stratimikos')
        conflicts('~thyraepetraadapters', when='+stratimikos')
        conflicts('~thyratpetraadapters', when='+stratimikos')
        conflicts('~triutils', when='+stratimikos')
        conflicts('~ifpack2', when='+stratimikos')
        conflicts('~galeri', when='+stratimikos')
        conflicts('~thyratpetraadapters', when='+stratimikos')
        conflicts('~aztec', when='+fei')
        conflicts('~belos', when='+fei')
        conflicts('~amesos', when='+fei')
        conflicts('~ifpack', when='+fei')
        conflicts('~ml', when='+fei')
        conflicts('~isorropia', when='+teko')
        conflicts('~ifpack2', when='+teko')
        conflicts('~amesos2', when='+teko')
        conflicts('~belos', when='+teko')
        conflicts('~epetra', when='+intrepid')
        conflicts('~epetraext', when='+intrepid')
        conflicts('~amesos', when='+intrepid')
        conflicts('~pamgen', when='+intrepid')
        conflicts('~sacado', when='+intrepid2')
        conflicts('~kokkoskernels', when='+intrepid2')
        conflicts('~sacado', when='+intrepid2')
        conflicts('~seacasaprepro_lib', when='+stkutil')
        conflicts('~stkmesh', when='+stkunit_test_utils')
        conflicts('~stkio', when='+stkunit_test_utils')
        conflicts('~stkbalance', when='+stkunit_test_utils')
        conflicts('~shards', when='+stkunit_tests')
        conflicts('~stkcoupling', when='+stkunit_tests')
        conflicts('~stktopology', when='+stkunit_tests')
        conflicts('~stkmath', when='+stkunit_tests')
        conflicts('~stksimd', when='+stkunit_tests')
        conflicts('~stkmesh', when='+stkunit_tests')
        conflicts('~stkio', when='+stkunit_tests')
        conflicts('~stkbalance', when='+stkunit_tests')
        conflicts('~stktransfer', when='+stkunit_tests')
        conflicts('~stksearch', when='+stkunit_tests')
        conflicts('~stktools', when='+stkunit_tests')
        conflicts('~stktopology', when='+stkdoc_tests')
        conflicts('~stkmath', when='+stkdoc_tests')
        conflicts('~stksimd', when='+stkdoc_tests')
        conflicts('~stkmesh', when='+stkdoc_tests')
        conflicts('~stkio', when='+stkdoc_tests')
        conflicts('~stktransfer', when='+stkdoc_tests')
        conflicts('~stkutil', when='+stk')
        conflicts('~stkemend', when='+stk')
        conflicts('~stkcoupling', when='+stk')
        conflicts('~stkmath', when='+stk')
        conflicts('~stksimd', when='+stk')
        conflicts('~stkngp_test', when='+stk')
        conflicts('~stktopology', when='+stk')
        conflicts('~stkmesh', when='+stk')
        conflicts('~stkio', when='+stk')
        conflicts('~stksearch', when='+stk')
        conflicts('~stktransfer', when='+stk')
        conflicts('~stktools', when='+stk')
        conflicts('~stkbalance', when='+stk')
        conflicts('~stkunit_test_utils', when='+stk')
        conflicts('~stksearchutil', when='+stk')
        conflicts('~stkunit_tests', when='+stk')
        conflicts('~stkdoc_tests', when='+stk')
        conflicts('~stkexpreval', when='+stk')
        conflicts('~gtest', when='+percept')
        conflicts('~epetra', when='+nox')
        conflicts('~epetraext', when='+nox')
        conflicts('~thyracore', when='+nox')
        conflicts('~thyraepetraadapters', when='+nox')
        conflicts('~thyraepetraextadapters', when='+nox')
        conflicts('~amesos', when='+nox')
        conflicts('~aztec', when='+nox')
        conflicts('~ifpack', when='+nox')
        conflicts('~ml', when='+nox')
        conflicts('~belos', when='+nox')
        conflicts('~anasazi', when='+nox')
        conflicts('~stratimikos', when='+nox')
        conflicts('~teko', when='+nox')
        conflicts('~stratimikos', when='+nox')
        conflicts('~isorropia', when='+nox')
        conflicts('~tpetra', when='+nox')
        conflicts('~thyratpetraadapters', when='+nox')
        conflicts('~ifpack2', when='+nox')
        conflicts('~kokkos', when='+moertel')
        conflicts('~tpetra', when='+moertel')
        conflicts('~seacas', when='+moertel')
        conflicts('~amesos', when='+muelu')
        conflicts('~amesos2', when='+muelu')
        conflicts('~belos', when='+muelu')
        conflicts('~epetra', when='+muelu')
        conflicts('~epetraext', when='+muelu')
        conflicts('~teko', when='+muelu')
        conflicts('~ifpack', when='+muelu')
        conflicts('~ifpack2', when='+muelu')
        conflicts('~intrepid2', when='+muelu')
        conflicts('~ml', when='+muelu')
        conflicts('~tpetra', when='+muelu')
        conflicts('~zoltan', when='+muelu')
        conflicts('~zoltan2core', when='+muelu')
        conflicts('~stratimikos', when='+muelu')
        conflicts('~thyra', when='+muelu')
        conflicts('~thyratpetraadapters', when='+muelu')
        conflicts('~isorropia', when='+muelu')
        conflicts('~aztec', when='+muelu')
        conflicts('~pamgen', when='+muelu')
        conflicts('~muelu', when='+zoltan2sphynx')
        conflicts('~muelu', when='+zoltan2sphynx')
        conflicts('~zoltan2sphynx', when='+zoltan2')
        conflicts('~epetra', when='+zoltan2')
        conflicts('~galeri', when='+zoltan2')
        conflicts('~pamgen', when='+zoltan2')
        conflicts('~amesos', when='+shylu_ddfrosch')
        conflicts('~belos', when='+shylu_ddfrosch')
        conflicts('~epetra', when='+shylu_ddfrosch')
        conflicts('~epetraext', when='+shylu_ddfrosch')
        conflicts('~ifpack2', when='+shylu_ddfrosch')
        conflicts('~muelu', when='+shylu_ddfrosch')
        conflicts('~stratimikos', when='+shylu_ddfrosch')
        conflicts('~thyra', when='+shylu_ddfrosch')
        conflicts('~zoltan2', when='+shylu_ddfrosch')
        conflicts('~belos', when='+shylu_ddfrosch')
        conflicts('~thyra', when='+shylu_ddfrosch')
        conflicts('~shylu_ddcommon', when='+shylu_dd')
        conflicts('~epetraext', when='+rythmos')
        conflicts('~thyraepetraadapters', when='+rythmos')
        conflicts('~thyraepetraextadapters', when='+rythmos')
        conflicts('~sacado', when='+rythmos')
        conflicts('~stratimikos', when='+rythmos')
        conflicts('~belos', when='+rythmos')
        conflicts('~nox', when='+rythmos')
        conflicts('~epetraext', when='+stokhos')
        conflicts('~ifpack', when='+stokhos')
        conflicts('~ml', when='+stokhos')
        conflicts('~trikota', when='+stokhos')
        conflicts('~anasazi', when='+stokhos')
        conflicts('~sacado', when='+stokhos')
        conflicts('~nox', when='+stokhos')
        conflicts('~isorropia', when='+stokhos')
        conflicts('~kokkoskernels', when='+stokhos')
        conflicts('~teuchoskokkoscomm', when='+stokhos')
        conflicts('~kokkosalgorithms', when='+stokhos')
        conflicts('~kokkoscontainers', when='+stokhos')
        conflicts('~tpetra', when='+stokhos')
        conflicts('~ifpack2', when='+stokhos')
        conflicts('~muelu', when='+stokhos')
        conflicts('~belos', when='+stokhos')
        conflicts('~amesos2', when='+stokhos')
        conflicts('~thyra', when='+stokhos')
        conflicts('~xpetra', when='+stokhos')
        conflicts('~aztec', when='+stokhos')
        conflicts('~stratimikos', when='+stokhos')
        conflicts('~zoltan', when='+stokhos')
        conflicts('~kokkoscontainers', when='+stokhos')
        conflicts('~belos', when='+rol')
        conflicts('~epetra', when='+rol')
        conflicts('~tpetra', when='+rol')
        conflicts('~thyra', when='+rol')
        conflicts('~sacado', when='+rol')
        conflicts('~intrepid', when='+rol')
        conflicts('~minitensor', when='+rol')
        conflicts('~shards', when='+rol')
        conflicts('~amesos', when='+rol')
        conflicts('~amesos2', when='+rol')
        conflicts('~ifpack2', when='+rol')
        conflicts('~muelu', when='+rol')
        conflicts('~trikota', when='+rol')
        conflicts('~tempus', when='+rol')
        conflicts('~gtest', when='+rol')
        conflicts('~nox', when='+piro')
        conflicts('~rythmos', when='+piro')
        conflicts('~tempus', when='+piro')
        conflicts('~stokhos', when='+piro')
        conflicts('~trikota', when='+piro')
        conflicts('~rol', when='+piro')
        conflicts('~ifpack2', when='+piro')
        conflicts('~muelu', when='+piro')
        conflicts('~thyraepetraadapters', when='+piro')
        conflicts('~thyraepetraextadapters', when='+piro')
        conflicts('~epetra', when='+piro')
        conflicts('~epetraext', when='+piro')
        conflicts('~tpetra', when='+piro')
        conflicts('~teko', when='+piro')
        conflicts('~epetra', when='+panzerdofmgr')
        conflicts('~thyraepetraadapters', when='+panzerdiscfe')
        conflicts('~thyraepetraextadapters', when='+panzerdiscfe')
        conflicts('~epetra', when='+panzerdiscfe')
        conflicts('~epetraext', when='+panzerdiscfe')
        conflicts('~stksearch', when='+panzeradaptersstk')
        conflicts('~seacasioss', when='+panzeradaptersstk')
        conflicts('~seacasexodus', when='+panzeradaptersstk')
        conflicts('~percept', when='+panzeradaptersstk')
        conflicts('~teko', when='+panzeradaptersstk')
        conflicts('~muelu', when='+panzeradaptersstk')
        conflicts('~ifpack2', when='+panzeradaptersstk')
        conflicts('~tempus', when='+panzeradaptersstk')
        conflicts('~pamgen', when='+panzeradaptersstk')
        conflicts('~stksearch', when='+panzeradaptersstk')
        conflicts('~ml', when='+panzerminiem')
        conflicts('~panzerdofmgr', when='+panzer')
        conflicts('~panzerdiscfe', when='+panzer')
        conflicts('~panzeradaptersstk', when='+panzer')
        conflicts('~panzerminiem', when='+panzer')
        conflicts('~epetra', when='+pytrilinos')
        conflicts('~triutils', when='+pytrilinos')
        conflicts('~tpetra', when='+pytrilinos')
        conflicts('~epetraext', when='+pytrilinos')
        conflicts('~domi', when='+pytrilinos')
        conflicts('~isorropia', when='+pytrilinos')
        conflicts('~aztec', when='+pytrilinos')
        conflicts('~galeri', when='+pytrilinos')
        conflicts('~amesos', when='+pytrilinos')
        conflicts('~ifpack', when='+pytrilinos')
        conflicts('~komplex', when='+pytrilinos')
        conflicts('~anasazi', when='+pytrilinos')
        conflicts('~pliris', when='+pytrilinos')
        conflicts('~ml', when='+pytrilinos')
        conflicts('~nox', when='+pytrilinos')
        conflicts('~stk', when='+pytrilinos')
        conflicts('~teuchos', when='+adelus')
        conflicts('~amesos', when='+trilinoscouplings')
        conflicts('~aztec', when='+trilinoscouplings')
        conflicts('~belos', when='+trilinoscouplings')
        conflicts('~epetraext', when='+trilinoscouplings')
        conflicts('~ifpack', when='+trilinoscouplings')
        conflicts('~isorropia', when='+trilinoscouplings')
        conflicts('~ml', when='+trilinoscouplings')
        conflicts('~muelu', when='+trilinoscouplings')
        conflicts('~nox', when='+trilinoscouplings')
        conflicts('~stokhos', when='+trilinoscouplings')
        conflicts('~zoltan', when='+trilinoscouplings')
        conflicts('~amesos', when='+trilinoscouplings')
        conflicts('~aztec', when='+trilinoscouplings')
        conflicts('~epetra', when='+trilinoscouplings')
        conflicts('~epetraext', when='+trilinoscouplings')
        conflicts('~ifpack', when='+trilinoscouplings')
        conflicts('~ifpack2', when='+trilinoscouplings')
        conflicts('~intrepid', when='+trilinoscouplings')
        conflicts('~intrepid2', when='+trilinoscouplings')
        conflicts('~isorropia', when='+trilinoscouplings')
        conflicts('~kokkoscontainers', when='+trilinoscouplings')
        conflicts('~kokkoscore', when='+trilinoscouplings')
        conflicts('~kokkoskernels', when='+trilinoscouplings')
        conflicts('~ml', when='+trilinoscouplings')
        conflicts('~muelu', when='+trilinoscouplings')
        conflicts('~muelu', when='+trilinoscouplings')
        conflicts('~pamgen', when='+trilinoscouplings')
        conflicts('~seacasexodus', when='+trilinoscouplings')
        conflicts('~seacasnemesis', when='+trilinoscouplings')
        conflicts('~sacado', when='+trilinoscouplings')
        conflicts('~stkio', when='+trilinoscouplings')
        conflicts('~stkmesh', when='+trilinoscouplings')
        conflicts('~stokhos', when='+trilinoscouplings')
        conflicts('~stratimikos', when='+trilinoscouplings')
        conflicts('~teko', when='+trilinoscouplings')
        conflicts('~teuchoskokkoscomm', when='+trilinoscouplings')
        conflicts('~teuchoskokkoscompat', when='+trilinoscouplings')
        conflicts('~tpetra', when='+trilinoscouplings')
        conflicts('~trikota', when='+trilinoscouplings')
        conflicts('~zoltan', when='+trilinoscouplings')
        conflicts('~pikeblackbox', when='+pike')
        conflicts('~pikeimplicit', when='+pike')
        conflicts('~tpetra', when='+trilinosinstalltests')
    # Spack logic auto-generated from Tribits ENDS here (no manual modifications)


    # Internal package options (alphabetical order)
    variant("basker", default=False, description="Compile with the Basker solver in Amesos2")
    variant("epetraextbtf", default=False, description="Compile with BTF in EpetraExt")
    variant(
        "epetraextexperimental",
        default=False,
        description="Compile with experimental in EpetraExt",
    )
    variant(
        "epetraextgraphreorderings",
        default=False,
        description="Compile with graph reorderings in EpetraExt",
    )

    # External package options
    variant("dtk", default=False, description="Enable DataTransferKit (deprecated)")
    variant("scorec", default=False, description="Enable SCOREC")
    variant("mesquite", default=False, description="Enable Mesquite (deprecated)")

    resource(
        name="dtk",
        git="https://github.com/ornl-cees/DataTransferKit.git",
        commit="4fe4d9d56cfd4f8a61f392b81d8efd0e389ee764",  # branch dtk-3.0
        placement="DataTransferKit",
        when="+dtk @12.14.0:12.14",
    )
    resource(
        name="dtk",
        git="https://github.com/ornl-cees/DataTransferKit.git",
        commit="edfa050cd46e2274ab0a0b7558caca0079c2e4ca",  # tag 3.1-rc1
        placement="DataTransferKit",
        submodules=True,
        when="+dtk @12.18.0:12.18",
    )
    resource(
        name="scorec",
        git="https://github.com/SCOREC/core.git",
        commit="73c16eae073b179e45ec625a5abe4915bc589af2",  # tag v2.2.5
        placement="SCOREC",
        when="+scorec",
    )
    resource(
        name="mesquite",
        url="https://github.com/trilinos/mesquite/archive/trilinos-release-12-12-1.tar.gz",
        sha256="e0d09b0939dbd461822477449dca611417316e8e8d8268fd795debb068edcbb5",
        placement="packages/mesquite",
        when="+mesquite @12.12.1:12.16",
    )
    resource(
        name="mesquite",
        git="https://github.com/trilinos/mesquite.git",
        commit="20a679679b5cdf15bf573d66c5dc2b016e8b9ca1",  # branch trilinos-release-12-12-1
        placement="packages/mesquite",
        when="+mesquite @12.18.1:12.18",
    )
    resource(
        name="mesquite",
        git="https://github.com/trilinos/mesquite.git",
        tag="develop",
        placement="packages/mesquite",
        when="+mesquite @master",
    )

    # ###################### Conflicts ##########################

    # Only allow DTK with Trilinos 12.14, 12.18
    conflicts("+dtk", when="~boost")
    conflicts("+dtk", when="~intrepid2")
    conflicts("+dtk", when="@:12.12,13:")

    # Installed FindTrilinos are broken in SEACAS if Fortran is disabled
    # see https://github.com/trilinos/Trilinos/issues/3346
    conflicts("+exodus", when="@:13.0.1 ~fortran")
    # Only allow Mesquite with Trilinos 12.12 and up, and master
    conflicts("+mesquite", when="@:12.10,master")
    # Strumpack is only available as of mid-2021
    conflicts("+strumpack", when="@:13.0")
    # Can only use one type of SuperLU
    conflicts("+superlu-dist", when="+superlu")
    # For Trilinos v11 we need to force SuperLUDist=OFF, since only the
    # deprecated SuperLUDist v3.3 together with an Amesos patch is working.
    conflicts("+superlu-dist", when="@11.4.1:11.14.3")
    # see https://github.com/trilinos/Trilinos/issues/3566
    conflicts(
        "+superlu-dist", when="+float+amesos2+explicit_template_instantiation^superlu-dist@5.3.0:"
    )
    # Amesos, conflicting types of double and complex SLU_D
    # see https://trilinos.org/pipermail/trilinos-users/2015-March/004731.html
    # and https://trilinos.org/pipermail/trilinos-users/2015-March/004802.html
    conflicts("+superlu-dist", when="+complex+amesos2")
    # https://github.com/trilinos/Trilinos/issues/2994
    conflicts(
        "+shared",
        when="+stk platform=darwin",
        msg="Cannot build Trilinos with STK as a shared library on Darwin.",
    )
    conflicts("+adios2", when="@:12.14.1")
    conflicts("cxxstd=11", when="@13.2:")
    conflicts("cxxstd=17", when="@:12")
    conflicts("cxxstd=11", when="+wrapper ^cuda@6.5.14")
    conflicts("cxxstd=14", when="+wrapper ^cuda@6.5.14:8.0.61")
    conflicts("cxxstd=17", when="+wrapper ^cuda@6.5.14:10.2.89")

    # Multi-value gotype only applies to trilinos through 12.14
    conflicts("gotype=all", when="@12.15:")

    # CUDA without wrapper requires clang
    for _compiler in spack.compilers.supported_compilers():
        if _compiler != "clang":
            conflicts(
                "+cuda",
                when="~wrapper %" + _compiler,
                msg="trilinos~wrapper+cuda can only be built with the " "Clang compiler",
            )
    conflicts("+cuda_rdc", when="~cuda")
    conflicts("+rocm_rdc", when="~rocm")
    conflicts("+wrapper", when="~cuda")
    conflicts("+wrapper", when="%clang")

    # Old trilinos fails with new CUDA (see #27180)
    conflicts("@:13.0.1 +cuda", when="^cuda@11:")
    # Build hangs with CUDA 11.6 (see #28439)
    conflicts("+cuda +stokhos", when="^cuda@11.6:")
    # Cuda UVM must be enabled prior to 13.2
    # See https://github.com/spack/spack/issues/28869
    conflicts("~uvm", when="@:13.1 +cuda")

    # stokhos fails on xl/xl_r
    conflicts("+stokhos", when="%xl")
    conflicts("+stokhos", when="%xl_r")

    # ###################### Dependencies ##########################

    depends_on("adios2", when="+adios2")
    depends_on("blas")
    depends_on("boost+graph+math+exception+stacktrace", when="+boost")
    # Need to revisit the requirement of STK
    depends_on("boost+graph+math+exception+stacktrace", when="+stk")

    depends_on("cgns", when="+exodus")
    depends_on("hdf5+hl", when="+hdf5")
    depends_on("hypre~internal-superlu~int64", when="+hypre")
    depends_on("kokkos-nvcc-wrapper", when="+wrapper")
    depends_on("lapack")
    # depends_on('perl', type=('build',)) # TriBITS finds but doesn't use...
    depends_on("libx11", when="+x11")
    depends_on("matio", when="+exodus")
    depends_on("metis", when="+zoltan")
    depends_on("mpi", when="+mpi")
    depends_on("netcdf-c", when="+exodus")
    depends_on("parallel-netcdf", when="+exodus+mpi")
    depends_on("parmetis", when="+mpi +zoltan")
    depends_on("parmetis", when="+scorec")
    depends_on("py-mpi4py", when="+mpi+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("python", when="+python")
    depends_on("python", when="@13.2: +ifpack +hypre", type="build")
    depends_on("python", when="@13.2: +ifpack2 +hypre", type="build")
    depends_on("scalapack", when="+mumps")
    depends_on("scalapack", when="+strumpack+mpi")
    depends_on("strumpack+shared", when="+strumpack")
    depends_on("suite-sparse", when="+suite-sparse")
    depends_on("superlu-dist", when="+superlu-dist")
    depends_on("superlu@4.3 +pic", when="+superlu")
    depends_on("swig", when="+python")
    depends_on("zlib", when="+zoltan")

    # Trilinos' Tribits config system is limited which makes it very tricky to
    # link Amesos with static MUMPS, see
    # https://trilinos.org/docs/dev/packages/amesos2/doc/html/classAmesos2_1_1MUMPS.html
    # One could work it out by getting linking flags from mpif90 --showme:link
    # (or alike) and adding results to -DTrilinos_EXTRA_LINK_FLAGS together
    # with Blas and Lapack and ScaLAPACK and Blacs and -lgfortran and it may
    # work at the end. But let's avoid all this by simply using shared libs
    depends_on("mumps@5.0:+shared", when="+mumps")

    for _flag in ("~mpi", "+mpi"):
        depends_on("hdf5" + _flag, when="+hdf5" + _flag)
        depends_on("mumps" + _flag, when="+mumps" + _flag)
    for _flag in ("~openmp", "+openmp"):
        depends_on("mumps" + _flag, when="+mumps" + _flag)

    depends_on("hwloc", when="@13: +kokkos")
    depends_on("hwloc+cuda", when="@13: +kokkos+cuda")
    depends_on("hypre@develop", when="@master: +hypre")
    depends_on("netcdf-c+mpi+parallel-netcdf", when="+exodus+mpi@12.12.1:")
    depends_on("superlu-dist@:4.3", when="@11.14.1:12.6.1+superlu-dist")
    depends_on("superlu-dist@4.4:5.3", when="@12.6.2:12.12.1+superlu-dist")
    depends_on("superlu-dist@5.4:6.2.0", when="@12.12.2:13.0.0+superlu-dist")
    depends_on("superlu-dist@6.3.0:7", when="@13.0.1:13 +superlu-dist")
    depends_on("superlu-dist@develop", when="@master: +superlu-dist")

    # ###################### Patches ##########################

    patch("umfpack_from_suitesparse.patch", when="@11.14.1:12.8.1")
    for _compiler in ["xl", "xl_r", "clang"]:
        patch("xlf_seacas.patch", when="@12.10.1:12.12.1 %" + _compiler)
        patch("xlf_tpetra.patch", when="@12.12.1 %" + _compiler)
    patch("fix_clang_errors_12_18_1.patch", when="@12.18.1%clang")
    patch("cray_secas_12_12_1.patch", when="@12.12.1%cce")
    patch("cray_secas.patch", when="@12.14.1:12%cce")
    patch(
        "https://patch-diff.githubusercontent.com/raw/trilinos/Trilinos/pull/10545.patch?full_index=1",
        sha256="62272054f7cc644583c269e692c69f0a26af19e5a5bd262db3ea3de3447b3358",
        when="@:13.4.0 +complex",
    )

    # workaround an NVCC bug with c++14 (https://github.com/trilinos/Trilinos/issues/6954)
    # avoid calling deprecated functions with CUDA-11
    patch("fix_cxx14_cuda11.patch", when="@13.0.0:13.0.1 cxxstd=14 ^cuda@11:")
    # Allow building with +teko gotype=long
    patch(
        "https://github.com/trilinos/Trilinos/commit/b17f20a0b91e0b9fc5b1b0af3c8a34e2a4874f3f.patch?full_index=1",
        sha256="063a38f402439fa39fd8d57315a321e6510adcd04aec5400a88e744aaa60bc8e",
        when="@13.0.0:13.0.1 +teko gotype=long",
    )

    def flag_handler(self, name, flags):
        spec = self.spec
        is_cce = spec.satisfies("%cce")

        if name == "cxxflags":
            if "+mumps" in spec:
                # see https://github.com/trilinos/Trilinos/blob/master/packages/amesos/README-MUMPS
                flags.append("-DMUMPS_5_0")
            if "+stk platform=darwin" in spec:
                flags.append("-DSTK_NO_BOOST_STACKTRACE")
            if "+stk%intel" in spec:
                # Workaround for Intel compiler segfaults with STK and IPO
                flags.append("-no-ipo")
            if "+wrapper" in spec:
                flags.append("--expt-extended-lambda")
        elif name == "ldflags":
            if is_cce:
                flags.append("-fuse-ld=gold")
            if spec.satisfies("platform=linux ~cuda"):
                # TriBITS explicitly links libraries against all transitive
                # dependencies, leading to O(N^2) library resolution. When
                # CUDA is enabled (possibly only with MPI as well) the linker
                # flag does not propagate correctly.
                flags.append("-Wl,--as-needed")
            elif spec.satisfies("+stk +shared platform=darwin"):
                flags.append("-Wl,-undefined,dynamic_lookup")

            # Fortran lib (assumes clang is built with gfortran!)
            if "+fortran" in spec and spec.compiler.name in ["gcc", "clang", "apple-clang"]:
                fc = Executable(self.compiler.fc)
                libgfortran = fc(
                    "--print-file-name", "libgfortran." + dso_suffix, output=str
                ).strip()
                # if libgfortran is equal to "libgfortran.<dso_suffix>" then
                # print-file-name failed, use static library instead
                if libgfortran == "libgfortran." + dso_suffix:
                    libgfortran = fc("--print-file-name", "libgfortran.a", output=str).strip()
                # -L<libdir> -lgfortran required for OSX
                # https://github.com/spack/spack/pull/25823#issuecomment-917231118
                flags.append("-L{0} -lgfortran".format(os.path.dirname(libgfortran)))

        if is_cce:
            return (None, None, flags)
        return (flags, None, None)

    def url_for_version(self, version):
        url = "https://github.com/trilinos/Trilinos/archive/refs/tags/trilinos-release-{0}.tar.gz"
        return url.format(version.dashed)

    def setup_dependent_run_environment(self, env, dependent_spec):
        if "+cuda" in self.spec:
            # currently Trilinos doesn't perform the memory fence so
            # it relies on blocking CUDA kernel launch. This is needed
            # in case the dependent app also run a CUDA backend via Trilinos
            env.set("CUDA_LAUNCH_BLOCKING", "1")

    def setup_dependent_package(self, module, dependent_spec):
        if "+wrapper" in self.spec:
            self.spec.kokkos_cxx = self.spec["kokkos-nvcc-wrapper"].kokkos_cxx
        else:
            self.spec.kokkos_cxx = spack_cxx

    def setup_build_environment(self, env):
        spec = self.spec
        if "+cuda" in spec and "+wrapper" in spec:
            if "+mpi" in spec:
                env.set("OMPI_CXX", spec["kokkos-nvcc-wrapper"].kokkos_cxx)
                env.set("MPICH_CXX", spec["kokkos-nvcc-wrapper"].kokkos_cxx)
                env.set("MPICXX_CXX", spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            else:
                env.set("CXX", spec["kokkos-nvcc-wrapper"].kokkos_cxx)

        if "+rocm" in spec:
            if "+mpi" in spec:
                env.set("OMPI_CXX", self.spec["hip"].hipcc)
                env.set("MPICH_CXX", self.spec["hip"].hipcc)
                env.set("MPICXX_CXX", self.spec["hip"].hipcc)
            else:
                env.set("CXX", self.spec["hip"].hipcc)
            if "+stk" in spec:
                # Using CXXFLAGS for hipcc which doesn't use flags in the spack wrappers
                env.set("CXXFLAGS", "-DSTK_NO_BOOST_STACKTRACE")

    def cmake_args(self):
        options = []

        spec = self.spec
        define = self.define
        define_from_variant = self.define_from_variant

        def _make_definer(prefix):
            def define_enable(suffix, value=None):
                key = prefix + suffix
                if value is None:
                    # Default to lower-case spec
                    value = suffix.lower()
                elif isinstance(value, bool):
                    # Explicit true/false
                    return define(key, value)
                return define_from_variant(key, value)

            return define_enable

        # Return "Trilinos_ENABLE_XXX" for spec "+xxx" or boolean value
        define_trilinos_enable = _make_definer("Trilinos_ENABLE_")
        # Same but for TPLs
        define_tpl_enable = _make_definer("TPL_ENABLE_")

        # #################### Base Settings #######################

        options.extend(
            [
                define("Trilinos_VERBOSE_CONFIGURE", False),
                define_from_variant("BUILD_SHARED_LIBS", "shared"),
                define_trilinos_enable("ALL_OPTIONAL_PACKAGES"),
                define_trilinos_enable("ALL_PACKAGES", False),
                define_trilinos_enable("CXX11", True),
                define_trilinos_enable("DEBUG", "debug"),
                define_trilinos_enable("EXAMPLES", False),
                define_trilinos_enable("SECONDARY_TESTED_CODE", True),
                define_trilinos_enable("TESTS", False),
                define_trilinos_enable("Fortran"),
                define_trilinos_enable("OpenMP"),
                define_trilinos_enable(
                    "EXPLICIT_INSTANTIATION", "explicit_template_instantiation"
                ),
            ]
        )

        if spec.version >= Version("13"):
            options.append(define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        else:
            # Prior to version 13, Trilinos would erroneously inject
            # '-std=c++11' regardless of CMAKE_CXX_STANDARD value
            options.append(
                define(
                    "Trilinos_CXX11_FLAGS",
                    self.compiler.cxx14_flag
                    if spec.variants["cxxstd"].value == "14"
                    else self.compiler.cxx11_flag,
                )
            )

        # ################## Trilinos Packages #####################

        options.extend(
            [
                define_trilinos_enable("Adelus"),
                define_trilinos_enable("Amesos"),
                define_trilinos_enable("Amesos2"),
                define_trilinos_enable("Anasazi"),
                define_trilinos_enable("AztecOO", "aztec"),
                define_trilinos_enable("Belos"),
                define_trilinos_enable("Epetra"),
                define_trilinos_enable("EpetraExt"),
                define_trilinos_enable("FEI", False),
                define_trilinos_enable("Gtest"),
                define_trilinos_enable("Ifpack"),
                define_trilinos_enable("Ifpack2"),
                define_trilinos_enable("Intrepid"),
                define_trilinos_enable("Intrepid2"),
                define_trilinos_enable("Isorropia"),
                define_trilinos_enable("Kokkos"),
                define_trilinos_enable("MiniTensor"),
                define_trilinos_enable("Mesquite"),
                define_trilinos_enable("ML"),
                define_trilinos_enable("MueLu"),
                define_trilinos_enable("NOX"),
                define_trilinos_enable("Pamgen", False),
                define_trilinos_enable("Panzer"),
                define_trilinos_enable("Pike", False),
                define_trilinos_enable("Piro"),
                define_trilinos_enable("Phalanx"),
                define_trilinos_enable("PyTrilinos", "python"),
                define_trilinos_enable("ROL"),
                define_trilinos_enable("Rythmos"),
                define_trilinos_enable("Sacado"),
                define_trilinos_enable("SCOREC"),
                define_trilinos_enable("Shards"),
                define_trilinos_enable("ShyLU"),
                define_trilinos_enable("STK"),
                define_trilinos_enable("Stokhos"),
                define_trilinos_enable("Stratimikos"),
                define_trilinos_enable("Teko"),
                define_trilinos_enable("Tempus"),
                define_trilinos_enable("Thyra"),
                define_trilinos_enable("Tpetra"),
                define_trilinos_enable("TrilinosCouplings"),
                define_trilinos_enable("Triutils", True),
                define_trilinos_enable("Zoltan"),
                define_trilinos_enable("Zoltan2"),
                define_from_variant("EpetraExt_BUILD_BTF", "epetraextbtf"),
                define_from_variant("EpetraExt_BUILD_EXPERIMENTAL", "epetraextexperimental"),
                define_from_variant(
                    "EpetraExt_BUILD_GRAPH_REORDERINGS", "epetraextgraphreorderings"
                ),
                define_from_variant("Amesos2_ENABLE_Basker", "basker"),
                define_from_variant("Amesos2_ENABLE_LAPACK", "amesos2"),
            ]
        )

        if "+dtk" in spec:
            options.extend(
                [
                    define("Trilinos_EXTRA_REPOSITORIES", "DataTransferKit"),
                    define_trilinos_enable("DataTransferKit", True),
                ]
            )

        if "+exodus" in spec:
            options.extend(
                [
                    define_trilinos_enable("SEACAS", True),
                    define_trilinos_enable("SEACASExodus", True),
                    define_trilinos_enable("SEACASIoss", True),
                    define_trilinos_enable("SEACASEpu", True),
                    define_trilinos_enable("SEACASExodiff", True),
                    define_trilinos_enable("SEACASNemspread", True),
                    define_trilinos_enable("SEACASNemslice", True),
                ]
            )
        else:
            options.extend(
                [
                    define_trilinos_enable("SEACASExodus", False),
                    define_trilinos_enable("SEACASIoss", False),
                ]
            )

        if "+chaco" in spec:
            options.extend(
                [
                    define_trilinos_enable("SEACAS", True),
                    define_trilinos_enable("SEACASChaco", True),
                ]
            )
        else:
            # don't disable SEACAS, could be needed elsewhere
            options.extend(
                [
                    define_trilinos_enable("SEACASChaco", False),
                    define_trilinos_enable("SEACASNemslice", False),
                ]
            )

        if "+stratimikos" in spec:
            # Explicitly enable Thyra (ThyraCore is required). If you don't do
            # this, then you get "NOT setting ${pkg}_ENABLE_Thyra=ON since
            # Thyra is NOT enabled at this point!" leading to eventual build
            # errors if using MueLu because `Xpetra_ENABLE_Thyra` is set to
            # off.

            # Add thyra adapters based on package enables
            options.extend(
                define_trilinos_enable("Thyra" + pkg + "Adapters", pkg.lower())
                for pkg in ["Epetra", "EpetraExt", "Tpetra"]
            )

        # ######################### TPLs #############################

        def define_tpl(trilinos_name, spack_name, have_dep):
            options.append(define("TPL_ENABLE_" + trilinos_name, have_dep))
            if not have_dep:
                return
            depspec = spec[spack_name]
            libs = depspec.libs
            try:
                options.extend(
                    [
                        define(trilinos_name + "_INCLUDE_DIRS", depspec.headers.directories),
                    ]
                )
            except NoHeadersError:
                # Handle case were depspec does not have headers
                pass

            options.extend(
                [
                    define(trilinos_name + "_ROOT", depspec.prefix),
                    define(trilinos_name + "_LIBRARY_NAMES", libs.names),
                    define(trilinos_name + "_LIBRARY_DIRS", libs.directories),
                ]
            )

        # Enable these TPLs explicitly from variant options.
        # Format is (TPL name, variant name, Spack spec name)
        tpl_variant_map = [
            ("ADIOS2", "adios2", "adios2"),
            ("Boost", "boost", "boost"),
            ("CUDA", "cuda", "cuda"),
            ("HDF5", "hdf5", "hdf5"),
            ("HYPRE", "hypre", "hypre"),
            ("MUMPS", "mumps", "mumps"),
            ("UMFPACK", "suite-sparse", "suite-sparse"),
            ("SuperLU", "superlu", "superlu"),
            ("SuperLUDist", "superlu-dist", "superlu-dist"),
            ("X11", "x11", "libx11"),
        ]
        if spec.satisfies("@13.0.2:"):
            tpl_variant_map.append(("STRUMPACK", "strumpack", "strumpack"))

        for tpl_name, var_name, spec_name in tpl_variant_map:
            define_tpl(tpl_name, spec_name, spec.variants[var_name].value)

        # Enable these TPLs based on whether they're in our spec; prefer to
        # require this way so that packages/features disable availability
        tpl_dep_map = [
            ("BLAS", "blas"),
            ("CGNS", "cgns"),
            ("LAPACK", "lapack"),
            ("Matio", "matio"),
            ("METIS", "metis"),
            ("Netcdf", "netcdf-c"),
            ("SCALAPACK", "scalapack"),
            ("Zlib", "zlib"),
        ]
        if spec.satisfies("@12.12.1:"):
            tpl_dep_map.append(("Pnetcdf", "parallel-netcdf"))
        if spec.satisfies("@13:"):
            tpl_dep_map.append(("HWLOC", "hwloc"))

        for tpl_name, dep_name in tpl_dep_map:
            define_tpl(tpl_name, dep_name, dep_name in spec)

        # MPI settings
        options.append(define_tpl_enable("MPI"))
        if "+mpi" in spec:
            # Force Trilinos to use the MPI wrappers instead of raw compilers
            # to propagate library link flags for linkers that require fully
            # resolved symbols in shared libs (such as macOS and some newer
            # Ubuntu)
            options.extend(
                [
                    define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
                    define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
                    define("MPI_BASE_DIR", spec["mpi"].prefix),
                ]
            )

        # ParMETIS dependencies have to be transitive explicitly
        have_parmetis = "parmetis" in spec
        options.append(define_tpl_enable("ParMETIS", have_parmetis))
        if have_parmetis:
            options.extend(
                [
                    define(
                        "ParMETIS_LIBRARY_DIRS",
                        [spec["parmetis"].prefix.lib, spec["metis"].prefix.lib],
                    ),
                    define("ParMETIS_LIBRARY_NAMES", ["parmetis", "metis"]),
                    define(
                        "TPL_ParMETIS_INCLUDE_DIRS",
                        spec["parmetis"].headers.directories + spec["metis"].headers.directories,
                    ),
                ]
            )

        if spec.satisfies("^superlu-dist@4.0:"):
            options.extend(
                [
                    define("HAVE_SUPERLUDIST_LUSTRUCTINIT_2ARG", True),
                ]
            )

        if spec.satisfies("^parallel-netcdf"):
            options.extend(
                [
                    define("TPL_Netcdf_Enables_Netcdf4", True),
                    define("TPL_Netcdf_PARALLEL", True),
                    define("PNetCDF_ROOT", spec["parallel-netcdf"].prefix),
                ]
            )

        options.append(define_tpl_enable("Cholmod", False))

        if spec.satisfies("platform=darwin"):
            # Don't let TriBITS define `libdl` as an absolute path to
            # the MacOSX{nn.n}.sdk since that breaks at every xcode update
            options.append(define_tpl_enable("DLlib", False))

        # ################# Explicit template instantiation #################

        complex_s = spec.variants["complex"].value
        float_s = spec.variants["float"].value

        options.extend(
            [
                define("Teuchos_ENABLE_COMPLEX", complex_s),
                define("Teuchos_ENABLE_FLOAT", float_s),
            ]
        )

        if "+tpetra +explicit_template_instantiation" in spec:
            options.append(define_from_variant("Tpetra_INST_OPENMP", "openmp"))
            options.extend(
                [
                    define("Tpetra_INST_DOUBLE", True),
                    define("Tpetra_INST_COMPLEX_DOUBLE", complex_s),
                    define("Tpetra_INST_COMPLEX_FLOAT", float_s and complex_s),
                    define("Tpetra_INST_FLOAT", float_s),
                    define("Tpetra_INST_SERIAL", True),
                ]
            )

            gotype = spec.variants["gotype"].value
            if gotype == "all":
                # default in older Trilinos versions to enable multiple GOs
                options.extend(
                    [
                        define("Tpetra_INST_INT_INT", True),
                        define("Tpetra_INST_INT_LONG", True),
                        define("Tpetra_INST_INT_LONG_LONG", True),
                    ]
                )
            else:
                options.extend(
                    [
                        define("Tpetra_INST_INT_INT", gotype == "int"),
                        define("Tpetra_INST_INT_LONG", gotype == "long"),
                        define("Tpetra_INST_INT_LONG_LONG", gotype == "long_long"),
                    ]
                )

        # ################# Kokkos ######################

        if "+kokkos" in spec:
            arch = Kokkos.get_microarch(spec.target)
            if arch:
                options.append(define("Kokkos_ARCH_" + arch.upper(), True))

            define_kok_enable = _make_definer("Kokkos_ENABLE_")
            options.extend(
                [
                    define_kok_enable("CUDA"),
                    define_kok_enable("OPENMP" if spec.version >= Version("13") else "OpenMP"),
                ]
            )
            if "+cuda" in spec:
                use_uvm = "+uvm" in spec
                options.extend(
                    [
                        define_kok_enable("CUDA_UVM", use_uvm),
                        define_kok_enable("CUDA_LAMBDA", True),
                        define_kok_enable("CUDA_RELOCATABLE_DEVICE_CODE", "cuda_rdc"),
                    ]
                )
                arch_map = Kokkos.spack_cuda_arch_map
                options.extend(
                    define("Kokkos_ARCH_" + arch_map[arch].upper(), True)
                    for arch in spec.variants["cuda_arch"].value
                )

            if "+rocm" in spec:
                options.extend(
                    [
                        define_kok_enable("ROCM", False),
                        define_kok_enable("HIP", True),
                        define_kok_enable("HIP_RELOCATABLE_DEVICE_CODE", "rocm_rdc"),
                    ]
                )
                if "+tpetra" in spec:
                    options.append(define("Tpetra_INST_HIP", True))
                amdgpu_arch_map = Kokkos.amdgpu_arch_map
                for amd_target in spec.variants["amdgpu_target"].value:
                    try:
                        arch = amdgpu_arch_map[amd_target]
                    except KeyError:
                        pass
                    else:
                        options.append(define("Kokkos_ARCH_" + arch.upper(), True))

        # ################# System-specific ######################

        if sys.platform == "darwin" and macos_version() >= Version("10.12"):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append(define("CMAKE_MACOSX_RPATH", True))
        else:
            options.append(define("CMAKE_INSTALL_NAME_DIR", self.prefix.lib))

        return options

    @run_after("install")
    def filter_python(self):
        # When trilinos is built with Python, libpytrilinos is included
        # through cmake configure files. Namely, Trilinos_LIBRARIES in
        # TrilinosConfig.cmake contains pytrilinos. This leads to a
        # run-time error: Symbol not found: _PyBool_Type and prevents
        # Trilinos to be used in any C++ code, which links executable
        # against the libraries listed in Trilinos_LIBRARIES.  See
        # https://github.com/trilinos/Trilinos/issues/569 and
        # https://github.com/trilinos/Trilinos/issues/866
        # A workaround is to remove PyTrilinos from the COMPONENTS_LIST
        # and to remove -lpytrilonos from Makefile.export.Trilinos
        if "+python" in self.spec:
            filter_file(
                r"(SET\(COMPONENTS_LIST.*)(PyTrilinos;)(.*)",
                (r"\1\3"),
                "%s/cmake/Trilinos/TrilinosConfig.cmake" % self.prefix.lib,
            )
            filter_file(r"-lpytrilinos", "", "%s/Makefile.export.Trilinos" % self.prefix.include)

    def setup_run_environment(self, env):
        if "+exodus" in self.spec:
            env.prepend_path("PYTHONPATH", self.prefix.lib)

        if "+cuda" in self.spec:
            # currently Trilinos doesn't perform the memory fence so
            # it relies on blocking CUDA kernel launch.
            env.set("CUDA_LAUNCH_BLOCKING", "1")
