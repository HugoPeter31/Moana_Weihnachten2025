import streamlit as st
import time
from datetime import date
import re
import random
from pathlib import Path
from typing import List, Tuple, Optional


# ----------------------------
# Configuration constants
# ----------------------------
APP_TITLE = "🎄 Frohe Weihnachten 🎄"
RECIPIENT_RELATION = "eine meiner Lieblingsschwestern"

# Tip: Put images in a local folder, e.g. ./assets/
# Example structure:
#   christmas_card_app.py
#   assets/
#     photo1.jpg
#     ...
PHOTO_PATHS: List[str] = [
    "assets/photo1.jpg",
    "assets/photo2.jpg",
    "assets/photo3.jpg",
    "assets/photo4.jpg",
    "assets/photo5.jpg",
]

PHOTO_CAPTIONS: List[str] = [
    "Unser Moment 1 – ich musste so lachen 😄",
    "Unser Moment 2 – einfach typisch wir ❤️",
    "Unser Moment 3 – ein kleines Abenteuer ✨",
    "Unser Moment 4 – das war so schön 🥹",
    "Unser Moment 5 – und davon bitte mehr! 🎁",
]

FINAL_PERSONAL_TEXT = (
    "Liebe Schwester\n\n"
    "Danke für all die Momente dieses Jahr – für dein Herz, deinen Humor "
    "und dafür, dass du immer da bist.\n\n"
    "Ich freue mich auf alles, was kommt – und vor allem auf Zeit mit dir. ❤️\n\n"
    "Frohe Weihnachten! 🎄✨"
)


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


def safe_image(path_or_url: str) -> Optional[str]:
    """
    Return a valid local path if it exists; otherwise None.
    We avoid crashing when images are missing.
    """
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url

    path = Path(path_or_url)
    return str(path) if path.exists() else None


def goto_page(page: str) -> None:
    """Central navigation helper to keep page transitions consistent."""
    st.session_state.page = page


def init_state() -> None:
    """
    Initialize session_state defaults once.
    This prevents KeyErrors and keeps app behavior predictable.
    """
    st.session_state.setdefault("page", "card")
    st.session_state.setdefault("message_shown", False)
    st.session_state.setdefault("last_surprise", None)
    st.session_state.setdefault("validated_name", None)


# ----------------------------
# UI sections (Page 1: Card)
# ----------------------------
def show_header() -> None:
    """Display the application header and introduction."""
    st.title(APP_TITLE)
    st.subheader(f"Eine kleine digitale Überraschung für {RECIPIENT_RELATION} ❤️")


def show_personal_message(name: str) -> None:
    """
    Show the animated Christmas message only once.
    Using session_state prevents re-triggering the typing animation.
    """
    message = (
        f"Liebe {name},\n\n"
        "ich wünsche dir von Herzen wunderschöne Weihnachten 🎄✨\n"
        "voller Wärme, Lachen und ganz vielen schönen Momenten.\n\n"
        "Danke, dass es dich gibt ❤️"
    )

    if not st.session_state.get("message_shown", False):
        typing_effect(message)
        st.session_state.message_shown = True
    else:
        st.markdown(message)


def show_surprise() -> None:
    """
    Display a random Christmas surprise.
    The chosen surprise is stored so it does not change unexpectedly.
    """
    wishes = [
        "🎄 Lebkuchenhaus backen",
        "✨ Gemeinsam Guetzle",
        "🏃 Zusammen Squashen",
    ]

    if st.button("🎄 Überraschung öffnen"):
        st.session_state.last_surprise = random.choice(wishes)

    if st.session_state.get("last_surprise"):
        st.success(st.session_state.last_surprise)


def render_card_page() -> None:
    """First page: original card + continue button."""
    show_header()

    name_input = st.text_input("Wie heisst du?")

    if not name_input:
        return

    if not validate_name(name_input):
        st.warning("Bitte gib einen gültigen Namen ein (nur Buchstaben, keine Zahlen).")
        return

    # Store validated name so later pages can reuse it (personal touch).
    st.session_state.validated_name = name_input.strip()

    st.divider()
    show_personal_message(st.session_state.validated_name)

    st.divider()
    show_surprise()

    st.info(f"⏳ Noch {days_until_christmas()} Tage bis Weihnachten")

    st.divider()
    if st.button("let’s continue ➜"):
        goto_page("gallery")
        st.rerun()


# ----------------------------
# UI sections (Page 2: Gallery)
# ----------------------------
def render_gallery_page() -> None:
    """Second page: 5 photos with short text."""
    st.title("📸 Kleine Erinnerungen")
    name = st.session_state.get("validated_name") or "du"
    st.caption(f"Für {name} – ein paar Momente, die ich nie vergesse ❤️")

    # Defensive programming: keep data aligned even if someone edits lists later.
    pairs: List[Tuple[str, str]] = list(zip(PHOTO_PATHS, PHOTO_CAPTIONS))
    if len(pairs) < 5:
        st.warning("Hinweis: Du hast weniger als 5 Fotos/Captions definiert.")
    if len(pairs) > 5:
        pairs = pairs[:5]

    for idx, (path_or_url, caption) in enumerate(pairs, start=1):
        st.subheader(f"Moment {idx}")
        resolved = safe_image(path_or_url)

        if resolved is None:
            st.warning(f"Foto nicht gefunden: `{path_or_url}` (Pfad prüfen)")
        else:
            st.image(resolved, use_container_width=True)

        st.write(caption)
        st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        if st.button("⬅️ zurück"):
            goto_page("card")
            st.rerun()
    with col_right:
        if st.button("Weiter zur Weihnachtskarte ➜"):
            goto_page("final")
            st.rerun()


# ----------------------------
# UI sections (Page 3: Final)
# ----------------------------
def render_final_page() -> None:
    """Third page: final personal message page."""
    st.title("🎁 Deine Weihnachtskarte")

    name = st.session_state.get("validated_name")
    greeting = f"Liebe {name}," if name else "Liebe Schwester,"
    st.markdown(f"### {greeting}")

    # We use typing only once to keep UX smooth.
    if not st.session_state.get("final_shown", False):
        typing_effect(FINAL_PERSONAL_TEXT)
        st.session_state.final_shown = True
    else:
        st.markdown(FINAL_PERSONAL_TEXT)

    st.divider()
    if st.button("⬅️ zurück zu den Fotos"):
        goto_page("gallery")
        st.rerun()


# ----------------------------
# Main application
# ----------------------------
def main() -> None:
    """
    Main entry point.
    A simple page router keeps the code in one file and easy to grade/review.
    """
    st.set_page_config(page_title=APP_TITLE, page_icon="🎄", layout="centered")

    init_state()

    page = st.session_state.page
    if page == "card":
        render_card_page()
    elif page == "gallery":
        render_gallery_page()
    elif page == "final":
        render_final_page()
    else:
        # Fallback to a safe default instead of crashing on corrupted state.
        goto_page("card")
        st.rerun()


if __name__ == "__main__":
    main()
