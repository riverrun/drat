# Drat

Text analysis tool written in Python 3.

### Features

Drat is a tool that analyzes reading texts and produces a brief report which details the lexical density of the text and the number of uncommon words in the text. It also lists all of these uncommon words.

Drat supports **docx**, **odt**, **ods**, **odp** files as well as text files. It is also possible to analyze a text from the Internet by supplying a url.

### Use

At the moment, Drat has 3 options (-o [for office files], -t [for text files], and -u [for urls]).

For example, the following command will analyze an office (Writer) document called 'NorwegianBlue.odt':

    drat -o NorwegianBlue.odt

And this command will analyze a text file called 'CastleAaarrggh.txt':

    drat -t CastleAaarrggh.txt

### Todo

* Make it easier to call multiple files in one command.
* More support for analyzing the complexity of texts.
* Support other languages.
* Whatever feature requests people have - as long as it's not too much work :)

### Name

Drat is a recursive acronym which either stands for Drat is a Reading Analysis Tool or Drat is a Rabid Assessor of Texts.

### Author

This program has been developed by David Whitlock.

### License

Drat is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
