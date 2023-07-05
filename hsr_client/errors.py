# define Python user-defined exceptions
class InvalidLanguage(Exception):
    "Raised when the language is not of type Languages"
    pass



class InvalidSearchItem(Exception):
    """raised when incorrect searchitem is used."""
    pass



class InvalidFilter(Exception):
    def __init__(self, filters) -> None:
        super().__init__()
        self.filters = filters
        

    def __str__(self) -> str:
        return f"Provided parameter doesnot exist in search item, available paramaters for filter [{' ,'.join(self.filters)}]"
    
class EmptyResponse(Exception):
    """Raised when returned data is empty, 404 response is got"""

class BackendError(Exception):
    """
    Raised when a problem is detected with backend, mostly happens when
    backend changes , please report such errors
    """