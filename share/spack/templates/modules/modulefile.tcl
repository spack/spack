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

{% block variants %}
{% if variants|length > 0 %}
proc variant_set_spec {name is_bool} {
    set value [getvariant --return-value $name __undef__]
    if {$value eq {__undef__} || [module-info mode scan]} {
       return
    }
    if {!$is_bool} {
        lappend ::variant_spec_list $name=$value
    } elseif {$value} {
        lappend ::variant_spec_list +$name
    } else {
        lappend ::variant_spec_list ~$name
    }
}

{# Define variants and their values instanciated in actual installations #}
{# Build along the definition the variant set specified when loading module #}
set variant_spec_list [list]
{% for name, v in variants.items() %}
{% if v['type'] == 'bool' %}
variant --boolean --default {{ v['value'] }} {{ name }}
variant_set_spec {{ name }} 1
{% else %}
variant --default {{ v['value'] }} {{ name }} {{ v['value'] }}
variant_set_spec {{ name }} 0
{% endif %}
{% endfor %}

array set avail_installation [list\
    {{ '{' }}{{ variants_spec }}{{ '}' }} {{ hash }}\
]

proc select_installation {spec} {
    if {[info exists ::avail_installation($spec)]} {
        return $::avail_installation($spec)
    }
    # raise error if selected set does not correspond to an installed package
    set err_msg "Specified package is not installed, available packages for this version are:\n"
    foreach avail_spec [array names ::avail_installation] {
        append err_msg "* \"$avail_spec\"\n"
    }
    reportError $err_msg
    break
}

set selected_installation [select_installation [join $variant_spec_list]]
{% endif %}
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
