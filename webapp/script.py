def rundrat(form):
    from drat import analysis
    data = form.textinput.data.encode('utf-8')
    check = analysis.Checktext('reading text', None, True, True)
    result = check.run_check(data)
    check.fmt_output(*result)
    return check.message.splitlines()
