PYTHON ?= python3
SPEC := see_api_doc.json
SKILL_DIR := .claude/skills/see
API_REFERENCE := $(SKILL_DIR)/references/api.md

.PHONY: all generate check package clean

all: check

generate:
	$(PYTHON) scripts/generate_api_reference.py $(SPEC) $(API_REFERENCE)

check: generate
	$(PYTHON) scripts/validate.py

package: check
	./scripts/package.sh

clean:
	rm -rf dist scripts/__pycache__
