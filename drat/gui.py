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

from tkinter import Tk, ttk, Text, INSERT, W, E
from tkinter.filedialog import askopenfilename
from . import app

class MainWin(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Drat Readability Tool')

        self.setup_maingrid()
        self.setup_textwin()

    def setup_maingrid(self):
        self.maingrid = ttk.Frame(self, padding='3 3 12 12')
        self.maingrid.grid(column=0, row=0, sticky=(W, E))

        open_btn = ttk.Button(self.maingrid, text='Open', command=self.open_file)
        open_btn.grid(column=0, row=0)
        #p = ttk.Progressbar(parent, orient=HORIZONTAL, length=200, mode='determinate')

    def setup_textwin(self):
        self.results = Text(self, fg='black', bg='white')
        self.results.grid(column=0, row=1)

    def open_file(self):
        arg = askopenfilename()
        if arg.startswith(('http', 'ftp')):
            result = app.check_url(arg, None)
        else:
            result = app.check_file(arg, None)
        message = app.fmt_output(arg, False, *result) + '\n'
        self.results.insert(INSERT, message)

def main():
    root = MainWin()
    root.mainloop()
