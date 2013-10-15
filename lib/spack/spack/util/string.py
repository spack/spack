
def comma_list(sequence, article=''):
    if type(sequence) != list:
        sequence = list(sequence)

    if not sequence:
        return
    elif len(sequence) == 1:
        return sequence[0]
    else:
        out =  ', '.join(str(s) for s in sequence[:-1])
        out += ', '
        if article:
            out += article + ' '
        out += str(sequence[-1])
        return out

def comma_or(sequence):
    return comma_list(sequence, 'or')


def comma_and(sequence):
    return comma_list(sequence, 'and')
