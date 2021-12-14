import setuptools
from setuptools import setup


# Utility function to read the README.md file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README.md file and 2) it's easier to type in the README.md file than to put a raw
# string in below ...

setup(
    name="EPAM-project",
    version="1.0",
    author="SideShowBoBGOT",
    author_email="sideshowbobgot@gmail.com",
    description=("Flask application"),
    license="BSC",
    keywords="documentation",
    url="https://github.com/SideShowBoBGOT/EPAM-project",
    packages=setuptools.find_packages(),
    install_requires=['Flask', 'pytest', 'gunicorn', 'Flask-SQLAlchemy', 'Flask-Migrate',
                      'Flask-Script', 'bs4', 'pylint', 'Werkzeug', 'Flask-Login',
                      'flask-restful', 'requests'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
    ],
)
