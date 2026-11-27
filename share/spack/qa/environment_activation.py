import spack.config
from spack.active_environment import active_environment

KEY = "concretizer:unify"

env = active_environment()
before = spack.config.CONFIG.get(KEY)
with env.write_transaction():
    within = spack.config.CONFIG.get(KEY)
after = spack.config.CONFIG.get(KEY)

if before == within == after:
    print(f"SUCCESS: {before}")
else:
    print(f"FAILURE: {before} -> {within} -> {after}")
