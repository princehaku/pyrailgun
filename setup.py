NAME = 'PyRailgun'
VERSION = '0.10'
DESCRIPTION = "Fast Craweler for Python"
LONG_DESCRIPTION = """\
"""
AUTHOR = "zhongwei bai"
AUTHOR_EMAIL = 'baizhongwei@163.com'
LICENSE = "MIT"
PLATFORMS = "Any"
URL = "http://3haku.net"
DOWNLOAD_URL = "http://lab.3haku.net/pyrailgun/%s-%s.tar.gz" % (NAME, VERSION)
CLASSIFIERS = [
    "Development Status :: Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Crawel Processing :: Yaml",
]
REQUIRS = [
    'pyyaml',
    'beautifulsoup4',
    'requests',
    ]
import sys, os.path

from setuptools import setup, find_packages

if __name__ == '__main__':

    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        platforms=PLATFORMS,
        url=URL,
        download_url=DOWNLOAD_URL,
        classifiers=CLASSIFIERS,
        packages=find_packages(),
        requires=REQUIRS
    )

