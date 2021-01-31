import logging

log = logging.getLogger('root')

class KnowledgeGraphChatbotService:
    def __init__(self, graph, sql_engine):
        self.graph = graph
        self.engine = sql_engine