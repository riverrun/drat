Drat
====

Text (readability) analysis tool written in Python (2.7 and 3).

Features
~~~~~~~~

Drat is a tool that analyzes reading texts and produces a brief report
which provides the following information:

- the Dale-Chall readability score.
- the Coleman-Liau Readability Index.
- the number of uncommon words (based on the General Service List).
- a list of all of these uncommon words (if you choose the verbose option).


Drat supports **docx**, **odt**, **ods**, **odp** files as well as text
files and urls.

You can also analyze multiple texts / links by creating a text file
with the filenames / links written in it.

A simple example of how drat can be used in a web application is provided in the
webapp directory.

Use
~~~

Please read the `wiki <https://github.com/riverrun/drat/wiki>`_ for information about how to use drat.

Dependencies
~~~~~~~~~~~~

Python (2.7 or 3), click and requests.

Name
~~~~

Drat is a recursive acronym which either stands for Drat is a Readability
Analysis Tool or Drat is a Rabid Assessor of Texts.

Author
~~~~~~

This program has been developed by David Whitlock.

License
~~~~~~~

Drat is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.
