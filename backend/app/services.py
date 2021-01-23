from app.business import cases_service, conversation_service, resolution_service, validation_service, guidelines_service
from app.database import db
from app import supa

with supa.app_context():
    engine = db.engine
    cases_service = cases_service.CasesService(engine)
    conversation_service = conversation_service.ConversationService(engine)
    guidelines_service = guidelines_service.GuidelinesService(engine)
    resolution_service = resolution_service.ResolutionService(engine)
    validation_service = validation_service.ValidationService(engine)

