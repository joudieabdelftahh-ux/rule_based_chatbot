"""
bot_brain.py
------------
The brain of RuleBot.
Contains the RuleBot class with all rules, cleaning logic, and response matching.
No UI code lives here — this file is purely about language and logic.
"""

import re
import random


class RuleBot:
    """
        exact match  — cleaned input equals a keyword exactly
         partial match — a keyword is found anywhere inside the input
         fallback      — no match found
    """

    FALLBACK = "I don't have a rule for that yet. Try saying hello or asking for a joke!"

    def __init__(self):
        self._rules = self._build_rules()

    # ─ public API

    def get_response(self, user_input: str) -> str:
        """Return a response string for the given user input."""
        cleaned = self._clean(user_input)

        if not cleaned:
            return "Please type something first!"

        return (
            self._exact_match(cleaned)
            or self._partial_match(cleaned)
            or self.FALLBACK
        )

    # ** Private helpers
    @staticmethod
    def _clean(text: str) -> str:
        """Lowercase, strip punctuation, and trim whitespace."""
        return re.sub(r"[^\w\s]", "", text.lower()).strip()

    @staticmethod
    def _pick(responses: list[str]) -> str:
        """Pick a random response from a list."""
        return random.choice(responses)

    def _exact_match(self, cleaned: str) -> str | None:
        for rule in self._rules:
            if cleaned in rule["keywords"]:
                return self._pick(rule["responses"])
        return None

    def _partial_match(self, cleaned: str) -> str | None:
        for rule in self._rules:
            for keyword in rule["keywords"]:
                if keyword in cleaned:
                    return self._pick(rule["responses"])
        return None

    # **rules data
    @staticmethod
    def _build_rules() -> list[dict]:
    
        return [
            {
                "keywords": ["hello", "hi", "hey", "howdy"],
                "responses": [
                    "Hey there! Great to see you!",
                    "Hi! How can I help?",
                    "Hello! What's on your mind?",
                ],
            },
            {
                "keywords": ["bye", "goodbye", "see you", "later", "cya"],
                "responses": [
                    "Goodbye! Come back anytime!",
                    "See you later! Take care!",
                    "Bye! It was nice chatting.",
                ],
            },
            {
                "keywords": ["joke", "funny", "laugh", "humor"],
                "responses": [
                    "Why did the programmer quit? Because they didn't get arrays!",
                    "Why do Java devs wear glasses? Because they don't C#.",
                    "I told my dog she was adopted. She said: 'I knew it — you never fetch.'",
                ],
            },
            {
                "keywords": ["name", "who are you", "what are you called"],
                "responses": [
                    "I'm RuleBot — a simple rule-based chatbot!",
                    "My name is RuleBot. Nice to meet you!",
                ],
            },
            {
                "keywords": ["how are you", "how re you", "you okay", "you good"],
                "responses": [
                    "I'm doing great, thanks for asking!",
                    "Running perfectly — all rules firing correctly.",
                ],
            },
            {
                "keywords": ["what do you do", "help", "capabilities", "can you"],
                "responses": [
                    "I match your words against preset rules and reply. Simple but effective!",
                    "I respond to keywords — try asking for a joke or saying hello.",
                ],
            },
            {
                "keywords": ["thanks", "thank you", "thx", "ty"],
                "responses": [
                    "You're very welcome!",
                    "Happy to help!",
                    "Anytime!",
                ],
            },
            {
                "keywords": ["weather", "forecast"],
                "responses": ["I can't check the weather — but I hear it's always sunny in chat!"],
            },
            {
                "keywords": ["time", "date", "today"],
                "responses": ["I don't have a clock, but your device should!"],
            },
            {
                "keywords": ["age", "how old"],
                "responses": ["I was just compiled — so pretty young!"],
            },
            {
                "keywords": ["good", "great", "nice", "awesome", "amazing"],
                "responses": ["Glad to hear it!", "That's wonderful!"],
            },
            {
                "keywords": ["bad", "sad", "upset", "terrible", "awful"],
                "responses": ["I'm sorry to hear that. Hope things look up soon."],
            },
        ]
