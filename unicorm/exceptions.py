class NoRowFoundError(Exception):
    def __init__(self):
        msg = "No row was found"
        super().__init__(msg)
