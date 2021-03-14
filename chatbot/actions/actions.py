from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormValidationAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
)
from typing import Text, Dict, Any, List, Optional
from actions.api.knowledge_graph import KnowledgeGraphAPI # noqa
from actions.api.location import LocationAPI # noqa
from actions.api.validator import GeneralValidator # noqa
from actions.api.guidelines import GuidelinesAPI # noqa
import os

knowledge_graph_api = KnowledgeGraphAPI(os.environ.get("BACKEND_HOST", "http://localhost:5000"))
location_api = LocationAPI(os.environ.get("BACKEND_HOST", "http://localhost:5000"))
guidelines_api = GuidelinesAPI(os.environ.get("BACKEND_HOST", "http://localhost:5000"))

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
            return {"use_class": value.title()}
        else:
            dispatcher.utter_message(template="utter_invalid_use_class", use_class_list=knowledge_graph_api.get_all_use_classes())
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

    def validate_postal_code(self,
                           value: Text,
                           dispatcher: CollectingDispatcher,
                           tracker: Tracker,
                           domain: Dict[Text, Any]
                           ):
        if location_api.is_valid_postal_code(value):
            return {"postal_code": value}
        else:
            dispatcher.utter_message(template="utter_invalid_postal_code")
            return {"postal_code": None}

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
        return [SlotSet("similar_cases_list", similar_cases_list)]

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

    def process_address_list(self, address_list):
        processed_list = ""
        for i, address in enumerate(address_list):
            block = address["block"]
            road = address["road"]
            processed = f"{i+1}. {block} {road} \n"
            processed_list += processed
        return processed_list

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[EventType]:
        postal_code = tracker.get_slot("postal_code")
        address_list = location_api.get_addresses_from_postal_code(postal_code)
        processed = self.process_address_list(address_list)
        if len(address_list) > 1:
            dispatcher.utter_message(
                text=f"I found {len(address_list)} addresses for this postal code. "
                     f"Could you confirm which one is it? \n\n {processed}"
            )
        else:
            dispatcher.utter_message(
                text=f"I found the following address for this postal code. "
                     f"Could you confirm if this is correct? \n\n {processed}"
            )
        return [SlotSet("address_list", address_list), SlotSet("address_checked", False)]


class ActionSetAddressSlots(Action):
    '''
    Sets address slots
    '''
    def name(self):
        return "action_set_address_slots"

    def resolve_ordinal(self, text):
        if any(s in text.lower() for s in ["first", "1st", "one"]):
            return 0
        elif any(s in text.lower() for s in ["second", "2nd", "two"]):
            return 1
        elif any(s in text.lower() for s in ["third", "3rd", "three"]):
            return 2
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[EventType]:
        ordinal = 0
        intent = tracker.latest_message['intent'].get('name')
        if intent == "enter_ordinal":
            ordinal = self.resolve_ordinal(tracker.latest_message["text"])
        address_list = tracker.get_slot("address_list")
        address = address_list[ordinal]
        return [SlotSet("block", address["block"]), SlotSet("road", address["road"]), SlotSet("address_checked", True)]

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
        block = tracker.get_slot("block")
        road = tracker.get_slot("road")
        postal_code = tracker.get_slot("postal_code")
        floor = tracker.get_slot("floor")
        unit = tracker.get_slot("unit")
        lot_number = tracker.get_slot("lot_number")
        gfa = tracker.get_slot("gross_floor_area")

        try:
            if int(floor) < 10:
                floor = "0"+str(floor)
        except ValueError:
            pass

        try:
            if int(unit) < 10:
                unit = "0"+str(unit)
        except ValueError:
            pass

        response = f"Proposed use class:  {proposed_use_class} \n" \
                   f"Proposed use description: {proposed_use_desc} \n" \
                   f"Address: {block} {road} #{floor}-{unit} {postal_code} \n" \
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
        postal_code = tracker.get_slot("postal_code")
        use_class = tracker.get_slot("use_class")
        property_type = location_api.get_property_type_from_postal_code(postal_code)
        print(f"use_class: {use_class}")
        print(f"property_type: {property_type}")
        if not property_type:
            dispatcher.utter_message(template="utter_verified", outcome="Not allowed.")
            return []
        outcome = guidelines_api.get_eval_outcome(property_type, use_class)
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

class ActionGetAllUseClasses(Action):
    def name(self) -> Text:
        return "action_get_all_use_classes"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        use_classes = knowledge_graph_api.get_all_use_classes()
        dispatcher.utter_message(template="utter_use_classes",
                                 use_class_list=use_classes)
        return []


class ActionGetDefinition(Action):
    def name(self) -> Text:
        return "action_get_definition"

    def get_use_class_from_entity(self, entity):
        entity_to_use_class_map = {
            "restaurant": "Restaurant",
            "barpub": "Bar/Pub",
            "shop": "Shop",
            "amusement_centre": "Amusement Centre",
            "massage_establishment": "Massage Establishment"
        }
        if entity in entity_to_use_class_map:
            return entity_to_use_class_map[entity]
        return None

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message["entities"]
        slot_set_event = None
        for entity in entities:
            use_class = self.get_use_class_from_entity(entity['entity'])
            if use_class:
                slot_set_event = SlotSet("current_use_class", use_class)
                definition = knowledge_graph_api.get_definition(use_class)
                dispatcher.utter_message(template="utter_definition",
                                         definition=definition)
            else:
                dispatcher.utter_message(text=f"Sorry, I didn't understand the use class {entity['entity']}")
        return [slot_set_event] if slot_set_event else []


class ActionGetRequirements(Action):
    def name(self) -> Text:
        return "action_get_requirements"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        current_use_class = tracker.get_slot("current_use_class")
        if not current_use_class:
            dispatcher.utter_message(text="Please specify a use class!")
        else:
            requirements = knowledge_graph_api.get_requirements(current_use_class)
            dispatcher.utter_message(template="utter_requirements", requirements=requirements)
        return []


class ActionGetExamples(Action):
    def name(self) -> Text:
        return "action_get_examples"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        current_use_class = tracker.get_slot("current_use_class")
        if not current_use_class:
            dispatcher.utter_message(text="Please specify a use class!")
        else:
            examples = knowledge_graph_api.get_examples(current_use_class)
            dispatcher.utter_message(template="utter_examples", examples=examples)
        return []


class ActionGetDifferences(Action):
    def name(self) -> Text:
        return "action_get_differences"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        # entities = tracker.latest_message["entities"]
        raise NotImplementedError
