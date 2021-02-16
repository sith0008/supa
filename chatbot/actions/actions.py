from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
)
from typing import Text, Dict, Any, List
from actions.api.knowledge_graph import KnowledgeGraphAPI # noqa
from actions.api.location import LocationAPI # noqa
from actions.api.validator import GeneralValidator # noqa
import os

knowledge_graph_api = KnowledgeGraphAPI(os.environ.get("BACKEND_HOST", "http://localhost:5000"))
location_api = LocationAPI(os.environ.get("BACKEND_HOST", "http://localhost:5000"))

class ValidateVerifyForm(FormValidationAction):
    '''
    validate all verify form fields
    '''
    def name(self):
        return "validate_verify_form"

    def validate_use_class(self,
                           value: Text,
                           dispatcher: CollectingDispatcher,
                           tracker: Tracker,
                           domain: Dict[Text, Any]
                           ):
        if knowledge_graph_api.is_valid_use_class(value):
            return {"use_class": value}
        else:
            dispatcher.utter_message(template="utter_invalid_use_class")
            return {"use_class": None}

    # TODO: uncomment after GeneralValidator is implemented
    def validate_gfa(self,
                           value: Text,
                           dispatcher: CollectingDispatcher,
                           tracker: Tracker,
                           domain: Dict[Text, Any]
                           ):
        if GeneralValidator.is_valid_float(value):
            return {"gross_floor_rea": value}
        else:
            dispatcher.utter_message(template="utter_invalid_gfa")
            return {"gross_floor_area": None}
    # TODO: uncomment after location DB is implemented
    # def validate_postal_code(self,
    #                        value: Text,
    #                        dispatcher: CollectingDispatcher,
    #                        tracker: Tracker,
    #                        domain: Dict[Text, Any]
    #                        ):
    #     if LocationAPI.is_valid_postal_code(value):
    #         return {"postal_code": value}
    #     else:
    #         dispatcher.utter_message(template="utter_invalid_postal_code")
    # TODO: uncomment after GeneralValidator is implemented
    def validate_floor(self,
                           value: Text,
                           dispatcher: CollectingDispatcher,
                           tracker: Tracker,
                           domain: Dict[Text, Any]
                           ):
        if GeneralValidator.is_valid_integer(value):
            return {"floor": value}
        else:
            dispatcher.utter_message(template="utter_invalid_floor")
            return {"floor": None}
    def validate_unit(self,
                           value: Text,
                           dispatcher: CollectingDispatcher,
                           tracker: Tracker,
                           domain: Dict[Text, Any]
                           ):
        if GeneralValidator.is_valid_integer(value):
            return {"unit": value}
        else:
            dispatcher.utter_message(template="utter_invalid_unit")
            return {"unit": None}

class ActionShowUseClasses(Action):
    '''
    Retrieve all specific use class from KG
    '''
    def name(self):
        return "action_show_all_use_classes"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[EventType]:
        use_class_list = knowledge_graph_api.get_all_use_classes()
        dispatcher.utter_message(
            text=f"These are the use classes that we use: \n {use_class_list}"
        )
        return []

class ActionGetSimilarCases(Action):
    '''
    Retrieve similar cases based on use class and prop type
    '''
    def name(self):
        return "action_get_similar_cases"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[EventType]:

        postal_code = tracker.get_slot("postal_code")
        use_class = tracker.get_slot("use_class")

        similar_cases_list = knowledge_graph_api.get_similar_cases(
            use_class=use_class,
            postal_code=postal_code,
        )

        processed_similar_cases_list = self.process_similar_cases_list(similar_cases_list)
        dispatcher.utter_message(
            text=f"These are the past cases similar to your application: \n {processed_similar_cases_list}"
        )
        return [SlotSet("similar_cases_list"), similar_cases_list]

    # TODO: to add processing code, for readability
    def process_similar_cases_list(self, similar_cases_list):
        return similar_cases_list


class ActionGetAddresses(Action):
    '''
    Retrieve addresses based on postal code
    Sets address_list slot to contain retrieved addresses
    '''
    def name(self):
        return "action_get_addresses"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[EventType]:
        postal_code = tracker.get_slot("postal_code")
        address_list = location_api.get_addresses_from_postal_code(postal_code)
        if len(address_list) >= 1:
            dispatcher.utter_message(
                text=f"I found {len(address_list)} addresses for this postal code. "
                     f"Could you confirm which one is it? \n {address_list}"
            )
        else:
            dispatcher.utter_message(
                text=f"I found the following address for this postal code. "
                     f"Could you confirm if this is correct? \n {address_list[0]}"
            )
        return [SlotSet("address_list"), address_list]

class ActionReviewVerifyForm(Action):
    '''
    Display filled slots to user
    '''
    def name(self):
        return "action_review_verify_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[EventType]:
        print("displaying slots")
        proposed_use_class = tracker.get_slot("use_class")
        proposed_use_desc = tracker.get_slot("use_description")
        postal_code = tracker.get_slot("postal_code")
        floor = tracker.get_slot("floor")
        unit = tracker.get_slot("unit")
        lot_number = tracker.get_slot("lot_number")
        gfa = tracker.get_slot("gross_floor_area")
        response = f"Proposed use class:  {proposed_use_class} \n" \
                   f"Proposed use description: {proposed_use_desc} \n" \
                   f"Postal code: {postal_code} \n" \
                   f"Floor: {floor} \n" \
                   f"Unit: {unit} \n" \
                   f"Lot number: {lot_number} \n" \
                   f"GFA: {gfa}"
        print(response)
        dispatcher.utter_message(template="utter_verify_form_inputs", form_inputs=response)
        return []


class ActionVerifyProposal(Action):
    '''
    Using filled slots, query guideline DB to get outcome
    '''

    def name(self):
        return "action_verify_proposal"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[EventType]:
        # TODO: add verification logic here
        print("verifying proposal")
        outcome = "APPROVED!!!"
        dispatcher.utter_message(template="utter_verified", outcome=outcome)
        return []


class ActionExplainOutcome(Action):
    '''
    Using filled slots, query guideline DB to get outcome
    vary reply for similar case vs user case
    '''
    def name(self):
        return "action_explain_outcome"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[EventType]:
        # TODO: add explain logic here
        print("explaining outcome")
        explanation = "I CANNOT EXPAIN YET!!!"
        dispatcher.utter_message(template="utter_explain_outcome", explanation=explanation)
        return []

class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        # data = tracker.latest_message["text"]
        # print(f"resetting slot {data}")
        # return [SlotSet(data), None]
        entities = tracker.latest_message["entities"]
        slot_set_events = []
        for entity in entities:
            print(entity['entity'])
            slot_set_events.append(SlotSet(entity['entity'], None))
        return slot_set_events

# class ActionSubmitProposal(Action):
#     '''
#
#     '''
#
# class ActionSetLiveMusic(Action):
#     '''
#     set live music slot to true/false
#     '''