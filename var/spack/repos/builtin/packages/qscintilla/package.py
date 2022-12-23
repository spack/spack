# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Qscintilla(QMakePackage):
    """QScintilla is a port to Qt of Neil Hodgson's Scintilla C++ editor control."""

    homepage = "https://www.riverbankcomputing.com/software/qscintilla/intro"
    url = "https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.12.0/QScintilla_src-2.12.0.tar.gz"
    list_url = "https://riverbankcomputing.com/software/qscintilla/download"

    version("2.13.3", sha256="711d28e37c8fccaa8229e8e39a5b3b2d97f3fffc63da10b71c71b84fa3649398")
    version("2.12.0", sha256="a4cc9e7d2130ecfcdb18afb43b813ef122473f6f35deff747415fbc2fe0c60ed")
    version("2.11.6", sha256="e7346057db47d2fb384467fafccfcb13aa0741373c5d593bc72b55b2f0dd20a7")
    version("2.11.2", sha256="029bdc476a069fda2cea3cd937ba19cc7fa614fb90578caef98ed703b658f4a1")
    version("2.10.2", sha256="14b31d20717eed95ea9bea4cd16e5e1b72cee7ebac647cba878e0f6db6a65ed0")

    variant("designer", default=False, description="Enable plugin for Qt-Designer")
    variant("python", default=False, description="Build python bindings")

    depends_on("qt+opengl", when="+python")
    depends_on("qt")
    depends_on("py-pyqt5", type=("build", "run"), when="+python ^qt@5")
    depends_on("py-pyqt4", type=("build", "run"), when="+python ^qt@4")
    # adter install inquires py-sip variant : so we need to have it
    depends_on("py-sip", type="build", when="~python")

    extends("python", when="+python")

    # TODO: newer versions do not have a configure.py script, figure out how to specify sip dir
    conflicts("+python", when="@2.12:")

    @property
    def build_directory(self):
        if self.version >= Version("2.12"):
            return "src"
        else:
            return "Qt4Qt5"

    def url_for_version(self, version):
        url = "https://www.riverbankcomputing.com/static/Downloads/QScintilla/{0}/QScintilla{1}-{0}.tar.gz"
        suffix = ""
        if version >= Version("2.12"):
            suffix = "_src"
        elif version <= Version("2.11.2"):
            suffix = "_gpl"
        return url.format(version, suffix)

    def qmake_args(self):
        # Needed for old C++ compilers without a working std::regex
        return ["CONFIG+=-std=c++11", "DEFINES+=NO_CXX11_REGEX=1"]

    def setup_build_environment(self, env):
        # When INSTALL_ROOT is unset, qscintilla is installed under qt_prefix
        # giving 'Nothing Installed Error'
        env.set("INSTALL_ROOT", self.prefix)

    def setup_run_environment(self, env):
        env.prepend_path("QT_PLUGIN_PATH", self.prefix.plugins)

    @run_after("qmake")
    def fix_install_path(self):
        # Fix install prefix
        makefile = FileFilter(join_path(self.build_directory, "Makefile"))
        makefile.filter("$(INSTALL_ROOT)" + self.spec["qt"].prefix, "$(INSTALL_ROOT)", string=True)

    @run_after("install")
    def postinstall(self):
        # Make designer plugin
        if "+designer" in self.spec:
            if self.version >= Version("2.12"):
                directory = "designer"
                includepath = "../src"
            else:
                directory = "designer-Qt4Qt5"
                includepath = "../Qt4Qt5"

            with working_dir(os.path.join(self.stage.source_path, directory)):
                qscipro = FileFilter("designer.pro")
                qscipro.filter("TEMPLATE = lib", f"TEMPLATE = lib\nINCLUDEPATH += {includepath}\n")

                qmake()
                make()
                makefile = FileFilter("Makefile")
                makefile.filter(
                    "$(INSTALL_ROOT)" + self.spec["qt"].prefix, "$(INSTALL_ROOT)", string=True
                )
                make("install")

    @run_after("install")
    def make_qsci(self):
        if "+python" in self.spec:
            if "^py-pyqt4" in self.spec:
                py_pyqtx = "py-pyqt4"
                pyqtx = "PyQt4"
            elif "^py-pyqt5" in self.spec:
                py_pyqtx = "py-pyqt5"
                pyqtx = "PyQt5"

            with working_dir(join_path(self.stage.source_path, "Python")):
                pydir = join_path(python_platlib, pyqtx)
                mkdirp(os.path.join(self.prefix.share.sip, pyqtx))
                python = self.spec["python"].command
                python(
                    "configure.py",
                    "--pyqt=" + pyqtx,
                    "--sip=" + self.spec["py-sip"].prefix.bin.sip,
                    "--qsci-incdir=" + self.spec.prefix.include,
                    "--qsci-libdir=" + self.spec.prefix.lib,
                    "--qsci-sipdir=" + os.path.join(self.prefix.share.sip, pyqtx),
                    "--apidir=" + self.prefix.share.qsci,
                    "--destdir=" + pydir,
                    "--pyqt-sipdir=" + os.path.join(self.spec[py_pyqtx].prefix.share.sip, pyqtx),
                    "--sip-incdir="
                    + join_path(
                        self.spec["py-sip"].prefix.include,
                        "python" + str(self.spec["python"].version.up_to(2)),
                    ),
                    "--stubsdir=" + pydir,
                )

                # Fix build errors
                # "QAbstractScrollArea: No such file or directory"
                # "qprinter.h: No such file or directory"
                # ".../Qsci.so: undefined symbol: _ZTI10Qsci...."
                qscipro = FileFilter("Qsci/Qsci.pro")
                if "^qt@4" in self.spec:
                    qtx = "qt4"
                elif "^qt@5" in self.spec:
                    qtx = "qt5"

                link_qscilibs = "LIBS += -L" + self.prefix.lib + " -lqscintilla2_" + qtx
                qscipro.filter(
                    "TEMPLATE = lib",
                    "TEMPLATE = lib\nQT += widgets" + "\nQT += printsupport\n" + link_qscilibs,
                )

                make()

                # Fix installation prefixes
                makefile = FileFilter("Makefile")
                makefile.filter("$(INSTALL_ROOT)", "", string=True)
                makefile = FileFilter("Qsci/Makefile")
                makefile.filter("$(INSTALL_ROOT)", "", string=True)

                if "@2.11:" in self.spec:
                    make("install", parallel=False)
                else:
                    make("install")
