# chatbot_engine.py
from __future__ import annotations

import re
import difflib
from typing import Dict, List, Optional, Tuple

from rules import RULES

FALLBACK = "I'm not sure about that. Please contact the university administration."

class UniversityFAQBot:
    def __init__(self, show_trace: bool = False):
        # Default: answer only (no trace). This fixes your "it prints the code/trace" problem.
        self.show_trace = show_trace

        # Lightweight conversation memory (only for real follow-ups)
        self.last_topic: Optional[str] = None

        # Synonyms (simple + reliable)
        self.synonyms = {
            "sign up": "register",
            "enrol": "enroll",
            "enrolling": "enroll",
            "registered": "register",
            "registering": "register",
            "course selection": "register",
            "add classes": "register",
            "take courses": "register",
            "academic record": "transcript",
        }
        self._multiword = sorted([k for k in self.synonyms if " " in k], key=len, reverse=True)

        # Safety thresholds (tuned so you get answers for real FAQ and fallback for random questions)
        self.min_keyword_hits = 1
        self.min_score = 1.0

    # -------- preprocessing --------
    def _normalize(self, text: str) -> str:
        t = (text or "").lower().strip()
        for phrase in self._multiword:
            t = t.replace(phrase, self.synonyms[phrase])
        t = re.sub(r"[^\w\s']", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def _tokenize(self, norm: str) -> List[str]:
        return [x for x in norm.split() if x]

    # -------- intent detection (simple) --------
    def _intent(self, tokens: List[str]) -> str:
        if any(w in tokens for w in ["when", "date", "open", "start"]):
            return "when"
        if any(w in tokens for w in ["how", "process", "steps"]):
            return "how"
        if any(w in tokens for w in ["what", "which"]):
            return "what"
        return "general"

    # -------- fuzzy matching --------
    def _fuzzy(self, a: str, b: str, thr: float = 0.82) -> bool:
        if a == b:
            return True
        if difflib.SequenceMatcher(None, a, b).ratio() >= thr:
            return True
        # allow matching parts of multi-word keywords
        for part in b.split():
            if difflib.SequenceMatcher(None, a, part).ratio() >= thr:
                return True
        return False

    # -------- scoring --------
    def _score_rule(self, rule: Dict, tokens: List[str], intent: str) -> Tuple[float, Dict]:
        score = 0.0
        evidence = {"hits": [], "fuzzy": [], "intent_ok": False}

        # intent bonus (only if rule supports it or rule is general)
        if intent in rule.get("intents", []) or "general" in rule.get("intents", []):
            evidence["intent_ok"] = True
            score += 0.5

        hit_count = 0
        for kw in rule.get("keywords", []):
            for tok in tokens:
                if tok == kw:
                    hit_count += 1
                    evidence["hits"].append((tok, kw))
                elif self._fuzzy(tok, kw):
                    hit_count += 1
                    evidence["fuzzy"].append((tok, kw))

        if hit_count < self.min_keyword_hits:
            return -1.0, evidence  # not enough domain evidence to answer

        score += hit_count * 1.0
        score = score * float(rule.get("weight", 1.0)) + float(rule.get("priority", 0)) * 0.1
        return score, evidence

    # -------- follow-up (context) --------
    def _maybe_use_context(self, norm: str, tokens: List[str], intent: str) -> Optional[str]:
        if self.last_topic is None:
            return None

        # Only allow context if the user is clearly referring back (it/that) and is short
        if len(tokens) <= 8 and ({"it", "that", "those", "them"} & set(tokens)) and intent in {"when", "how", "what"}:
            # If user introduced a new domain keyword, don't force old topic
            for r in RULES:
                for kw in r.get("keywords", []):
                    if kw in norm:
                        return None
            return self.last_topic
        return None

    # -------- public interface --------
    def get_response(self, user_input: str) -> str:
        raw = user_input or ""
        norm = self._normalize(raw)
        tokens = self._tokenize(norm)
        intent = self._intent(tokens)

        forced = self._maybe_use_context(norm, tokens, intent)
        candidate_topics = [forced] if forced else [r["topic"] for r in RULES if any(kw in norm for kw in r.get("keywords", []))]

        # If we found no domain topic at all -> hard fallback (and clear memory)
        if not candidate_topics:
            self.last_topic = None
            return FALLBACK

        # Score rules within detected topics
        best: Optional[Tuple[Dict, float, Dict]] = None
        for r in RULES:
            if r["topic"] not in candidate_topics:
                continue
            score, ev = self._score_rule(r, tokens, intent)
            if score < 0:
                continue
            if best is None or score > best[1]:
                best = (r, score, ev)

        # If best is not confident enough -> fallback (and clear memory)
        if best is None or best[1] < self.min_score:
            self.last_topic = None
            return FALLBACK

        rule, score, ev = best
        self.last_topic = rule["topic"]

        answer = rule["response"]

        if not self.show_trace:
            return answer

        # Trace mode (only when explicitly enabled)
        lines = [
            answer,
            "",
            "--- REASONING TRACE ---",
            f"Input (normalized): {norm}",
            f"Detected intent: {intent}",
            f"Chosen topic: {rule['topic']}",
            f"Rule id: {rule['id']}",
            f"Score: {score:.2f}",
        ]
        if ev["hits"]:
            lines.append("Exact hits: " + ", ".join([f"{t}->{k}" for t, k in ev["hits"]]))
        if ev["fuzzy"]:
            lines.append("Fuzzy hits: " + ", ".join([f"{t}≈{k}" for t, k in ev["fuzzy"]]))
        return "\n".join(lines)
