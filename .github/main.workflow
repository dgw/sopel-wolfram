workflow "Upload tagged releases to PyPI" {
  resolves = ["upload"]
  on = "push"
}

action "tag-filter" {
  uses = "actions/bin/filter@master"
  args = "tag"
}

action "check" {
  uses = "ross/python-actions/setup-py/3.7@b01151c"
  args = "check"
  needs = "tag-filter"
}

action "sdist" {
  uses = "ross/python-actions/setup-py/3.7@b01151c"
  args = "sdist"
  needs = "check"
}

action "upload" {
  uses = "ross/python-actions/twine@45ba52e"
  args = "upload ./dist/sopel_modules.wolfram-*.tar.gz"
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
  needs = "sdist"
}
