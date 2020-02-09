class Version:
    def __init__(self, version):
        self.value = version
        self.version_list = version.split('.')

    def divide(self, string):
        symb_list = []
        for ind, symbol in enumerate(string):
            if not symbol.isdigit():
                symb_list.append(string[:ind])
                symb_list.append(string[ind:].strip('-'))
                break
        # print('S list: ', symb_list)
        return symb_list

    def compare_lists(self, list_a, list_b):
        for a_elem, b_elem in zip(list_a, list_b):
            if a_elem.isdigit() and b_elem.isdigit():
                if a_elem < b_elem:
                    return 1
                elif a_elem > b_elem:
                    return 0
                else:
                    continue
            elif a_elem.isdigit() and not b_elem.isdigit():
                b_elem = self.divide(b_elem)
                if a_elem < b_elem[0]:
                    return 1
                elif a_elem > b_elem[0]:
                    return 0
                else:
                    return 0
            elif not a_elem.isdigit() and b_elem.isdigit():
                a_elem = self.divide(a_elem)
                if a_elem[0] < b_elem:
                    return 1
                elif a_elem[0] > b_elem:
                    return 0
                else:
                    return 1
            else:
                a_elem = self.divide(a_elem)
                b_elem = self.divide(b_elem)
                return self.compare_lists(a_elem, b_elem)
        else:
            return -1

    def __lt__(self, other):
        a = self.version_list
        b = other.version_list
        print(a, b, sep='\n')
        result = self.compare_lists(a, b)

        return True if result == 1 else False

    def __eq__(self, other):
        a = self.version_list
        b = other.version_list
        result = self.compare_lists(a, b)
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
