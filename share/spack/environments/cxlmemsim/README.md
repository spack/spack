# Ocean CXLMemSim Spack Environment

This environment builds the Ocean CXLMemSim test stack with an x86_64 CXL-capable QEMU on macOS. It is meant to give a repeatable path for downloading the VM image, launching QEMU, and connecting QEMU to a CXLMemSim host server through shared memory or a local TCP port.

## What This Environment Installs

- `qemu-system-x86_64` with CXL Type 3 and experimental accelerator device support.
- `qemu_launch_cxl.sh` and `qemu_launch_cxl1.sh` for one-host and second-host launches.
- `download_trimmed_qemu_image.sh` and `cxlmemsim-download-qemu-image` for the guest kernel and disk image.
- `cxlmemsim_server`, required by QEMU's CXL Type 3 transport path.
- `cxlmemsim_latency` for quick latency calculations.

The default spec is:

```console
cxlmemsim@2026-05-07+tools+server+qemu+hvf+rosetta target=x86_64 build_type=Release
```

On Apple Silicon this builds and launches the x86_64 QEMU path through Rosetta. The launcher uses a Rosetta-compatible acceleration default; native x86_64 macOS builds can override the accelerator with `QEMU_ACCEL=hvf`.

## Build

From the root of this Spack checkout:

```console
source share/spack/setup-env.sh
spack env activate ./share/spack/environments/cxlmemsim
spack concretize -f
spack install
spack load cxlmemsim
```

Check the installed prefix:

```console
spack location -i cxlmemsim
```

## Download The Guest Image

After `spack load cxlmemsim`, run:

```console
cxlmemsim-download-qemu-image
```

By default images are stored in:

```console
$CXL_QEMU_IMAGE_DIR
```

To force a 4 GB raw guest image after download:

```console
qemu-img resize "$CXL_QEMU_IMAGE_DIR/qemu.img" 4G
cp "$CXL_QEMU_IMAGE_DIR/qemu.img" "$CXL_QEMU_IMAGE_DIR/qemu1.img"
```

## Launch QEMU

Default single-host launch:

```console
qemu_launch_cxl.sh
```

Second-host launch:

```console
qemu_launch_cxl1.sh
```

The launchers install both into `bin/` and `share/cxlmemsim/` under the package prefix.

Useful macOS defaults:

```console
QEMU_NET=none QEMU_NOGRAPHIC=1 qemu_launch_cxl.sh
```

Inside the guest, quick CXL checks are:

```console
lspci | grep -i cxl
dmesg | grep -i cxl
ls /sys/bus/cxl/devices
```

## Server And Transport Modes

QEMU reads these environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `CXL_TRANSPORT_MODE` | `shm` | QEMU transport: `shm` or `tcp`. |
| `CXL_MEMSIM_HOST` | `127.0.0.1` | Host used by TCP mode. |
| `CXL_MEMSIM_PORT` | `9999` | Local TCP port used by TCP mode. |
| `CXL_PGAS_SHM` | `/cxlmemsim_pgas` | POSIX shared-memory name used by QEMU SHM mode. |
| `CXL_MEMSIM_SERVER_BINARY` | `$prefix/bin/cxlmemsim_server` | Host server binary started before QEMU. |
| `CXL_MEMSIM_SERVER_AUTOSTART` | `auto` | `auto`, `1`, or `0` for launcher-managed server startup. |

The launcher maps QEMU `CXL_TRANSPORT_MODE=shm` to the server's `pgas-shm` mode because QEMU opens the PGAS shared-memory object named by `CXL_PGAS_SHM`.

### Shared-Memory Mode

Shared-memory mode is the default:

```console
CXL_TRANSPORT_MODE=shm qemu_launch_cxl.sh
```

The launcher starts `cxlmemsim_server` with `--comm-mode pgas-shm` and `--pgas-shm-name "$CXL_PGAS_SHM"` before starting QEMU.

Manual equivalent:

```console
mkdir -p "${TMPDIR:-/tmp}/cxlmemsim"
cxlmemsim_server \
  --comm-mode pgas-shm \
  --pgas-shm-name /cxlmemsim_pgas \
  --capacity 1024 \
  --backing-file "${TMPDIR:-/tmp}/cxlmemsim/cxlmemsim_shared"
```

Then launch QEMU in another shell:

```console
CXL_TRANSPORT_MODE=shm CXL_PGAS_SHM=/cxlmemsim_pgas qemu_launch_cxl.sh
```

### TCP Mode

TCP mode requires a running server on the local port. The launcher will fail early if `CXL_TRANSPORT_MODE=tcp` and no `cxlmemsim_server` binary is available.

Launcher-managed TCP:

```console
CXL_TRANSPORT_MODE=tcp \
CXL_MEMSIM_HOST=127.0.0.1 \
CXL_MEMSIM_PORT=9999 \
qemu_launch_cxl.sh
```

Manual server:

```console
cxlmemsim_server \
  --comm-mode tcp \
  --port 9999 \
  --tcp-addr 127.0.0.1 \
  --tcp-port 9999 \
  --capacity 1024 \
  --backing-file "${TMPDIR:-/tmp}/cxlmemsim/cxlmemsim_shared"
```

Then launch QEMU:

```console
CXL_TRANSPORT_MODE=tcp \
CXL_MEMSIM_HOST=127.0.0.1 \
CXL_MEMSIM_PORT=9999 \
qemu_launch_cxl.sh
```

## Common Overrides

| Variable | Example | Effect |
| --- | --- | --- |
| `DISK_IMAGE` | `/path/to/qemu.img` | Use a custom guest disk. |
| `KERNEL_IMAGE` | `/path/to/bzImage` | Use a custom guest kernel. |
| `VM_MEMORY` | `8G` | Guest RAM size. |
| `CXL_MEM_SIZE` | `1G` | CXL Type 3 backing memory size. |
| `CXL_FMW_SIZE` | `4G` | CXL fixed memory window size. |
| `HOST_SHM_DIR` | `/tmp/cxlmemsim` | Host directory for QEMU memory-backend files. |
| `QEMU_NOGRAPHIC` | `1` | Run in serial-console mode. |
| `QEMU_NET` | `none` or `user` | macOS network mode. |

## Troubleshooting

- `cxlmemsim_server not found`: rebuild this environment with `+server`, then run `spack load cxlmemsim`. You can also set `CXL_MEMSIM_SERVER_BINARY` to a compatible server binary.
- `SHM invalid magic`: QEMU and the server are using different shared-memory names, or QEMU started before the server was ready. Use the same `CXL_PGAS_SHM` value on both sides.
- TCP connection failure: confirm the server is listening on `127.0.0.1:9999` or set matching `CXL_MEMSIM_HOST` and `CXL_MEMSIM_PORT`.
- Rosetta launch issues: make sure Rosetta is installed with `softwareupdate --install-rosetta`, then rerun the Spack install or launcher.
