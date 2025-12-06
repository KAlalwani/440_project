# rules.py

RULES = [
    # Registration
    {
        "id": "reg_when",
        "topic": "registration",
        "intents": ["when"],
        "keywords": ["register", "registration", "enroll", "sign up", "course selection", "add classes"],
        "response": "Registration opens on January 5.",
        "priority": 3,
        "weight": 1.0,
    },
    {
        "id": "reg_how",
        "topic": "registration",
        "intents": ["how"],
        "keywords": ["register", "registration", "enroll", "sign up", "course selection", "add classes"],
        "response": "You can register through the SIS website (Student Information System).",
        "priority": 3,
        "weight": 1.0,
    },

    # Credit hours
    {
        "id": "credits",
        "topic": "credits",
        "intents": ["what", "general"],
        "keywords": ["credit", "credits", "credit hours", "course hours", "ects"],
        "response": "Each course is worth 3 credit hours.",
        "priority": 2,
        "weight": 1.0,
    },

    # Add/Drop deadline
    {
        "id": "adddrop",
        "topic": "add_drop",
        "intents": ["when", "general"],
        "keywords": ["deadline", "add drop", "add/drop", "last day to add", "last day to drop", "course change deadline"],
        "response": "The add/drop deadline is January 18.",
        "priority": 2,
        "weight": 1.0,
    },

    # GPA
    {
        "id": "gpa",
        "topic": "gpa",
        "intents": ["what", "how", "general"],
        "keywords": ["gpa", "grade point average", "calculate gpa"],
        "response": "Your GPA is visible in SIS under the academic record section.",
        "priority": 2,
        "weight": 1.0,
    },

    # Transcript
    {
        "id": "transcript",
        "topic": "transcript",
        "intents": ["how", "general"],
        "keywords": ["transcript", "official transcript", "academic record", "grades", "get transcript"],
        "response": "You can request transcripts from the registrar or via SIS.",
        "priority": 2,
        "weight": 1.0,
    },

    # Fees
    {
        "id": "fees",
        "topic": "fees",
        "intents": ["what", "general"],
        "keywords": ["fees", "payment", "tuition", "installments", "invoice", "balance", "financial hold"],
        "response": "Tuition fees must be paid before Week 2.",
        "priority": 2,
        "weight": 1.0,
    },

    # Library
    {
        "id": "library",
        "topic": "library",
        "intents": ["what", "general"],
        "keywords": ["library", "books", "borrow", "library hours", "printing", "study room"],
        "response": "Library hours are 8AM–10PM every day.",
        "priority": 1,
        "weight": 0.9,
    },

    # IT support
    {
        "id": "it_support",
        "topic": "it_support",
        "intents": ["how", "general"],
        "keywords": ["it support", "technical help", "computer help", "tech support"],
        "response": "For technical support, contact IT Helpdesk or email support@university.com.",
        "priority": 2,
        "weight": 1.0,
    },
]
