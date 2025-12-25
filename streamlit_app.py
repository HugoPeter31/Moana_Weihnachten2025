import streamlit as st
import time
from datetime import date
import re
import random


# ----------------------------
# Configuration constants
# ----------------------------
APP_TITLE = "🎄 Frohe Weihnachten 🎄"
RECIPIENT_RELATION = "eine meiner Lieblingsschwestern"


# ----------------------------
# Helper functions
# ----------------------------
def validate_name(name: str) -> bool:
    """
    Validate the user's name input.
    Only letters and spaces are allowed to keep the greeting personal and clean.
    """
    return bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß ]+", name.strip()))


def typing_effect(text: str, speed: float = 0.04) -> None:
    """
    Display text character by character to create a typing animation.
    This enhances the emotional impact of the message.
    """
    placeholder = st.empty()
    rendered_text = ""

    for char in text:
        rendered_text += char
        placeholder.markdown(rendered_text)
        time.sleep(speed)


def days_until_christmas() -> int:
    """
    Calculate the number of days until next Christmas.
    Handles the case where Christmas of the current year has already passed.
    """
    today = date.today()
    christmas = date(today.year, 12, 25)

    if today > christmas:
        christmas = date(today.year + 1, 12, 25)

    return (christmas - today).days


# ----------------------------
# UI sections
# ----------------------------
def show_header() -> None:
    """Display the application header and introduction."""
    st.title(APP_TITLE)
    st.subheader(f"Eine kleine digitale Überraschung für {RECIPIENT_RELATION} ❤️")


def show_personal_message(name: str) -> None:
    """Show the animated Christmas message."""
    message = (
        f"Liebe {name},\n\n"
        "ich wünsche dir von Herzen wunderschöne Weihnachten 🎄✨\n"
        "voller Wärme, Lachen und ganz vielen schönen Momenten.\n\n"
        "Danke, dass es dich gibt ❤️"
    )
    typing_effect(message)


def show_surprise() -> None:
    """Display a random Christmas wish as a small interactive surprise."""
    wishes = [
        "🎁 Lebkuchenhaus backen",
        "✨ Gemeinsam Guetzle",
        "☕ Zusammen Squashen",
    ]

    if st.button("🎄 Überraschung öffnen"):
        st.success(random.choice(wishes))


# ----------------------------
# Main application
# ----------------------------
def main() -> None:
    """
    Main entry point of the Streamlit app.
    Orchestrates user input, validation, and UI flow.
    """
    show_header()

    name_input = st.text_input("Wie heisst du?")

    if name_input:
        if validate_name(name_input):
            st.divider()
            show_personal_message(name_input.strip())

            st.divider()
            show_surprise()

            st.info(f"⏳ Noch {days_until_christmas()} Tage bis Weihnachten")
        else:
            st.warning(
                "Bitte gib einen gültigen Namen ein (nur Buchstaben, keine Zahlen)."
            )


if __name__ == "__main__":
    main()
