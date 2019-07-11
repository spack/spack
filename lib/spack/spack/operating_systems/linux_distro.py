# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
from spack.architecture import OperatingSystem
import platform
from spack.util.module_cmd import module

class LinuxDistro(OperatingSystem):
    """ This class will represent the autodetected operating system
        for a Linux System. Since there are many different flavors of
        Linux, this class will attempt to encompass them all through
        autodetection using the python module platform and the method
        platform.dist()
    """

    def __init__(self):
        self.modulecmd = module
        try:
            # This will throw an error if imported on a non-Linux platform.
            from external.distro import linux_distribution
            distname, version, _ = linux_distribution(
                full_distribution_name=False)
            distname, version = str(distname), str(version)
        except ImportError:
            distname, version = 'unknown', ''

        # Grabs major version from tuple on redhat; on other platforms
        # grab the first legal identifier in the version field.  On
        # debian you get things like 'wheezy/sid'; sid means unstable.
        # We just record 'wheezy' and don't get quite so detailed.
        version = re.split(r'[^\w-]', version)

        if 'ubuntu' in distname:
            version = '.'.join(version[0:2])
        else:
            version = version[0]

        super(LinuxDistro, self).__init__(distname, version)

    def arguments_to_detect_version_fn(self, paths):
        import spack.compilers

        command_arguments = []
        for compiler_name in spack.compilers.supported_compilers():
            cmp_cls = spack.compilers.class_for_compiler_name(compiler_name)

            if cmp_cls.modules is None:
                continue

            compiler_id = spack.compilers.CompilerID(self, compiler_name, None)
            detect_version_args = spack.compilers.DetectVersionArgs(
                id=compiler_id, variation=(None, None),
                language='cc', path='cc'
            )
            command_arguments.append(detect_version_args)
        return command_arguments

    def detect_version(self, detect_version_args):
        import spack.compilers
        modulecmd = self.modulecmd
        compiler_name = detect_version_args.id.compiler_name
        compiler_cls = spack.compilers.class_for_compiler_name(compiler_name)
        output = modulecmd('avail', compiler_cls.modules)
        version_regex = r'(%s)/([\d\.]+[\d])' % compiler_cls.modules
        matches = re.findall(version_regex, output)
        version = tuple(version for _, version in matches)
        compiler_id = detect_version_args.id
        value = detect_version_args._replace(
            id=compiler_id._replace(version=version)
        )
        return value, None

    def make_compilers(self, compiler_id, paths):
        import spack.spec
        name = compiler_id.compiler_name
        cmp_cls = spack.compilers.class_for_compiler_name(name)
        compilers = []
        for v in compiler_id.version:
            comp = cmp_cls(
                spack.spec.CompilerSpec(name + '@' + v),
                self, platform.machine(),
                [cmp_cls.cc_names[0],
                 cmp_cls.cxx_names[0],
                 cmp_cls.f77_names[0],
                 cmp_cls.fc_names[0]],
                [name + '/' + v])

            compilers.append(comp)
        return compilers
