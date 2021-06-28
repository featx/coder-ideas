import re


def len_utf8(string: str):
    return len(string.encode('utf-8'))


def camel(s: str, lower_1=False):
    camel_s = re.sub(r"(\s|_|-)+", " ", s).title().replace(" ", "")
    if lower_1:
        return camel_s[0].lower() + camel_s[1:]
    return camel_s


def snake(s: str):
    return '_'.join(re.sub('([A-Z][a-z]+)', r' \1',
                           re.sub('([A-Z]+)', r' \1',
                                  s.replace('-', ' '))).split()).lower()


def kebab(s: str):
    return re.sub(r"(\s|_|-)+", "-",
                  re.sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                         lambda mo: mo.group(0).lower(), s))


def is_anagram(str1: str, str2: str):
    _str1, _str2 = str1.replace(" ", ""), str2.replace(" ", "")

    if len(_str1) != len(_str2):
        return False
    else:
        return sorted(_str1.lower()) == sorted(_str2.lower())


def palindrome(string: str):
    s = re.sub('[\W_]', '', string.lower())
    return s == s[::-1]
