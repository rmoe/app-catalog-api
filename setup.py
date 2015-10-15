# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='appcatalog',
    version='0.1',
    description='',
    author='',
    entry_points="""
    [pecan.command]
    reset-db = appcatalog.cmd.reset_db:GetCommand
    """,
    author_email='',
    install_requires=[
        "pecan",
    ],
    test_suite='appcatalog',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)
