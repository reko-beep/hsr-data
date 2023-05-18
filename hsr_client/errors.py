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

class InvalidSearchItem(Exception):
    "Raised provided item is not a SearchItem"
    pass

class InvalidFilter(Exception):
    def __init__(self, filters) -> None:
        super().__init__()
        self.filters = filters
        

    def __str__(self) -> str:
        return f"Provided parameter doesnot exist in search item, available paramaters for filter [{' ,'.join(self.filters)}]"