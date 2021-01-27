from app.business import cases_service, conversation_service, resolution_service, validation_service, guidelines_service, use_class_service # noqa
from app.database import sql_db, graph_db # noqa
from app import supa # noqa


with supa.app_context():
    sql_engine = sql_db.engine
    neo4j_engine = graph_db
    cases_service = cases_service.CasesService(neo4j_engine)
    conversation_service = conversation_service.ConversationService(neo4j_engine)
    guidelines_service = guidelines_service.GuidelinesService(sql_engine)
    resolution_service = resolution_service.ResolutionService(neo4j_engine)
    validation_service = validation_service.ValidationService(neo4j_engine)
    use_class_service = use_class_service.UseClassService(neo4j_engine)
