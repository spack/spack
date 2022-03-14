{% if render_phase.bootstrap %}
{{ bootstrap.recipe }}

{% endif %}
{% if render_phase.build %}
# Build stage with Spack pre-installed and ready to be used
FROM {{ build.image }} as builder

{% if os_packages_build %}
# Install OS packages needed to build the software
RUN {% if os_package_update %}{{ os_packages_build.update }} \
 && {% endif %}{{ os_packages_build.install }} {{ os_packages_build.list | join | replace('\n', ' ') }} \
 && {{ os_packages_build.clean }}
{% endif %}

# What we want to install and how we want to install it
# is specified in a manifest file (spack.yaml)
RUN mkdir {{ paths.environment }} \
{{ manifest }} > {{ paths.environment }}/spack.yaml

# Install the software, remove unnecessary deps
RUN {% if monitor.enabled %}--mount=type=secret,id=su --mount=type=secret,id=st {% endif %}cd {{ paths.environment }} && \
    spack env activate . {% if monitor.enabled %}{% if not monitor.disable_auth %}&& export SPACKMON_USER=$(cat /run/secrets/su) && export SPACKMON_TOKEN=$(cat /run/secrets/st) {% endif %}{% endif %}&& \
    spack install {% if monitor.enabled %}--monitor {% if monitor.prefix %}--monitor-prefix {{ monitor.prefix }} {% endif %}{% if monitor.tags %}--monitor-tags {{ monitor.tags }} {% endif %}{% if monitor.keep_going %}--monitor-keep-going {% endif %}{% if monitor.host %}--monitor-host {{ monitor.host }} {% endif %}{% if monitor.disable_auth %}--monitor-disable-auth {% endif %}{% endif %}--fail-fast && \
    spack gc -y
{% if strip %}

# Strip all the binaries
RUN find -L {{ paths.view }}/* -type f -exec readlink -f '{}' \; | \
    xargs file -i | \
    grep 'charset=binary' | \
    grep 'x-executable\|x-archive\|x-sharedlib' | \
    awk -F: '{print $1}' | xargs strip -s
{% endif %}

# Modifications to the environment that are necessary to run
RUN cd {{ paths.environment }} && \
    spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

{% if extra_instructions.build %}
{{ extra_instructions.build }}
{% endif %}
{% endif %}
{% if render_phase.final %}
# Bare OS image to run the installed executables
FROM {{ run.image }}

COPY --from=builder {{ paths.environment }} {{ paths.environment }}
COPY --from=builder {{ paths.store }} {{ paths.store }}
COPY --from=builder {{ paths.view }} {{ paths.view }}
COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

{% if os_packages_final %}
RUN {% if os_package_update %}{{ os_packages_final.update }} \
 && {% endif %}{{ os_packages_final.install }} {{ os_packages_final.list | join | replace('\n', ' ') }} \
 && {{ os_packages_final.clean }}
{% endif %}
{% if extra_instructions.final %}

{{ extra_instructions.final }}
{% endif %}
{% for label, value in labels.items() %}
LABEL "{{ label }}"="{{ value }}"
{% endfor %}
ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]
{% endif %}
