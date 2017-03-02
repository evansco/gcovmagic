## Synopsis

gcovmagic is a tool to simplify unit testing with gcov

## Arguments

usage: gcovmagic.py [-h] FileToTest [-t TESTS [TESTS ...]] [-d [TESTDEPS [TESTDEPS ...]]]

## Motivation

gcov is a fantastic tool to get coverage statistics when unit testing a project, but it can certainly be a bit of a beast. This script simplifies the process of unit testing by compiling and linking the source files so that the gcov notes files are not overwritten by each successive compilation of a unit test.

## Installation

Make sure you have gcov installed.
The script should work out of the box.