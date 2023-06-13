#%Module1.0
## Module file created by spack (https://github.com/spack/spack) on {{ timestamp }}
##
## {{ spec.short_spec }}
##
{% if configure_options %}
## Configure options: {{ configure_options }}
##
{% endif %}


{% block header %}
{% if short_description %}
module-whatis "{{ short_description }}"
{% endif %}

proc ModulesHelp { } {
    puts stderr "Name   : {{ spec.name }}"
    puts stderr "Version: {{ spec.version }}"
    puts stderr "Target : {{ spec.target }}"
{% if long_description %}
    puts stderr ""
{{ long_description| textwrap(72)| quote()| prepend_to_line('    puts stderr ')| join() }}
{% endif %}
}
{% endblock %}

{% block autoloads %}
{% for module in autoload %}
module load {{ module }}
{% endfor %}
{% endblock %}
{#  #}
{% block prerequisite %}
{% for module in prerequisites %}
prereq {{ module }}
{% endfor %}
{% endblock %}
{#  #}
{% block conflict %}
{% for name in conflicts %}
conflict {{ name }}
{% endfor %}
{% endblock %}

{% block environment %}
{% for command_name, cmd in environment_modifications %}
{% if command_name == 'PrependPath' %}
prepend-path --delim "{{ cmd.separator }}" {{ cmd.name }} "{{ cmd.value }}"
{% elif command_name in ('AppendPath', 'AppendFlagsEnv') %}
append-path --delim "{{ cmd.separator }}" {{ cmd.name }} "{{ cmd.value }}"
{% elif command_name in ('RemovePath', 'RemoveFlagsEnv') %}
remove-path --delim "{{ cmd.separator }}" {{ cmd.name }} "{{ cmd.value }}"
{% elif command_name == 'SetEnv' %}
setenv {{ cmd.name }} "{{ cmd.value }}"
{% elif command_name == 'UnsetEnv' %}
unsetenv {{ cmd.name }}
{% endif %}
{#  #}
{% endfor %}
{# Make sure system man pages are enabled by appending trailing delimiter to MANPATH #}
{% if has_manpath_modifications %}
append-path --delim ":" MANPATH ""
{% endif %}
{% endblock %}

{% block footer %}
{# In case the module needs to be extended with custom Tcl code #}
{% endblock %}
