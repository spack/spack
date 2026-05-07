# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cxlmemsim(Package):
    """CXL memory-system simulator with an optional QEMU CXL build."""

    homepage = "https://github.com/SlugLab/CXLMemSim"
    git = "https://github.com/SlugLab/CXLMemSim.git"

    version("main", branch="main")
    version("2026-05-06", commit="3f09b5a58d8171f12fc930a66a6f9ef52c788cb5")

    resource(
        name="qemu",
        git="https://github.com/CXLMemUring/qemu.git",
        commit="fbd81476d5b85d89ae26819c4378254565b61025",
        destination="lib/qemu",
        when="+qemu",
    )

    variant(
        "qemu",
        default=False,
        description="Build the bundled CXL-enabled QEMU tree through QEMU's Meson/Ninja flow",
    )
    variant("hvf", default=False, description="Enable QEMU HVF acceleration on macOS")
    variant(
        "rosetta",
        default=False,
        description="Build and launch x86_64 QEMU through Rosetta on macOS",
    )
    variant("rdma", default=False, description="Enable RDMA transport support")
    variant(
        "tools",
        default=False,
        description="Build only portable tools and install runtime scripts for macOS smoke tests",
    )
    variant(
        "build_type",
        default="Release",
        values=("Debug", "Release", "RelWithDebInfo"),
        multi=False,
        description="CMake build type for the CXLMemSim server",
    )

    phases = ("cmake", "build", "build_qemu", "install")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cmake@3.25:", type="build", when="~tools")
    depends_on("ninja", type="build", when="~tools")
    depends_on("ninja", type="build", when="+qemu")
    depends_on("pkgconf", type="build", when="~tools")
    depends_on("pkgconf", type="build", when="+qemu")
    depends_on("cxxopts", when="~tools")
    depends_on("spdlog", when="~tools")
    depends_on("rdma-core", type=("build", "link"), when="+rdma platform=linux")

    with when("+qemu"):
        depends_on("bison", type="build")
        depends_on("diffutils", type="build")
        depends_on("flex", type="build")
        depends_on("meson@1.1.0:", type="build")
        depends_on("python@3.8:", type="build")
        depends_on("glib@2.66:", type=("build", "link"))
        depends_on("pixman@0.21.8:", type=("build", "link"))
        depends_on("zlib", type=("build", "link"))

    conflicts("+hvf", when="platform=linux", msg="HVF is a macOS accelerator.")
    conflicts("+rosetta", when="platform=linux", msg="Rosetta is a macOS compatibility layer.")
    conflicts("+rdma", when="platform=darwin", msg="RDMA transport requires Linux rdma-core.")

    @property
    def cmake_build_dir(self):
        return join_path(self.stage.path, "spack-build-cxlmemsim")

    @property
    def qemu_source_dir(self):
        qemu_dir = join_path(self.stage.source_path, "lib", "qemu")
        if os.path.exists(join_path(qemu_dir, "configure")):
            return qemu_dir
        return join_path(qemu_dir, "qemu")

    @property
    def qemu_build_dir(self):
        return join_path(self.qemu_source_dir, "build")

    @property
    def tools_only(self):
        return "+tools" in self.spec

    def setup_build_environment(self, env):
        if self.spec.satisfies("+rosetta platform=darwin"):
            arch_flags = "-arch x86_64"
            env.append_flags("CFLAGS", arch_flags)
            env.append_flags("CXXFLAGS", arch_flags)
            env.append_flags("LDFLAGS", arch_flags)
            env.set("QEMU_USE_ROSETTA", "1")
            env.set("QEMU_DARWIN_ARCH", "x86_64")

    def cmake(self, spec, prefix):
        if self.tools_only:
            return

        self._patch_cmake_for_non_rdma_builds()

        cmake = which("cmake")
        mkdirp(self.cmake_build_dir)

        prefix_entries = [spec["cxxopts"].prefix, spec["spdlog"].prefix]
        if spec.satisfies("^rdma-core"):
            prefix_entries.append(spec["rdma-core"].prefix)

        cmake(
            "-S",
            self.stage.source_path,
            "-B",
            self.cmake_build_dir,
            "-G",
            "Ninja",
            "-DCMAKE_BUILD_TYPE={0}".format(spec.variants["build_type"].value),
            "-DCMAKE_INSTALL_PREFIX={0}".format(prefix),
            "-DCMAKE_PREFIX_PATH={0}".format(";".join(str(x) for x in prefix_entries)),
        )

    def build(self, spec, prefix):
        if self.tools_only:
            self._build_portable_tools()
            return

        cmake = which("cmake")
        cmake("--build", self.cmake_build_dir, "--parallel", str(make_jobs))

    def build_qemu(self, spec, prefix):
        if "~qemu" in spec:
            return

        if spec.satisfies("platform=darwin"):
            self._patch_qemu_for_non_rdma_builds()
            self._patch_qemu_for_darwin()
        elif "~rdma" in spec:
            self._patch_qemu_for_non_rdma_builds()

        configure = Executable(join_path(self.qemu_source_dir, "configure"))
        ninja = which("ninja")

        configure_args = [
            "--prefix={0}".format(prefix),
            "--target-list=x86_64-softmmu",
            "--disable-docs",
            "--disable-werror",
            "--disable-bsd-user",
            "--disable-linux-user",
            "--disable-guest-agent",
            "--disable-sdl",
            "--disable-gtk",
            "--disable-vnc",
            "--disable-slirp",
        ]

        if spec.satisfies("platform=darwin"):
            configure_args.append("--disable-kvm")
            configure_args.append("--enable-hvf" if "+hvf" in spec else "--disable-hvf")

        configure_args.append("--enable-rdma" if "+rdma" in spec else "--disable-rdma")

        mkdirp(self.qemu_build_dir)
        with working_dir(self.qemu_build_dir):
            if spec.satisfies("+rosetta platform=darwin"):
                arch = Executable("/usr/bin/arch")
                arch("-x86_64", configure.path, *configure_args)
                arch("-x86_64", ninja.path, "-j{0}".format(make_jobs))
            else:
                configure(*configure_args)
                ninja("-j{0}".format(make_jobs))

    def _patch_qemu_for_darwin(self):
        cxl_type2 = join_path(self.qemu_source_dir, "hw", "cxl", "cxl_type2.c")
        if not os.path.exists(cxl_type2):
            return

        self._replace_in_file(
            cxl_type2,
            "#include <sys/eventfd.h>\n#include <linux/vfio.h>",
            "#ifdef __linux__\n#include <sys/eventfd.h>\n#include <linux/vfio.h>\n#endif",
        )
        self._replace_in_file(
            cxl_type2,
            "/* Open and setup VFIO container */\n"
            "static int cxl_type2_vfio_container_init",
            "/* Open and setup VFIO container */\n"
            "#ifdef __linux__\n"
            "static int cxl_type2_vfio_container_init",
        )
        self._replace_in_file(
            cxl_type2,
            "\n/* ========================================================================\n"
            " * hetGPU Backend Implementation",
            "\n#else\n"
            "static int cxl_type2_vfio_container_init(CXLType2State *ct2d, Error **errp)\n"
            "{\n"
            "    (void)ct2d;\n"
            "    error_setg(errp, \"VFIO GPU passthrough is only available on Linux\");\n"
            "    return -1;\n"
            "}\n\n"
            "static int cxl_type2_vfio_group_init(CXLType2State *ct2d, const char *pci_addr,\n"
            "                                      Error **errp)\n"
            "{\n"
            "    (void)ct2d;\n"
            "    (void)pci_addr;\n"
            "    error_setg(errp, \"VFIO GPU passthrough is only available on Linux\");\n"
            "    return -1;\n"
            "}\n\n"
            "static int cxl_type2_vfio_device_init(CXLType2State *ct2d, const char *pci_addr,\n"
            "                                       Error **errp)\n"
            "{\n"
            "    (void)ct2d;\n"
            "    (void)pci_addr;\n"
            "    error_setg(errp, \"VFIO GPU passthrough is only available on Linux\");\n"
            "    return -1;\n"
            "}\n\n"
            "static int cxl_type2_vfio_dma_map(CXLType2State *ct2d, Error **errp)\n"
            "{\n"
            "    (void)ct2d;\n"
            "    error_setg(errp, \"VFIO GPU passthrough is only available on Linux\");\n"
            "    return -1;\n"
            "}\n\n"
            "static void *cxl_type2_irq_thread(void *opaque)\n"
            "{\n"
            "    (void)opaque;\n"
            "    return NULL;\n"
            "}\n"
            "#endif\n\n"
            "/* ========================================================================\n"
            " * hetGPU Backend Implementation",
        )
        self._replace_in_file(
            cxl_type2,
            "    /* VFIO cleanup */\n    /* Stop IRQ forwarding thread */",
            "#ifdef __linux__\n"
            "    /* VFIO cleanup */\n    /* Stop IRQ forwarding thread */",
        )
        self._replace_in_file(
            cxl_type2,
            '    qemu_log("CXL Type2: GPU passthrough cleanup complete\\n");',
            "#else\n"
            "    if (ct2d->gpu_info.vfio_device_fd >= 0) {\n"
            "        close(ct2d->gpu_info.vfio_device_fd);\n"
            "        ct2d->gpu_info.vfio_device_fd = -1;\n"
            "    }\n"
            "    ct2d->gpu_info.vfio_group = NULL;\n"
            "    ct2d->gpu_info.vfio_container = NULL;\n"
            "#endif\n\n"
            '    qemu_log("CXL Type2: GPU passthrough cleanup complete\\n");',
        )

    def _replace_in_file(self, path, old, new):
        with open(path, "r", encoding="utf-8") as source:
            contents = source.read()
        if old not in contents:
            return
        with open(path, "w", encoding="utf-8") as source:
            source.write(contents.replace(old, new))

    def _patch_qemu_for_non_rdma_builds(self):
        meson_file = join_path(self.qemu_source_dir, "hw", "mem", "meson.build")
        if not os.path.exists(meson_file):
            return

        self._replace_in_file(
            meson_file,
            "mem_ss.add(when: 'CONFIG_CXL_MEM_DEVICE', if_true: files('cxl_type3.c', 'cxl_type3_rdma.c'))",
            "mem_ss.add(when: 'CONFIG_CXL_MEM_DEVICE', if_true: files('cxl_type3.c', 'cxl_type3_rdma_stub.c'))",
        )

    def install(self, spec, prefix):
        if self.tools_only:
            mkdirp(prefix.bin)
            install(join_path(self.cmake_build_dir, "cxlmemsim_latency"), prefix.bin)
        else:
            cmake = which("cmake")
            cmake("--install", self.cmake_build_dir)

            for binary in ("cxlmemsim_latency", "test_distributed_shm"):
                path = join_path(self.cmake_build_dir, binary)
                if os.path.exists(path):
                    install(path, prefix.bin)

        if "+qemu" in spec:
            ninja = which("ninja")
            if spec.satisfies("+rosetta platform=darwin"):
                arch = Executable("/usr/bin/arch")
                arch("-x86_64", ninja.path, "-C", self.qemu_build_dir, "install")
            else:
                ninja("-C", self.qemu_build_dir, "install")

        self._install_runtime_files(prefix)

    def _build_portable_tools(self):
        mkdirp(self.cmake_build_dir)
        cxx = Executable(self.compiler.cxx)
        cxx_args = ["-std=c++17", "-O2"]
        if self.spec.satisfies("+rosetta platform=darwin"):
            cxx_args.extend(["-arch", "x86_64"])

        cxx(
            *cxx_args,
            join_path(self.stage.source_path, "src", "calculateLatency.cc"),
            "-o",
            join_path(self.cmake_build_dir, "cxlmemsim_latency"),
        )

    def _patch_cmake_for_non_rdma_builds(self):
        if "+rdma" in self.spec:
            return

        cmake_file = join_path(self.stage.source_path, "CMakeLists.txt")

        filter_file(
            r"find_library\(RDMACM_LIB rdmacm\)\n"
            r"find_library\(IBVERBS_LIB ibverbs\)\n"
            r'message\(STATUS "RDMA support enabled: rdmacm=\$\{RDMACM_LIB\} '
            r'ibverbs=\$\{IBVERBS_LIB\}"\)\n'
            r"add_compile_definitions\(HAS_RDMA\)\n"
            r"set\(RDMA_LIBS \$\{RDMACM_LIB\} \$\{IBVERBS_LIB\}\)",
            'message(STATUS "RDMA support disabled by Spack package")\n'
            "set(RDMA_LIBS)\n"
            "find_library(RT_LIB rt)\n"
            'if(NOT RT_LIB)\n'
            '    set(RT_LIB "")\n'
            "endif()",
            cmake_file,
            string=False,
        )
        filter_file(
            "spdlog::spdlog_header_only rt ${RDMA_LIBS}",
            "spdlog::spdlog_header_only ${RT_LIB} ${RDMA_LIBS}",
            cmake_file,
        )
        filter_file(
            "spdlog::spdlog_header_only rt)",
            "spdlog::spdlog_header_only ${RT_LIB})",
            cmake_file,
        )

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.set("CXLMEMSIM_HOME", self.prefix)
        env.set("CXL_QEMU_IMAGE_DIR", self.prefix.share.cxlmemsim.images)
        env.set("CXL_MEMSIM_HOST", "127.0.0.1")
        env.set("CXL_MEMSIM_PORT", "9999")

    def _install_runtime_files(self, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.share.cxlmemsim)
        mkdirp(prefix.share.cxlmemsim.images)

        integration_dir = join_path(self.stage.source_path, "qemu_integration")
        if os.path.isdir(integration_dir):
            install_tree(integration_dir, prefix.share.cxlmemsim.qemu_integration)

        launch0 = self._launcher_script(
            prefix,
            host_id=0,
            disk="qemu.img",
            tap="tap0",
            mac="52:54:00:00:00:01",
            lsa="lsa0.raw",
        )
        launch1 = self._launcher_script(
            prefix,
            host_id=1,
            disk="qemu1.img",
            tap="tap1",
            mac="52:54:00:00:00:02",
            lsa="lsa1.raw",
        )
        download = self._download_script(prefix)

        for directory in (prefix.bin, prefix.share.cxlmemsim):
            self._write_executable(join_path(directory, "qemu_launch_cxl.sh"), launch0)
            self._write_executable(join_path(directory, "qemu_launch_cxl1.sh"), launch1)
            self._write_executable(join_path(directory, "download_trimmed_qemu_image.sh"), download)

        self._write_executable(join_path(prefix.bin, "cxlmemsim-download-qemu-image"), download)

    def _write_executable(self, path, contents):
        path = str(path)
        mkdirp(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as script:
            script.write(contents)
        os.chmod(path, 0o755)

    def _download_script(self, prefix):
        return """#!/usr/bin/env bash
set -euo pipefail

PREFIX="{prefix}"
IMAGE_DIR="${{1:-${{CXL_QEMU_IMAGE_DIR:-${{PREFIX}}/share/cxlmemsim/images}}}}"
QEMU_IMAGE_URL="${{CXL_QEMU_IMAGE_URL:-https://asplos.dev/about/qemu.img}}"
BZIMAGE_URL="${{CXL_BZIMAGE_URL:-https://asplos.dev/about/bzImage}}"

mkdir -p "${{IMAGE_DIR}}"

download() {{
    local url="$1"
    local output="$2"
    if [[ -s "${{output}}" ]]; then
        echo "Using existing ${{output}}"
        return
    fi

    if command -v curl >/dev/null 2>&1; then
        curl -L --fail --progress-bar "$url" -o "${{output}}"
    elif command -v wget >/dev/null 2>&1; then
        wget -O "${{output}}" "$url"
    else
        echo "error: curl or wget is required to download VM images" >&2
        exit 1
    fi
}}

download "${{QEMU_IMAGE_URL}}" "${{IMAGE_DIR}}/qemu.img"
download "${{BZIMAGE_URL}}" "${{IMAGE_DIR}}/bzImage"

if [[ ! -e "${{IMAGE_DIR}}/qemu1.img" ]]; then
    cp "${{IMAGE_DIR}}/qemu.img" "${{IMAGE_DIR}}/qemu1.img"
fi

echo "QEMU image directory: ${{IMAGE_DIR}}"
""".format(prefix=prefix)

    def _launcher_script(self, prefix, host_id, disk, tap, mac, lsa):
        rosetta_default = "1" if self.spec.satisfies("+rosetta platform=darwin") else "0"
        accel_default = "tcg"
        if self.spec.satisfies("+hvf platform=darwin") and "+rosetta" not in self.spec:
            accel_default = "hvf"
        cpu_default = "max" if self.spec.satisfies("platform=darwin") and accel_default == "tcg" else "host"
        return """#!/usr/bin/env bash
set -euo pipefail

PREFIX="{prefix}"
QEMU_BINARY="${{QEMU_BINARY:-${{PREFIX}}/bin/qemu-system-x86_64}}"
IMAGE_DIR="${{CXL_QEMU_IMAGE_DIR:-${{PREFIX}}/share/cxlmemsim/images}}"
KERNEL_IMAGE="${{KERNEL_IMAGE:-${{IMAGE_DIR}}/bzImage}}"
DISK_IMAGE="${{DISK_IMAGE:-${{IMAGE_DIR}}/{disk}}}"
DISK_FORMAT="${{DISK_FORMAT:-raw}}"
VM_MEMORY="${{VM_MEMORY:-16G}}"
VM_MAX_MEMORY="${{VM_MAX_MEMORY:-32G}}"
VM_MEM_SLOTS="${{VM_MEM_SLOTS:-8}}"
VM_SMP="${{VM_SMP:-4}}"
TAP_IFACE="${{TAP_IFACE:-{tap}}}"
MAC_ADDR="${{MAC_ADDR:-{mac}}}"
DEFAULT_HOST_SHM_DIR="/dev/shm"
if [[ "$(uname -s)" == "Darwin" ]]; then
    DEFAULT_HOST_SHM_DIR="${{TMPDIR:-/tmp}}/cxlmemsim"
fi
HOST_SHM_DIR="${{HOST_SHM_DIR:-${{DEFAULT_HOST_SHM_DIR}}}}"
CXL_MEM_PATH="${{CXL_MEM_PATH:-${{HOST_SHM_DIR}}/cxlmemsim_shared}}"
CXL_LSA_PATH="${{CXL_LSA_PATH:-${{HOST_SHM_DIR}}/{lsa}}}"
CXL_MEM_SIZE="${{CXL_MEM_SIZE:-1G}}"
CXL_FMW_SIZE="${{CXL_FMW_SIZE:-4G}}"
CXL_TRANSPORT_MODE="${{CXL_TRANSPORT_MODE:-shm}}"
CXL_HOST_ID="${{CXL_HOST_ID:-{host_id}}}"
CXL_MEMSIM_HOST="${{CXL_MEMSIM_HOST:-127.0.0.1}}"
CXL_MEMSIM_PORT="${{CXL_MEMSIM_PORT:-9999}}"
CXL_PGAS_SHM="${{CXL_PGAS_SHM:-/cxlmemsim_pgas}}"
CXL_MEMSIM_SERVER_MODE="${{CXL_MEMSIM_SERVER_MODE:-}}"
if [[ -z "${{CXL_MEMSIM_SERVER_MODE}}" ]]; then
    if [[ "${{CXL_TRANSPORT_MODE}}" == "shm" || "${{CXL_TRANSPORT_MODE}}" == "pgas" ]]; then
        CXL_MEMSIM_SERVER_MODE="pgas-shm"
    else
        CXL_MEMSIM_SERVER_MODE="${{CXL_TRANSPORT_MODE}}"
    fi
fi
CXL_MEMSIM_SERVER_AUTOSTART="${{CXL_MEMSIM_SERVER_AUTOSTART:-auto}}"
CXL_MEMSIM_SERVER_BINARY="${{CXL_MEMSIM_SERVER_BINARY:-${{PREFIX}}/bin/cxlmemsim_server}}"
CXL_MEMSIM_SERVER_LOG="${{CXL_MEMSIM_SERVER_LOG:-${{HOST_SHM_DIR}}/cxlmemsim_server_${{CXL_HOST_ID}}.log}}"
CXL_MEMSIM_SERVER_PID="${{CXL_MEMSIM_SERVER_PID:-${{HOST_SHM_DIR}}/cxlmemsim_server_${{CXL_HOST_ID}}.pid}}"
CXL_MEMSIM_TOPOLOGY="${{CXL_MEMSIM_TOPOLOGY:-${{PREFIX}}/share/cxlmemsim/qemu_integration/topology_simple.txt}}"
mkdir -p "${{HOST_SHM_DIR}}"

export CXL_TRANSPORT_MODE
export CXL_HOST_ID
export CXL_MEMSIM_HOST
export CXL_MEMSIM_PORT
export CXL_PGAS_SHM

size_to_mb() {{
    local value="$1"
    case "${{value}}" in
        *[Gg][Ii][Bb]) echo "$(( ${{value%[Gg][Ii][Bb]}} * 1024 ))" ;;
        *[Gg]) echo "$(( ${{value%[Gg]}} * 1024 ))" ;;
        *[Mm][Ii][Bb]) echo "${{value%[Mm][Ii][Bb]}}" ;;
        *[Mm]) echo "${{value%[Mm]}}" ;;
        *) echo "$(( value / 1024 / 1024 ))" ;;
    esac
}}

tcp_port_open() {{
    local probe_host="${{CXL_MEMSIM_HOST}}"
    if [[ "${{probe_host}}" == "0.0.0.0" ]]; then
        probe_host="127.0.0.1"
    fi
    (echo >"/dev/tcp/${{probe_host}}/${{CXL_MEMSIM_PORT}}") >/dev/null 2>&1
}}

start_cxlmemsim_server() {{
    case "${{CXL_MEMSIM_SERVER_AUTOSTART}}" in
        0|false|False|no|No|off|Off)
            return 0
            ;;
    esac

    if [[ ! -x "${{CXL_MEMSIM_SERVER_BINARY}}" ]]; then
        if [[ "${{CXL_TRANSPORT_MODE}}" == "tcp" || "${{CXL_MEMSIM_SERVER_AUTOSTART}}" == "1" || "${{CXL_MEMSIM_SERVER_AUTOSTART}}" == "true" || "${{CXL_MEMSIM_SERVER_AUTOSTART}}" == "True" ]]; then
            echo "error: cxlmemsim_server not found at ${{CXL_MEMSIM_SERVER_BINARY}}" >&2
            echo "Set CXL_MEMSIM_SERVER_BINARY or install a non-tools-only CXLMemSim server build." >&2
            exit 1
        fi

        echo "warning: cxlmemsim_server not found at ${{CXL_MEMSIM_SERVER_BINARY}}; continuing without host server" >&2
        return 0
    fi

    if [[ -s "${{CXL_MEMSIM_SERVER_PID}}" ]] && kill -0 "$(cat "${{CXL_MEMSIM_SERVER_PID}}")" >/dev/null 2>&1; then
        echo "Using existing cxlmemsim_server pid $(cat "${{CXL_MEMSIM_SERVER_PID}}")"
        return 0
    fi

    local server_mode="${{CXL_MEMSIM_SERVER_MODE}}"
    if [[ "${{server_mode}}" == "pgas" ]]; then
        server_mode="pgas-shm"
    fi

    case "${{server_mode}}" in
        shm|tcp|pgas-shm|distributed) ;;
        *)
            echo "warning: unsupported CXL_MEMSIM_SERVER_MODE=${{server_mode}}; using pgas-shm" >&2
            server_mode="pgas-shm"
            ;;
    esac

    local capacity_mb
    capacity_mb="$(size_to_mb "${{CXL_MEM_SIZE}}")"

    local server_args=(
        "--comm-mode" "${{server_mode}}"
        "--capacity" "${{capacity_mb}}"
        "--port" "${{CXL_MEMSIM_PORT}}"
        "--topology" "${{CXL_MEMSIM_TOPOLOGY}}"
        "--backing-file" "${{CXL_MEM_PATH}}"
    )

    if [[ "${{server_mode}}" == "tcp" ]]; then
        server_args+=("--tcp-addr" "${{CXL_MEMSIM_HOST}}" "--tcp-port" "${{CXL_MEMSIM_PORT}}")
    elif [[ "${{server_mode}}" == "pgas-shm" ]]; then
        server_args+=("--pgas-shm-name" "${{CXL_PGAS_SHM}}")
    fi

    local server_endpoint="${{CXL_MEMSIM_HOST}}:${{CXL_MEMSIM_PORT}}"
    if [[ "${{server_mode}}" == "pgas-shm" ]]; then
        server_endpoint="${{CXL_PGAS_SHM}}"
    fi
    echo "Starting cxlmemsim_server (${{server_mode}}) on ${{server_endpoint}}"
    nohup "${{CXL_MEMSIM_SERVER_BINARY}}" "${{server_args[@]}}" >"${{CXL_MEMSIM_SERVER_LOG}}" 2>&1 &
    echo "$!" >"${{CXL_MEMSIM_SERVER_PID}}"

    if [[ "${{server_mode}}" == "tcp" ]]; then
        for _ in 1 2 3 4 5 6 7 8 9 10; do
            if tcp_port_open; then
                return 0
            fi
            sleep 0.5
        done
        echo "error: cxlmemsim_server did not open ${{CXL_MEMSIM_HOST}}:${{CXL_MEMSIM_PORT}}" >&2
        echo "See ${{CXL_MEMSIM_SERVER_LOG}}" >&2
        exit 1
    fi

    sleep 0.5
    if ! kill -0 "$(cat "${{CXL_MEMSIM_SERVER_PID}}")" >/dev/null 2>&1; then
        echo "error: cxlmemsim_server exited during startup" >&2
        echo "See ${{CXL_MEMSIM_SERVER_LOG}}" >&2
        exit 1
    fi
}}

start_cxlmemsim_server

qemu_cmd=("${{QEMU_BINARY}}")
accel_args=()
network_args=()
if [[ "$(uname -s)" == "Darwin" ]]; then
    if [[ "${{QEMU_USE_ROSETTA:-{rosetta_default}}}" == "1" ]]; then
        qemu_cmd=(arch -x86_64 "${{QEMU_BINARY}}")
    fi
    accel_args=("-accel" "${{QEMU_ACCEL:-{accel_default}}}")
    if [[ "${{QEMU_NET:-none}}" == "user" ]]; then
        network_args=("-netdev" "user,id=net0" "-device" "virtio-net-pci,netdev=net0,mac=${{MAC_ADDR}}")
    elif [[ "${{QEMU_NET:-none}}" == "none" ]]; then
        network_args=("-nic" "none")
    elif [[ "${{QEMU_NET:-none}}" != "none" ]]; then
        echo "error: unsupported Darwin QEMU_NET=${{QEMU_NET}}" >&2
        exit 1
    fi
else
    accel_args=("${{QEMU_ACCEL_ARG:---enable-kvm}}")
    network_args=("-netdev" "tap,id=net0,ifname=${{TAP_IFACE}},script=no,downscript=no")
    network_args+=("-device" "virtio-net-pci,netdev=net0,mac=${{MAC_ADDR}}")
fi

qemu_args=(
    "${{accel_args[@]}}"
    "-cpu" "${{QEMU_CPU:-{cpu_default}}}"
    "-m" "${{VM_MEMORY}},maxmem=${{VM_MAX_MEMORY}},slots=${{VM_MEM_SLOTS}}"
    "-smp" "${{VM_SMP}}"
    "-M" "q35,cxl=on"
    "-kernel" "${{KERNEL_IMAGE}}"
    "-append" "${{KERNEL_APPEND:-root=/dev/sda rw console=ttyS0,115200 nokaslr}}"
    "-drive" "file=${{DISK_IMAGE}},index=0,media=disk,format=${{DISK_FORMAT}}"
    "${{network_args[@]}}"
    "-fsdev" "local,security_model=none,id=fsdev0,path=${{HOST_SHM_DIR}}"
    "-device" "virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag=hostshm,bus=pcie.0"
    "-device" "pxb-cxl,bus_nr=12,bus=pcie.0,id=cxl.1"
    "-device" "cxl-rp,port=0,bus=cxl.1,id=root_port13,chassis=0,slot=0"
    "-device" "cxl-rp,port=1,bus=cxl.1,id=root_port14,chassis=0,slot=1"
    "-device" "cxl-type3,bus=root_port13,persistent-memdev=cxl-mem1,lsa=cxl-lsa1,id=cxl-pmem0,sn=0x1"
    "-device" "cxl-type1,bus=root_port14,size=1G,cache-size=64M"
    "-device" "virtio-cxl-accel-pci,bus=pcie.0"
    "-object" "memory-backend-file,id=cxl-mem1,share=on,mem-path=${{CXL_MEM_PATH}},size=${{CXL_MEM_SIZE}}"
    "-object" "memory-backend-file,id=cxl-lsa1,share=on,mem-path=${{CXL_LSA_PATH}},size=1G"
    "-M" "cxl-fmw.0.targets.0=cxl.1,cxl-fmw.0.size=${{CXL_FMW_SIZE}}"
)

if [[ "${{QEMU_NOGRAPHIC:-1}}" == "1" ]]; then
    qemu_args+=("-nographic")
fi

if [[ -n "${{VFIO_GPU_PCI:-}}" ]]; then
    qemu_args+=(
        "-device"
        "vfio-pci,host=${{VFIO_GPU_PCI}},bus=pcie.0,id=gpu0,x-pci-vendor-id=${{VFIO_GPU_VENDOR_ID:-0x10de}}"
    )
fi

exec "${{qemu_cmd[@]}}" "${{qemu_args[@]}}"
""".format(
            prefix=prefix,
            host_id=host_id,
            disk=disk,
            tap=tap,
            mac=mac,
            lsa=lsa,
            rosetta_default=rosetta_default,
            accel_default=accel_default,
            cpu_default=cpu_default,
        )
