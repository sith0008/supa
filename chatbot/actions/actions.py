# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# TODO: add actions here, instantiate the 3 classes in the api folder
import logging
import json
import requests
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
from actions.api.knowledge_graph import KnowledgeGraphAPI


class ValidateVerifyForm(FormValidationAction):
    '''
    validate all form fields
    '''
    raise NotImplementedError


class ActionShowUseClasses(Action):
    '''
    Retrieve all specific use class from KG
    '''
    raise NotImplementedError

class ActionGetSimilarCases(Action):
    '''
    Retrieve similar cases based on use class and prop type
    '''
    raise NotImplementedError


class ActionGetAddresses(Action):
    '''
    Retrieve addresses based on postal code
    Sets address_list slot to contain retrieved addresses
    '''
    raise NotImplementedError


class ActionVerifyProposal(Action):
    '''
    Using filled slots, query guideline DB to get outcome
    '''
    raise NotImplementedError


class ActionExplainOutcome(Action):
    '''
    Using filled slots, query guideline DB to get outcome
    vary reply for similar case vs user case
    '''
    raise NotImplementedError


class ActionSubmitProposal(Action):
    '''

    '''

class ActionSetLiveMusic(Action):
    '''
    set live music slot to true/false
    '''