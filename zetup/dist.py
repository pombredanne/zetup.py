# zetup.py
#
# Zimmermann's Python package setup.
#
# Copyright (C) 2014 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# zetup.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# zetup.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with zetup.py. If not, see <http://www.gnu.org/licenses/>.

__all__ = ['Distribution']

import os
from pkg_resources import (
  get_distribution, DistributionNotFound, VersionConflict)


class Distribution(str):
    """Simple proxy to get a pkg_resources.Distribution instance
       matching the given name and :class:`Version` instance.
    """
    def __new__(cls, name, pkg, version):
        return str.__new__(cls, name)

    def __init__(self, name, pkg, version):
        self.pkg = pkg
        self.version = version

    def find(self, modpath, raise_=True):
        """Try to find the distribution and check version.

        :param raise_: Raise a VersionConflict
          if version doesn't match the given one?
          If false just return None.
        """
        try:
            dist = get_distribution(self)
        except DistributionNotFound:
            return None
        if os.path.realpath(dist.location) \
          != os.path.realpath(os.path.dirname(modpath)):
            return None
        if dist.parsed_version != self.version.parsed:
            if raise_:
                raise VersionConflict(
                  "Version of distribution %s"
                  " doesn't match %s.__version__ %s."
                  % (dist, self.pkg, self.version))
            return None
        return dist
