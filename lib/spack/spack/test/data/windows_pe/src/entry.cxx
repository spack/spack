/**
 * Copyright Spack Project Developers. See COPYRIGHT file for details.
 *
 * SPDX-License-Identifier: (Apache-2.0 OR MIT)
 */

/* Minimal DLL entry point. Linking with /NODEFAULTLIB /ENTRY:DllEntry keeps the
 * fixture DLLs down to a few KB by avoiding the CRT entirely. These binaries are
 * only ever inspected, never loaded for execution. */

extern "C" int __stdcall DllEntry(void* /*module*/, unsigned long /*reason*/,
                                  void* /*reserved*/) {
    return 1;
}
