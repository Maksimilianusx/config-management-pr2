# Package Dependency Analyzer - Variant 28

## Description
A Python CLI tool for analyzing Ubuntu APT package dependencies.

## Stage 1
The application reads YAML configuration, validates all parameters and displays them as key-value pairs.

## Configuration
- package: package name
- repository: repository URL or local test file path
- test_mode: true for local testing, false for real repository
- version: package version
- max_depth: maximum dependency depth (0 or greater)

## Installation
py -m pip install PyYAML

## Run
.\run.bat
py src/main.py

## Tests
py -m unittest discover -s tests -p "test_*.py" -v

## Example
The sample config.yaml analyzes package A in test mode.

## Future stages
Real APT repository parsing, BFS traversal, load order and Mermaid visualization.

## Stage 2 - APT Repository
Download Ubuntu Packages.gz metadata via HTTP.
Find a package by exact name and version.
Extract direct Depends and Pre-Depends.
Support local test repository mode.

## Stage 3 - Dependency Graph
Build dependency graphs using iterative BFS.
Support maximum traversal depth.
Handle cyclic dependencies.
Support test repositories with uppercase package names.
Build graphs from Ubuntu APT repository metadata.
