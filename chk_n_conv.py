def chkNConv(instr):
    print (instr)
    if isinstance(instr, str):
        print('DEBUG: is str')
        return instr.encode(encoding='utf-8')
    elif isinstance(instr, unicode):
        print('DEBUG: is unicode')
        return instr
    else:
        return u''