class MyClass:
    def __init__(self, value):
        self._value = value  # Use a private attribute for internal storage

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        print(f"Setting value to {new_value}")
        self._value = new_value


obj = MyClass(10)
print(obj.value)  # Get value
obj.value = 20
