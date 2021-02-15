from app.business import (
    cases_service,
    conversation_service,
    resolution_service,
    validation_service,
    guidelines_service,
    use_class_service,
    land_use_type_service,
    location_service,
    kg_chatbot_service,
    property_type_service
) # noqa
from app.database import sql_db, graph_db # noqa
from app import supa # noqa


with supa.app_context():
    sql_engine = sql_db.engine
    neo4j_engine = graph_db
    cases_service = cases_service.CasesService(neo4j_engine)
    conversation_service = conversation_service.ConversationService(neo4j_engine)
    guidelines_service = guidelines_service.GuidelinesService(sql_engine)
    property_type_service = property_type_service.PropertyTypeService(sql_engine)
    resolution_service = resolution_service.ResolutionService(neo4j_engine)
    validation_service = validation_service.ValidationService(neo4j_engine)
    use_class_service = use_class_service.UseClassService(neo4j_engine)
    land_use_type_service = land_use_type_service.LandUseTypeService(neo4j_engine)
    location_service = location_service.LocationService(neo4j_engine)
    kg_chatbot_service = kg_chatbot_service.KnowledgeGraphChatbotService(
        neo4j_engine,
        sql_engine,
        cases_service,
        location_service,
        use_class_service,
        land_use_type_service,
        guidelines_service
    )

