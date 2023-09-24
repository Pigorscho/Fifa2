def reg_params(reg):
    left, top, width, height = reg
    right = left + width
    lower = top + height
    return {'reg': (left, top, right, lower)}


# Container Classes
class PILRegs:
    pass
