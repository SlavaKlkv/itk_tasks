from datetime import datetime


class AttrAddingMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class NewClass(metaclass=AttrAddingMeta):
    pass


if __name__ == "__main__":
    assert hasattr(NewClass, "created_at")
    assert isinstance(NewClass.created_at, datetime)

    print(NewClass.created_at)
