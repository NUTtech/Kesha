# How to contribute

## First steps
1. Fork [our repo](https://github.com/Uma-Tech/parrot),
here's the [guide on forking](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
1. [Clone your new repo](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) (forked repo) to have a local copy of the code
1. Apply the required changes!
1. Send a Pull Request to our original repo. Here's [the helpful guide](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) on how to do that


## Dependencies
We use [poetry](https://github.com/sdispater/poetry) to manage the dependencies.

To install them you would need to run `install` command:

```bash
poetry install
```

To activate your `virtualenv` run `poetry shell`.

## Two magic command
Run `make autotests` or `make lint` to run checks in docker/

## Tests
We use `pytest` and `flake8` for quality control.
We also use `wemake_python_styleguide`.

To run all tests:

```bash
pytest
```

To run linting:

```bash
flake8 .
```

### Before submitting

Before submitting your code please do the following steps:

1. Run `pytest` to make sure everything was working before
1. Add any changes you want
1. Add tests for the new changes
1. Edit documentation if you have changed something significant
1. Update `CHANGELOG.md` with a quick summary of your changes
1. Run `pytest` again to make sure it is still working
1. Run `flake8` to ensure that style is correct

You can run everything at once with `make autotests`,
run `make help` for more details.


## Notes for maintainers

This section is intended for maintainers only.
If you are not a maintainer (or do not know what it means),
just skip it. You are not going to miss anything useful.

### Making new release
Releases are shipped using git-flow
[https://danielkummer.github.io/git-flow-cheatsheet/index.html](https://danielkummer.github.io/git-flow-cheatsheet/index.html)

This command has to be run only once to set up git flow, keep default value
for all parameters.
```shell script
git flow init
```

1. Update master and develop branches
    ```shell script
    git checkout develop && git pull
    git checkout master && git pull
    ```
   
1. Start a new release
    ```shell script
    git flow release start <VERSION>
    ```
    `<VERSION>` - new release version

1. Update project version
    ```shell script
    poetry version <VERSION>
    ```

1. Commit project configuration with the new version
    ```shell script
    git commit -m "bump version" pyproject.toml
    ```

1. Finish building a release
    ```shell script
    git flow release finish <VERSION>
    ```

1. Push all the changes into the repository
    ```shell script
    git push origin master develop --follow-tags
    ```

1. [Create](https://github.com/Uma-Tech/parrot/releases/new)
 a new release specifying pushed tag
