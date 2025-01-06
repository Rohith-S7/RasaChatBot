from typing import Text, List, Any, Dict
import json
from datetime import datetime
import os
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from typing import Optional, List, Text
from rasa_sdk.events import Restarted
from rasa_sdk.events import FollowupAction, AllSlotsReset
import requests
from rasa_sdk.events import UserUtteranceReverted

import os
import re
import nltk

nltk.download('words')
from nltk.corpus import words

# Create a set of English words for reference
english_words = set(words.words())


def is_gibberish(value):
    # Split the input value into words
    words_in_value = value.split()

    # Check each word against the set of English words
    for word in words_in_value:
        if word.lower() not in english_words:
            return True  # If any word is not found in English words, consider it gibberish
    return False  # All words are in English, not gibberish


class ValidateMedicalCheckForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_medical_check_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        return ["symptoms", "medication_status", "triggers", "lifestyle_changes", "consultation", "medical_history",
                "current_medication", "environmental_factors", "additional_info"]

    async def validate_symptoms(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"symptoms": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"symptoms": None}

        return {"symptoms": value}

    async def validate_medication_status(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                         domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"medication_status": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"medication_status": None}

        return {"medication_status": value}

    async def validate_triggers(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"triggers": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"triggers": None}

        return {"triggers": value}

    async def validate_lifestyle_changes(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                         domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"lifestyle_changes": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"lifestyle_changes": None}

        return {"lifestyle_changes": value}

    async def validate_consultation(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                    domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"consultation": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"consultation": None}

        return {"consultation": value}

    async def validate_medical_history(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                       domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"medical_history": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"medical_history": None}

        return {"medical_history": value}

    async def validate_current_medication(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                          domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"current_medication": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"current_medication": None}

        return {"current_medication": value}

    async def validate_environmental_factors(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                             domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"environmental_factors": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"environmental_factors": None}

        return {"environmental_factors": value}

    async def validate_additional_info(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                       domain: DomainDict) -> Dict[Text, Any]:
        if value.lower() == 'exit':
            dispatcher.utter_message(text="Restarting conversation...")
            return {"additional_info": None, "requested_slot": None}

        if is_gibberish(value):
            dispatcher.utter_message(text="I couldn't understand that. Could you please rephrase?")
            return {"additional_info": None}

        action_save = ActionSaveConversation()
        action_save.run(dispatcher, tracker, domain)  # Save conversation

        dispatcher.utter_message(text="SWITCH_TO_LLM")
        return [AllSlotsReset()]

        # return {"additional_info": value}
        return await super(ValidateMedicalCheckForm, self).run(dispatcher, tracker, domain)


# [The rest of your action classes remain unchanged...]


class ActionCheckDeny(Action):
    def name(self) -> Text:
        return "action_check_deny"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print()
            print("Action check_deny")
            requested_slot = tracker.get_slot("requested_slot")
            print(requested_slot)

            # if requested_slot == 'disease':
            #    dispatcher.utter_message(response="utter_ask_disease")

            if requested_slot == 'symptoms':
                return [SlotSet("symptoms", "Not Given")]

            elif requested_slot == 'medication_status':
                return [SlotSet("medication_status", "Not Given")]

            elif requested_slot == 'triggers':
                return [SlotSet("triggers", "Not Given")]

            elif requested_slot == 'lifestyle_changes':
                return [SlotSet("lifestyle_changes", "Not Given")]

            elif requested_slot == 'consultation':
                return [SlotSet("consultation", "Not Given")]

            elif requested_slot == 'medical_history':
                return [SlotSet("medical_history", "Not Given")]

            elif requested_slot == 'current_medication':
                return [SlotSet("current_medication", "Not Given")]

            elif requested_slot == 'environmental_factors':
                return [SlotSet("environmental_factors", "Not Given")]

            elif requested_slot == 'additional_info':
                return [SlotSet("additional_info", "Not Given")]

        except Exception as e:
            print(str(e))
            return []


class ActionSaveConversation(Action):

    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    TOKEN = "hf_gfbm"

    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract conversation data
        events = tracker.events

        if not os.path.isfile('conversation.json'):
            with open('conversation.json', 'w') as file:
                file.write("[]")

        conversation = []
        turn = {}

        for event in events:
            if event.get("event") == "bot":
                turn["Chatdoctor"] = event.get("text")
            elif event.get("event") == "user":
                turn["human"] = event.get("text")
                if "Chatdoctor" in turn:
                    conversation.append(turn.copy())
                    turn = {}

        formatted_conversation = ""
        for turn in conversation:
            formatted_conversation += f"ChatDoctor: {turn['Chatdoctor']},\nPatient: {turn['human']}\n"

        data = {
            'inputs': formatted_conversation,
            'options': {
                'flag': 'fromrasa'
            }
        }
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        try:
            response = requests.post(self.url, headers=headers, json=data)  # Sending JSON data
            if response.status_code == 200:
                print(f'Success: {response.text}')
                # rasa_response = response.text
                llm_responses = response.json()
                for llm_response in llm_responses:
                    generated_text = llm_response.get('generated_text')
                    if generated_text:
                        dispatcher.utter_message(text=generated_text)
            else:
                print(f'Error: {response.text}')
        except Exception as e:
            print(f"Failed to send data to llm: {e}")

        return []


class ActionRestartConversation(Action):
    def name(self) -> Text:
        return "action_restart_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # You can send a message to the user here if necessary
        dispatcher.utter_message(text="Restarting conversation...")

        # Emit the 'Restarted' event to reset the tracker
        return [Restarted()]


