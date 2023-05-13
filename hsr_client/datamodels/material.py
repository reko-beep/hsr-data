from pydantic import BaseModel

class Material(BaseModel):
    name: str
    description: str

    # TODO: determine icon stratergy
    # is it image, or url or what?
    pass


    def __hash__(self):
        return hash(self.name)
