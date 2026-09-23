import spack.config
from spack.active_environment import active_environment

KEY = "concretizer:unify"

before = spack.config.CONFIG.get(KEY)
with active_environment().manifest.use_config():
    within = spack.config.CONFIG.get(KEY)
after = spack.config.CONFIG.get(KEY)

if before == within == after:
    print(f"SUCCESS: {before}")
else:
    print(f"FAILURE: {before} -> {within} -> {after}")
