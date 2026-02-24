import spack.config
import spack.environment

KEY = "concretizer:unify"

before = spack.config.CONFIG.get(KEY)
with spack.environment.active_environment().manifest.use_config():
    within = spack.config.CONFIG.get(KEY)
after = spack.config.CONFIG.get(KEY)

if before == within == after:
    print(f"SUCCESS: {before}")
else:
    print(f"FAILURE: {before} -> {within} -> {after}")
