import os
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


def delete_dir(path):
    for p, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(p, file))
        for directory in dirs:
            delete_dir(os.path.join(p, directory))
    os.rmdir(path)
