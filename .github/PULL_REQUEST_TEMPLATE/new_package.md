---
name: Deploy a new package/module
about: Deploy a new package as a module on BB5

---

# Checklist for new modules

For software developped by BBP:

* [ ] `package@version` has been added into `deploy/packages/bbp-packages.yaml`
* [ ] `package` has been whitelisted in `deploy/configs/applications/modules.yaml`

Otherwise, adjust the mentioned directories accordingly.

_Note:_ PRs can be tested on BB5:

    $ . /gpfs/bbp.cscs.ch/apps/hpc/jenkins/pulls/<MY_PULL_REQUEST>/config/modules.sh
    $ module load my_new_module
