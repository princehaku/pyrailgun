NAME = 'pyrailgun'
VERSION = '0.23'
DESCRIPTION = "Fast Crawler For Python"
LONG_DESCRIPTION = """\
This is a simple python crawler framework for human

you can crawler website more easily

only need a json file to descrip your crawler


optional module: webkit

if you have PyQt4 And QtWebkit installed, you can specific to use webkit to crawler html after javascript rendered

see https://github.com/princehaku/pyrailgun/tree/master/demo for some demos

see https://github.com/princehaku/pyrailgun for more infomation

"""
AUTHOR = "zhongwei bai"
AUTHOR_EMAIL = 'baizhongwei@163.com'
LICENSE = "MIT"
PLATFORMS = "Any"
URL = "https://github.com/princehaku/pyrailgun"
DOWNLOAD_URL = "https://pypi.python.org/packages/source/P/pyrailgun/%s-%s.tar.gz" % (NAME, VERSION)
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
REQUIRS = [
    'pyyaml >=3.10',
    'beautifulsoup4 >=4.2.0',
    'requests >=1.2.3'
    ]

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
        packages=['pyrailgun'],
        include_package_data = True,
        package_data = {
            'pyrailgun':['*.conf']
        },
        install_requires=REQUIRS
    )

