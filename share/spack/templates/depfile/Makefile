SPACK ?= spack

.PHONY: {{ all_target }} {{ clean_target }}

{{ all_target }}: {{ env_target }}

{{ env_target }}: {{ root_install_targets }}
	@touch $@

{{ dirs_target }}:
	@mkdir -p {{ install_target }} {{ install_deps_target }}

# The spack install commands are of the form:
# spack -e my_env --no-add --only=package --only=concrete /hash
# This is an involved way of expressing that Spack should only install
# an individual concrete spec from the environment without deps.
{{ install_target }}/%: {{ install_deps_target }}/% | {{ dirs_target }}
	$(info Installing $(SPEC))
	{{ jobserver_support }}$(SPACK) -e '{{ environment }}' install $(SPACK_INSTALL_FLAGS) --only-concrete --only=package --no-add /$(notdir $@)
	@touch $@

# Targets of the form {{ install_deps_target }}/<hash> install dependencies only
{{ install_deps_target }}/%: | {{ dirs_target }}
	@touch $@

# Set a human-readable SPEC variable for each target that has a hash
{% for (hash, name) in hash_with_name -%} 
{{ any_hash_target }}/{{ hash }}: SPEC = {{ name }}
{% endfor %}

# The Spack DAG expressed in targets:
{% for (target, prereqs) in targets_to_prereqs -%}
{{ target }}: {{prereqs}}
{% endfor %}

{{ clean_target }}:
	rm -rf {{ env_target }} {{ all_install_targets }} {{ all_install_deps_targets }}
