from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.calendar import CalendarService
from app.nlp import NLPService
from app.schema import ChatRequest

app = FastAPI()

# Initialize services
calendar_service = CalendarService()
nlp_service = NLPService()

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message

    # 1. NLP Parsing
    parsed = nlp_service.parse(user_message)

    # 2. Handle Intent
    if parsed["intent"] == "create_event":
        if not parsed.get("date") or not parsed.get("time"):
            return JSONResponse(
                status_code=400,
                content={
                    "message": "I couldn't figure out the date and time. Please rephrase your request (e.g., 'schedule a meeting tomorrow at 3 pm')."
                }
            )

        event = calendar_service.create_event(parsed)
        return {"message": f"Event created: {event['summary']}"}

    elif parsed["intent"] == "list_events":
        events = calendar_service.list_events()
        return {"events": events}

    elif parsed["intent"] == "delete_event":
        result = calendar_service.delete_event(parsed)
        return {"message": result}

    else:
        return {"message": "Sorry, I didn't understand your request. Please try again."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
