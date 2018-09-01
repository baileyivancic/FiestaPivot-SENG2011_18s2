def isPrefix(token, string):
    r = false
    if len(token) == 0:
        r = true
    if len(string) < token:
        r = false
    else:
        r = (token == str[..len(token)])
    return r