from backend.app.models.conversation import Conversation

class ConversationAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, conversation: Conversation):
        raise NotImplementedError

    def read(self, conversation_id: int):
        raise NotImplementedError

    def update(self, conversation: Conversation):
        raise NotImplementedError

    def delete(self, conversation_id: int):
        raise NotImplementedError
