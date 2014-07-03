Drat
====

Text (readability) analysis tool written in Python (2.7 and 3).

Features
~~~~~~~~

Drat is a tool that analyzes reading texts and produces a brief report
which gives a readability score (according to the Dale-Chall readability
formula) and the number of uncommon words (based on the General Service List)
in the text. It also lists all of these uncommon words (if you choose the verbose option).

There is now also support for the Coleman-Liau Readability Index.

Drat supports **docx**, **odt**, **ods**, **odp** files as well as text
files and urls.

You can also analyze multiple texts / links by creating a text file
with the filenames / links written in it.

A simple example of how drat can be used in a web application is provided in the
webapp directory.

Use
~~~

drat [--help] [-v] [-w wordlist-file] file-or-url

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

The -w (wordlist-file) option will let you filter out additional words:

::

    drat -w euphemisms_death.txt NorwegianBlue.odt 

You can use the -w option multiple times if you want to use more than one wordlist:

::

    drat -w euphemisms_death.txt -w customer_service.txt NorwegianBlue.odt 

And this command will download the following url and analyze the text in
it:

::

    drat url_you_want_analyzed.html

It is also possible to analyze several files in one command:

::

    drat text_file.txt word_document.docx open_office_file.odt

The following command is an example of redirecting the output of the contents of
a text file. The text file has one link per line (url or file) and each link in it is parsed:

::

    drat < list-of-urls.txt

Adding the -v option to any of the above commands will give you a list
of the uncommon words.

Todo
~~~~

-  Whatever feature requests anyone has (as long as it's not too much work).
-  Improve html parsing.
-  More support for other readability scores.
-  Maybe support other languages.

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
