from itertools import zip_longest


class Comparator:

    def divide_to_letters_and_digit(self, string):
        symb_list = []
        new_substring = ''
        prev_ind = 0
        for ind, symbol in enumerate(string):
            if symbol in '0123456789':
                if ind - prev_ind > 1 and new_substring != '':
                    symb_list.append(new_substring)
                    symb_list.append(string[prev_ind + 1:ind].strip('-'))
                    new_substring = symbol
                elif ind - prev_ind > 1 and new_substring == '':
                    new_substring = string[:ind].strip('-')
                    prev_ind = ind
                else:
                    new_substring += symbol
                    prev_ind = ind
            if ind == len(string) - 1:
                symb_list.append(new_substring)
                if ind - prev_ind > 1:
                    symb_list.append(string[prev_ind + 1:ind])
                else:
                    symb_list.append(symbol)
        return symb_list

    def compare_lists(self, list_a, list_b):
        for a_elem, b_elem in zip_longest(list_a, list_b, fillvalue=''):
            if a_elem.isdigit() and b_elem.isdigit():
                if a_elem < b_elem:
                    return 1
                elif a_elem > b_elem:
                    return 0
                else:
                    continue
            elif a_elem.isdigit() and not b_elem.isdigit():
                b_elem = self.divide_to_letters_and_digit(b_elem)
                return 1 if a_elem < b_elem[0] else 0
            elif not a_elem.isdigit() and b_elem.isdigit():
                a_elem = self.divide_to_letters_and_digit(a_elem)
                return 0 if a_elem[0] > b_elem else 1
            else:
                if a_elem == '':
                    return 0
                elif b_elem == '':
                    return 1
                elif a_elem.isalpha() and b_elem.isalpha():
                    if a_elem < b_elem:
                        return 1
                    elif a_elem > b_elem:
                        return 0
                    else:
                        continue
                else:
                    a_elem = self.divide_to_letters_and_digit(a_elem)
                    b_elem = self.divide_to_letters_and_digit(b_elem)
                    return self.compare_lists(a_elem, b_elem)
        else:
            return -1


class Version:
    def __init__(self, version):
        self.value = version
        self.version_list = version.split('.')
        self.cmp = Comparator()

    def __lt__(self, other):
        result = self.cmp.compare_lists(self.version_list, other.version_list)
        return True if result == 1 else False

    def __eq__(self, other):
        result = self.cmp.compare_lists(self.version_list, other.version_list)
        return True if result == -1 else False


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
