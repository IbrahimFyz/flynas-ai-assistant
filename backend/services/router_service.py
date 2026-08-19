def route_question(question):
    question = question.lower().strip()

    # =========================
    # RAG / FAQ
    # =========================
    # These questions are general FAQ questions
    # and should go to the knowledge base before
    # generic baggage/flight keyword detection.

    rag_keywords = [
        # FlyNAS information
        "what is flynas",
        "وش هو طيران ناس",
        "ما هو طيران ناس",
        "من هو طيران ناس",
        "وش طيران ناس",

        # Changing a flight
        "can i change my flight",
        "can i change the flight",
        "change my flight",
        "هل اقدر اغير رحلتي",
        "هل أقدر أغير رحلتي",
        "هل يمكنني تغيير رحلتي",
        "أقدر أغير رحلتي",
        "اقدر اغير رحلتي",
        "تغيير الرحلة",

        # Adding baggage to booking
        "can i add baggage to my booking",
        "can i add baggage to booking",
        "can i add extra baggage to my booking",
        "هل اقدر اضيف امتعة الى حجزي",
        "هل أقدر أضيف أمتعة إلى حجزي",
        "هل يمكنني اضافة امتعة الى حجزي",
        "هل يمكنني إضافة أمتعة إلى حجزي",
        "اضافة امتعة للحجز",
        "إضافة أمتعة للحجز",

        # Online check-in
        "can i check in online",
        "can i check-in online",
        "online check in",
        "online check-in",
        "هل اقدر اسجل الوصول الكترونيا",
        "هل أقدر أسجل الوصول إلكترونيًا",
        "هل يمكنني تسجيل الوصول الكترونيا",
        "هل يمكنني تسجيل الوصول إلكترونيًا",
        "تسجيل الوصول الإلكتروني",
        "تسجيل الوصول الكترونيا",
    ]

    for keyword in rag_keywords:
        if keyword in question:
            return "rag"


    # =========================
    # FARE COMPARISON
    # =========================

    fare_comparison_keywords = [
        "الفرق بين",
        "فرق بين",
        "مقارنة",
        "قارن",
        "compare",
        "comparison",
        "difference between",
    ]

    for keyword in fare_comparison_keywords:
        if keyword in question:
            return "fare_comparison"


    # =========================
    # BAGGAGE
    # =========================

    baggage_keywords = [
        "baggage",
        "luggage",
        "bag",
        "baggage allowance",
        "extra luggage",
        "extra baggage",
        "baggage policy",

        "أمتعة",
        "أمتعه",
        "شنطة",
        "شنط",
        "شنطه",
        "شنطتي",
        "حقائب",
        "حقيبة",
        "أمتعة إضافية",
        "وزن الأمتعة",
        "وزن الامتعة",
        "وزن الشنطة",
        "وزن الشنط",
        "الوزن المسموح",
        "كم الوزن",
        "وزن",
    ]

    for keyword in baggage_keywords:
        if keyword in question:
            return "baggage_sql"


    # =========================
    # BOOKING
    # =========================

    booking_keywords = [
        "cancel",
        "cancellation",
        "change booking",
        "change my booking",
        "change fee",
        "refund",
        "cancellation fee",

        "إلغاء",
        "الغاء",
        "ألغي",
        "الغي",
        "ألغى",
        "الغاء الحجز",
        "إلغاء الحجز",
        "تغيير الحجز",
        "تعديل الحجز",
        "تغيير حجزي",
        "تعديل حجزي",
        "رسوم التغيير",
        "رسوم تغيير",
        "رسوم الإلغاء",
        "رسوم الغاء",
        "استرجاع",
        "استرداد",
    ]

    for keyword in booking_keywords:
        if keyword in question:
            return "booking_sql"


    # =========================
    # FLIGHTS
    # =========================

    flight_keywords = [
        "flights",
        "what flights",
        "available flights",
        "flight from",
        "flight to",
        "flights from",
        "flights to",
        "flight schedule",
        "flight departure",
        "flight arrival",
        "schedule",
        "departure",
        "arrival",

        "رحلات",
        "الرحلات",
        "رحلة من",
        "رحلة إلى",
        "رحلات من",
        "رحلات إلى",
        "الرحلات المتاحة",
        "مواعيد الرحلات",
        "موعد الرحلة",
        "مغادرة",
        "وصول",
    ]

    for keyword in flight_keywords:
        if keyword in question:
            return "flight_sql"


    # =========================
    # FARE
    # =========================

    fare_keywords = [
        "light",
        "value",
        "plus",
        "fare",
        "فئة",
        "فئات",
        "سعر",
        "باقة",
        "باقات",
    ]

    for keyword in fare_keywords:
        if keyword in question:
            return "fare_sql"


    # =========================
    # RAG
    # =========================

    return "rag"


if __name__ == "__main__":

    test_questions = [
        # Flights
        "What flights are available from Riyadh to Dubai?",

        # Baggage
        "Can I add extra baggage?",
        "كم الوزن المسموح في Value؟",
        "وش أمتعة Plus؟",

        # Booking
        "Can I cancel my Value fare?",
        "هل أقدر ألغي Value؟",
        "كم رسوم تغيير Light؟",

        # Fares
        "كم سعر Light؟",
        "وش الفرق بين Light وValue وPlus؟",
        "قارن بين Light وValue وPlus",

        # RAG / FAQ
        "What is FlyNAS?",
        "وش هو طيران ناس؟",
        "Can I change my flight?",
        "هل أقدر أغير رحلتي؟",
        "Can I add baggage to my booking?",
        "هل أقدر أضيف أمتعة إلى حجزي؟",
        "Can I check in online?",
        "هل أقدر أسجل الوصول إلكترونيًا؟",

        # General RAG
        "وش المستندات المطلوبة للسفر؟",
    ]

    print("----- ROUTER TESTS -----")

    for question in test_questions:
        print(f"\nQuestion: {question}")
        print(f"Route: {route_question(question)}")