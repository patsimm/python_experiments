def rainbow(i):
    # Given a color index 'i' this returns a color of an rainbow. The rainbow
    # restarts at index 360.
    i = (i % 360) / 120.
    r, g, b = 0, 0, 0
    if i >= 2:
        i -= 2
        r, g, b = i, 0., 1 - i
    elif i >= 1:
        i -= 1
        r, g, b = 0., 1 - i, i
    elif i < 1:
        r, g, b = 1 - i, i, 0.
    return r, g, b
