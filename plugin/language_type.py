def dict_type_by_lang(language: str):
    if language == "java":
        return {0: "String", 1: "Boolean", 2: "Byte", 3: "Short", 4: "Integer", 5: "Long", 6: "Float", 7: "Double",
                8: "Char", 9: "LocalDateTime"}
    elif language == "python":
        return {0: "str", 1: "bool", 2: "", 3: "int", 4: "int", 5: "int", 6: "float", 7: "float",
                8: "int", 9: "datetime"}
    else:
        return {0: ""}


def dict_type_by_lang_code(language_code: str):
    if language_code == "LAN100001":
        return {0: "String", 1: "Boolean", 2: "Byte", 3: "Short", 4: "Integer", 5: "Long", 6: "Float", 7: "Double",
                8: "Char", 9: "LocalDateTime"}
    elif language_code == "LAN100003":
        return {0: "str", 1: "bool", 2: "", 3: "int", 4: "int", 5: "int", 6: "float", 7: "float",
                8: "int", 9: "datetime"}
    else:
        return {0: ""}
