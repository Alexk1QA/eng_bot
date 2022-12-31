#

#


class TestClass1:

    @staticmethod
    def test_1_1():
        pass

    @classmethod
    def test_1_2(cls):
        pass


class TestClass2:

    @staticmethod
    def test_2_1():
        pass

    @classmethod
    def test_2_2(cls):
        pass


class TestClass3:

    @staticmethod
    def test_3_1():
        pass

    @classmethod
    def test_3_2(cls):
        pass


def annotations_test(a: [int, str], b: int) -> [int, str]:
    """
    :param a: fsd
    :param b: fds
    :param c: fds
    :return: fds
    """
    if type(a) == int:
        return a + b

    elif type(a) == str:
        return a * b

    return [1]


print(annotations_test("e", 5))
print(annotations_test.__annotations__)
