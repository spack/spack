/**
 * Copyright Spack Project Developers. See COPYRIGHT file for details.
 *
 * SPDX-License-Identifier: (Apache-2.0 OR MIT)
 */

/* Compiled to an object and archived with lib.exe to produce a true static
 * library, i.e. a COFF archive that is *not* an import library. The wrapper's
 * `relocate.exe --coff <lib> --verify` must report exit code 1 for this. */
extern "C" int subtract(int a, int b) { return a - b; }
