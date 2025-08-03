import unittest.mock


def lru_cache(func=None, *, maxsize=128):
    def decorator(decorated_func):
        cache = {}
        keys_queue = []

        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                keys_queue.remove(key)
                keys_queue.append(key)
                return cache[key]
            result = decorated_func(*args, **kwargs)
            cache[key] = result
            keys_queue.append(key)
            if len(keys_queue) > maxsize:
                lru = keys_queue.pop(0)
                del cache[lru]
            return result

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
