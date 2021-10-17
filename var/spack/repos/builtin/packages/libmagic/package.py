# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libmagic(AutotoolsPackage):
    """An open source implementation of the file(1) command that ships with
    most free operating systems.

    The file command is "a file type guesser", that is, a command-line tool
    that tells you in words what kind of data a file contains. Unlike most GUI
    systems, command-line UNIX systems - with this program leading the charge -
    don't rely on filename extentions to tell you the type of a file, but look
    at the file's actual contents. This is, of course, more reliable, but
    requires a bit of I/O.

    NOTE: some package managers delete the resulting "file" command to avoid
    installing the system utility, but we currently do not. Note also that some
    system-installed file commands do *not* come paired with shared-object
    libmagic libraries that are necessary to load python-based packages
    (py-python-magic, py-filemagic).
    """

    homepage = "https://www.darwinsys.com/file/"
    url      = "https://astron.com/pub/file/file-5.40.tar.gz"

    maintainers = ['sethrj']

    executables = [r'^file$']

    version('5.40', sha256='167321f43c148a553f68a0ea7f579821ef3b11c27b8cbe158e4df897e4a5dd57')

    variant('static', default=True, description='Also build static libraries')

    depends_on('bzip2')
    depends_on('xz')
    depends_on('zlib')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'file-([0-9.]+)', output)
        return match.group(1) if match else None

    def configure_args(self):
        args = [
            "--disable-dependency-tracking",
            "--enable-fsect-man5",
            "--enable-zlib",
            "--enable-bzlib",
            "--enable-xzlib",
        ]
        args += self.enable_or_disable('static')
        return args
