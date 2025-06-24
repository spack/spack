from spack.package import *

class {{ cls_name }}(PackageBase):
    homepage = "http://www.example.com"
    url = "http://www.example.com/root-1.0.tar.gz"

    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = "Package"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "generic"

    build_system("generic")

    version("3.0", sha256='abcde')
    version("2.0", sha256='abcde')
    version("1.0", sha256='abcde')

{% for dep_spec, dep_type, condition in dependencies %}
{% if dep_type and condition %}
    depends_on("{{ dep_spec }}", type="{{ dep_type }}", when="{{ condition }}")
{% elif dep_type %}
    depends_on("{{ dep_spec }}", type="{{ dep_type }}")
{% elif condition %}
    depends_on("{{ dep_spec }}", when="{{ condition }}")
{% else %}
    depends_on("{{ dep_spec }}")
{% endif %}
{% endfor %}


@register_builder("generic")
class GenericBuilder(Builder):
    """A generic builder for a mocked package.
    """

    #: A generic package has only the "install" phase
    phases = ("install",)

    def install(
        self, pkg: {{ cls_name }}, spec: Spec, prefix: Prefix
    ) -> None:
        """Noop install"""
        pass
