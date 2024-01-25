# Make sure user config is not picked up.
export SPACK_USER_CONFIG_PATH=$(CURDIR)/.spack
export SPACK_USER_CACHE_PATH=$(CURDIR)/.spack
export PATH:=$(CURDIR)/stage1/.spack-env/view/bin:$(PATH)

.SUFFIXES:

.PHONY: all clean %/cleanstage %push container

all: stage4/generated/env
stage4/push: stage4/generated/env
	mkdir -p buildcache
	spack -e stage4 buildcache push --unsigned --update-index ./buildcache
push: stage4/push
container: stage4/push
	docker buildx build -t spackos-experimental --load -f Dockerfile --target=spackos ../../..

TGT_FILES:=spack.mk spack.lock compilers.yaml generated .spack-env spack.yaml
STAGES:=1 2 3 4
clean: stage1/cleanstage stage2/cleanstage stage3/cleanstage stage4/cleanstage
	rm -rf buildcache

%/cleanstage:
	for file in $(TGT_FILES) ; do\
					rm -rf $(STAGE)/$${file} ; \
	done

SPACK=SPACK_USER_CONFIG_PATH=$(STAGE) spack
stage1/%: STAGE=stage1
stage2/%: STAGE=stage2
stage3/%: STAGE=stage3
stage4/%: STAGE=stage4
stage1/%: STAGENUM=1
stage2/%: STAGENUM=2
stage3/%: STAGENUM=3
stage4/%: STAGENUM=4
stage2/%: PREV=stage1
stage3/%: PREV=stage2
stage4/%: PREV=stage3

stage1/%: ENV=
stage2/%: ENV=SPACKOS_VERSION=0
stage3/%: ENV=SPACKOS_VERSION=0
stage4/%: ENV=SPACKOS_VERSION=0

stage2/compilers.yaml: stage1/generated/env
stage3/compilers.yaml: stage2/generated/env
stage4/compilers.yaml: stage3/generated/env
stage2/spack.yaml: stage1/generated/env
stage3/spack.yaml: stage2/generated/env
stage4/spack.yaml: stage3/generated/env

HOST_COMPILER_PATH=
%/compilers.yaml:
	# was what follows, but then need path modifications, now using compiler path addition to get bison and gawk $$(spack -e $(PREV) find --format '{prefix}' gcc)
	echo $(CURDIR)/$(PREV)/.spack-env/view/bin
	[ "$(STAGE)" = "stage1" ] || env $(ENV) $(SPACK) compiler find --scope=user $(CURDIR)/$(PREV)/.spack-env/view/bin
	# [ "$(STAGE)" = "stage1" ] || sed -i'' -e '/spec:/s/\(@=.*\)/\1.$(PREV)/' $(STAGE)/compilers.yaml
	env $(ENV) $(SPACK) compiler find --scope=user $(HOST_COMPILER_PATH)

%/spack.yaml: %/spack.in.yaml
	if [ $(STAGENUM) -lt 3 ] ; then \
				cp -f $< $@ ; \
	else \
				sed -e "s|@GLIBC_HASH@|$$(SPACKOS_VERSION=0 spack -e stage2 find -H glibc)|" $< > $@ ; \
	fi

.PRECIOUS: %/spack.yaml %/spack.lock %/compilers.yaml
%/spack.lock: %/spack.yaml %/compilers.yaml
	env $(ENV) spack -e $(STAGE) concretize --force

%/spack.mk: %/spack.lock
	env $(ENV) spack -e $(STAGE) env depfile --make-target-prefix $(STAGE)/generated -o $@


ifeq (,$(filter clean,$(MAKECMDGOALS)))
include stage1/spack.mk
ifneq (,$(wildcard stage1/spack.mk))
include stage2/spack.mk
ifneq (,$(wildcard stage2/spack.mk))
include stage3/spack.mk
ifneq (,$(wildcard stage3/spack.mk))
include stage4/spack.mk
endif
endif
endif
endif
