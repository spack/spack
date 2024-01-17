FROM alpine as prep
RUN apk add python3 git file gnupg patchelf make patch bash xz clingo py3-clingo py3-cffi
ENV PATH=/spack/profile/.spack-env/view/bin:/spack/base/.spack-env/view/bin:/spack/bin:/usr/bin:/usr/sbin:/bin:/sbin
RUN --mount=type=bind,target=/source,readonly,source=. \
  git clone file:///source /spack ; \
  mkdir -p /spack/base ; \
  cd /spack ; git checkout bootstrap-test ; \
  cp -r /source/bootstraps/stage4/spack.* /spack/base ; \
  sed -i.orig -e 's|bootstraps/stage3|base|' /spack/base/spack.yaml ; \
  python3 /spack/bin/spack mirror add source file:///source/spack-cache ; \
  python3 /spack/bin/spack bootstrap disable github-actions-v0.4 ; \
  python3 /spack/bin/spack bootstrap disable github-actions-v0.5 ; \
  python3 /spack/bin/spack -e /spack/base install --use-buildcache only --no-check-signature

FROM scratch as spackos
COPY --from=prep /spack /spack/
ENV PATH=/spack/profile/.spack-env/view/bin:/spack/base/.spack-env/view/bin:/spack/bin:/usr/bin:/usr/sbin:/bin:/sbin
# must use exec mode commands until /bin/sh exists
RUN [ "mkdir", "-p", "/usr", "/bin", "/tmp", "/etc"]
RUN [ "ln", "-s", "/spack/base/.spack-env/view/bin/bash", "/bin/sh"]
RUN [ "ln", "-s", "/spack/base/.spack-env/view/bin/bash", "/bin/bash"]
RUN ln -s /bin /usr/bin ; \
    ln -s /spack/base/.spack-env/view/bin/env /bin/env
RUN echo "root:x:0:0:root:/root:/usr/bin/bash" > /etc/passwd
RUN echo "root:*:17937:0:99999:7:::" > /etc/shadow
ENV SPACKOS_VERSION=0

CMD bash
