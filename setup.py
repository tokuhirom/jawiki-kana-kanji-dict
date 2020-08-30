from setuptools import setup
import sys

sys.path.append('./jawiki')
sys.path.append('./tests')

name = 'jawiki-kana-kanji-dict'

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: Japanese",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8"
]

setup(
    name='jawiki-kana-kanji-dict',
    version="0.9.9",
    description='Japanese wikipedia based dictionary.',
    long_description="Japanese wikipedia based dictionary",
    author='Tokuhiro Matsuno',
    author_email='tokuhriom@gmail.com',
    license='MIT',
    classifiers=classifiers,
    url='https://github.tokuhirom/jawiki-kana-kanji-dict/',
    packages=[],
    package_data={},
    scripts=['bin/makedict.py'],
    test_suite='suite'
)
