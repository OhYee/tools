import os


class I18n:
    def __init__(self,  text_list, default_language=None):
        if default_language == None:
            default_language = os.environ.get(
                'LANG', "en_US"
            ).split(".")[0]
        self.default_language = default_language
        self.texts = text_list

    def getLanguage(self, language=None):
        if language == None:
            language = self.default_language
        return self.texts.get(self.default_language, {})

    def get(self, key, default_text="", language=None):
        return self.getLanguage(language).get(key, default_text)
