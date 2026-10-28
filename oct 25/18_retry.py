from functools import wraps

def retry(times=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    result = func(*args,**kwargs)
                    return result
                except Exception as e:
                    if i == times-1:
                        raise

        return wrapper
    return decorator


@retry(times=3)
def divide_zero():
    error = 2 / 0

divide_zero()