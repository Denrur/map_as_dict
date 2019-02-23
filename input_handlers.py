from bearlibterminal import terminal as blt


def handle_keys():
    code = blt.read()
    # Movement keys
    if code == blt.TK_UP or code == blt.TK_W:
        return {'move': (0, -1)}
    elif code == blt.TK_DOWN or code == blt.TK_X:
        return {'move': (0, 1)}
    elif code == blt.TK_LEFT or code == blt.TK_A:
        return {'move': (-1, 0)}
    elif code == blt.TK_RIGHT or code == blt.TK_D:
        return {'move': (1, 0)}
    elif code == blt.TK_Q:
        return {'move': (-1, -1)}
    elif code == blt.TK_E:
        return {'move': (1, -1)}
    elif code == blt.TK_Z:
        return {'move': (-1, 1)}
    elif code == blt.TK_C:
        return {'move': (1, 1)}

    if code == blt.TK_G:
        return{'pickup': True}

    elif code == blt.TK_I:
        # print('show_inventory')
        return{'show_inventory': True}

    elif code == blt.TK_O:
        return{'drop_inventory': True}

    if code == blt.TK_RETURN and blt.TK_ALT:
        return {'fullscreen': True}

    elif code == blt.TK_ESCAPE:
        return {'exit': True}

    return {}
