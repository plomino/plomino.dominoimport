from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='plomino.dominoimport',
      version=version,
      description="Allows to import Lotus Notes Domino database (design + documents) into Plomino",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Emmanuelle Helly',
      author_email='e.helly@gmail.com',
      url='http://www.brehault.net/plomino',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plomino'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.CMFPlomino',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )
