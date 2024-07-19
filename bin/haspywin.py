# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import subprocess
import sys


def ensure_pywin32_installed():
    try:
        import win32con  # noqa: F401
    except ImportError:
        print("pyWin32 not installed but is required.\nInstalling via pip:")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])


if __name__ == "__main__":
    ensure_pywin32_installed()
