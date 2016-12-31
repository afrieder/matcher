from os import path
from distutils.core import setup

here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'README.rst')

description = 'A simple functional, type-safe pattern matcher in Python'

if path.isfile(readme):
    with open(readme, encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = description

setup(
    name='matcher',
    version='0.1',
    description=description,
    long_description=long_description,
    url='https://github.com/afrieder/matcher',
    download_url='https://github.com/afrieder/matcher/tarball/0.1',
    author='Alex Frieder',
    author_email='alex.frieder@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Other/Nonlisted Topic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['case', 'pattern', 'matching', 'functional', 'typesafe'],
    packages=['matcher']
)
