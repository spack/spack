# Windows PE/COFF test fixtures

Binaries used by `lib/spack/spack/test/relocate_windows.py` to exercise the ctypes-level
PE inspection in `spack.relocate` against real files. The tests never use the sources
in `src/` directly; `generate_fixtures.bat` compiles them into the binaries checked in
here. The binaries are only ever inspected, never executed.

| File | Sources | Built with | What it is for |
| --- | --- | --- | --- |
| `calc.dll` | `calc.cxx`, `entry.cxx` | MSVC compiler wrapper | DLL carrying the `spack`/`SPACKRESOURCE` resource |
| `calc.lib` | (import library of `calc.dll`) | MSVC compiler wrapper | Import library whose name field is the padded absolute path to `calc.dll` |
| `tester.exe` | `main.cxx`, `exe_entry.cxx`, `calc.lib` | MSVC compiler wrapper | EXE importing `calc.dll`, with its own resource and no exports |
| `plain.dll` | `calc.cxx`, `entry.cxx` | stock `cl.exe`/`link.exe` | DLL that exports symbols but has no spack resource, as if the wrapper was bypassed |
| `static.lib` | `static_only.cxx` | stock `cl.exe`/`lib.exe` | A true static archive, not an import library |
| `sfn_calc.dll` | `calc.cxx`, `entry.cxx` | MSVC compiler wrapper | Linked from a path over the wrapper's 143-character limit, so its resource holds an 8.3 short path |
| `sfn_calc.lib` | (import library of `sfn_calc.dll`) | MSVC compiler wrapper | Import library for `sfn_calc.dll` |

`fixtures.txt` records the absolute path each PE was linked at — what the wrapper
stores (padded) in the resource and in the import library name field. The fixtures
are staged under a fixed `C:\spack-pe-fixtures` rather than `%TEMP%`, so that path
is the same for anyone who regenerates them instead of recording whoever ran the
script last. Set `SPACK_PE_FIXTURE_STAGE` to stage elsewhere, but note that changes
the recorded paths, so commit the regenerated `fixtures.txt` with the binaries.

The tests read the paths from `fixtures.txt` rather than hard coding them, because
the `sfn_calc.dll` entry still depends on how 8.3 names came out on the generating
machine.

## Regenerating

1. Build the wrapper: run `nmake cl.exe` in the MSVC wrapper repository, which
   produces `install\cl.exe`.
2. From a Visual Studio Developer Command Prompt, run:

   ```
   generate_fixtures.bat <path-to-msvc-wrapper-repo>
   ```

   or set `SPACK_MSVC_WRAPPER_ROOT` instead of passing the path.
3. Commit every binary here together with `fixtures.txt`.

The `sfn_calc.*` pair additionally requires 8.3 short filename creation to be enabled on
the staging volume. If it is not, the script says so and skips those two files, and the
tests that need them skip in turn. Enable it with `fsutil 8dot3name set 0` from an
elevated prompt.

## Build flags

The fixtures are kept to a few KB by leaving out the C runtime. Every object is
compiled with:

```
cl /c /EHsc /GS- /Gs9999999 /O1
```

- `/GS-` drops buffer security checks, which need the CRT.
- `/Gs9999999` disables stack probes (`__chkstk`), which also come from the CRT.
- `/O1` optimizes for size.

DLLs are linked with:

```
link /DLL /NODEFAULTLIB /ENTRY:DllEntry /OPT:REF /OPT:ICF /INCREMENTAL:NO
```

and `tester.exe` the same way, without `/DLL` and with `/ENTRY:ExeEntry`.

- `/NODEFAULTLIB` links no default libraries, including the CRT.
- `/ENTRY` sets the entry point to the minimal one in `entry.cxx` or `exe_entry.cxx`,
  since the CRT's is not linked.
- `/OPT:REF /OPT:ICF` remove unreferenced and duplicate code.
- `/INCREMENTAL:NO` avoids the padding incremental linking adds.
