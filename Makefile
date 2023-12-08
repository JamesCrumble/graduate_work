.PHONY = help setup test dev clean
.DEFAULT_GOAL := help

SHELL := /bin/bash

init_dev:
	pip install -r ./requirements-dev.txt
	pre-commit install
