# encoding: utf-8
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import tempfile
import time

import pytest

here = os.path.abspath(__file__)

def test_regtest(regtest, tmpdir):

    print("this is expected outcome", file=regtest)
    print(tmpdir.join("test").strpath, file=regtest)
    print(tempfile.gettempdir(), file=regtest)
    print(tempfile.mkdtemp(), file=regtest)
    print("obj id is", hex(id(here)), file=regtest)


def test_always_fail():
    assert 1 * 1 == 2


def test_always_fail_regtest(regtest):
    regtest.write(str(time.time()))
    assert 1 * 1 == 2

def test_only_fail_regtest(regtest):
    regtest.identifier = "dev"
    regtest.write(str(time.time()))


def test_always_ok():
    assert 1 * 1 == 1


@pytest.mark.xfail
def test_xfail_0():
    assert 1 == 2


@pytest.mark.xfail
def test_xfail_with_regtest(regtest):
    assert 1 == 2


def test_always_ok_regtest(regtest):
    regtest.identifier = "my_computer"
    assert 1 * 1 == 1


@pytest.mark.parametrize("a, b, c", [(1, 2, 3), ("a", "b", "ab")])
def test_with_paramertrization(a, b, c, regtest):
    print(a, b, c, file=regtest)
    assert a + b == c
