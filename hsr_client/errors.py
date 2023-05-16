# define Python user-defined exceptions
class InvalidLanguage(Exception):
    "Raised when the language is not of type Languages"
    pass

class InvalidItemType(Exception):
    "Raised when the passed SearchItem is not of required type"
    pass

class InvalidSearchItem(Exception):
    "Raised provided item is not a SearchItem"
    pass