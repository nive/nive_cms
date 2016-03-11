import os
import sys

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'readme.md')).read()
    CHANGES = open(os.path.join(here, 'changes.txt')).read()
except:
    README = ''
    CHANGES = ''

requires = [
    'nive',
    'nive_userdb'
]

setupkw = dict(
      name='nive_cms',
      version='1.0rc2',
      description='Nive cms - out of the box content management system for mobile and desktop websites based on the webframework pyramid',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
      ],
      author='Arndt Droullier, Nive GmbH',
      author_email='info@nive.co',
      url='http://os.nive.co/',
      keywords='cms website publisher pyramid',
      license='GPL 3',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="nive_cms",
      entry_points = """\
        [pyramid.scaffold]
        cms-sqlite=nive_cms.scaffolds:DefaultSqliteTemplate
        cms-pysql=nive_cms.scaffolds:DefaultMysqlTemplate
        cms-postgres=nive_cms.scaffolds:DefaultPostgreSQLTemplate
      """
)

setup(**setupkw)
