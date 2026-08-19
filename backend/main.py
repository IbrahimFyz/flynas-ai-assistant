from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.vector_store import build_vector_store
from services.similarity_service import search_knowledge
from services.router_service import route_question
from services.flight_service import search_flights_from_question
from services.ai_service import get_ai_response
from services.baggage_service import get_baggage_policy
from services.booking_service import get_booking_policy
from services.fare_service import (
    find_mentioned_fare,
    get_fare,
    get_all_fares,
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


build_vector_store()


class ChatRequest(BaseModel):
    message: str


def is_arabic(text: str) -> bool:
    return any("\u0600" <= char <= "\u06FF" for char in text)


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

    arabic = is_arabic(request.message)

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
                "response": (
                    "إلى أي وجهة ترغب بالسفر؟"
                    if arabic
                    else "What destination would you like to fly to?"
                )
            }

        if not flights:
            return {
                "route": "flight_sql",
                "response": (
                    "لم يتم العثور على رحلات للمسار المطلوب."
                    if arabic
                    else "No flights were found for the requested route."
                )
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
                "response": (
                    "أي فئة تريد معرفة تفاصيل أمتعتها: Light أو Value أو Plus؟"
                    if arabic
                    else "Which fare would you like to check: Light, Value, or Plus?"
                )
            }

        if mentioned_fare not in ["Light", "Value", "Plus"]:
            return {
                "route": "baggage_sql",
                "response": (
                    f"فئة {mentioned_fare} غير متاحة. "
                    "الفئات المتاحة هي Light وValue وPlus."
                    if arabic
                    else
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
Cabin baggage allowance: {baggage[2]} kg
Checked baggage allowance: {baggage[3]} kg
Extra baggage allowed: {"Yes" if baggage[4] else "No"}
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
                "response": (
                    "أي فئة تريد معرفة سياسة الحجز الخاصة بها: Light أو Value أو Plus؟"
                    if arabic
                    else "Which fare would you like to check: Light, Value, or Plus?"
                )
            }

        if mentioned_fare not in ["Light", "Value", "Plus"]:
            return {
                "route": "booking_sql",
                "response": (
                    f"فئة {mentioned_fare} غير متاحة. "
                    "الفئات المتاحة هي Light وValue وPlus."
                    if arabic
                    else
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
Cancellation allowed: {"Yes" if policy[2] else "No"}
Change allowed: {"Yes" if policy[3] else "No"}
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
    # FARE SQL
    # =========================

    if route == "fare_sql":

        mentioned_fare = find_mentioned_fare(
            request.message
        )

        if mentioned_fare is None:
            return {
                "route": "fare_sql",
                "response": (
                    "أي فئة تريد معرفة تفاصيلها: Light أو Value أو Plus؟"
                    if arabic
                    else "Which fare would you like to check: Light, Value, or Plus?"
                )
            }

        if mentioned_fare not in ["Light", "Value", "Plus"]:
            return {
                "route": "fare_sql",
                "response": (
                    f"فئة {mentioned_fare} غير متاحة. "
                    "الفئات المتاحة هي Light وValue وPlus."
                    if arabic
                    else
                    f"The {mentioned_fare} fare is not available. "
                    "Available fares are Light, Value, and Plus."
                )
            }

        fare = get_fare(
            mentioned_fare
        )

        fare_context = f"""
Fare: {fare[0]}
Price: {fare[1]} SAR
Cabin class: {fare[2]}
Refundable: {"Yes" if fare[3] else "No"}
Changeable: {"Yes" if fare[4] else "No"}
Cabin baggage allowance: {fare[5]} kg
Checked baggage allowance: {fare[6]} kg
Extra baggage allowed: {"Yes" if fare[7] else "No"}
Change allowed: {"Yes" if fare[8] else "No"}
Cancellation allowed: {"Yes" if fare[9] else "No"}
Change fee: {fare[10]} SAR
Cancellation fee: {fare[11]} SAR
"""

        answer = get_ai_response(
            request.message,
            fare_context
        )

        return {
            "route": "fare_sql",
            "response": answer
        }


    # =========================
    # FARE COMPARISON
    # =========================

    if route == "fare_comparison":

        fares = get_all_fares()

        fare_context = "Available FlyNAS fare information:\n\n"

        for fare in fares:

            fare_context += f"""
Fare: {fare[0]}
Price: {fare[1]} SAR
Cabin class: {fare[2]}
Refundable: {"Yes" if fare[3] else "No"}
Changeable: {"Yes" if fare[4] else "No"}
Cabin baggage allowance: {fare[5]} kg
Checked baggage allowance: {fare[6]} kg
Extra baggage allowed: {"Yes" if fare[7] else "No"}
Change allowed: {"Yes" if fare[8] else "No"}
Cancellation allowed: {"Yes" if fare[9] else "No"}
Change fee: {fare[10]} SAR
Cancellation fee: {fare[11]} SAR

"""

        answer = get_ai_response(
            request.message,
            fare_context
        )

        return {
            "route": "fare_comparison",
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