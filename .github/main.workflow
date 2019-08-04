workflow "New workflow" {
  on = "pull_request"
  resolves = [".github/actions/add-maintainers-as-reviewers"]
}

action ".github/actions/add-maintainers-as-reviewers" {
  uses = ".github/actions/add-maintainers-as-reviewers"
  secrets = ["GITHUB_TOKEN"]
}
