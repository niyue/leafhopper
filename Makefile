dev:
	find leafhopper -iname "*.py" -iname "pyproject.toml" | entr -s "poetry build && pip install ./dist/leafhopper-*-any.whl --force-reinstall --no-dependencies"

setup:
	# install the library into system python
	rm -fr ./dist
	poetry build && pip install ./dist/leafhopper-*-py3-none-any.whl --force-reinstall

test: clean
	poetry run pytest

clean:
	rm -fr ./build 
