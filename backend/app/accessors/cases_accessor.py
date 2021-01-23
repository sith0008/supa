from backend.app.models.past_case import PastCase

class ConversationAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, past_case: PastCase):
        raise NotImplementedError

    def read(self, past_case_id: str):
        raise NotImplementedError

    def update(self, past_case: PastCase):
        raise NotImplementedError

    def delete(self, past_case_id: str):
        raise NotImplementedError
