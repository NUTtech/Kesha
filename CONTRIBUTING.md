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

### Выпуск нового релиза:
Релизы происходят по git-flow  
[https://danielkummer.github.io/git-flow-cheatsheet/index.ru_RU.html](https://danielkummer.github.io/git-flow-cheatsheet/index.ru_RU.html)

Необходимо выполнить только однажды для настройки git flow,
все парамеры оставляем дефолтные:
```shell script
git flow init
```

1. Обновляем ветки master и develop
    ```shell script
    git checkout develop && git pull
    git checkout master && git pull
    ```
   
1. Запускаем новый релиз
    ```shell script
    git flow release start <VERSION>
    ```
    `<VERSION>` - Версия нового релиза

1. Обновляем версию проекта
    ```shell script
    poetry version <VERSION>
    ```

1. Коммитим конфигурацию проекта с новой версией
    ```shell script
    git commit -m "bump version" pyproject.toml
    ```

1. Завершаем сборку релиза
    ```shell script
    git flow release finish <VERSION>
    ```

1. Пушим всё в репозиторий
    ```shell script
    git push origin master develop --follow-tags
    ```

1. [Создаём](https://github.com/Uma-Tech/parrot/releases/new)
 новый релиз, указав запушенный тег
