"""
Setup.py for ona tasking
"""
from setuptools import setup

setup(
    name='ona-tasking',
    version='0.1',
    description='A Django app that provides adds tasking to your Django '
    'project.',
    license='Apache 2.0',
    author='Ona Kenya',
    author_email='tech@ona.io',
    url='https://github.com/onaio/tasking',
    install_requires=[
        'Django >= 1.11',
        'python-dateutil',
        'djangorestframework',  # Adds Serializers and API support
        'markdown',  # adds markdown support for browsable REST API
        'django-filter',  # for filtering in the API
        'djangorestframework-gis',  # for location model
        'django_countries',  # for location model
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
