from src.singleton_import import instance as import_singleton


# Singleton через метакласс
class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class MetaSingleton(metaclass=SingletonMeta):
    pass


# Singleton через __new__
class NewSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Проверка
if __name__ == "__main__":
    a = MetaSingleton()
    b = MetaSingleton()
    print(a is b)  # True, обе переменные указывают на один и тот же объект

    c = NewSingleton()
    d = NewSingleton()
    print(c is d)  # True

    e = import_singleton
    f = import_singleton
    print(e is f)  # True
    print(e is import_singleton)  # True
