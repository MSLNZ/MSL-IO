from collections import namedtuple

__author__ = 'jborbely'
__copyright__ = '\xa9 2018, ' + __author__
__version__ = '0.1.0'

version_info = namedtuple('version_info', 'major minor micro')(*map(int, __version__.split('.')[:3]))
""":obj:`~collections.namedtuple`: Contains the version information as a (major, minor, micro) tuple."""
