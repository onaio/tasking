"""
Setup.py for ona tasking
"""
from setuptools import setup, find_packages

setup(
    name='ona-tasking',
    version=__import__('tasking').__version__,
    description='A Django app that provides adds tasking to your Django '
    'project.',
    license='Apache 2.0',
    author='Ona Kenya',
    author_email='tech@ona.io',
    url='https://github.com/onaio/tasking',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'Django >= 1.11.19, < 2.1',
        'python-dateutil',
        'markdown',  # adds markdown support for browsable REST API
        'django-filter',  # for filtering in the API
        'djangorestframework-gis',  # for location model
        'django_countries',  # for location model
        'django-mptt',  # For MPTT
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
    ],
)
