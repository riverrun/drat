Examples
========

Some examples of how you can use drat in different scripts.

Notes
~~~~~

The webapp example has two html files -- drat and dratreport. The drat file has a text
input box, in which text can be pasted. The dratreport file shows a report of the
analysis. Both these forms are written using Jinja2, which is used by Flask, the
web framework.

The short function in the webapp_script file takes the text from the input box and calls
drat to analyze it.

The simple_script file shows how you might call drat from a script.
