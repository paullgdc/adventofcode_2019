start = 236491
end =  713787

def number_to_digits(num, base=10):
    quotient = num
    written = []
    while quotient > 0:
        written.append(quotient % base)
        quotient = quotient // base
    return written


def check_validity(digits):
    if len(digits) != 6:
        return False
    last_digit = 10
    has_single_double = False
    has_double = False
    is_in_streak = False
    for d in digits:
        if last_digit == d:
            has_double = True
            has_single_double = has_single_double or not is_in_streak
            is_in_streak = True
        else:
            is_in_streak = False
        if last_digit < d:
            return False
        last_digit = d
    return has_single_double

print(sum((check_validity(number_to_digits(i)) for i in range(start, end))))
