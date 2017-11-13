# Spack in a Box

## Build

```bash
$ docker build -t qnib/$(basename $(pwd)) .
Sending build context to Docker daemon  54.58MB
Step 1/5 : FROM ubuntu:16.04
 ---> dd6f76d9cc90
Step 2/5 : RUN apt-get update  && apt-get install -y curl gcc python make automake
 ---> Using cache
 ---> ab0af3b042cd
Step 3/5 : COPY . /usr/local/src/spack/
 ---> 13176b1b8ef0
Step 4/5 : COPY docker/entrypoint.sh /usr/local/bin/
 ---> 5e7efbcea916
Step 5/5 : ENTRYPOINT /usr/local/bin/entrypoint.sh
 ---> Running in 19510efa4353
 ---> ef286bac7ca8
Removing intermediate container 19510efa4353
Successfully built ef286bac7ca8
Successfully tagged qnib/spack:latest
$
```

## Run

Interactively starting a container using `bash`.

```bash
$ docker run -ti --rm qnib/spack bash
root@9c3f03585e95:/# spack install zlib
==> Installing zlib
==> Fetching http://zlib.net/fossils/zlib-1.2.11.tar.gz
######################################################################## 100.0%
==> Staging archive: /usr/local/src/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb/zlib-1.2.11.tar.gz
==> Created stage in /usr/local/src/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
==> No patches needed for zlib
==> Building zlib [Package]
==> Executing phase: 'install'
==> Successfully installed zlib
  Fetch: 0.80s.  Build: 3.92s.  Total: 4.71s.
[+] /usr/local/src/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
$
```

Installing into a local directory.

```bash
$ docker run -ti --rm -v ~/spack/:/usr/local/src/spack/opt/spack/ qnib/spack spack install zlib
==> Installing zlib
==> Fetching http://zlib.net/fossils/zlib-1.2.11.tar.gz
######################################################################## 100.0%
==> Staging archive: /usr/local/src/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb/zlib-1.2.11.tar.gz
==> Created stage in /usr/local/src/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
==> No patches needed for zlib
==> Building zlib [Package]
==> Executing phase: 'install'
==> Successfully installed zlib
  Fetch: 1.03s.  Build: 4.06s.  Total: 5.09s.
[+] /usr/local/src/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
$ ls ~/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb/
include lib     share
$
```
