from fastapi import FastAPI
from pydantic import BaseModel

from services.vector_store import build_vector_store
from services.similarity_service import search_knowledge
from services.router_service import route_question
from services.flight_service import search_flights_from_question
from services.ai_service import get_ai_response
from services.baggage_service import get_baggage_policy
from services.booking_service import get_booking_policy
from services.fare_service import find_mentioned_fare


app = FastAPI()

build_vector_store()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "Welcome to FlyNAS AI Travel Assistant!"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.get("/about")
def about():
    return {
        "message": "About FlyNAS AI Travel Assistant"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    route = route_question(request.message)


    # =========================
    # FLIGHT SQL
    # =========================

    if route == "flight_sql":

        flights = search_flights_from_question(
            request.message
        )

        if flights is None:
            return {
                "route": "flight_sql",
                "response": "What destination would you like to fly to?"
            }

        if not flights:
            return {
                "route": "flight_sql",
                "response": "No flights were found for the requested route."
            }

        answer = get_ai_response(
            request.message,
            flights
        )

        return {
            "route": "flight_sql",
            "response": answer
        }


    # =========================
    # BAGGAGE SQL
    # =========================

    if route == "baggage_sql":

        mentioned_fare = find_mentioned_fare(
            request.message
        )

        if mentioned_fare is None:
            return {
                "route": "baggage_sql",
                "response": "Which fare would you like to check: Light, Value, or Plus?"
            }

        if mentioned_fare not in ["Light", "Value", "Plus"]:
            return {
                "route": "baggage_sql",
                "response": (
                    f"The {mentioned_fare} fare is not available. "
                    "Available fares are Light, Value, and Plus."
                )
            }

        baggage = get_baggage_policy(
            mentioned_fare
        )

        baggage_context = f"""
Fare: {baggage[0]}
Price: {baggage[1]} SAR
Baggage allowance: {baggage[2]} kg
Extra baggage: {baggage[3]} kg
Policy available: {baggage[4]}
"""

        answer = get_ai_response(
            request.message,
            baggage_context
        )

        return {
            "route": "baggage_sql",
            "response": answer
        }


    # =========================
    # BOOKING SQL
    # =========================

    if route == "booking_sql":

        mentioned_fare = find_mentioned_fare(
            request.message
        )

        if mentioned_fare is None:
            return {
                "route": "booking_sql",
                "response": "Which fare would you like to check: Light, Value, or Plus?"
            }

        if mentioned_fare not in ["Light", "Value", "Plus"]:
            return {
                "route": "booking_sql",
                "response": (
                    f"The {mentioned_fare} fare is not available. "
                    "Available fares are Light, Value, and Plus."
                )
            }

        policy = get_booking_policy(
            mentioned_fare
        )

        booking_context = f"""
Fare: {policy[0]}
Price: {policy[1]} SAR
Cancellation allowed: {policy[2]}
Change allowed: {policy[3]}
Cancellation fee: {policy[4]} SAR
Change fee: {policy[5]} SAR
"""

        answer = get_ai_response(
            request.message,
            booking_context
        )

        return {
            "route": "booking_sql",
            "response": answer
        }


    # =========================
    # RAG
    # =========================

    result = search_knowledge(
        request.message
    )

    answer = get_ai_response(
        request.message,
        result["chunk"]
    )

    return {
        "route": "rag",
        "response": answer
    }