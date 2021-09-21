def decorator(func):
    def wrapper(*args, **kwargs):
        func()

    return wrapper
