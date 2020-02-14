from itertools import zip_longest


class Comparator:

    def divide_to_letters_and_digit(self, string):
        letters_and_numbers_list = []
        new_substring = ''
        prev_ind = 0
        for ind, symbol in enumerate(string):
            if symbol.isdigit():
                if ind - prev_ind > 1 and new_substring != '':
                    letters_and_numbers_list.append(new_substring)
                    letters_and_numbers_list.append(string[prev_ind + 1:ind].strip('-'))
                    new_substring = symbol
                elif ind - prev_ind > 1 and new_substring == '':
                    new_substring = string[:ind].strip('-')
                    prev_ind = ind
                else:
                    new_substring += symbol
                    prev_ind = ind
            if ind == len(string) - 1:
                letters_and_numbers_list.append(new_substring)
                if ind - prev_ind > 1:
                    letters_and_numbers_list.append(string[prev_ind + 1:].strip('-'))
                else:
                    letters_and_numbers_list.append(symbol)
        return letters_and_numbers_list

    def compare_lists(self, list_a, list_b):
        less, equal = False, False  # less - list_a < list_b, equal - list_a == list_b
        for a_elem, b_elem in zip_longest(list_a, list_b, fillvalue=''):
            if a_elem.isdigit() and b_elem.isdigit():
                if a_elem < b_elem:
                    less = True
                    return less, equal
                elif a_elem > b_elem:
                    return less, equal
                else:
                    continue
            elif a_elem.isdigit() and not b_elem.isdigit():
                b_elem = self.divide_to_letters_and_digit(b_elem)
                return (True, equal) if a_elem < b_elem[0] else (less, equal)
            elif not a_elem.isdigit() and b_elem.isdigit():
                a_elem = self.divide_to_letters_and_digit(a_elem)
                return (less, equal) if a_elem[0] > b_elem else (True, equal)
            elif a_elem.isalpha() and b_elem.isalpha():
                if a_elem < b_elem:
                    less = True
                    return less, equal
                elif a_elem > b_elem:
                    return less, equal
                else:
                    continue
            else:
                if a_elem == '':
                    return less, equal
                elif b_elem == '':
                    less = True
                    return less, equal
                else:
                    a_elem = self.divide_to_letters_and_digit(a_elem)
                    b_elem = self.divide_to_letters_and_digit(b_elem)
                    return self.compare_lists(a_elem, b_elem)
        else:
            equal = True
            return less, equal


class Version:
    def __init__(self, version):
        self.value = version
        self.version_list = version.split('.')
        self.cmp = Comparator()

    def __lt__(self, other):
        is_less, _ = self.cmp.compare_lists(self.version_list, other.version_list)
        return is_less

    def __eq__(self, other):
        _, is_equal = self.cmp.compare_lists(self.version_list, other.version_list)
        return is_equal


def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),
        ('1.0.0-rc.1', '1.0.0')
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), 'lt failed'
        assert Version(version_2) > Version(version_1), 'gt failed'
        assert Version(version_2) != Version(version_1), 'ne failed'


if __name__ == '__main__':
    main()
