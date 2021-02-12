# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyReportlab(PythonPackage):
    """The ReportLab Toolkit. An Open Source Python library for generating
    PDFs and graphics."""

    pypi = "reportlab/reportlab-3.4.0.tar.gz"

    version('3.5.59', sha256='a755cca2dcf023130b03bb671670301a992157d5c3151d838c0b68ef89894536')
    version('3.5.58', sha256='83b3f4394aac383b24cee9f8bd93484b109a6144ba709c8671fdac1b1ac6ce86')
    version('3.5.57', sha256='6c89b10e6bafc429840932a25504bf61e1b12e9e87bf4360be9e618377ec13a1')
    version('3.5.56', sha256='51b16e297f7b937fc530dd151e4b38f1d305b01c9aa10657bc32a5d2901b8ad7')
    version('3.5.55', sha256='4f307accda32c9f17015ed77c7424f904514e349dff063f78d2462d715963e53')
    version('3.5.54', sha256='8365efe779e43e8005eace19c11c36e6a4bbea86ddc868b8db122240391c1747')
    version('3.5.53', sha256='49e32586d3a814a5f77407c0590504a72743ca278518b3c0f90182430f2d87af')
    version('3.5.52', sha256='a5ad4696987fdb42d976093e1b1a585ec2ad42634b5ce94dbb71362dcc758afb')
    version('3.5.51', sha256='bd1ed4d8a064e7372d46b7a23774d984c024d8bb0c2ff3283d5213749b9ffa1c')
    version('3.5.50', sha256='876ce59164245f62bf67b8502e127b0a3ffd40f37c7177d1b4d9da24e42a77b0')
    version('3.5.49', sha256='2ccf5165aa64e51abf240cd3f0062b860bb19346bd2c268fb00c33c09a53f8a8')
    version('3.5.48', sha256='0bfe3fe6e1bd1d922f83683eae2ba1d2d29de94e25fb115eacca9530b4b02f76')
    version('3.5.47', sha256='45b2a7aa65e082bf481eea9994cdc00292698f8dc9e4a8c0ecfc6be90548803f')
    version('3.5.46', sha256='56d71b78e7e4bb31a93e1dff13c22d19b7fb3890b021a39b6c3661b095bd7de8')
    version('3.5.45', sha256='593325a1ee889088c188b8989049f8f014b2cc28db083962444c4ff5c580c7c2')
    version('3.5.44', sha256='670650970c7ba7164cf6340bcd182e7e933eff5d65183af98ee77b40cc25a438')
    version('3.5.42', sha256='9c21f202697a6cea57b9d716288fc919d99cbabeb30222eebfc7ff77eac32744')
    version('3.5.34', sha256='9675a26d01ec141cb717091bb139b6227bfb3794f521943101da50327bff4825')
    version('3.5.32', sha256='83ef44936ef4e9c432d62bc2b72ec8d772b87af319d123e827a72e9b6884c851')
    version('3.5.31', sha256='3e2d2ea8ac3d63c918a2b40476c2745704d0364abe2b9c844c75992132a5eac7')
    version('3.5.28', sha256='7195c6ea096d10c91cc470f9f0ced3ad74470d9c0fd97923b5e764597dd13671')
    version('3.5.26', sha256='739e81a32cd51be8d8225d316b1399d4b6ff6ee109963d3b5320b0718ce2aa0f')
    version('3.5.23', sha256='6c81ee26753fa09062d8404f6340eefb02849608b619e3843e0d17a7cda8798f')
    version('3.5.21', sha256='08e6e63a4502d3a00062ba9ff9669f95577fbdb1a5f8c6cdb1230c5ee295273a')
    version('3.5.20', sha256='7b248d2d9d4ab6d4cad91eb2b153b2c4c7b3fced89cb5a5b5bfbc7d09593871a')
    version('3.5.19', sha256='47951166d897b60e9e7ca349db82a2b689e6478ac6078e2c7c88ca8becbb0c7d')
    version('3.5.18', sha256='99d74fffc201a3bd4b603cc27901917c283e6deed1c8bf7c65d14ac1fb78f5e3')
    version('3.5.17', sha256='a70d970619014dc83b4406bcfed7e2f9d5aaf5f521aad808f5560d90ea896fb4')
    version('3.5.16', sha256='b9c6ac3bd737a45b3bf5ec2719725fed91d26e9d7022864d529a09084a673756')
    version('3.5.13', sha256='6116e750f98018febc08dfee6df20446cf954adbcfa378d2c703d56c8864aff3')
    version('3.5.12', sha256='7e10261065d0f926d9d83fd1f2edb8bec466f3c60b3e927ef40e2262805c069d')
    version('3.5.11', sha256='234e1790858f1608d2fc8f820fa5660b7838cb14f12dec81e3c1156a4891ee1a')
    version('3.5.10', sha256='9041d17556b9652cd9cf13b56a4efad7b51df6c567279ced26584cb4eb712b09')
    version('3.5.9',  sha256='f92f81314807cd860f29fe07a1a4100b03910ae6bbfca20a07e02c3b460f4f20')
    version('3.5.8',  sha256='59fbd93f20169878e2d505d60e3e044bf100b6a4ded51370603df4548ec219fe')
    version('3.5.6',  sha256='3836a49e7ea7bce458f437cbc094633c7fd4ac027180565875c18ecc726f261e')
    version('3.5.5',  sha256='d18485c5b7561519138fd94a29239d8361cb3e204d38342f98f40c8d7774b4a5')
    version('3.5.4',  sha256='1d51b848c85c6e9a5603a0a9be7b0cf82e04b5e6addd4859418ea0e543501682')
    version('3.5.2',  sha256='08986267eaf25d62c3802512f0a97dc3426d0c82f52c8beb576689582eb85b7f')
    version('3.5.1',  sha256='5345494df4f1563fdab5597f7f543eae44c0aeecce05bd4d93c199f34c4b8c0c')
    version('3.5.0',  sha256='711036cadb7828c2ca291b0ad34c9e9782f61962664400e70e0eeedbb704bd94')
    version('3.4.0', sha256='5beaf35e59dfd5ebd814fdefd76908292e818c982bd7332b5d347dfd2f01c343')

    # py-reportlab provides binaries that duplicate those of other packages,
    # thus interfering with activation.
    # - easy_install, provided by py-setuptools
    # - pip, provided by py-pip
    extends('python', ignore=r'bin/.*')
