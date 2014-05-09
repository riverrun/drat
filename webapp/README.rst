Webapp
======

A simple example of how you can use drat in a webapp.

Notes
~~~~~

This example has two html files -- drat and dratreport. The drat file has a text
input box, in which text can be pasted. The dratreport file shows a report of the
analysis. Both these forms are written using Jinja2, which is used by Flask, the
web framework.

The short function in the script file takes the text from the input box and calls
drat to analyze it.
