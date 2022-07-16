# leafhopper
Do you get asked for a list of open source projects you used in the project for legal review?

`leafhopper` is a command line tool used for generating a table of dependencies for a project, so that you don't have to manually maintain such a list.

# how it works
The tool parses the project descriptor, based on different project type, and generates a table of dependencies. When some critical information, such as license, is not available in the project descriptor, `leafhopper` will test if this is a github project and try loading it from github.com.

# installation
`pip install leafhopper`

# usage
`leafhopper /path/to/project/descriptor`
## arguments
* `--format`: the format of the output. Possible values are `markdown`/`html`/`json`/`latex`/`csv`. Default is `markdown`.
* `--output`: the output file. Default is `stdout`.
* `--logging-level`: the logging level. Possible values are `debug`/`info`/`warning`/`error`/`critical`. Default is `info`. Set the logging level to above `info` (e.g. `error`) to supress non critical messages so that only table is printed to stdout (if no output file is specified).

## example
1. extract vcpkg.json dependencies with markdown format and save it into `dependencies.md` file
`leafhopper /path/to/vckpg.json --format=markdown --output=dependencies.md`


2. suppress logging and output to stdout and use CLI tool [`glow`](https://github.com/charmbracelet/glow) to display it
```
leafhopper /path/to/vcpkg.json --format md --logging-level error | glow -
```

# supported formats
* markdown
* LaTex
* html
* json
* csv

# supported project types
* vcpkg project described using vcpkg.json
  * https://vcpkg.readthedocs.io/en/latest/specifications/manifests/
* more project types such as poetry will be supported in the future