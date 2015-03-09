import os
del os.link

from distutils.core import setup

setup(
    # Application name:
    name="geokey_cartodb",

    description='Provides API endpoints for cartodb',

    # Version number (initial):
    version="0.1.0-beta-1",

    # Application author details:
    author="Oliver Roick",
    author_email="o.roick@ucl.ac.uk",

    # url='https://github.com/ExCiteS/geokey-cartodb', # use the URL to the github repo
    # download_url='https://github.com/ExCiteS/geokey-cartodb/tarball/0.1-beta-2',

    # Packages
    packages=["geokey_cartodb"],

    package_data={'geokey_cartodb': ['templates/*.html', 'migrations/*.py']},

    # Include additional files into the package
    include_package_data=True,

    # Dependent packages (distributions)
    install_requires=[

    ],
)
