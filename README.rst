Drat
====

Text analysis tool written in Python 3.

Features
~~~~~~~~

Drat is a tool that analyzes reading texts and produces a brief report
which gives a readability score (according to the Dale-Chall readability
formula) and the number of uncommon words (based on the General Service List)
in the text. It also lists all of these uncommon words (if you choose the verbose option).

Drat supports **docx**, **odt**, **ods**, **odp** files as well as text
files and urls.

You can also analyze multiple texts / links by creating a text file
with the filenames / links written in it.

Use
~~~

drat [-h] [-v] [-w wordlist-file] file-or-url

-  multiple files, or urls, can be analyzed
-  the files can be text files, docx files, or odf files
-  a list of urls, or files, written in a text file can be redirected to drat:
   e.g., drat < list-of-urls.txt
-  -w use an additional wordlist(s)
-  This wordlist needs to be a text file with each word on a separate line
-  More than one wordlist can be used

For example, the following command will analyze an office (Writer)
document called 'NorwegianBlue.odt':

::

    drat NorwegianBlue.odt

The -w option will let you filter out additional words:

::

    drat -w euphemisms_death.txt NorwegianBlue.odt 

And this command will download the following url and analyze the text in
it:

::

    drat http://www.ibras.dk/montypython/episode24.htm

It is also possible to analyze several files in one command:

::

    drat CastleAaaarrrggh.txt LuvinmyTummy.docx PininFjords.odt

The following command uses a text file with links in it (one link per
line) and parses the links in it:

::

    drat < list-of-urls.txt

Adding the -v option to any of the above commands will give you a list
of the uncommon words.

Todo
~~~~

-  Improve html parsing.
-  More support for analyzing the complexity of texts.
-  Support other languages.

Dependencies
~~~~~~~~~~~~

Python3 and requests.

Name
~~~~

Drat is a recursive acronym which either stands for Drat is a Reading
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
