from threading import Lock


default_lock = Lock()


def synchronized(func):
    def function(*args, **kwargs):
        default_lock.acquire()
        try:
            return func(*args, **kwargs)
        finally:
            default_lock.release()
    return function


class IdGenerate:

    def next_id(self):
        return 0

    def next_base_36(self):
        return base_n(self.next_id(), 36)


def base_n(num, n):
    return ((num == 0) and "0") or (base_n(num // n, n).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % n])
