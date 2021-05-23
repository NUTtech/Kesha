# Version history
We follow [Semantic Versions](https://semver.org/).

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
