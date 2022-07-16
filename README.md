# leafhopper
Do you get asked for a list of open source projects you used in the project for legal review?

`leafhopper` is a command line tool used for generating a table of dependencies for a project, so that you don't have to manually maintain such a list.

# installation
`pip install leafhopper`

# usage
`leafhopper /path/to/project/descriptor`
## arguments
* `--format`: the format of the output. Possible values are `markdown`/`html`/`json`/`latex`/`csv`. Default is `markdown`.
* `--output`: the output file. Default is `stdout`.

## example
`leafhopper /path/to/vckpg.json --format=markdown --output=dependencies.md`
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