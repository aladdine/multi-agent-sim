import uuid 

class Entity:
    def __init__(self, name, type, parent, children):
        self.id = self.id = uuid.uuid4().__str__()
        self.name = name
        self.type = type
        self.parent = parent
        self.children = children
