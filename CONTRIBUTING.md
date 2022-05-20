# How to Contribute

Every code that is contributed must relate to an issue.
For new features, please create an issue accordingly first.

## Submit an issue

There is no direct means communication to the initial project team yet.
For every request, please open an issue.

## Rules

1. No pull request without an issue. Every branch and pull request has to be linked to an issue.
2. No direct push to `main` or `development`.
3. No pushing of code that is not your own work.
4. Every branch besides `main` or `development` must be named after the issue id and short name it relates to.

## Branching Strategy

1. `main` represents the production branch. This is the latests stable version.
2. `development` is the dev branch. This is the latests preview version used in active development.
3. Every development is done in dedicated feature branches derived from issues.

### Bug fixes and new features

For every bug fix or new feature there must be a dedicated feature branch realted to an open issue.
Feature branches should be merged via pull requests towards `development`.

### Hot fixes

A hot fix follows the same process as an ordinary bug fix. However, a verified hot fix can be merged into `development` as well as `main`. A hot fix should not result in `development` getting merged into `main` as a whole.

## New versions

A new version of the package results from a successful pull request of `development` towards `main` at the end of each project sprint or when reaching a milestone. Hot fixes may result in a minor version increase.
Versioning follows the rules of [semantic versioning](https://semver.org/).

