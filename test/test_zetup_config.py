"""Test the zetup config management on zetup package's own config.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
import sys
from types import ModuleType
from inspect import ismodule

from pkg_resources import (
  parse_requirements, get_distribution, DistributionNotFound)

from path import Path

import zetup
from zetup import Zetup

import pytest


def test_name(zfg):
    assert zfg.NAME == 'zetup'


def test_zetup_config(zfg, zfg_path, pkg_path, in_repo, in_site_packages):
    if in_site_packages:
        assert zfg.__name__ == 'zetup.zetup_config'
        assert zfg_path == pkg_path # / 'zetup_config'
    else:
        with pytest.raises(ImportError):
            from zetup import zetup_config

        assert isinstance(zfg, Zetup)
        assert zfg_path == pkg_path.dirname()


def test_description(zfg):
    assert zetup.__description__ == zfg.DESCRIPTION


def test_distribution(zfg, pkg_path, in_repo, in_site_packages):
    try:
        dist = get_distribution('zetup')
    except DistributionNotFound:
        if in_repo:
            dist = None
        else:
            raise
    else:
        if in_repo and not Path(dist.location).samefile(pkg_path.dirname()):
            dist = None
    assert zetup.__distribution__ == zfg.DISTRIBUTION.find(pkg_path) \
      == dist


def test_version(zfg):
    assert zetup.__version__ == zfg.VERSION


def test_requires(zfg, zfg_path, in_repo, in_site_packages):
    assert zetup.__requires__ == zfg.REQUIRES
    if in_repo:
        assert list(parse_requirements(str(zetup.__requires__))) == list(
          parse_requirements((zfg_path / 'requirements.txt').text()))


def test_extras(zfg, zfg_path, in_repo, in_site_packages):
    for extra in zetup.__extras__:
        assert zetup.__extras__[extra] == zfg.EXTRAS[extra]
        if in_repo:
            assert list(parse_requirements(str(zetup.__extras__[extra]))) \
              == list(parse_requirements(
                   (zfg_path / ('requirements.%s.txt' % extra))
                   .text()))


def test_python(zfg):
    assert ('%s.%s' % sys.version_info[:2]) in zfg.PYTHON


def test_classifiers(zfg):
    assert all('Programming Language :: Python :: %s' % version
               for version in zfg.PYTHON)
