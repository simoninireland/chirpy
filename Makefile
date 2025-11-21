# Makefile for St Andrews bird counting sensor suite
#
# Copyright (C) 2025 Simon Dobson


# ----- Sources -----

# Source code
SOURCES_CODE =
SOURCES_TESTS_INIT = test/__init__.py
SOURCES_TESTS =
TESTSUITE = test

# Extras for the build and packaging system
SOURCES_EXTRA = \
	README.org
SOURCES_GENERATED = \
	MANIFEST \
	TAGS \
	setup.py


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
ACTIVATE = . $(VENV)/bin/activate


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run tests for all versions of Python we're interested in
test: env Makefile setup.py
	$(ACTIVATE) && $(RUN_TESTS)

# Build a development venv from the requirements in the repo
.PHONY: env
env: $(VENV) models

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CAT) $(REQUIREMENTS) $(DEV_REQUIREMENTS) >$(VENV)/requirements.txt
	$(ACTIVATE) && $(PIP) install -U pip wheel && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt

# Download the machine learning models
.PHONY: models
models:
	$(MKDIR) $(MODELS_DIR)
	for fn in $(BIRDNET_MODEL_FILES); do $(CURL) -o $(MODELS_DIR)/$$fn $(BIRDNET_MODEL_BASE_URL)/$$fn?download=1; done
	$(ACTIVATE) && $(PYTHON) -c "import kagglehub; path = kagglehub.model_download('$(PERCH_MODEL)'); print(path)"

# Clean up the distribution build
clean:
	$(RM) $(SOURCES_GENERATED)

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
   make env          create a development virtual environment
   make clean        clean-up the build
   make reallyclean  clean up the virtualenv and models as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
