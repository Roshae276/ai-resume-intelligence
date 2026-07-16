class ResumeException(Exception):

    def __init__(self, message: str):
        self.message = message


class JobException(Exception):

    def __init__(self, message: str):
        self.message = message


class ATSException(Exception):

    def __init__(self, message: str):
        self.message = message