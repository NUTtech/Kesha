# Version history
We follow [Semantic Versions](https://semver.org/).

## 2.0.0 - New major version

### Important changes
- Add templating for response body and response headers [#7](https://github.com/NUTtech/Kesha/issues/7)
- Add status saving to the log [#75](https://github.com/NUTtech/Kesha/issues/75)
- Add proxy requests with a two-way log record  [#9](https://github.com/NUTtech/Kesha/issues/9)

BACKWARD COMPATIBILITY BREAK:
- Renamed LogEntry model fields [#9](https://github.com/NUTtech/Kesha/issues/9): 
  - body -> request_body
  - date -> request_date
  - headers -> request_headers

### Minor changes
- Add type annotations [#4](https://github.com/NUTtech/Kesha/issues/4)
- Change logo [#60](https://github.com/NUTtech/Kesha/issues/60)
- Update wemake-style-guide [#61](https://github.com/NUTtech/Kesha/issues/61)
- Adds badge for CodeQL [#19](https://github.com/NUTtech/Kesha/pull/19)
- Fixes run CodeQL [#18](https://github.com/NUTtech/Kesha/pull/18)

### Updating dependencies
- django from 3.1.13 to 3.1.14 [#124](https://github.com/NUTtech/Kesha/pull/124)
- ipython from 7.28.0 to 7.31.0 [#119](https://github.com/NUTtech/Kesha/pull/119)
- uvicorn from 0.15.0 to 0.16.0 [#104](https://github.com/NUTtech/Kesha/pull/104)
- django-debug-toolbar from 3.2.2 to 3.2.4 [#109](https://github.com/NUTtech/Kesha/pull/109)
- django-extensions from 3.1.3 to 3.1.5 [#89](https://github.com/NUTtech/Kesha/pull/89)
- psycopg2-binary from 2.9.1 to 2.9.3 [#116](https://github.com/NUTtech/Kesha/pull/116)
- mypy from 0.910 to 0.931 [#121](https://github.com/NUTtech/Kesha/pull/121)
- requests from 2.26.0 to 2.27.1 [#118](https://github.com/NUTtech/Kesha/pull/118)
- wemake-python-styleguide from 0.15.3 to 0.16.0 [#107](https://github.com/NUTtech/Kesha/pull/107)
- pytest-django from 4.4.0 to 4.5.2 [#102](https://github.com/NUTtech/Kesha/pull/102)
- celery-types from 0.8.2 to 0.10.0 [#117](https://github.com/NUTtech/Kesha/pull/117)
- django-simpleui from 2021.10.15 to 2022.1 [#106](https://github.com/NUTtech/Kesha/pull/106)
- celery from 5.1.2 to 5.2.3 [#115](https://github.com/NUTtech/Kesha/pull/115)
- restrictedpython from 5.1 to 5.2 [#94](https://github.com/NUTtech/Kesha/pull/94)
- types-requests from 2.25.11 to 2.27.5 [#122](https://github.com/NUTtech/Kesha/pull/122)
- lake8-use-fstring from 1.2.1 to 1.3 [#79](https://github.com/NUTtech/Kesha/pull/79)
- django-environ from 0.8.0 to 0.8.1 [#76](https://github.com/NUTtech/Kesha/pull/76)
- flake8-use-fstring from 1.2 to 1.2.1 [#77](https://github.com/NUTtech/Kesha/pull/77)
- pytest-mypy-plugins from 1.9.1 to 1.9.2 [#73](https://github.com/NUTtech/Kesha/pull/73)
- flake8-use-fstring from 1.1 to 1.2 [#74](https://github.com/NUTtech/Kesha/pull/74)
- celery-types from 0.8.1 to 0.8.2 [#72](https://github.com/NUTtech/Kesha/pull/72)
- django-environ from 0.7.0 to 0.8.0 [#69](https://github.com/NUTtech/Kesha/pull/69)
- django-simpleui from 2021.8.17 to 2021.10.15 [#68](https://github.com/NUTtech/Kesha/pull/68)
- pytest-django from 4.3.0 to 4.4.0 [#33](https://github.com/NUTtech/Kesha/pull/33)
- django-environ from 0.4.5 to 0.7.0 [#54](https://github.com/NUTtech/Kesha/pull/54)
- django-simpleui from 2021.3 to 2021.8.17 [#48](https://github.com/NUTtech/Kesha/pull/48)
- celery from 5.1.0 to 5.1.2 [#38](https://github.com/NUTtech/Kesha/pull/38)
- requests from 2.25.1 to 2.26.0 [#41](https://github.com/NUTtech/Kesha/pull/41)
- psycopg2-binary from 2.8.6 to 2.9.1 [#34](https://github.com/NUTtech/Kesha/pull/34)
- pytest from 6.2.4 to 6.2.5 [#51](https://github.com/NUTtech/Kesha/pull/51)
- ipython from 7.23.1 to 7.28.0 [#55](https://github.com/NUTtech/Kesha/pull/55)
- pytest-cov from 2.12.0 to 3.0.0 [#56](https://github.com/NUTtech/Kesha/pull/56)
- celery from 5.0.5 to 5.1.0 [#21](https://github.com/NUTtech/Kesha/pull/21)
- pytest-django from 4.1.0 to 4.3.0 [#13](https://github.com/NUTtech/Kesha/pull/13)
- pytest-cov from 2.11.1 to 2.12.0 [#16](https://github.com/NUTtech/Kesha/pull/16)

## 1.2.0 - The parrot's name is now Kesha!

## 1.1.0 - Disable logs by default

### Important changes
- Disable the log for a specific stub [#110](https://github.com/Uma-Tech/parrot/pull/110)

### Updating dependencies
- django-simpleui from 2021.1.1 to 2021.3 [#106](https://github.com/Uma-Tech/parrot/pull/106)
- django-extensions from 3.1.0 to 3.1.1 [#101](https://github.com/Uma-Tech/parrot/pull/101)
- pytest-cov from 2.10.1 to 2.11.1 [#96](https://github.com/Uma-Tech/parrot/pull/96)
- pytest from 6.2.1 to 6.2.2 [#97](https://github.com/Uma-Tech/parrot/pull/97)
- uvicorn from 0.13.2 to 0.13.4 [#105](https://github.com/Uma-Tech/parrot/pull/105)
- django from 3.1.4 to 3.1.7 [#104](https://github.com/Uma-Tech/parrot/pull/104)
- flake8-annotations-coverage from 0.0.4 to 0.0.5 [#94](https://github.com/Uma-Tech/parrot/pull/94)
- ipython from 7.19.0 to 7.21.0 [#107](https://github.com/Uma-Tech/parrot/pull/107)

## 1.0.1 - Improving docs

### Important changes
- Improving docs [#91](https://github.com/Uma-Tech/parrot/pull/91)

### Updating dependencies
- django-simpleui from 2020.9.26 to 2021.1.1 [#80](https://github.com/Uma-Tech/parrot/pull/80)
- pytest from 6.1.2 to 6.2.1 [#88](https://github.com/Uma-Tech/parrot/pull/88)
- uvicorn from 0.12.3 to 0.13.2 [#89](https://github.com/Uma-Tech/parrot/pull/89)

## 1.0.0 - First stable release
### New functionality
- Custom script for each request [#70](https://github.com/Uma-Tech/parrot/pull/70)

### Bug fixes
- Fix absolute request url in HttpStubAdmin with regex [#78](https://github.com/Uma-Tech/parrot/pull/78)

### Minor improvements
- Fix lgtm alert [#90](https://github.com/Uma-Tech/parrot/pull/90)
- Improves deploy [#85](https://github.com/Uma-Tech/parrot/pull/85)
- Display headers in column [#46](https://github.com/Uma-Tech/parrot/pull/46)
- Formatting request body [#52](https://github.com/Uma-Tech/parrot/pull/52)

## 0.1.10
- Fixed issue with Vue breaking on log entries [#79](https://github.com/Uma-Tech/parrot/pull/79)

## 0.1.9
- Fixed enormously long logs page loading time [#75](https://github.com/Uma-Tech/parrot/pull/75)
- Added django-extensions and ipython for ease of development [#74](https://github.com/Uma-Tech/parrot/pull/74)

## 0.1.8
- Fixed regex stubs with query args [#69](https://github.com/Uma-Tech/parrot/pull/69)

## 0.1.7
- Fix build [#66](https://github.com/Uma-Tech/parrot/pull/66)

## 0.1.6
- Changed max_length for LogEntry.path [#65](https://github.com/Uma-Tech/parrot/pull/65)
- Move django secret key to env vars [#61](https://github.com/Uma-Tech/parrot/pull/61)
- Added reading environment from the .env file [#60](https://github.com/Uma-Tech/parrot/pull/60)

## 0.1.5
- Add PARROT_ALLOWED_HOSTS env var [#63](https://github.com/Uma-Tech/parrot/pull/63)

## 0.1.4
- Remove inline logs from http-stub page [#58](https://github.com/Uma-Tech/parrot/pull/58)

## 0.1.3
- Translate into English the popup text [#50](https://github.com/Uma-Tech/parrot/pull/50)
- Limit the maximum number of query log entries [#16](https://github.com/Uma-Tech/parrot/pull/16)
- Add a request url to the stub edit page [#35](https://github.com/Uma-Tech/parrot/pull/35)
- Updates lots of dependencies ([issues](https://github.com/Uma-Tech/parrot/issues?q=milestone%3A0.1.3+label%3Adependencies))

## 0.1.2
- Adds documentation [#34](https://github.com/Uma-Tech/parrot/pull/34)
- Updates lots of dependencies ([issues](https://github.com/Uma-Tech/parrot/issues?q=milestone%3A0.1.2+label%3Adependencies))

## 0.1.1
This is the first public version of the project. Happy Birthday Parrot!
