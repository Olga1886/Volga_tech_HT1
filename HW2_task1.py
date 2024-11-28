class StringList:
    def __init__(self, *items):
        self._data = [str(item) for item in items]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

# Usage example

my_string_list = StringList(2, 3.14, ["t", "r", "y"])

for el in my_string_list:
    assert type(el) == str
    print(my_string_list)