{% extends "modules/modulefile.lua" %}
{% block footer %}
-- Access is granted only to specific groups, most likely because the software is licensed
if not isDir("{{ spec.prefix }}") then
    LmodError (
        "You don't have the necessary rights to run \"{{ spec.name }}\".\n\n",
        "\tPlease write an e-mail to 1234@epfl.ch if you need further information on how to get access to it.\n"
    )
end
{% endblock %}
