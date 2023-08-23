# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os,sys

from spack.package import *


class Qscintilla(QMakePackage):
    """
    QScintilla is a port to Qt of Neil Hodgson's Scintilla C++ editor control.
    """

    homepage = "https://www.riverbankcomputing.com/software/qscintilla/intro"
    url = "https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.12.0/QScintilla_src-2.12.0.tar.gz"

    # Directory structure is changed in latest release, logic is lost
    version("2.13.3", sha256="711d28e37c8fccaa8229e8e39a5b3b2d97f3fffc63da10b71c71b84fa3649398")
    version(
        "2.12.0",
        sha256="a4cc9e7d2130ecfcdb18afb43b813ef122473f6f35deff747415fbc2fe0c60ed",
        url="https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.12.0/QScintilla_src-2.12.0.tar.gz",
    )

    # Last standard release dates back to 2021/11/23
    version(
        "2.11.6",
        sha256="e7346057db47d2fb384467fafccfcb13aa0741373c5d593bc72b55b2f0dd20a7",
        url="https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.11.6/QScintilla-2.11.6.tar.gz",
    )
    version(
        "2.11.2",
        sha256="029bdc476a069fda2cea3cd937ba19cc7fa614fb90578caef98ed703b658f4a1",
        url="https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.11.2/QScintilla_gpl-2.11.2.tar.gz",
    )
    version(
        "2.10.2",
        sha256="14b31d20717eed95ea9bea4cd16e5e1b72cee7ebac647cba878e0f6db6a65ed0",
        url="https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.10.2/QScintilla-2.10.2.tar.gz",
    )

    variant("designer", default=False, description="Enable pluging for Qt-Designer")
    variant("python", default=False, description="Build python bindings")

    depends_on("qt+opengl", when="+python ^qt@5")
    depends_on("qt-base+opengl", when="+python ^qt-base")
    depends_on("qmake")
    depends_on("py-pyqt6", type=("build", "run"), when="+python ^qt-base")
    depends_on("py-pyqt-builder", type="build", when="+python")
    depends_on("py-pyqt5", type=("build", "run"), when="+python ^qt@5")
    depends_on("py-pyqt4 +qsci_api", type=("build", "run"), when="+python ^qt@4")
    depends_on("python", type=("build", "run"), when="+python")
    # adter install inquires py-sip variant : so we need to have it
    depends_on("py-sip", type="build", when="~python")

    extends("python", when="+python")
    @property
    def build_directory(self):
        if self.version >= Version("2.12"):
            return "src"
        else:
            return "Qt4Qt5"

    def qmake_args(self):
        # below, DEFINES ... gets rid of ...regex...errors during build
        # although, there shouldn't be such errors since we use '-std=c++11'
        args = ["CONFIG+=-std=c++11", "DEFINES+=NO_CXX11_REGEX=1"]
        return args

    # When INSTALL_ROOT is unset, qscintilla is installed under qt_prefix
    # giving 'Nothing Installed Error'
    def setup_build_environment(self, env):
        env.set("INSTALL_ROOT", self.prefix)

    def setup_run_environment(self, env):
        env.prepend_path("QT_PLUGIN_PATH", self.prefix.plugins)

    # Fix install prefix
    @run_before("qmake")
    def fix_qaccesswidget(self):
        with working_dir(join_path(self.stage.source_path, "src")):
            qscipro = FileFilter("qscintilla.pro")

            qscipro.filter(
                "TEMPLATE = lib",
                "TEMPLATE = lib\nDEFINES += QT_NO_ACCESSIBILITY\nINCLUDEPATH += "+str(self.spec['qt-base'].prefix)+'/include'+"\nQT += widgets" + "\nQT += printsupport\n",
            )


    # Fix install prefix
    @run_after("qmake")
    def fix_install_path(self):
        # qt <= 5
        #makefile = FileFilter(join_path("Qt4Qt5", "Makefile"))
        #makefile.filter(r"\$\(INSTALL_ROOT\)" + self.spec["qt"].prefix, "$(INSTALL_ROOT)")
        # qt-base@6
        makefile = FileFilter(join_path(self.build_directory, "Makefile"))
        makefile.filter("$(INSTALL_ROOT)" + self.spec["qt-base"].prefix, "$(INSTALL_ROOT)", string=True, backup=True)


    @run_after("install")
    def postinstall(self):
        # Make designer plugin
        if "+designer" in self.spec:
            with working_dir(os.path.join(self.stage.source_path, "designer-Qt4Qt5")):
                qscipro = FileFilter("designer.pro")
                qscipro.filter("TEMPLATE = lib", "TEMPLATE = lib\nINCLUDEPATH += ../Qt4Qt5\n")

                qmake()
                make()
                makefile = FileFilter("Makefile")
                makefile.filter(r"\$\(INSTALL_ROOT\)" + self.spec["qt"].prefix, "$(INSTALL_ROOT)")
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
            elif "^py-pyqt6" in self.spec:
                py_pyqtx = "py-pyqt6"
                pyqtx = "PyQt6"

            with working_dir(join_path(self.stage.source_path, "src")):
                # Fix build errors
                # "QAbstractScrollArea: No such file or directory"
                # "qprinter.h: No such file or directory"
                # ".../Qsci.so: undefined symbol: _ZTI10Qsci...."
                qscipro = FileFilter("qscintilla.pro")
                if "^qt@4" in self.spec:
                    qtx = "qt4"
                elif "^qt@5" in self.spec:
                    qtx = "qt5"
                elif "^qt-base@6" in self.spec:
                    qtx = "qt6"


                link_qscilibs = "LIBS += -L" + self.prefix.lib + " -lqscintilla2_" + qtx
                qscipro.filter(
                    "TEMPLATE = lib",
                    "TEMPLATE = lib\nINCLUDEPATH += {includepath}\nQT += widgets" + "\nQT += printsupport\n" + link_qscilibs,
                )

                make()

                # Fix installation prefixes
                makefile = FileFilter("Makefile")
                makefile.filter("$(INSTALL_ROOT)", "", string=True)
                #makefile = FileFilter("Qsci/Makefile")
                #makefile.filter("$(INSTALL_ROOT)", "", string=True)

                if "@2.11:" in self.spec:
                    make("install", parallel=False)
                else:
                    make("install", parallel=False)

            if 'py-pyqt6' in self.spec:
                with working_dir(join_path(self.stage.source_path, "Python")):
                    cp = which('cp')
                    cp('pyproject-qt6.toml', 'pyproject.toml')
                    # TODO below sip_inc_dir is incorrect:
                    # its prefix of qscintilla itself as opposed to prefix for py-pyqt6
                    # qscintilla+python builds fine when sip_inc_dir is hardcoded!
                    str(self.spec)
                    sip_inc_dir = join_path(self.spec['py-pyqt6'].prefix, self.spec['python'].package.platlib, 'PyQt6', 'bindings' )
                    with open('pyproject.toml', 'a') as tomlfile:
                        tomlfile.write('\n[tool.sip.project]\nsip-include-dirs = ["/home/sbulut/Downloads/spack/opt/spack/linux-linuxmint21-skylake/gcc-11.4.0/py-pyqt6-6.5.1-6vq3475u5e3s74qbpv3gnwashddf6pni/lib/python3.10/site-packages/PyQt6/bindings"]\n')
                        #tomlfile.write('\n[tool.sip.project]\nsip-include-dirs = ["'+str(sip_inc_dir)+'"]\n')
                    mkdirp(os.path.join(self.prefix.share.sip, pyqtx))

                    sip_build = Executable(self.spec["py-sip"].prefix.bin.join("sip-build"))
                    sip_build(
                        "--target-dir=" + self.spec.prefix,
                        "--qsci-include-dir=" + self.spec.prefix.include,
                        "--qsci-library-dir=" + self.spec.prefix.lib,
                        "--api-dir=" + self.prefix.share.qsci,
                        "--verbose",
                    )
                    make("install","-C","build/")

            else: #pyqt4 or 5
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


    @run_after("install")
    def extend_path_setup(self):
        if self.spec["py-sip"].satisfies("@:4"):
            # See github issue #14121 and PR #15297
            module = self.spec["py-sip"].variants["module"].value
            if module != "sip":
                module = module.split(".")[0]
                with working_dir(python_platlib):
                    with open(os.path.join(module, "__init__.py"), "w") as f:
                        f.write("from pkgutil import extend_path\n")
                        f.write("__path__ = extend_path(__path__, __name__)\n")
