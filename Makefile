# Makefile for chirpy, the St Andrews bird counting sensor suite
#
# Copyright (C) 2025 Simon Dobson
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/gpl.html>.

PACKAGENAME = chirpy


# ----- Sources -----

# Source code
SOURCES_CODE = \
	chirpy/__init__.py \
	chirpy/utils.py \
	chirpy/audiofiles.py \
	chirpy/audiosample.py \
	chirpy/classify.py \
	chirpy/db.py \
	chirpy/mqtt.py \
	chirpy/observations.py

# Tests
SOURCES_TESTS_INIT = test/__init__.py
SOURCES_TESTS = \
	test/test_basic.py \
	test/cli/identify \
	test/cli/list \
	test/cli/play \
	test/cli/record
TESTSUITE = test

# Extras for the build and packaging system
SOURCES_EXTRA = \
	README.org \
	chirpy.py.in
SOURCES_GENERATED = \
	MANIFEST \
	TAGS \
	setup.py

# Documentation
SOURCES_DOC_CONF = doc/conf.py
SOURCES_DOC_BUILD_DIR = doc/_build
SOURCES_DOC_BUILD_HTML_DIR = $(SOURCES_DOC_BUILD_DIR)/html
SOURCES_DOC_ZIP = $(PACKAGENAME)-doc-$(VERSION).zip
SOURCES_DOCUMENTATION = \
	doc/index.rst \
	doc/install.rst \
	doc/config.rst \
	doc/architecture.rst \
	doc/scripts.rst \
	doc/db-schema.rst


# ----- Models -----

# Models directory
MODELS_DIR = models

# BirdNET models (from Zenodo)
BIRDNET_MODEL_BASE_URL = https://zenodo.org/records/15050749/files
BIRDNET_MODEL_STEM = BirdNET_v2.4_
BIRDNET_MODEL_FORMATS = tflite tfline_fp16 tflite_int8

# Google Perch model (from Kaggle)
PERCH_MODEL = google/bird-vocalization-classifier/tensorFlow2/perch_v2_cpu


# ----- Tools -----

# Base commands
PYTHON = python3
PYTEST = pytest
PIP = pip
GIT = git
ETAGS = etags
VIRTUALENV = $(PYTHON) -m venv
ACTIVATE = . $(VENV)/bin/activate
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
MKDIR = mkdir -p
CURL = curl
ZIP = zip -r

# Makefile environment
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# All model files
BIRDNET_MODEL_FILES = $(foreach format,$(BIRDNET_MODEL_FORMATS),"$(BIRDNET_MODEL_STEM)$(format).zip")
MODEL_FILES = $(BIRDNET_MODEL_FILES)

# Root directory
ROOT = $(shell pwd)

# Requirements for running the library and for the development venv needed to build it
VENV = venv3
REQUIREMENTS = requirements.txt
DEV_REQUIREMENTS = dev-requirements.txt

# Constructed commands
RUN_TESTS = $(PYTEST) $(SOURCES_TESTS)
RUN_SPHINX_HTML = PYTHONPATH=$(ROOT) $(CHDIR) doc && make html


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run tests for all versions of Python we're interested in
test: env Makefile
	$(ACTIVATE) && $(RUN_TESTS)

# Build the API documentation using Sphinx
.PHONY: doc
doc: env $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	$(ACTIVATE) && $(RUN_SPHINX_HTML)

# Build a development venv from the requirements in the repo
env: $(VENV) models

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CAT) $(REQUIREMENTS) $(DEV_REQUIREMENTS) >$(VENV)/requirements.txt
	$(ACTIVATE) && $(PIP) install -U pip wheel && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt

# Download the machine learning models
#
# The BirdNET models on Zeonodo are openly available.
# Downloading the Perch model from Kaggle assumes that you have
# Kaggle API keys installed in ~/.kaggle/kaggle.json
$(MODELS_DIR):
	$(MKDIR) $(MODELS_DIR)
	for fn in $(BIRDNET_MODEL_FILES); do $(CURL) -o $(MODELS_DIR)/$$fn $(BIRDNET_MODEL_BASE_URL)/$$fn?download=1; done
	$(ACTIVATE) && $(PYTHON) -c "import kagglehub; path = kagglehub.model_download('$(PERCH_MODEL)'); print(path)"

# Clean up the distribution build
clean:
	$(RM) $(SOURCES_GENERATED) $(PACKAGENAME).egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP) dist build
	$(CHDIR) doc && make clean

# Clean up everything, including the computational environment and models
reallyclean: clean
	$(RM) $(VENV)
	$(RM) $(MODELS_DIR)


# ----- Generated files -----

# The tags file
TAGS:
	$(ETAGS) -o TAGS $(SOURCES_CODE)


# ----- Usage -----

define HELP_MESSAGE
Available targets:
   make test         run the test suite
   make doc          generate the documentation
   make env          create a development virtual environment
   make clean        clean-up the build
   make reallyclean  clean up the virtualenv and models as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
