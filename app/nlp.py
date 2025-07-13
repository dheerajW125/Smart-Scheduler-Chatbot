import spacy
from dateparser.search import search_dates

class NLPService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def parse(self, text):
        text_lower = text.lower()
        intent = "unknown"

        # Detect intent
        if any(keyword in text_lower for keyword in ["schedule", "create", "fix", "book", "set up"]):
            intent = "create_event"
        elif any(keyword in text_lower for keyword in ["list", "show", "what", "view"]):
            intent = "list_events"
        elif any(keyword in text_lower for keyword in ["cancel", "delete", "remove"]):
            intent = "delete_event"

        # Extract participants using spaCy NER
        doc = self.nlp(text)
        participants = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        # Use dateparser to extract first datetime from full text
        parsed_date = None
        parsed_time = None

        search_result = search_dates(text)
        if search_result:
            dt = search_result[0][1]
            parsed_date = dt.strftime("%Y-%m-%d")
            parsed_time = dt.strftime("%H:%M")

        return {
            "intent": intent,
            "summary": text,
            "date": parsed_date,
            "time": parsed_time,
            "participants": participants
        }
