# coding: utf-8

from fabkit import task
from fablib.base import TestSimpleBase


@task
def setup():
    test_simplebase = TestSimpleBase()
    test_simplebase.setup()

    return {'status': 1}
