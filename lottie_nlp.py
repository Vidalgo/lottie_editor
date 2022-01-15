import string
import enchant
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter, WikiWordFilter, HTMLChunker


class Lottie_nlp:
    def __init__(self, dictionary="en_US"):
        if not self.dictionary_exists(dictionary):
            raise TypeError("Error: dictionary does not exist")
        self.dictionary = enchant.Dict(dictionary)
        self.tokenizer = None
        self.set_tokenizer()

    def set_tokenizer(self, dictionary="en_US", chunkers=None, filters=None):
        self.tokenizer = get_tokenizer(dictionary, filters=filters, chunkers=chunkers)

    @staticmethod
    def dictionary_exists(dictionary: str):
        return enchant.dict_exists(dictionary)

    @staticmethod
    def list_languages():
        return enchant.list_languages()

    @staticmethod
    def contains_number(source: str):
        if True in [char.isdigit() for char in source]:
            return True
        return False

    @staticmethod
    def all_letters(source: str):
        return source.isalpha()

    @staticmethod
    def all_numbers(source: str):
        return source.isdecimal()

    @staticmethod
    def to_lower(source: str):
        return source.lower()

    @staticmethod
    def contains_sub_string(source: str, sub_string: str):
        return sub_string in source

    @staticmethod
    def remove_numbers(source: str):
        #return re.sub(r'\d+', '', source)
        return source.translate(str.maketrans('', '', string.digits))

    @staticmethod
    def remove_punctuation(source: str):
        return source.translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def remove_white_spaces(source: str):
        return source.replace(" ", "")

    def is_in_english(self, source: str):
        return self.dictionary.check(source)

    def suggest_other_words(self, source: str):
        return self.dictionary.suggest(source)

    def tokenize(self, source: str):
        return [w for w in self.tokenizer(source)]


'''str1 = "Hello Rivia world!, this is the yeer 2022.01 and I am chacking #$! the nlp package fot Lottie files."
lnlp = Lottie_nlp()
print(lnlp.list_languages())
words = lnlp.tokenize(str1)
print(words)
print(lnlp.is_in_english(words[0][0]))
print(lnlp.is_in_english(words[1][0]))
print(lnlp.suggest_other_words(words[1][0]))
print(lnlp.suggest_other_words(words[6][0]))
print(lnlp.suggest_other_words(words[10][0]))
print(lnlp.suggest_other_words(words[14][0]))
print()
str2 = "  ,0  T1., e2.., s34., 64   t6,, in5.   g66!  "
print(str2)
str2 = lnlp.remove_white_spaces(str2)
print(str2)
str2 = lnlp.remove_numbers(str2)
print(str2)
str2 = lnlp.remove_punctuation(str2)
print(str2)
print()
str3 = "Does This strIng contAin layErs or shAPes?"
print(str3)
str3 = lnlp.to_lower(str3)
print(str3)
print(lnlp.contains_sub_string(str3, "precomp"))
print(lnlp.contains_sub_string(str3, "layers"))
print(lnlp.contains_sub_string(str3, "shapes"))
print()
print(lnlp.all_numbers("1234"))
print(lnlp.all_numbers("1.234"))
print(lnlp.all_numbers("12r34"))
print(lnlp.all_numbers(" 1234 "))
print(lnlp.all_numbers("1 234"))
print(lnlp.all_numbers("1234$"))
print()
print(lnlp.all_letters("abcd"))
print(lnlp.all_letters("abc1d"))
print(lnlp.all_letters("abcd#%"))
print(lnlp.all_letters("abcd "))
print()
print(lnlp.contains_number("abcd"))
print(lnlp.contains_number("abc1d"))
print(lnlp.contains_number("abcd#%"))
print(lnlp.contains_number("abcd "))'''

