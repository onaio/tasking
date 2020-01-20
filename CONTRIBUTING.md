# Contribution Guidelines

Welcome! Thank you for showing interest in contributing to this package 🥰🥳

The following information comprises of some guidelines & details important in ensuring you're first contribution is as smooth as possible. Following the guidelines also helps communicate that you respect the time of the maintainers and your intent to help develop this project.

## How to contribute to the project

### 1. Report a bug 🐛

In case you have enountered any bug while utilizing this package, please ensure:

- You are using the latest [release](https://github.com/onaio/tasking/releases).

After confirming the above, browse through our [tickets](https://github.com/onaio/tasking/issues) and ensure the bug has not been reported already. If it hasn't been reported yet, [open a ticket](https://github.com/onaio/tasking/issues/new) with the as much informations as possible like:

- What you expected to happen
- What actually happened
- Logs and other interesting information
- All steps to reproduce the issue

### 2. Suggest Enhancements or New Features 🔥

Feature and enhancement requests are always welcome! We ask you ensure the following details are provided while [opening a ticket](https://github.com/onaio/tasking/issues/new), in order to start a constructive discussion:

- Describe the feature/enhancement in detail.
- Explain why the feature/enhancement is needed.
- Describe how the feature/enhancement should work
- List any advantages & disadvantages of implementing the feature/enhancement

### 3. Code Contributions / Pull Requests 🖥️

Pull requests are wholeheartedly welcome!❤️ If you are unsure about how to make your first pull request, here are some helpful resources:

- [Creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)
- [How to create effective pull requests](https://dev.to/mpermar/how-to-create-effective-pull-requests-2m8e)

In order to make it easier for us to facilitate the smooth merging of your pull request, please make sure the following standards are met within your pull request.

- Code & commits follow our [styleguides](#styleguides).
- Setup your development environment as advised [here](#Setting-up-your-development-environment).
- Implement / Update tests that need to be updated and ensure that they pass.

With the above points in mind feel free to comment on one of our [beginner-friendly issues](https://github.com/onaio/tasking/issues?q=is%3Aissue+is%3Aopen+label%3A%22Good+First+Issue%22) expressing your intent to work on it.


## Setting up your development environment

This project utilizes [pipenv](https://pipenv-fork.readthedocs.io/en/latest/), one can setup the pipenv environment by running the following:

```shell
$ pipenv install --dev
$ pipenv shell
$ pre-commit install
```

If you aren't comfortable utilizing `pipenv` but are comfortable in utilizing `virtualenv`. You can run the following to setup the environment within a `virtualenv`:

```shell
$ pip install pipenv
$ pipenv install --dev
$ pre-commit install
```

## Styleguides

### Git commit messages

Git commits help communicate what has changed within the project. Making it easier to track down changes or implementation within the codebase. Before contributing please read the following article by [Chris Beams](https://chris.beams.io) on [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/).

### Python code styleguide

This project utilizes a variety of python code linters & formatters. Most of these checks are run before a commit is made as long as one has setup the project as defined in [_Setting up your development environment_](#Setting-up-your-development-environment).

If you'd like to manually run the checks, run the following command.

```shell
$ tox
```
