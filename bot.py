import re
import tkinter as tk
from tkinter import scrolledtext, ttk
from datetime import datetime
from typing import List, Dict
import threading
import time

# Enhanced Rules with better keyword coverage and intent support
RULES = [
    {
        "id": "reg_when",
        "topic": "registration",
        "intents": ["when", "time"],
        "keywords": ["register", "registration", "enroll", "enrollment", "sign up", "signup", "course selection", "add classes", "take courses", "pick classes"],
        "patterns": ["when.*register", "registration.*date", "register.*when", "start.*registration"],
        "response": "Registration opens on January 5th. Mark your calendar!",
        "priority": 3,
        "weight": 1.2,
    },
    {
        "id": "reg_how",
        "topic": "registration",
        "intents": ["how", "process", "steps"],
        "keywords": ["register", "registration", "enroll", "enrollment", "sign up", "signup", "course selection"],
        "patterns": ["how.*register", "register.*how", "process.*register", "steps.*register"],
        "response": "To register: 1) Log into the SIS (Student Information System) at sis.university.edu, 2) Navigate to 'Course Registration', 3) Search for courses, 4) Add them to your cart, and 5) Submit your registration. Need help? Contact the registrar's office.",
        "priority": 3,
        "weight": 1.2,
    },
    {
        "id": "reg_where",
        "topic": "registration",
        "intents": ["where", "location"],
        "keywords": ["register", "registration", "enroll", "enrollment"],
        "patterns": ["where.*register", "register.*where"],
        "response": "You can register online through the SIS website at sis.university.edu. No need to visit campus!",
        "priority": 3,
        "weight": 1.1,
    },
    {
        "id": "credits_what",
        "topic": "credits",
        "intents": ["what", "general"],
        "keywords": ["credit", "credits", "credit hours", "course hours", "ects", "units"],
        "patterns": ["how many.*credit", "credit.*per.*course"],
        "response": "Each course is typically worth 3 credit hours. Some lab courses or special seminars may vary between 1-4 credits.",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "credits_how_many",
        "topic": "credits",
        "intents": ["how", "what"],
        "keywords": ["many", "credit", "credits", "semester", "take"],
        "patterns": ["how many.*credit", "credits.*semester", "credit.*load"],
        "response": "Full-time students typically take 12-18 credit hours per semester. The recommended load is 15 credits (5 courses).",
        "priority": 2,
        "weight": 1.1,
    },
    {
        "id": "adddrop_when",
        "topic": "add_drop",
        "intents": ["when", "time"],
        "keywords": ["deadline", "add drop", "add/drop", "last day", "drop course", "withdraw", "course change"],
        "patterns": ["when.*deadline", "deadline.*when", "last day.*drop"],
        "response": "The add/drop deadline is January 18th. After this date, you'll need special permission to make schedule changes.",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "adddrop_how",
        "topic": "add_drop",
        "intents": ["how", "process"],
        "keywords": ["drop", "add", "course", "class", "withdraw"],
        "patterns": ["how.*drop", "how.*add", "drop.*course"],
        "response": "To add/drop courses: Go to SIS → My Schedule → Add/Drop Courses. Select the courses you want to add or drop, then submit. Make sure to do this before January 18th!",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "gpa_what",
        "topic": "gpa",
        "intents": ["what", "general"],
        "keywords": ["gpa", "grade point average", "grades"],
        "patterns": ["what.*gpa", "gpa.*is"],
        "response": "GPA (Grade Point Average) is calculated on a 4.0 scale: A=4.0, B=3.0, C=2.0, D=1.0, F=0.0. Your cumulative GPA is the average of all your courses.",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "gpa_where",
        "topic": "gpa",
        "intents": ["where", "how", "check"],
        "keywords": ["gpa", "grade point average", "check", "find", "see", "view"],
        "patterns": ["where.*gpa", "check.*gpa", "see.*gpa", "find.*gpa"],
        "response": "You can check your GPA in SIS under 'Academic Record' or 'Grades'. It shows both semester and cumulative GPA.",
        "priority": 2,
        "weight": 1.1,
    },
    {
        "id": "gpa_how_calculate",
        "topic": "gpa",
        "intents": ["how"],
        "keywords": ["calculate", "gpa", "computation"],
        "patterns": ["how.*calculate.*gpa", "calculate.*gpa"],
        "response": "GPA is calculated by: (Sum of (Grade Points × Credit Hours)) / (Total Credit Hours). For example: If you got an A (4.0) in a 3-credit course and a B (3.0) in another 3-credit course, your GPA = ((4.0×3) + (3.0×3)) / 6 = 3.5",
        "priority": 2,
        "weight": 1.1,
    },
    {
        "id": "transcript_how",
        "topic": "transcript",
        "intents": ["how", "get", "request"],
        "keywords": ["transcript", "official transcript", "academic record", "grades", "get transcript", "request transcript"],
        "patterns": ["how.*transcript", "get.*transcript", "request.*transcript"],
        "response": "To request an official transcript: 1) Log into SIS, 2) Go to 'Academic Records', 3) Click 'Request Transcript', 4) Choose delivery method (electronic/mail), and 5) Pay the $10 processing fee. Or visit the Registrar's Office in person.",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "transcript_time",
        "topic": "transcript",
        "intents": ["when", "time", "how long"],
        "keywords": ["transcript", "long", "take", "processing", "delivery"],
        "patterns": ["how long.*transcript", "transcript.*take"],
        "response": "Electronic transcripts are typically processed within 2-3 business days. Paper transcripts mailed domestically take 5-7 business days.",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "fees_what",
        "topic": "fees",
        "intents": ["what", "general", "how much"],
        "keywords": ["fees", "tuition", "cost", "price", "how much"],
        "patterns": ["how much.*fee", "cost.*tuition", "tuition.*cost"],
        "response": "Tuition fees vary by program. Undergraduate: $450/credit hour. Graduate: $650/credit hour. Additional fees include technology fee ($150/semester) and student services ($100/semester).",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "fees_when",
        "topic": "fees",
        "intents": ["when", "deadline"],
        "keywords": ["fees", "payment", "tuition", "deadline", "due", "pay"],
        "patterns": ["when.*pay", "payment.*deadline", "due.*date"],
        "response": "Tuition fees must be paid by the end of Week 2 of the semester. Late payments incur a $50 fee and may result in schedule cancellation.",
        "priority": 2,
        "weight": 1.1,
    },
    {
        "id": "fees_how",
        "topic": "fees",
        "intents": ["how", "process"],
        "keywords": ["pay", "payment", "tuition", "fees"],
        "patterns": ["how.*pay", "pay.*tuition", "payment.*method"],
        "response": "You can pay tuition through: 1) SIS online payment (credit/debit card), 2) Bank transfer to university account, 3) Payment plan (installments), or 4) In-person at the Bursar's Office.",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "library_hours",
        "topic": "library",
        "intents": ["when", "time", "hours"],
        "keywords": ["library", "hours", "open", "close", "timing"],
        "patterns": ["library.*hours", "when.*library.*open", "library.*open"],
        "response": "Library hours: Monday-Friday 8AM-10PM, Saturday-Sunday 10AM-8PM. Extended hours during finals week (24/7)!",
        "priority": 1,
        "weight": 0.9,
    },
    {
        "id": "library_services",
        "topic": "library",
        "intents": ["what", "general"],
        "keywords": ["library", "books", "borrow", "printing", "study room", "resources"],
        "patterns": ["what.*library", "library.*services"],
        "response": "Library services include: book lending (21-day checkout), computer access, printing/scanning, study rooms (reservable online), research assistance, and access to online databases. First 100 pages of printing are free!",
        "priority": 1,
        "weight": 0.9,
    },
    {
        "id": "it_support_how",
        "topic": "it_support",
        "intents": ["how", "general"],
        "keywords": ["it support", "technical help", "computer help", "tech support", "helpdesk", "technical issue"],
        "patterns": ["how.*contact.*it", "it.*help", "tech.*support"],
        "response": "For technical support: Email support@university.edu, call (555) 123-4567, or visit IT Helpdesk in Building A, Room 101. Available Mon-Fri 9AM-5PM. For urgent issues, use the live chat on the IT website.",
        "priority": 2,
        "weight": 1.0,
    },
    {
        "id": "advising",
        "topic": "advising",
        "intents": ["what", "how", "when"],
        "keywords": ["advisor", "advising", "academic advisor", "counseling", "guidance"],
        "patterns": ["meet.*advisor", "academic.*advising"],
        "response": "Academic advising is available through your assigned faculty advisor. Schedule appointments via SIS or email your advisor directly. Walk-in hours: Tuesday/Thursday 2-4PM at the Academic Advising Center.",
        "priority": 2,
        "weight": 0.9,
    },
    {
        "id": "financial_aid",
        "topic": "financial_aid",
        "intents": ["what", "how", "when"],
        "keywords": ["financial aid", "scholarship", "grant", "loan", "fafsa", "funding"],
        "patterns": ["financial.*aid", "apply.*scholarship"],
        "response": "Financial aid applications open November 1st. Complete the FAFSA at fafsa.gov and submit supporting documents to financialaid@university.edu. Scholarships are awarded based on merit and need. Priority deadline: March 1st.",
        "priority": 2,
        "weight": 1.0,
    },
]

SYNONYMS = {
    "sign up": "register",
    "enrol": "enroll",
    "enrolling": "enroll",
    "registered": "register",
    "registering": "register",
    "signing up": "register",
    "course selection": "register",
    "add classes": "register",
    "take courses": "register",
    "academic record": "transcript",
    "official grades": "transcript",
    "tuition": "fees",
    "cost": "fees",
    "helpdesk": "it support",
    "tech help": "it support",
}


class EnhancedFAQBot:
    def __init__(self):
        self.last_topic = None
        self.conversation_context = []

    def normalize(self, text: str) -> str:
        t = (text or "").lower().strip()
        multi_word = sorted([k for k in SYNONYMS.keys() if " " in k], key=len, reverse=True)
        for phrase in multi_word:
            t = re.sub(phrase, SYNONYMS[phrase], t)
        for word, replacement in SYNONYMS.items():
            if " " not in word:
                t = re.sub(rf"\b{word}\b", replacement, t)
        t = re.sub(r"[^\w\s']", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def detect_intent(self, text: str, tokens: List[str]) -> str:
        t = text.lower()
        if re.search(r"\b(when|what time|what date|schedule|timing)\b", t):
            return "when"
        if re.search(r"\b(where|location|place)\b", t):
            return "where"
        if re.search(r"\b(how|process|steps|procedure|way to|method)\b", t):
            return "how"
        if re.search(r"\b(what|which|tell me about|explain)\b", t):
            return "what"
        if re.search(r"\b(how much|cost|price|fee amount)\b", t):
            return "how much"
        if re.search(r"\b(how many|number of|amount of)\b", t):
            return "how many"
        if re.search(r"\b(how long|duration|take time)\b", t):
            return "how long"
        return "general"

    def levenshtein(self, a: str, b: str) -> int:
        if len(a) == 0:
            return len(b)
        if len(b) == 0:
            return len(a)
        matrix = [[0] * (len(a) + 1) for _ in range(len(b) + 1)]
        for i in range(len(b) + 1):
            matrix[i][0] = i
        for j in range(len(a) + 1):
            matrix[0][j] = j
        for i in range(1, len(b) + 1):
            for j in range(1, len(a) + 1):
                if b[i - 1] == a[j - 1]:
                    matrix[i][j] = matrix[i - 1][j - 1]
                else:
                    matrix[i][j] = min(matrix[i - 1][j - 1] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j] + 1)
        return matrix[len(b)][len(a)]

    def fuzzy_match(self, a: str, b: str, threshold: float = 0.75) -> bool:
        if a == b:
            return True
        longer = a if len(a) > len(b) else b
        shorter = b if len(a) > len(b) else a
        if len(longer) == 0:
            return True
        edit_distance = self.levenshtein(longer, shorter)
        similarity = (len(longer) - edit_distance) / len(longer)
        return similarity >= threshold

    def score_rule(self, rule: Dict, text: str, tokens: List[str], intent: str) -> float:
        score = 0.0
        if intent in rule["intents"] or "general" in rule["intents"]:
            score += 2.0
        if "patterns" in rule:
            for pattern in rule["patterns"]:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 3.0
        keyword_hits = 0
        for keyword in rule["keywords"]:
            keyword_parts = keyword.split(" ")
            if len(keyword_parts) > 1:
                if all(part in text for part in keyword_parts):
                    keyword_hits += 1
                    score += 1.5
            else:
                for token in tokens:
                    if token == keyword:
                        keyword_hits += 1
                        score += 1.0
                    elif self.fuzzy_match(token, keyword):
                        keyword_hits += 1
                        score += 0.8
        if keyword_hits == 0 and score < 3.0:
            return -1
        score = score * rule["weight"] + rule["priority"] * 0.5
        return score

    def get_response(self, user_input: str) -> str:
        normalized = self.normalize(user_input)
        tokens = [t for t in normalized.split(" ") if t]
        intent = self.detect_intent(user_input, tokens)
        best_match = None
        best_score = -1
        for rule in RULES:
            score = self.score_rule(rule, normalized, tokens, intent)
            if score > best_score and score > 1.0:
                best_score = score
                best_match = rule
        if best_match:
            self.last_topic = best_match["topic"]
            self.conversation_context.append({"input": user_input, "topic": best_match["topic"], "intent": intent})
            if len(self.conversation_context) > 5:
                self.conversation_context.pop(0)
            return best_match["response"]
        return "I'm not sure about that. Please contact the university administration at admin@university.edu or call (555) 123-4567 for assistance."


class ModernChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("University FAQ Assistant")
        self.root.geometry("700x750")
        self.bot = EnhancedFAQBot()
        self.is_typing = False
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.add_welcome_message()

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg="#f5f7fa")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header with gradient effect (simulated with frame)
        header = tk.Frame(main_container, bg="#4f46e5", height=90)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_frame = tk.Frame(header, bg="#4f46e5")
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, text="✨ University FAQ Assistant", font=("Segoe UI", 22, "bold"), 
                bg="#4f46e5", fg="white").pack()
        tk.Label(title_frame, text="AI-Powered Support • Available 24/7", font=("Segoe UI", 11), 
                bg="#4f46e5", fg="#c7d2fe").pack()
        
        # Chat area
        chat_container = tk.Frame(main_container, bg="#f5f7fa")
        chat_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Canvas for custom scrollbar
        canvas_frame = tk.Frame(chat_container, bg="white", relief=tk.FLAT, bd=0)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.chat_canvas.yview)
        self.scrollable_frame = tk.Frame(self.chat_canvas, bg="white")
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Input area
        input_container = tk.Frame(main_container, bg="#f5f7fa")
        input_container.pack(fill=tk.X, padx=30, pady=(0, 25))
        
        input_frame = tk.Frame(input_container, bg="white", relief=tk.SOLID, bd=1, highlightbackground="#e5e7eb", highlightthickness=1)
        input_frame.pack(fill=tk.X)
        
        # Entry widget
        self.input_entry = tk.Entry(input_frame, font=("Segoe UI", 13), bg="white", fg="#1f2937", 
                                    relief=tk.FLAT, bd=0, insertbackground="#4f46e5")
        self.input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        self.input_entry.focus()
        
        # Send button
        self.send_btn = tk.Button(input_frame, text="Send", font=("Segoe UI", 12, "bold"), 
                                  bg="#4f46e5", fg="white", relief=tk.FLAT, cursor="hand2",
                                  activebackground="#4338ca", activeforeground="white",
                                  command=self.send_message, padx=25, pady=10)
        self.send_btn.pack(side=tk.RIGHT, padx=10, pady=8)
        
        # Quick suggestions
        suggestions_frame = tk.Frame(input_container, bg="#f5f7fa")
        suggestions_frame.pack(fill=tk.X, pady=(12, 0))
        
        tk.Label(suggestions_frame, text="Quick Questions:", font=("Segoe UI", 10), 
                bg="#f5f7fa", fg="#6b7280").pack(anchor=tk.W, pady=(0, 8))
        
        suggestions = [
            "When does registration open?",
            "How do I register?",
            "Library hours?",
            "Tuition fees?"
        ]
        
        btn_frame = tk.Frame(suggestions_frame, bg="#f5f7fa")
        btn_frame.pack(fill=tk.X)
        
        for i, q in enumerate(suggestions):
            btn = tk.Button(btn_frame, text=q, font=("Segoe UI", 10), bg="white", fg="#374151",
                          relief=tk.FLAT, cursor="hand2", activebackground="#f3f4f6",
                          command=lambda query=q: self.quick_send(query), padx=12, pady=8,
                          bd=1, highlightbackground="#e5e7eb", highlightthickness=1)
            btn.pack(side=tk.LEFT, padx=(0, 8))

    def add_welcome_message(self):
        msg = "👋 Hi! I'm your University FAQ Assistant. I can help you with registration, courses, fees, transcripts, library services, and more. What would you like to know?"
        self.add_message("bot", msg)

    def add_message(self, sender, text):
        msg_frame = tk.Frame(self.scrollable_frame, bg="white", pady=8)
        msg_frame.pack(fill=tk.X, padx=20, pady=5)
        
        if sender == "user":
            bubble_frame = tk.Frame(msg_frame, bg="white")
            bubble_frame.pack(anchor=tk.E)
            
            bubble = tk.Frame(bubble_frame, bg="#4f46e5", bd=0)
            bubble.pack(side=tk.RIGHT)
            
            tk.Label(bubble, text=text, font=("Segoe UI", 12), bg="#4f46e5", fg="white",
                    wraplength=500, justify=tk.LEFT, padx=16, pady=12).pack()
            
            time_label = tk.Label(bubble_frame, text=datetime.now().strftime("%H:%M"), 
                                 font=("Segoe UI", 9), bg="white", fg="#9ca3af")
            time_label.pack(side=tk.RIGHT, padx=(0, 8))
        else:
            bubble_frame = tk.Frame(msg_frame, bg="white")
            bubble_frame.pack(anchor=tk.W)
            
            avatar = tk.Label(bubble_frame, text="🤖", font=("Segoe UI", 16), bg="white")
            avatar.pack(side=tk.LEFT, padx=(0, 10))
            
            content_frame = tk.Frame(bubble_frame, bg="white")
            content_frame.pack(side=tk.LEFT)
            
            bubble = tk.Frame(content_frame, bg="#f3f4f6", bd=0)
            bubble.pack(anchor=tk.W)
            
            tk.Label(bubble, text=text, font=("Segoe UI", 12), bg="#f3f4f6", fg="#1f2937",
                    wraplength=500, justify=tk.LEFT, padx=16, pady=12).pack()
            
            time_label = tk.Label(content_frame, text=datetime.now().strftime("%H:%M"), 
                                 font=("Segoe UI", 9), bg="white", fg="#9ca3af")
            time_label.pack(anchor=tk.W, pady=(2, 0))
        
        self.root.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def send_message(self):
        text = self.input_entry.get().strip()
        if not text or self.is_typing:
            return
        
        self.add_message("user", text)
        self.input_entry.delete(0, tk.END)
        self.is_typing = True
        self.send_btn.config(state=tk.DISABLED, text="Typing...")
        
        threading.Thread(target=self.get_response, args=(text,), daemon=True).start()

    def quick_send(self, text):
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, text)
        self.send_message()

    def get_response(self, user_text):
        time.sleep(0.7)
        response = self.bot.get_response(user_text)
        self.root.after(0, self.display_response, response)

    def display_response(self, response):
        self.add_message("bot", response)
        self.is_typing = False
        self.send_btn.config(state=tk.NORMAL, text="Send")


def main():
    root = tk.Tk()
    app = ModernChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()