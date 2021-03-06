# leafhopper
Do you get asked by your employer to provide a list of open source libraries that you use in the project for legal review?

`leafhopper` is a command line tool used for generating a table of dependencies for a project, including their licenses, so that you don't have to manually maintain such a list for every release of your project.

# How it works
The tool parses the project descriptor, based on different project types (`poetry`/`maven`/`vcpkg` are supported currently), and generates a table of dependencies. When some critical information, such as license, is not available in the project descriptor, `leafhopper` will test if this is a github/sourceforge project and try loading relevant information from `github.com`/`sourceforge.net`.

# Features
* parse multiple different project types to generate a table of dependencies from them
* load license information from github/sourceforge
* support overriding the list of dependencies from the project descriptor when you cannot get correct information from the project descriptor
* support customizing the output columns
* multiple outout formats
* generate a combined license file from all the licenses of the dependencies
* github token can be provided in environment variable to avoid github API rate limiting

# Installation
```
pip install leafhopper
```

# Usage
```
leafhopper /path/to/project/descriptor
```

## arguments
* `--format`: the format of the output. Possible values are `markdown`/`html`/`json`/`latex`/`csv`. Default is `markdown`.
* `--output`: the output file path. If not specified, the output will be printed to stdout.
* `--columns`: the output table header columns. It is a comma separated string. Default value is `name,version,homepage,license,description`. You can change the order of columns or add empty columns by changing the value. For example, `name,license,homepage,component` add a new empty column called `component` and reorder the columns as well.
* `--logging-level`: the logging level. Possible values are `debug`/`info`/`warning`/`error`/`critical`. Default is `info`. 
  * Set the logging level to above `info` (e.g. `error`) to supress non critical messages so that only table is printed to stdout (if no output file is specified).
  * Set the logging level to `debug` to enable debug messages.
* `--extra`: the file path to a JSON file path containing extra package information to override the information parsed from project descriptors. The `overrides` property in JSON file is an array of objects with the following properties (here is an [example](tests/data/extra.json)):
  * `name`
  * `version`, optional
  * `license`, optional
  * `homepage`, optional
  * `description`, optional
  * `disclosed_source`, optional, a url to the discolosed source for some license requirement such as MPL
* `--combine`: whether to generate a combined license file. Use `true`/`false` to toggle it. Default is false.
* `--help`: show the help message

## examples
1. extract `pyproject.toml` dependencies with markdown format and save it into `dependencies.md` file
```
leafhopper /path/to/pyproject.toml --output=dependencies.md
```

2. extract `pom.xml` dependencies with html format
```
leaphopper /path/to/pom.xml --format=html
```

3. suppress logging and output to stdout and use CLI tool [`glow`](https://github.com/charmbracelet/glow) to display it
```
leafhopper /path/to/vcpkg.json --format md --logging-level error | glow -
```

4. use custom columns to change the column order and add an empty column called `component`, which you can fill later on
```
leaphopper /path/to/pom.xml --columns name,component,version,license,homepage,description
```

5. use an extra JSON file to override the information parsed from project descriptors
```
leaphopper /path/to/pom.xml --extra=tests/data/extra.json
```

6. generate a combined license file so that you can put it as part of your project
```
leaphopper /path/to/pom.xml --combine=true
```
It will generate a file called `LICENSES.txt` with all the licenses information of the dependencies.

7. [advanced] when providing both `--extra` and `--columns`, you can get any information from the extra JSON file to be shown in the output table. For example, if you would like to add a `disclosed_source` column, you can specify this property in the `extra.json` file and specify the `disclosed_source` column in the `--columns` argument.
```
leaphopper /path/to/vcpkg.json --extra=/extra/with/disclosed/sources/extra.json --columns name,version,homepage,license,description,disclosed_source
```

# Supported formats
* markdown
* LaTex
* html
* json
* csv
## sample output
* markdown format output
```markdown
# Package Dependencies
|      name       |version|           homepage            | license  |                               description                               |
|-----------------|-------|-------------------------------|----------|-------------------------------------------------------------------------|
|simdjson         |2.2.0  |https://simdjson.org/          |Apache-2.0|A extremely fast JSON library that can parse gigabytes of JSON per second|
|pcre             |   8.45|https://www.pcre.org/          |          |Perl Compatible Regular Expressions                                      |
|pugixml          |1.12.1 |https://github.com/zeux/pugixml|MIT       |Light-weight, simple and fast XML parser for C++ with XPath support      |
|arrow            |8.0.0  |https://arrow.apache.org       |Apache-2.0|Cross-language development platform for in-memory analytics              |
```

# Supported project types
* poetry project described by `pyproject.toml`
    * https://python-poetry.org/docs/pyproject/    
* maven project described by `pom.xml`
    * https://maven.apache.org/pom.html
    * `pom.xml` with or without Maven XML namespace are supported.
* vcpkg project described by `vcpkg.json`
    * https://vcpkg.readthedocs.io/en/latest/specifications/manifests/
* more project types such as npm will be supported in the future

# Github API rating limit
If you have a really large project, you may encounter github API rate limiting. You can provide a github personal token in the environment variables to avoid this:
  * `LEAFHOPPER_GITHUB_USERNAME`
  * `LEAFHOPPER_GITHUB_PASSWORD`
  You can export these variables to your shell environment like this:
  ```
  export LEAFHOPPER_GITHUB_USERNAME={your_github_user_name}
  export LEAFHOPPER_GITHUB_PASSWORD={your_personal_token} # something like `ghp_pciFGDQlXAqDGNBXHsUbHHHZly7cf71ZKEVg`
  ```
To create a Github personal token, follow the instructions [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
  * Unless you need to access some private project information in Github, you can keep the personal token's permission minimal in Github since it only needs to be authencated against Github so that you can use higher the rate limit (see more details [here](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#requests-from-personal-accounts)).

# Changelog
[Changelog](CHANGELOG.md)

# Known issues
* Some open source libraries, doesn't have the license information available in the project descriptor (or in `github.com`/`sourceforge.net`), and the cell will be blank and you have to manually fill it.

# TODO
* Support more project types, such as `npm`'s `package.json` and `pip`'s `requirements.txt`
