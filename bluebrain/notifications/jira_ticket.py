"""
Creates a jira ticket, based on a script provided by Luis
You need a personal access token: go to your jira profile and click on Personal Access Tokens
"""
import subprocess
import typing

import click
import requests


def create_generic_jira_body(
    summary: str,
    description: str,
    component_names: typing.List[str],
    project_key: str = "INFRA",
    labels: typing.List[str] = [],
    issue_type: str = "Story",
    epic: typing.Optional[str] = None,
):
    components = [{"name": x} for x in component_names]
    data = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
            "components": components,
            "labels": labels,
        }
    }
    if epic is not None:
        data["fields"]["customfield_10611"] = epic
    return data


def create_jira_ticket_generic(body, token: str, api_url: str):
    """Creates a jira ticket. Raises an HTTPError if the ticket could not be created"""
    body = body
    result = requests.post(
        api_url,
        json=(body),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    print(result)
    print(body)

    try:
        retval = result.json()
        print(f"Created issue {retval['key']}")
    except Exception:
        print("No ticket key returned, here's the raw result conten:")
        print(result.content)

    result.raise_for_status()


@click.command
@click.option(
    "--project",
    default="BSD",
    type=click.Choice(["BSD", "HELP"], case_sensitive=False),
    help="Which JIRA project to file a ticket under",
)
@click.option("--summary", help="What to put in the summary field")
@click.option("--description", help="What to put in the description field")
@click.option(
    "--description-file",
    help=(
        "Path to the file with the contents of what to put in the description field. "
        "If both this and --description are given, --description will be appended."
    ),
)
@click.option(
    "--token",
    envvar="JIRA_TOKEN",
    help="Jira auth token. Can also be specified as JIRA_TOKEN",
)
def file_ticket(project, summary, description, description_file, token):
    """
    File a JIRA ticket in the given project, with the specified summary and description
    """
    print(f"Project: {project}")
    print(f"Summary: {summary}")
    print(f"Description: {description}")
    print(f"Description file: {description_file}")

    api_url: str = "https://bbpteam.epfl.ch/project/issues/rest/api/2/issue/"

    if description and description_file:
        with open(description_file, "r") as fp:
            final_description = fp.read()
        final_description += description
    elif description:
        final_description = description
    elif description_file:
        with open(description_file, "r") as fp:
            final_description = fp.read()

    git_log = subprocess.check_output(["git", "log", "-n", "3", "--color=never"]).decode()
    final_description = final_description.format(git_log=git_log)
    if project == "BSD":
        issue_type = "Task"
    elif project == "HELP":
        issue_type = "Support request"
    else:
        raise ValueError("Unknown project, don't know what issue type to set")

    body = create_generic_jira_body(
        summary=summary,
        description=final_description,
        component_names=[],
        project_key=project,
        labels=[],
        issue_type=issue_type,
    )

    print(body)
    create_jira_ticket_generic(body, token, api_url)


if __name__ == "__main__":
    file_ticket()
