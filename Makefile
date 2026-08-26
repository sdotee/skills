PYTHON ?= python3

.PHONY: all check package clean

all: check

check:
	$(PYTHON) scripts/validate.py

package: check
	./scripts/package.sh

clean:
	rm -rf dist scripts/__pycache__
