# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = "v0.1.0a"

LONG_DESCRIPTION = """
This package contains a `Sphinx <http://www.sphinx-doc.org/en/master/>`_ extension
for converting to rst to myst documents from the sphinx AST.

This project is maintained and supported by `mmcky <http://mmcky.org/>`_.

Status
------

|status-docs| |status-travis|

.. |status-docs| image:: https://readthedocs.org/projects/sphinxcontrib-tomyst/badge/?version=latest
   :target: http://sphinxcontrib-tomyst.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |status-travis| image:: https://travis-ci.org/mmcky/sphinxcontrib-tomyst.svg?branch=master
   :target: https://travis-ci.org/mmcky/sphinxcontrib-tomyst

"""

requires = ["Sphinx>=0.6"]

setup(
    name="sphinxcontrib-tomyst",
    version=VERSION,
    url="https://github.com/mmcky/sphinxcontrib-tomyst",
    download_url="https://github.com/mmcky/sphinxcontrib-tomyst/archive/{}.tar.gz".format(
        VERSION
    ),
    license="BSD",
    author="QuantEcon",
    author_email="admin@quantecon.org",
    description='Sphinx "MyST" extension: Convert your RST files into MyST documents.',
    long_description=LONG_DESCRIPTION,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Sphinx",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Framework :: Sphinx :: Extension",
    ],
    platforms="any",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["docutils", "sphinx"],
    extras_require={
        "code_style": ["flake8<3.8.0,>=3.7.0", "black", "pre-commit==1.17.0"],
        "testing": [
            "coverage",
            "pytest>=3.6,<4",
            "pytest-cov",
            "pytest-regressions",
        ],
    },
    namespace_packages=["sphinxcontrib"],
)
