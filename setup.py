# Authors: David Whitlock <alovedalongthe@gmail.com>
# A simple text analysis tool
# Copyright (C) 2013-2016 David Whitlock
#
# Drat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Drat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Drat.  If not, see <http://www.gnu.org/licenses/gpl.html>.

from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='drat',
    version='1.0.3',
    author='David Whitlock',
    author_email='alovedalongthe@gmail.com',
    url='https://github.com/riverrun/drat',
    description='A reading text analysis tool',
    long_description=long_description,
    license='GPLv3',
    packages=['drat'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['requests', 'click'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Office/Business',
    ],
    entry_points={
        'console_scripts': [
            'drat = drat.app:cli',
            ]
        },
)
