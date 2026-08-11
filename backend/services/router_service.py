def route_question(question):
    question = question.lower()

    flight_keywords = [
        "flight",
        "flights",
        "schedule",
        "departure",
        "arrival",
        "رحلة",
        "رحلات",
        "مغادرة",
        "وصول"
    ]

    baggage_keywords = [
        "baggage",
        "luggage",
        "bag",
        "baggage allowance",
        "extra luggage",
        "extra baggage",
        "أمتعة",
        "أمتعه",
        "شنطة",
        "شنط",
        "أمتعة إضافية"
    ]

    booking_keywords = [
        "cancel",
        "cancellation",
        "change booking",
        "change my booking",
        "change fee",
        "refund",
        "إلغاء",
        "الغاء",
        "تغيير الحجز",
        "رسوم التغيير",
        "استرجاع"
    ]

    for keyword in flight_keywords:
        if keyword in question:
            return "flight_sql"

    for keyword in baggage_keywords:
        if keyword in question:
            return "baggage_sql"

    for keyword in booking_keywords:
        if keyword in question:
            return "booking_sql"

    return "rag"


if __name__ == "__main__":
    print(route_question("What flights are available from Riyadh to Dubai?"))
    print(route_question("Can I add extra baggage?"))
    print(route_question("Can I cancel my Value fare?"))
    print(route_question("What is FlyNAS?"))