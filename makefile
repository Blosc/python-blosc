# This is the maintainers undocumented Makefile.
# Nothin to see here, please move along.
.PHONY: build test clean doc

build:
	python setup.py build_ext -i

test:
	python -c "import blosc ; blosc.test()"

clean:
	git clean -dfX; git clean -dfx

doc:
	cd doc && make html
