# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from pymongo import MongoClient
# import re

# class ActionAskSymptom(Action):
#     def name(self) -> Text:
#         return "action_ask_symptom"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # Detect language by checking if message contains Gujarati Unicode range
#         user_message = tracker.latest_message.get('text', '')
#         lang = "gu" if re.search(r'[\u0A80-\u0AFF]', user_message) else "en"

#         # Connect to MongoDB
#         client = MongoClient("mongodb+srv://aayupatel015:aayu%407991@cluster0.xq5rv0d.mongodb.net/")
#         db = client["medical_chatbot"]
#         collection = db["symptoms"]

#         # Fetch symptoms from DB (limit to 20 for buttons)
#         symptoms = collection.find().limit(20)
#         buttons = []

#         # Prepare buttons for the frontend, showing symptom names in user language
#         for symptom in symptoms:
#             name = symptom.get(f"symptom_{lang}")
#             if name:
#                 buttons.append({
#                     "title": name.capitalize(),
#                     "payload": f'/select_symptom{{"symptom": "{name.lower()}"}}'
#                 })

#         if buttons:
#             text = "કૃપા કરીને લક્ષણ પસંદ કરો:" if lang == "gu" else "Please select a symptom:"
#             dispatcher.utter_message(text=text, buttons=buttons)
#         else:
#             dispatcher.utter_message(text="No symptoms found.")

#         return []



# class ActionProvideTreatment(Action):
#     def name(self) -> Text:
#         return "action_provide_treatment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # Connect to MongoDB
#         client = MongoClient("mongodb+srv://aayupatel015:aayu%407991@cluster0.xq5rv0d.mongodb.net/")
#         db = client["medical_chatbot"]
#         collection = db["symptoms"]

#         user_message = tracker.latest_message.get('text', '').lower()
#         lang = "gu" if re.search(r'[\u0A80-\u0AFF]', user_message) else "en"

#         all_symptoms = list(collection.find())
#         detected_symptoms = []

#         # Detect all symptoms by matching keywords
#         for symptom_doc in all_symptoms:
#             keywords = symptom_doc.get(f"keywords_{lang}", [])
#             keywords = [kw.lower() for kw in keywords if kw.strip()]

#             if any(kw in user_message for kw in keywords):
#                 symptom_name = symptom_doc.get(f"symptom_{lang}", "").lower()
#                 if symptom_name and symptom_name not in detected_symptoms:
#                     detected_symptoms.append(symptom_name)

#         # If no symptoms detected
#         if not detected_symptoms:
#             msg = "કૃપા કરીને તમારા લક્ષણો સ્પષ્ટ કરો." if lang == "gu" else "Please specify your symptoms clearly."
#             dispatcher.utter_message(text=msg)
#             return []

#         # Prepare responses for each detected symptom
#         response_texts = []
#         for symptom in detected_symptoms:
#             data = collection.find_one({f"symptom_{lang}": symptom})
#             if not data:
#                 response_texts.append(f"No treatment found for {symptom}.")
#                 continue

#             treatment = data.get(f"treatment_{lang}", "N/A")
#             homeo = data.get(f"homeopathic_treatment_{lang}", "N/A")
#             alt = data.get(f"alternative_treatment_{lang}", "N/A")

#             if lang == "gu":
#                 msg = (
#                     f"🔎 *{symptom.capitalize()} માટે ઉપચાર:*\n\n"
#                     f"🩺 એલોપેથી: {treatment}\n\n"
#                     f"🌿 હોમિયોપેથી: {homeo}\n\n"
#                     f"🌱 વૈકલ્પિક: {alt}\n\n"
#                 )
#             else:
#                 msg = (
#                     f"🔎 *Treatment for {symptom.capitalize()}:*\n\n"
#                     f"🩺 Allopathic: {treatment}\n\n"
#                     f"🌿 Homeopathic: {homeo}\n\n"
#                     f"🌱 Alternative: {alt}\n\n"
#                 )

#             response_texts.append(msg)

#         # Add disclaimer
#         disclaimer = (
#             "⚠️ This is for informational purposes only. Please consult a certified doctor."
#             if lang == "en" else
#             "⚠️ આ માત્ર માહિતી માટે છે. કૃપા કરીને પ્રમાણિત ડૉક્ટરનો સંપર્ક કરો."
#         )

#         final_output = "\n\n".join(response_texts) + "\n\n" + disclaimer
#         dispatcher.utter_message(text=final_output)
#         return []

# import requests
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from typing import Any, Text, Dict, List

# class ActionNearbyClinics(Action):
#     def name(self) -> Text:
#         return "action_nearby_clinics"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         metadata = tracker.latest_message.get("metadata", {})
#         lat = metadata.get("latitude")
#         lng = metadata.get("longitude")

#         if not lat or not lng:
#             dispatcher.utter_message(text="📍 Location not provided.")
#             return []

#         try:
#             api_key = "YOUR_GOOGLE_PLACES_API_KEY"
#             url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
#             params = {
#                 "location": f"{lat},{lng}",
#                 "radius": 3000,
#                 "type": "hospital",
#                 "key": api_key
#             }
#             response = requests.get(url, params=params)
#             places = response.json().get("results", [])[:5]

#             if not places:
#                 dispatcher.utter_message(text="No nearby clinics found.")
#                 return []

#             msg = "🏥 *Nearby Clinics:*\n"
#             for i, place in enumerate(places, 1):
#                 name = place.get("name")
#                 address = place.get("vicinity")
#                 msg += f"{i}. {name}, {address}\n"

#             dispatcher.utter_message(text=msg)
#         except Exception as e:
#             print(f"Error fetching clinics: {e}")
#             dispatcher.utter_message(text="⚠️ Error fetching clinics.")
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
import re
import requests


class ActionAskSymptom(Action):
    def name(self) -> Text:
        return "action_ask_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '')
        lang = "gu" if re.search(r'[\u0A80-\u0AFF]', user_message) else "en"

        client = MongoClient("mongodb+srv://aayupatel015:aayu%407991@cluster0.xq5rv0d.mongodb.net/")
        db = client["medical_chatbot"]
        collection = db["symptoms"]

        symptoms = collection.find().limit(20)
        buttons = []

        for symptom in symptoms:
            name = symptom.get(f"symptom_{lang}")
            if name:
                buttons.append({
                    "title": name.capitalize(),
                    "payload": f'/select_symptom{{"symptom": "{name.lower()}"}}'
                })

        if buttons:
            text = "કૃપા કરીને લક્ષણ પસંદ કરો:" if lang == "gu" else "Please select a symptom:"
            dispatcher.utter_message(text=text, buttons=buttons)
        else:
            dispatcher.utter_message(text="No symptoms found.")

        return []


class ActionProvideTreatment(Action):
    def name(self) -> Text:
        return "action_provide_treatment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = MongoClient("mongodb+srv://aayupatel015:aayu%407991@cluster0.xq5rv0d.mongodb.net/")
        db = client["medical_chatbot"]
        collection = db["symptoms"]

        user_message = tracker.latest_message.get('text', '').lower()
        lang = "gu" if re.search(r'[\u0A80-\u0AFF]', user_message) else "en"

        all_symptoms = list(collection.find())
        detected_symptoms = []

        for symptom_doc in all_symptoms:
            keywords = symptom_doc.get(f"keywords_{lang}", [])
            keywords = [kw.lower() for kw in keywords if kw.strip()]
            if any(kw in user_message for kw in keywords):
                symptom_name = symptom_doc.get(f"symptom_{lang}", "").lower()
                if symptom_name and symptom_name not in detected_symptoms:
                    detected_symptoms.append(symptom_name)

        if not detected_symptoms:
            msg = "કૃપા કરીને તમારા લક્ષણો સ્પષ્ટ કરો." if lang == "gu" else "Please specify your symptoms clearly."
            dispatcher.utter_message(text=msg)
            return []

        for symptom in detected_symptoms:
            text = f"{symptom.capitalize()} માટે ઉપચાર પસંદ કરો:" if lang == "gu" else f"Select treatment type for {symptom.capitalize()}:"
            buttons = [
                {"title": "🩺 Allopathic", "payload": f'/show_treatment{{"type": "allopathic", "symptom": "{symptom}"}}'},
                {"title": "🌿 Homeopathic", "payload": f'/show_treatment{{"type": "homeopathic", "symptom": "{symptom}"}}'},
                {"title": "🌱 Alternative", "payload": f'/show_treatment{{"type": "alternative", "symptom": "{symptom}"}}'},
            ]
            dispatcher.utter_message(text=text, buttons=buttons)

        return []

class ActionShowSpecificTreatment(Action):
    def name(self) -> Text:
        return "action_show_specific_treatment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        treatment_type = tracker.get_slot("type")
        symptom = tracker.get_slot("symptom")

        if not treatment_type or not symptom:
            dispatcher.utter_message(text="❗Please specify both symptom and treatment type.")
            return []

        user_message = tracker.latest_message.get('text', '')
        lang = "gu" if re.search(r'[\u0A80-\u0AFF]', user_message) else "en"

        client = MongoClient("mongodb+srv://aayupatel015:aayu%407991@cluster0.xq5rv0d.mongodb.net/")
        db = client["medical_chatbot"]
        collection = db["symptoms"]

        data = collection.find_one({f"symptom_{lang}": symptom.lower()})
        if not data:
            dispatcher.utter_message(text="⚠️ Symptom not found.")
            return []

        type_map = {
            "allopathic": f"treatment_{lang}",
            "homeopathic": f"homeopathic_treatment_{lang}",
            "alternative": f"alternative_treatment_{lang}"
        }

        emoji_map = {
            "allopathic": "🩺",
            "homeopathic": "🌿",
            "alternative": "🌱"
        }

        treatment_key = type_map.get(treatment_type)
        treatment_value = data.get(treatment_key, "N/A")
        emoji = emoji_map.get(treatment_type, "")

        title = (
            f"{emoji} *{treatment_type.capitalize()} treatment for {symptom.capitalize()}:*"
            if lang == "en"
            else f"{emoji} *{symptom.capitalize()} માટે {treatment_type} ઉપચાર:*"
        )

        disclaimer = (
            "⚠️ This is for informational purposes only. Please consult a certified doctor."
            if lang == "en"
            else "⚠️ આ માત્ર માહિતી માટે છે. કૃપા કરીને પ્રમાણિત ડૉક્ટરનો સંપર્ક કરો."
        )

        dispatcher.utter_message(text=f"{title}\n\n{treatment_value}\n\n{disclaimer}")
        return []
