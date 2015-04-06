# an example of how to call drat from a Flask web app

def rundrat(form):
    from drat import app
    data = form.textinput.data.lower()
    message = app.raw_check(data)
    return render_template('webapp.html', message=message.splitlines())
