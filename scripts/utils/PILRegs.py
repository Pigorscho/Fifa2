def reg_params(reg):
    left, top, width, height = reg
    right = left + width
    lower = top + height
    return {'reg': (left, top, right, lower)}


class PILRegs:
    current_items = reg_params((28, 1443, 170, 157))
    current_selling = reg_params((410, 1468, 236, 100))
    current_sold = reg_params((364, 1565, 236, 100))
    budget = reg_params((900, 243, 330, 80))
