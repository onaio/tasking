"""
Setup.py for ona tasking
"""
from setuptools import setup

setup(
    name='ona-tasking',
    version='0.1',
    description='A tasking library.',
    license='GPL 3',
    author='Ona Kenya',
    author_email='tech@ona.io',
    url='https://github.com/onaio/tasking',
    install_requires=[
        'django',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
    ],
)
