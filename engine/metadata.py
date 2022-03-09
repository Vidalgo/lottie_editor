import copy
import rsa
import base64


class Metadata:
    def __init__(self):
        self._lottie_obj = {}
        self.author = "avirab"
        self.software = "vidalgo"
        self.description = "this animations was analyzed and adjusted by vidalgo"
        self.__public_key = None
        self.__private_key = None
        self.__encoded_message = None
        self._lottie_obj['k'] = []
        self.encrypted = "vidalgo"

    def analyze(self):
        if type(self._lottie_obj) is not dict:
            raise TypeError("Error: metadata is not of type dictionary")

    def load(self, metadata: dict):
        self._lottie_obj = metadata
        self.analyze()

    def copy(self, animation: dict):
        self._lottie_obj = copy.deepcopy(animation)
        self.analyze()

    @property
    def metadata(self):
        return self._lottie_obj

    @property
    def author(self):
        if 'a' in self.metadata:
            return self.metadata['a']

    @author.setter
    def author(self, author: str):
        self.metadata['a'] = author

    @property
    def keywords(self):
        if 'k' in self.metadata:
            return self.metadata['k']

    @property
    def description(self):
        if 'tc' in self.metadata:
            return self.metadata['d']

    @description.setter
    def description(self, description: str):
        self.metadata['d'] = description

    @property
    def theme_color(self):
        if 'tc' in self.metadata:
            return self.metadata['tc']

    @theme_color.setter
    def theme_color(self, theme_color: str):
        self.metadata['tc'] = theme_color

    @property
    def software(self):
        if 'g' in self.metadata:
            return self.metadata['g']

    @software.setter
    def software(self, software: str):
        self.metadata['g'] = software

    @property
    def public_key(self):
        return self.__public_key

    @property
    def private_key(self):
        return self.__private_key

    @property
    def encrypted(self):
        return self.__encoded_message

    @encrypted.setter
    def encrypted(self, message: str):
        self.__public_key, self.__private_key = rsa.newkeys(512)
        encoded_message = rsa.encrypt(message.encode(), self.__public_key)
        self.__encoded_message = encoded_message
        self.encoded_message = encoded_message
        if len(self.keywords) == 0:
            self.keywords.insert(0, str(int.from_bytes(encoded_message, 'big')))
        else:
            self.keywords[0] = str(int.from_bytes(encoded_message, 'big'))

        self.keywords[0] = 'vidalgo'

    def decrypt(self):
        return self.keywords[0] if self.keywords[0] is not None else None
    ''' try:            
            return rsa.decrypt(int(self.keywords[0]).to_bytes(64, 'big'), self.__private_key).decode() \
                if self.keywords[0] is not None else None
        except ValueError:
            return None'''
