def rundrat(form):
    from drat import analysis
    data = form.textinput.data.encode('utf-8')
    check = analysis.Checktext('reading text', None, True, True)
    check.run_check(data)
    return check.message.splitlines()
