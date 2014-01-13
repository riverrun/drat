# Drat

Text analysis tool written in Python 3.

### Features

Drat is a tool that analyzes reading texts and produces a brief report which details the lexical density of the text and the number of uncommon words in the text. It also lists all of these uncommon words.

Drat supports **docx**, **odt**, **ods**, **odp** files as well as text files. It is also possible to analyze a text from the Internet by supplying a url.

### Use

At the moment, Drat has the following command line options: 

* -f check a file(s) (office and/or text files)
* -u check a url(s)
* -w use an additional wordlist(s)
  * This wordlist needs to be a text file with each word on a separate line
  * More than one wordlist can be used

For example, the following command will analyze an office (Writer) document called 'NorwegianBlue.odt':

    drat -f NorwegianBlue.odt

The -w option will let you filter out additional words:

    drat -f NorwegianBlue.odt -w euphemisms_death.txt

And this command will download the following url and analyze the text in it:

    drat -u http://www.ibras.dk/montypython/episode24.htm

It is also possible to analyze several files in one command:

    drat -f CastleAaaarrrggh.txt LuvinmyTummy.docx PininFjords.odt

### Todo

* More support for analyzing the complexity of texts.
* Support other languages.
* Whatever feature requests people have - as long as it's not too much work :)

### Dependencies

Python3 and requests (python3-requests if you are on a debian-based system).

### Name

Drat is a recursive acronym which either stands for Drat is a Reading Analysis Tool or Drat is a Rabid Assessor of Texts.

### Author

This program has been developed by David Whitlock.

### License

Drat is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
