from spack.bootstrap.config import abi_spec_for_current_python, store_path
from typing import Optional
import json
from spack.installer import log
from spack.spec import ArchSpec, Spec, FlagMap
import spack.deptypes as dt
import sys
from spack.store import use_store
import spack.vendor.archspec.cpu as ascpu
import spack.platforms
from spack.bootstrap.config import root_path
import hashlib
import spack.environment
import spack.tengine
from pathlib import Path
from spack.detection import by_path
import spack.environment.shell
import sys
import os
import spack.llnl.util.tty as tty
from spack.spec import Spec, parse_with_version_concrete
import spack.platforms
import spack.binary_distribution
import spack.config
from spack.llnl.util.lang import Singleton
_SPACK_SPACK_ENV_VAR = "SPACK_SPACK_ENV"
def _init_env():
    sse =SpackSpackEnvironment(os.environ.get(_SPACK_SPACK_ENV_VAR, None))
    sse.setup()
    return sse
SPACK_SPACK_ENV = Singleton(_init_env)
_RUNNING_PYTHON_SPEC = None
def detect_running_python_external() -> Spec:
    global _RUNNING_PYTHON_SPEC
    if _RUNNING_PYTHON_SPEC is None:
        tty.debug("Attempting to detect spec for currently executing python interpreter")
        detected = by_path(['python'], path_hints=[sys.exec_prefix])
        if "python" in detected:
            detected_python = detected["python"][0]
            detected_python.external_path = sys.exec_prefix
            detected_python.namespace = "builtin"
            detected_python._set_architecture(
                platform=str(spack.platforms.host()),
                os=str(spack.platforms.host().default_os),
                target=str(ascpu.host().family)
            )
            for flag_type in FlagMap.valid_compiler_flags():
                detected_python.compiler_flags[flag_type] = []
            tty.debug(f"Detected: {detected_python.long_spec}")
            _RUNNING_PYTHON_SPEC = detected_python
        else:
            raise Exception("Detection for current python failed")
    return _RUNNING_PYTHON_SPEC

def refresh_system_path():
    '''
    sys.path is derived at startup, when we edit the venv we reload it
    '''
    import importlib
    importlib.invalidate_caches()
    
def spec_for_current_python_venv() -> Spec:
    if _SPACK_SPACK_ENV_VAR in os.environ:
        venv_spec = SPACK_SPACK_ENV.matching_spec(Spec("python-venv"))
        assert venv_spec is not None
    else:
        venv_spec = Spec("python-venv@=1.0")
        venv_spec.namespace = "builtin"
        venv_spec.architecture = ArchSpec.default_arch()
        venv_spec.add_dependency_edge(
            parse_with_version_concrete(detect_running_python_external()),
            virtuals=(),
            direct=True,
            depflag=(dt.BUILD | dt.RUN)
        )
        for flag_type in FlagMap.valid_compiler_flags():
            venv_spec.compiler_flags[flag_type] = []
        venv_spec._finalize_concretization()
    return venv_spec

def reexec_spack_under_venv():
    tty.info("Attempting to re-execute spack ")
    if _SPACK_SPACK_ENV_VAR not in os.environ:
        new_env = dict(os.environ)
        new_spack_python = SPACK_SPACK_ENV.python_interpreter
        for d in SPACK_SPACK_ENV.view_root.iterdir():
            print(d)
        assert SPACK_SPACK_ENV.python_interpreter.exists(), "interpreter should exist"
        tty.info(f"Setting new spack python to: {new_spack_python}")
        new_env["SPACK_PYTHON"] = str(new_spack_python)
        new_env[_SPACK_SPACK_ENV_VAR] = str(SPACK_SPACK_ENV.env_path)
        os.execvpe(sys.argv[0], sys.argv, env=new_env)
    else:
        tty.info("Already executing under the base environment")
    

def spack_in_env() -> bool:
    return _SPACK_SPACK_ENV_VAR in os.environ

class SpackSpackEnvironment(spack.environment.Environment):
    def __init__(self, env_path = None) -> None:
        self._env_path = Path(env_path) if env_path is not None else None
        self._spack_yaml_path = None
        self._spack_lock_path = None
        self._view_root = None
        self._python_interpreter = None
        if not self.spack_yaml_path.exists():
            self._write_spack_yaml_file()
        super().__init__(self.env_path)
    def setup(self):
        if not self.spack_lock_path.exists():
            with self.write_transaction():
                tty.info("Locking base Spack environment to current python interpreter")
                self.add_concrete_spec(
                    Spec("python-venv"),
                    spec_for_current_python_venv()
                )
                self.install_all()
                self.write(regenerate=True)
    def add_concrete_spec(
            self,
            spec: Spec,
            concrete: Spec,
            *,
            new: bool = True,
            group: Optional[str] = None
    ):
        self.add(spec)
        return super().add_concrete_spec(spec, concrete, new=new, group=group)

                
    @property
    def env_path(self) -> Path:
        if self._env_path is None:
            bootstrap_root = Path(root_path())
            python_part = abi_spec_for_current_python().replace("@", "")
            arch_part = ascpu.host().family
            interpreter_part = hashlib.md5(sys.exec_prefix.encode()).hexdigest()[:5]
            environment_dir = f"venv-{python_part}-{arch_part}-{interpreter_part}"
            self._env_path = Path(bootstrap_root / "environments" / environment_dir)
        return self._env_path
    
    @property
    def spack_yaml_path(self) -> Path:
        if self._spack_yaml_path is None:
            self._spack_yaml_path = self.env_path / "spack.yaml"
        return self._spack_yaml_path
    
    @property
    def spack_lock_path(self) -> Path:
        if self._spack_lock_path is None:
            self._spack_lock_path = self.env_path / "spack.lock"
        return self._spack_lock_path
    
    def _write_spack_yaml_file(self):
        tty.info(f"Creating base Spack environment at: {self.env_path}")
        temp_env = spack.tengine.make_environment()
        template = temp_env.get_template("spack_spack_env/spack.yaml")
        context = {
            "environment_path": self.env_path,
            "python_spec": f"{abi_spec_for_current_python()}+ctypes",
            "python_prefix": sys.exec_prefix
        }
        self.env_path.mkdir(parents=True, exist_ok=True)
        self.spack_yaml_path.write_text(template.render(context), encoding="utf-8")
        
    @property
    def view_root(self) -> Path:
        """Location of the view"""
        if self._view_root is None:
            self._view_root = self.env_path / ".spack-env" / "view"
        return self._view_root

    @property
    def python_interpreter(self) -> Path:
        if self._python_interpreter is None:
            self._python_interpreter = self.view_root / "bin" / "python"
        return self._python_interpreter
    
    def load(self):
        env_mods = spack.environment.shell.activate(self)
        # We don't want this environment to interfere with the user active environment
        env_mods.drop(spack.environment.spack_env_var)
        env_mods.drop(spack.environment.spack_env_view_var)
        if os.environ.get("SPACK_PYTHON", None) != str(self.python_interpreter):
            env_mods.set("SPACK_PYTHON", str(self.python_interpreter))
        refresh_system_path()
        env_mods.apply_modifications()



def _splice_in_python_venv_from_buildcache(pkg_hash: str):
    tty.debug(f'Fetching spec for {pkg_hash}')
    full_candidate_spec = (
        spack.binary_distribution.BINARY_INDEX._known_specs[pkg_hash]
    )
    tty.debug(f'Got {full_candidate_spec.long_spec}')
    return full_candidate_spec.splice(
        spec_for_current_python_venv()
    )

