

class Project():

    def __init__(self):

        self.id = str()

        self.name = str()
        self.description = str()
        self.created_at = str()

        self.dirList = dict()

class List():

    def __init__(self):

        self.id = str()

        self.name = str()
        self.project_id = str()
        self.created_at = str()

        self.dirLines = dict()

class Line():

    def __init__(self):
        self.id = str()

        self.name = str()
        self.tag = str()
        self.type = str()
        self.signal = str()
        self.pid = str()
        self.version = int()
        self.list_id = str()
        self.created_at = str()
