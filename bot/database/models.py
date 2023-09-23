class User:

    def __init__(self, id, username, firstname, lastname, role='user', language='en'):
        self.id: str = id
        self.username: str = username
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.role: str = role
        self.language: str = language

    def __eq__(self, other):
        if isinstance(other, User):
            return (
                self.id == other.id and
                self.username == other.username and
                self.firstname == other.firstname and
                self.lastname == other.lastname and
                self.role == other.role and
                self.language == other.language
            )
        return False
