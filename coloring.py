def rainbow(i):
    # Given a color index 'i' this returns a color of an rainbow. The rainbow
    # restarts at index 360.
    i = (i % 360) / 120.
    if i >= 2:
        i -= 2
        return i, 0., 1-i
    elif i >= 1:
        i -= 1
        return 0., 1-i, i
    elif i < 1:
        return 1-i, i, 0.


def green_to_red(i):
    # Given a color index 'i' this returns a color beginning with green, ending
    # with red and restarting at index 360
    i = (i % 360) / 360.
    return i, 1-i, 0.
