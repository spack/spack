#%Module1.0
## Module file created by spack (https://github.com/spack/spack) on {{ timestamp }}
##
## {{ spec.short_spec }}
##
{% if configure_options %}
## Configure options: {{ configure_options | wordwrap(8192 - 23, True, "\n##                    ", 0) }}
##
{% endif %}


{% block header %}
{% if short_description %}
module-whatis {{ '{' }}{{ short_description }}{{ '}' }}
{% endif %}

proc ModulesHelp { } {
    puts stderr {{ '{' }}Name   : {{ spec.name }}{{ '}' }}
    puts stderr {{ '{' }}Version: {{ spec.version }}{{ '}' }}
    puts stderr {{ '{' }}Target : {{ spec.target }}{{ '}' }}
{% if long_description %}
    puts stderr {}
{{ long_description| textwrap(72)| curly_quote()| prepend_to_line('    puts stderr ')| join() }}
{% endif %}
}
{% endblock %}

{% block provides %}
{# Prepend the path I unlock as a provider of #}
{# services and set the families of services I provide #}
{% if has_modulepath_modifications %}
# Services provided by the package
{% for name in provides %}
family {{ name }}
{% endfor %}

# Loading this module unlocks the path below unconditionally
{% for path in unlocked_paths %}
prepend-path MODULEPATH {{ '{' }}{{ path }}{{ '}' }}
{% endfor %}

{# Try to see if missing providers have already #}
{# been loaded into the environment #}
{% if has_conditional_modifications %}
# Try to load variables into path to see if providers are there
{% for name in missing %}
set {{ name }}_name [getenv MODULES_{{ name|upper() }}_NAME]
set {{ name }}_version [getenv MODULES_{{ name|upper() }}_VERSION]
{% endfor %}

# Change MODULEPATH based on the result of the tests above
{% for condition, path in conditionally_unlocked_paths %}
if { {{ condition }} } {
    prepend-path MODULEPATH [file join {{ path }}]
}
{% endfor %}

# Set variables to notify the provider of the new services
{% for name in provides %}
setenv MODULES_{{ name|upper() }}_NAME {{ '{' }}{{ name_part }}{{ '}' }}
setenv MODULES_{{ name|upper() }}_VERSION {{ '{' }}{{ version_part }}{{ '}' }}
{% endfor %}
{% endif %}
{% endif %}
{% endblock %}

{% block autoloads %}
{% if autoload|length > 0 %}
# define missing command if using Environment Modules <5.1
if {![llength [info commands depends-on]]} {
    proc depends-on {args} {
        module load {*}$args
    }
}
{% for module in autoload %}
depends-on {{ module }}
{% endfor %}
{% endif %}
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
prepend-path -d {{ '{' }}{{ cmd.separator }}{{ '}' }} {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% elif command_name in ('AppendPath', 'AppendFlagsEnv') %}
append-path -d {{ '{' }}{{ cmd.separator }}{{ '}' }} {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% elif command_name in ('RemovePath', 'RemoveFlagsEnv') %}
remove-path -d {{ '{' }}{{ cmd.separator }}{{ '}' }} {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% elif command_name == 'SetEnv' %}
setenv {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% elif command_name == 'UnsetEnv' %}
unsetenv {{ cmd.name }}
{% endif %}
{#  #}
{% endfor %}
{# Make sure system man pages are enabled by appending trailing delimiter to MANPATH #}
{% if has_manpath_modifications %}
append-path MANPATH {{ '{' }}{{ '}' }}
{% endif %}
{% endblock %}

{% block footer %}
{# In case the module needs to be extended with custom Tcl code #}
{% endblock %}
