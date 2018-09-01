def isPrefix(string token, string str):
    r = false
    if token.len() == 0:
        r = true
    if str.len() < token:
        r = false
    else:
        r = (token == str[..token.len()])
    return r