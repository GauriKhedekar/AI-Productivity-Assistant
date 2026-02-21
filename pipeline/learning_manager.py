import json
from pathlib import Path
from typing import Any, Dict
from email.utils import parseaddr


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
EMAIL_RULES_FILE = CONFIG_DIR / "email_rules.json"


DEFAULT_RULES = {
    "trusted_senders": [],
    "ignored_keywords": [],
    "priority_keywords": [],
    "mode": "balanced"
}


class LearningManager:
    """
    Manages email_rules.json directly.
    """

    def __init__(self, rules_file: Path = EMAIL_RULES_FILE):
        self.rules_file = rules_file
        self.data = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        if self.rules_file.exists():
            try:
                with self.rules_file.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading rules: {e}. Using defaults.")
                return DEFAULT_RULES.copy()
        return DEFAULT_RULES.copy()

    def save_rules(self) -> None:
        try:
            self.rules_file.parent.mkdir(parents=True, exist_ok=True)

            temp_file = self.rules_file.with_suffix(".tmp")
            with temp_file.open("w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

            temp_file.replace(self.rules_file)
            print("email_rules.json updated successfully.")

        except Exception as e:
            print(f"Error saving rules: {e}")

    # =========================
    # ADD FUNCTIONS
    # =========================

    def add_trusted_sender(self, sender: str):
        email = self._extract_email(sender)

        if email and email not in self.data["trusted_senders"]:
            self.data["trusted_senders"].append(email)
            self.save_rules()

    def add_ignored_keyword(self, keyword: str):
        keyword = keyword.lower().strip()
        if keyword and keyword not in self.data["ignored_keywords"]:
            self.data["ignored_keywords"].append(keyword)
            self.save_rules()

    # =========================
    # CHECK FUNCTIONS
    # =========================

    def is_trusted_sender(self, sender: str) -> bool:
        email = self._extract_email(sender)
        return email in self.data["trusted_senders"]

    def has_ignored_keywords(self, text: str) -> bool:
        text = text.lower()
        return any(k in text for k in self.data["ignored_keywords"])

    # =========================
    # UTIL
    # =========================

    @staticmethod
    def _extract_email(sender: str) -> str:
        _, email = parseaddr(sender)
        return email.lower().strip()   # ✅ FIXED (removed comma)
