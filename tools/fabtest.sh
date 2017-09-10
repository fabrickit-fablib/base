#!/bin/bash
#

# exit on error
set -e
flake8 --exclude=test-repo/*

fablib=`echo $PWD | awk -F '/' '{print $NF}'`
coverage run `which fab` test:l=$fablib
coverage report
