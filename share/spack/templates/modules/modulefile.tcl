#%Module1.0
## Module file created by spack (https://github.com/spack/spack) on {{ timestamp }}
##
{% if aggregated_variants|length > 0 %}
{% for install in installations %}
## {{ install.spec.short_spec }}
{% endfor %}
{% else %}
## {{ spec.short_spec }}
{% endif %}
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
{% if aggregated_variants|length > 0 %}
# Variants defined across the installations held by this module file, with their possible
# values, then the values of each installation in the order of variant_names, and its hash
set variant_names [list {{ ' '.join(aggregated_variants.keys()) }}]
set boolean_variants [list {% for name, v in aggregated_variants.items() if v['type'] == 'bool' %}{{ name }}{{ ' ' if not loop.last }}{% endfor %}]
array set variant_values [list\
{% for name, v in aggregated_variants.items() %}
    {{ name }} {{ '{' }}{{ ' '.join(v['values']) }}{{ '}' }}\
{% endfor %}
]
set installations [list\
{% for install in installations %}
    {{ '{' }}{{ install.variant_values }}{{ '}' }} {{ install.hash }}\
{% endfor %}
]

proc variants_spec {values} {
    set spec [list]
    foreach name $::variant_names value $values {
        if {$name in $::boolean_variants} {
            lappend spec [expr {$value ? "+$name" : "~$name"}]
        } else {
            lappend spec $name=$value
        }
    }
    return [join $spec]
}

# Variants stated on the command line form a mask, the first installation matching it is
# selected and variants left unset take its values
proc select_installation {} {
    set mask [list]
    foreach name $::variant_names {
        lappend mask [getvariant --return-value $name __unset__]
    }
    foreach {values hash} $::installations {
        set match 1
        foreach value $values requested $mask {
            if {$requested ni [list __unset__ {}] && $requested ne $value} {
                set match 0
                break
            }
        }
        if {$match} {
            return [list $values $hash]
        }
    }
    # raise error if stated variants do not correspond to an installed package
    set err_msg "Specified package is not installed, available packages for this version are:\n"
    foreach {values hash} $::installations {
        append err_msg "* \"[variants_spec $values]\"\n"
    }
    reportError $err_msg
    break
}

# Declare variants without checking their value to get those stated on the command line
foreach name $variant_names {
    variant --default __unset__ $name
}
lassign [select_installation] selected_values selected_installation
foreach name $variant_names value $selected_values {
    if {$name in $boolean_variants} {
        variant --boolean --default $value $name
    } else {
        variant --default $value $name {*}$variant_values($name)
    }
}
{% else %}
set selected_installation {{ hash }}
{% endif %}
{% endblock %}

{% if any_installation_has_autoload %}
# define missing command if using Environment Modules <5.1 or fix it to
# properly handle multi-word specification if using Environment Modules <5.7
if {![info exists ::env(LMOD_VERSION_MAJOR)]} {
    proc depends-on {args} {
        module load {*}$args
    }
}

{% endif %}
{% for install in installations %}
if {$selected_installation eq {{ '{' }}{{ install.hash }}{{ '}' }}} {
{% block provides scoped %}
{# Prepend the path I unlock as a provider of #}
{# services and set the families of services I provide #}
{% if install.has_modulepath_modifications %}
# Services provided by the package
{% for name in install.provides %}
    family {{ name }}
{% endfor %}

# Loading this module unlocks the path below unconditionally
{% for path in install.unlocked_paths %}
    prepend-path MODULEPATH {{ '{' }}{{ path }}{{ '}' }}
{% endfor %}

{# Try to see if missing providers have already #}
{# been loaded into the environment #}
{% if install.has_conditional_modifications %}
# Try to load variables into path to see if providers are there
{% for name in install.missing %}
    set {{ name }}_name [getenv MODULES_{{ name|upper() }}_NAME]
    set {{ name }}_version [getenv MODULES_{{ name|upper() }}_VERSION]
{% endfor %}

# Change MODULEPATH based on the result of the tests above
{% for condition, path in install.conditionally_unlocked_paths %}
    if { {{ condition }} } {
        prepend-path MODULEPATH [file join {{ path }}]
    }
{% endfor %}

# Set variables to notify the provider of the new services
{% for name in install.provides %}
    setenv MODULES_{{ name|upper() }}_NAME {{ '{' }}{{ name_part }}{{ '}' }}
    setenv MODULES_{{ name|upper() }}_VERSION {{ '{' }}{{ version_part }}{{ '}' }}
{% endfor %}

{% endif %}
{% endif %}
{% endblock %}
{#  #}
{% block autoloads scoped %}
{% if install.autoload|length > 0 %}
{% for module in install.autoload %}
    depends-on {{ module }}
{% endfor %}

{% endif %}
{% endblock %}
{#  #}
{% block prerequisite scoped %}
{% if install.prerequisites|length > 0 %}
{% for module in install.prerequisites %}
    prereq {{ module }}
{% endfor %}

{% endif %}
{% endblock %}
{#  #}
{% block conflict scoped %}
{% if install.conflicts|length > 0 %}
{% for name in install.conflicts %}
    conflict {{ name }}
{% endfor %}

{% endif %}
{% endblock %}
{% block environment scoped %}
{% for command_name, cmd in install.environment_modifications %}
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
{% if install.has_manpath_modifications %}
    append-path MANPATH {{ '{' }}{{ '}' }}
{% endif %}
{% endblock %}
}
{% endfor %}

{% block footer %}
{# In case the module needs to be extended with custom Tcl code #}
{% endblock %}
