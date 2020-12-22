from service.language import LanguageService
from service.model.language import Language


class LanguageManager:

    def __init__(self, services):
        self.__language_service: LanguageService = services["language"]

    def list_all(self):
        result = []
        languages = self.__language_service.list_all()
        for language in languages:
            result.append(_from_language(language))
        return result


def _from_language(language: Language):
    return {
        "id": language.id,
        "code": language.code,
        "name": language.name
    }