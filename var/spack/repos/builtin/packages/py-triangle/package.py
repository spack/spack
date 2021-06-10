# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#Date 10-June-2021

class PyTriangle(PythonPackage):
    """
    Python binding to the triangle library
    """

    homepage = "https://rufat.be/triangle"
    url      = "https://pypi.io/packages/source/t/triangle/triangle-20200424.tar.gz"
    git      = "https://github.com/drufat/triangle.git"

    maintainers = ['samcom12']
    version('master', branch='master')
    version('20200424', sha256='fc207641f8f39986f7d2bee1b91688a588cd235d2e67777422f94e61fece27e9')
    version('20200404', sha256='3d5c5a27a56bcb1a6ecdf536b6df35cdcebf6ce2f4bf348ac4b7ed7072830aaa')
    version('20200325', sha256='5c15304538b668e45732b4e445e960cd4852628c41eb99271cba67b26c535d12')
    version('20190115.3', sha256='69442062a1705f75b64166b161ade8a32a26b9323e09f5fa43079dbb6bf04bcc')
    version('20190115.2', sha256='a886e5613c7f441901d097dbf6244b8275c3cdb5dbea7c0e069664ae65c6fdd1')
    version('20190115.1', sha256='65a80d3d22aac0df1c5629d011609a0e85bf7d77a66a0c603a7c5fe388e24dae')
    version('20190115', sha256='896262d042a6bbbe7cdaeab7d5da919b839f064d2e7508fbf559f8f49c4df34c')
    version('20170429', sha256='31f9042e4af3a05774f1de49e2f255e76b702699bc0048b26c20f3be551e7742')
    version('20170106', sha256='006557958815d13b04d821abe7c4c47084d66a573808f7fd2824d69e677a044c')
    version('20160203', sha256='f782af1fcf969ae0d80a6cf2d2ff1eb8288f3c8b6a2c586d5766ef21bf641096')
    version('20160202', sha256='ef8473124882b6df99ca1bfbcfe67c39d915057b186a550ac79b79f29ae94050')
    version('2015.12.14', sha256='03a53886658785bb9381362c10405c61e6197d20d3d01a9c911959d4025adbac')
    version('2015.12.13', sha256='03443cdc37a109fac5df8437af5b985a7a734a0cfc439ce21bd0f8185366ffb4')
    version('2015.03.28', sha256='9a4876399fbf24d1e64cfa35eb9bb1d393802865ef092e2537c52805412a8e4c')
    version('2013.04.05', sha256='53ab87dff8d2cb82df34eb956037d2f823339a6444d567d10c3797f97312506f')
    version('2013.01.07', sha256='3b817346acc5fd1d03f810edca025ee7dfece0a8fb9b0bec7388faae2f5b5ecd')
    version('2013.01.06a', sha256='1a1f110a2d12de97d2f20afd1849bb92023977013f1e947cfadcbac4cd85265a')
    version('2013.01.06', sha256='c46ac664ea8083690b2dca986568c6c7089352157aa378d2ef514c5c9c4d5f8f')
    version('2012.07.04', sha256='25e3fa42f94405456df19c9648bc7df70de16d0f3c2a7c94e1e975c17ec3c48e')
    version('0.3', sha256='f2f8402907a3835b0e50c2a9ce466fb1921e240b816e55d42c0a1f1854dbfd6f')
    version('0.2', sha256='0f89cc5ae1e398183111e84794a8d213f616642628a6cb03fe5ae64a7a7235d4')
    version('0.1', sha256='32dbb76304ee0c522c7708623bd98dee5945528ec27eeb57182ef6b588e90a77')
    
	depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
