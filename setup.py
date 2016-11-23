# -*- coding: UTF-8 -*-
from setuptools import setup


setup(
    name='Flask-Vmomi',
    version='1.0.0',
    url='https://github.com/clement10601/flask-vmomi/',
    license='BSD',
    author='kchwang',
    author_email='kchwang@cs.nctu.edu.tw',
    description='',
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'pyvmomi'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
