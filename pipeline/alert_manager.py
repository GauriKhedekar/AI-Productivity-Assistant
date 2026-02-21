"""
User alert and interaction system for email decisions.
Supports both GUI (tkinter) and console-based prompts.
"""
import sys
from typing import Tuple


class AlertManager:
    """
    Handles user alerts and confirmations.
    Falls back to console input if GUI is unavailable.
    """

    def __init__(self, use_gui: bool = True):
        self.use_gui = use_gui
        self.gui_available = False
        
        if use_gui:
            try:
                import tkinter as tk
                from tkinter import messagebox
                self.tk = tk
                self.messagebox = messagebox
                self.gui_available = True
            except ImportError:
                print("GUI not available. Using console input.")
                self.use_gui = False

    def show_email_alert(self, sender: str, subject: str, preview: str) -> Tuple[bool, bool]:
        """
        Show alert for suspicious email found in spam folder.
        Returns (move_to_inbox, add_to_trusted)
        """
        if self.gui_available:
            return self._show_gui_alert(sender, subject, preview)
        else:
            return self._show_console_alert(sender, subject, preview)

    def _show_gui_alert(self, sender: str, subject: str, preview: str) -> Tuple[bool, bool]:
        """Show GUI-based alert dialog."""
        try:
            root = self.tk.Tk()
            root.withdraw()  # Hide the main window

            message = f"""
Potentially Important Email Found in SPAM:

From: {sender}
Subject: {subject}

Preview: {preview[:200]}...

Actions:
1. Move to INBOX?
2. Add sender to trusted list?
            """

            # Create a custom dialog
            move_to_inbox = self.messagebox.askyesno(
                "Move to INBOX?",
                f"Move this email to INBOX?\n\nFrom: {sender}\nSubject: {subject}"
            )

            add_to_trusted = False
            if move_to_inbox:
                add_to_trusted = self.messagebox.askyesno(
                    "Trust Sender?",
                    f"Add {sender} to trusted senders list?"
                )

            root.destroy()
            return move_to_inbox, add_to_trusted
        except Exception as e:
            print(f"Error showing GUI alert: {e}. Falling back to console.")
            return self._show_console_alert(sender, subject, preview)

    def _show_console_alert(self, sender: str, subject: str, preview: str) -> Tuple[bool, bool]:
        """Show console-based alert with user prompts."""
        print("\n" + "=" * 70)
        print("⚠️  IMPORTANT EMAIL FOUND IN SPAM FOLDER")
        print("=" * 70)
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Preview: {preview[:300]}")
        print("=" * 70)

        # Ask about moving to inbox
        move_response = self._prompt_yes_no("Move this email to INBOX?")

        # Ask about trusting sender
        add_to_trusted = False
        if move_response:
            add_to_trusted = self._prompt_yes_no(f"Add {sender} to trusted senders?")

        print("=" * 70 + "\n")
        return move_response, add_to_trusted

    @staticmethod
    def _prompt_yes_no(question: str) -> bool:
        """Prompt user for yes/no response."""
        while True:
            response = input(f"{question} (yes/no): ").strip().lower()
            if response in ["yes", "y"]:
                return True
            elif response in ["no", "n"]:
                return False
            else:
                print("Please enter 'yes' or 'no'.")

    def show_info(self, title: str, message: str) -> None:
        """Show informational message."""
        if self.gui_available:
            try:
                root = self.tk.Tk()
                root.withdraw()
                self.messagebox.showinfo(title, message)
                root.destroy()
            except:
                print(f"{title}: {message}")
        else:
            print(f"{title}: {message}")

    def show_warning(self, title: str, message: str) -> None:
        """Show warning message."""
        if self.gui_available:
            try:
                root = self.tk.Tk()
                root.withdraw()
                self.messagebox.showwarning(title, message)
                root.destroy()
            except:
                print(f"⚠️  {title}: {message}")
        else:
            print(f"⚠️  {title}: {message}")

    def show_priority_keyword_alert(self, sender: str, subject: str, preview: str, keywords_found: list) -> Tuple[bool, bool]:
        """
        Show alert for spam email containing priority keywords.
        Returns (move_to_inbox, add_to_trusted)
        """
        if self.gui_available:
            return self._show_gui_priority_alert(sender, subject, preview, keywords_found)
        else:
            return self._show_console_priority_alert(sender, subject, preview, keywords_found)

    def _show_gui_priority_alert(self, sender: str, subject: str, preview: str, keywords_found: list) -> Tuple[bool, bool]:
        """Show GUI-based alert dialog for priority keywords in spam."""
        try:
            root = self.tk.Tk()
            root.withdraw()

            keywords_str = ", ".join(keywords_found)
            message = f"""
⚠️  PRIORITY EMAIL DETECTED IN SPAM FOLDER

Priority Keywords Found: {keywords_str}

From: {sender}
Subject: {subject}

Preview: {preview[:150]}...

This email contains keywords from your priority list.
Move it to INBOX?
            """

            move_to_inbox = self.messagebox.askyesno(
                "Priority Email in Spam",
                f"Found keywords: {keywords_str}\n\nMove '{subject}' to INBOX?"
            )

            add_to_trusted = False
            if move_to_inbox:
                add_to_trusted = self.messagebox.askyesno(
                    "Trust Sender?",
                    f"Add {sender} to trusted senders list?"
                )

            root.destroy()
            return move_to_inbox, add_to_trusted
        except Exception as e:
            print(f"Error showing priority alert: {e}. Falling back to console.")
            return self._show_console_priority_alert(sender, subject, preview, keywords_found)

    def _show_console_priority_alert(self, sender: str, subject: str, preview: str, keywords_found: list) -> Tuple[bool, bool]:
        """Show console-based alert for priority keywords in spam."""
        keywords_str = ", ".join(keywords_found)
        print("\n" + "=" * 70)
        print(f"⚠️  PRIORITY EMAIL DETECTED IN SPAM FOLDER")
        print("=" * 70)
        print(f"Priority Keywords Found: {keywords_str}")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Preview: {preview[:300]}")
        print("=" * 70)

        # Ask about moving to inbox
        move_response = self._prompt_yes_no("Move this email to INBOX?")

        # Ask about trusting sender
        add_to_trusted = False
        if move_response:
            add_to_trusted = self._prompt_yes_no(f"Add {sender} to trusted senders?")

        print("=" * 70 + "\n")
        return move_response, add_to_trusted
