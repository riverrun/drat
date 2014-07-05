def rundrat(form):
    from drat import analysis, app
    data = form.textinput.data.lower()
    check = analysis.Checktext(None)
    result = check.run_check(data)
    message = app.fmt_output(None, True, *result)
    return message.splitlines()
