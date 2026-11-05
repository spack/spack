/**
 * Copyright Spack Project Developers. See COPYRIGHT file for details.
 *
 * SPDX-License-Identifier: (Apache-2.0 OR MIT)
 */

/* Minimal EXE entry point, see entry.cxx. Calls into main() so the import of
 * calc.dll is actually retained through /OPT:REF. */

int main(int argc, char** argv);

extern "C" int __stdcall ExeEntry() { return main(0, 0); }
