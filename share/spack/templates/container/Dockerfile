{% if render_phase.bootstrap %}
{{ bootstrap.recipe }}
{% endif %}

{% if render_phase.build %}
# Build stage with Spack pre-installed and ready to be used
FROM {{ build.image }} as builder

{% block build_stage %}

{% if os_packages_build %}
# Install OS packages needed to build the software
RUN {% if os_package_update %}{{ os_packages_build.update }} \
 && {% endif %}{{ os_packages_build.install }} {{ os_packages_build.list | join | replace('\n', ' ') }} \
 && {{ os_packages_build.clean }}
{% endif %}

{% block make_manifest %}
# What we want to install and how we want to install it
# is specified in a manifest file (spack.yaml)
RUN mkdir {{ paths.environment }} \
{{ manifest }} > {{ paths.environment }}/spack.yaml
{% endblock make_manifest %}

{% block install_software %}
# Install the software, remove unnecessary deps
{% if depfile %}
RUN cd {{ paths.environment }} && spack env activate . && spack concretize && spack env depfile -o Makefile && make -j $(nproc) && spack gc -y
{% else %}
RUN cd {{ paths.environment }} && spack env activate . && spack install --fail-fast && spack gc -y
{% endif %}
{% endblock install_software %}

{% if strip %}
{% block strip_binaries %}
# Strip all the binaries
RUN find -L {{ paths.view }}/* -type f -exec readlink -f '{}' \; | \
    xargs file -i | \
    grep 'charset=binary' | \
    grep 'x-executable\|x-archive\|x-sharedlib' | \
    awk -F: '{print $1}' | xargs strip
{% endif %}
{% endblock strip_binaries %}

{% block make_activate %}
# Modifications to the environment that are necessary to run
RUN cd {{ paths.environment }} && \
    spack env activate --sh -d . > activate.sh
{% endblock make_activate %}

{% endblock build_stage %}
{% endif %}

{% if render_phase.final %}
# Bare OS image to run the installed executables
FROM {{ run.image }}

{% block copy_into_final %}
COPY --from=builder {{ paths.environment }} {{ paths.environment }}
COPY --from=builder {{ paths.store }} {{ paths.store }}

# paths.view is a symlink, so copy the parent to avoid dereferencing and duplicating it
COPY --from=builder {{ paths.view_parent }} {{ paths.view_parent }}
{% endblock copy_into_final %}

{% block make_entrypoint %}
RUN { \
      echo '#!/bin/sh' \
      && echo '.' {{ paths.environment }}/activate.sh \
      && echo 'exec "$@"'; \
    } > /entrypoint.sh \
&& chmod a+x /entrypoint.sh \
&& ln -s {{ paths.view }} {{ paths.former_view }}
{% endblock make_entrypoint %}

{% block final_stage %}
{% if os_packages_final %}
RUN {% if os_package_update %}{{ os_packages_final.update }} \
 && {% endif %}{{ os_packages_final.install }} {{ os_packages_final.list | join | replace('\n', ' ') }} \
 && {{ os_packages_final.clean }}
{% endif %}
{% endblock final_stage %}

{% for label, value in labels.items() %}
LABEL "{{ label }}"="{{ value }}"
{% endfor %}

{% block define_entrypoint_cmd %}
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "/bin/bash" ]
{% endblock define_entrypoint_cmd %}
{% endif %}
