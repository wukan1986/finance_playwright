def repl_sync(f_globals, f_locals):
    """同步版交互

    Examples
    --------
    >>> repl_sync(globals(), locals())

    """
    while True:
        txt = input("IN>")
        if txt == "quit":
            break
        if txt == "":
            continue

        try:
            print("OUT:", eval(txt, f_globals, f_locals))
        except Exception as e:
            print(e)

    return f_globals, f_locals


async def repl_async(f_globals, f_locals):
    """异步版交互

    Examples
    --------
    >>> repl_async(globals(), locals())

    """
    while True:
        txt = input("IN>")
        if txt == "quit":
            break
        if txt == "":
            continue

        func_code = f"""
async def __inner_function__(f_globals, f_locals):
    globals().update(f_locals)
    {txt}
    globals().update(locals())
"""
        try:
            exec(func_code, f_globals, f_locals)
            print("OUT:", await f_locals['__inner_function__'](f_globals, f_locals))
        except Exception as e:
            print(e)

    return f_globals, f_locals
