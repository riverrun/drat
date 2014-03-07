#!/usr/bin/python3

# Authors: David Whitlock <alovedalongthe@gmail.com>
# A simple text analysis tool
# Copyright (C) 2013-2014 David Whitlock
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

from distutils.core import setup

setup(
    name = 'drat',
    version = '0.0.3',
    packages = ['drat'],
    scripts = ['bin/drat'],
    data_files = [
        ('share/drat', ['data/EN_vocab.txt', 'data/EN_function.txt']),
        ],
    author = 'David Whitlock',
    author_email = 'alovedalongthe@gmail.com',
    url = 'https://github.com/riverrun/drat',
    description = 'A reading text analysis tool',
    license = 'GPLv3',
)
