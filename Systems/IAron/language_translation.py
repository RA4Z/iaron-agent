import json
import getpass

class Language:
    def __init__(self):
        self.language = open('Systems/IAron/languages/selected.txt', 'r').readline().strip()
        if self.language not in 'DE, EN, ES, FR, PT':
            self.language = 'EN'
        with open(f'Systems/IAron/languages/{self.language}.json', 'r', encoding='utf-8') as file:
            self.translations = json.load(file)

    def search(self, desired_field: str):
        text = str(self.translations.get(desired_field, self.translations.get('not_found'))).replace('$username',
                                                                                                     getpass.getuser().upper())
        return text
