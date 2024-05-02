import functools
import inspect
import time


def caching_decorator(max_size=None, expiration=None):
    cache = {}

    def inner_decorator(func):
        @functools.wraps(func)
        def cached_func(*args, **kwargs):
            signature = inspect.signature(func)
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()

            arg_dict = dict(bound_args.arguments)
            key = tuple(arg_dict.items())

            if key in cache:
                if expiration and time.time() - cache[key][1] > expiration:
                    del cache[key]
                else:
                    return cache[key][0]

            result = func(*args, **kwargs)
            cache[key] = (result, time.time())

            if max_size and len(cache) > max_size:
                oldest_key = min(cache, key=cache.get)
                del cache[oldest_key]

            return result

        return cached_func

    return inner_decorator


@caching_decorator(max_size=10, expiration=60)
def add(a, b):
    print("Calculating...")
    return a + b


print(add(3, 5))
print(add(2, 4))
