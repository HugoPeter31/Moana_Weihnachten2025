"""
Streamlit Christmas Card 🎄
--------------------------
A small interactive "digital Christmas card" with Easter eggs and a final photo + message reveal.

Design goals (WHY this is built this way):
- Clear structure (readable + maintainable).
- Robust inputs: no crashes on wrong/empty input; user can simply try again.
- Modular functions: each part does one thing well.
- Session state for navigation + Easter-egg progress.

Run:
  streamlit run christmas_card.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List

import random
import re
import time

import streamlit as st


# =============================================================================
# Configuration
# =============================================================================
APP_TITLE = "🎄 Interaktive Weihnachtskarte 🎄"
MIN_MESSAGE_LEN = 10
MAX_MESSAGE_LEN = 600
SECRET_KONAMI_PHRASE = "up up down down left right left right b a"


@dataclass(frozen=True)
class CardConfig:
    """Small bundle of constants to avoid hardcoding values throughout the app."""
    recipient_relation: str = "meiner Schwester"
    footer_hint: str = "Pssst… irgendwo versteckt sich ein kleines ✨"


CONFIG = CardConfig()


# =============================================================================
# Session state init
# =============================================================================
def init_session_state() -> None:
    """Initialize all session state values in one place (prevents KeyErrors)."""
    defaults = {
        "page": "start",  # start -> eastereggs -> final
        "recipient_name": "",
        "secret_unlocked": False,
        "sparkle_clicks": 0,
        "quiz_score": 0,
        "quiz_done": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


# =============================================================================
# Validation helpers
# =============================================================================
def validate_name(name: str) -> bool:
    """
    Only allow letters and spaces for a friendly greeting.
    WHY: Prevent ugly rendering + accidental numeric/symbol inputs.
    """
    return bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß ]+", name.strip()))


def is_valid_message(message: str) -> bool:
    """
    Validate message length.
    WHY: Avoid empty/meaningless messages and overly long text that breaks layout.
    """
    clean = message.strip()
    return MIN_MESSAGE_LEN <= len(clean) <= MAX_MESSAGE_LEN


def has_at_least_one_image(images: List[st.runtime.uploaded_file_manager.UploadedFile]) -> bool:
    """
    Ensure at least one image was uploaded.
    WHY: The final reveal should feel complete with a shared memory element.
    """
    return len(images) >= 1


# =============================================================================
# Small UI helpers
# =============================================================================
def typing_effect(text: str, speed: float = 0.03) -> None:
    """
    Display text character-by-character.
    WHY: Adds emotion and 'handwritten' vibe to a digital card.
    """
    placeholder = st.empty()
    rendered = ""
    for char in text:
        rendered += char
        placeholder.markdown(rendered)
        time.sleep(speed)


def days_until_next_christmas() -> int:
    """Return days until the next Christmas (handles the case where it's already passed)."""
    today = date.today()
    christmas = date(today.year, 12, 25)
    if today > christmas:
        christmas = date(today.year + 1, 12, 25)
    return (christmas - today).days


def set_page(page: str) -> None:
    """Centralize page changes for clarity."""
    st.session_state.page = page


# =============================================================================
# Page: Start
# =============================================================================
def page_start() -> None:
    st.title(APP_TITLE)
    st.subheader(f"Eine kleine digitale Überraschung für {CONFIG.recipient_relation} ❤️")

    st.write(
        "Diese Karte ist interaktiv: Es gibt kleine Easter-Eggs und am Schluss kommt der Final Reveal "
        "mit Fotos + persönlicher Grussbotschaft."
    )

    name_input = st.text_input("Wie heisst sie (oder Spitzname)?", value=st.session_state.recipient_name)

    if name_input and validate_name(name_input):
        st.session_state.recipient_name = name_input.strip()
    elif name_input:
        st.warning("Bitte nur Buchstaben und Leerzeichen verwenden (z.B. „Sofia“).")

    st.divider()

    if st.button("🎁 Los geht's", disabled=not bool(st.session_state.recipient_name)):
        set_page("eastereggs")

    st.caption(f"⏳ Noch {days_until_next_christmas()} Tage bis Weihnachten.")


# =============================================================================
# Page: Easter Eggs
# =============================================================================
def konami_easter_egg() -> None:
    """
    Secret phrase input.
    WHY: Easter eggs should be optional and never block the user.
    """
    st.markdown("### 🕹️ Geheimcode (optional)")
    code = st.text_input("Tipp: Manchmal ist der Code länger als man denkt…", key="konami_input")

    if code.strip().lower() == SECRET_KONAMI_PHRASE:
        st.session_state.secret_unlocked = True
        st.success("🎆 Secret Mode aktiviert! (Bonus im Finale freigeschaltet)")


def sparkle_footer_easter_egg() -> None:
    """
    A tiny clickable element (5 clicks unlocks secret).
    WHY: Fun 'hidden in plain sight' interaction.
    """
    cols = st.columns([6, 1])
    with cols[0]:
        st.caption(CONFIG.footer_hint)

    with cols[1]:
        if st.button("✨"):
            st.session_state.sparkle_clicks += 1
            if st.session_state.sparkle_clicks >= 5:
                st.session_state.secret_unlocked = True
                st.toast("Secret Mode aktiviert ✨", icon="🎄")


def mini_memory_quiz() -> None:
    """
    A tiny quiz. Correct answers unlock a bonus.
    WHY: Creates a playful story arc (challenge -> reward).
    """
    st.markdown("### 🧠 Mini-Quiz (optional)")
    st.write("Nur zum Spass — wenn du alles richtig hast, gibt’s einen Bonus im Finale 😄")

    q1 = st.radio("1) Welche Jahreszeit ist am besten für heisse Schoggi?", ["Sommer", "Herbst", "Winter"], index=None)
    q2 = st.radio("2) Was passt am besten zu Weihnachten?", ["Glühwein", "Sushi", "Eistee"], index=None)
    q3 = st.radio("3) Was ist das wichtigste Geschenk?", ["Stress", "Zeit zusammen", "Mehr To-Do’s"], index=None)

    can_submit = all(x is not None for x in [q1, q2, q3])

    if st.button("✅ Quiz abgeben", disabled=not can_submit) and not st.session_state.quiz_done:
        score = 0
        score += 1 if q1 == "Winter" else 0
        score += 1 if q2 == "Glühwein" else 0
        score += 1 if q3 == "Zeit zusammen" else 0

        st.session_state.quiz_score = score
        st.session_state.quiz_done = True

        if score == 3:
            st.session_state.secret_unlocked = True
            st.success("3/3 🎉 Bonus freigeschaltet!")
        else:
            st.info(f"{score}/3 – immer noch stark 😄 (Du kannst trotzdem weiter)")


def random_wish_generator() -> None:
    st.markdown("### 🎁 Wunsch-Generator")
    wishes = [
        "✨ Viele kleine Wunder im Alltag",
        "❤️ Mehr Zeit für dich",
        "☕ Gemütliche Abende & gute Gespräche",
        "🌟 Mut für neue Abenteuer",
        "🎄 Ein warmes Herz – egal wie kalt es draussen ist",
    ]
    if st.button("🎄 Wunsch ziehen"):
        st.success(random.choice(wishes))


def page_eastereggs() -> None:
    st.title("🎄 Easter-Egg Zone")

    name = st.session_state.recipient_name
    st.write(f"Okay {name}… oder besser gesagt: **du** als Karten-Master 😄")

    st.divider()
    random_wish_generator()

    st.divider()
    mini_memory_quiz()

    st.divider()
    konami_easter_egg()

    st.divider()
    sparkle_footer_easter_egg()

    st.divider()
    cols = st.columns(2)
    with cols[0]:
        if st.button("⬅️ Zurück"):
            set_page("start")
    with cols[1]:
        if st.button("🎁 Zum Final Reveal"):
            set_page("final")


# =============================================================================
# Page: Final Reveal (photos + message)
# =============================================================================
def show_gallery(images) -> None:
    """Render images as a simple gallery."""
    st.subheader("📸 Unsere Erinnerungen")
    cols = st.columns(3)
    for idx, img in enumerate(images):
        cols[idx % 3].image(img, use_container_width=True)


def page_final() -> None:
    st.title("🎁 Final Reveal")

    recipient = st.session_state.recipient_name
    st.write(
        f"Jetzt kommt der Abschluss: **Fotos hochladen** und **deine persönliche Grussbotschaft** "
        f"für **{recipient}**."
    )

    uploaded_images = st.file_uploader(
        "Fotos hochladen (PNG/JPG, mehrere möglich)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    message = st.text_area(
        "Deine Grussbotschaft 💌",
        placeholder="Schreib hier deine persönliche Nachricht…",
        height=160,
    )

    if uploaded_images:
        show_gallery(uploaded_images)

    st.divider()

    images_ok = has_at_least_one_image(uploaded_images or [])
    message_ok = is_valid_message(message) if message else False

    # Gentle guidance instead of exceptions/crashes
    if not images_ok:
        st.info("Tipp: Lade mindestens **1 Foto** hoch, damit der Final Reveal freigeschaltet wird.")
    if message and not message_ok:
        st.warning(f"Die Nachricht sollte {MIN_MESSAGE_LEN}–{MAX_MESSAGE_LEN} Zeichen haben.")

    reveal_enabled = images_ok and message_ok

    # Bonus content if secret mode is unlocked
    if st.session_state.secret_unlocked:
        st.success("🎆 Secret Mode ist aktiv: Bonus wird nach dem Reveal angezeigt!")

    cols = st.columns(2)
    with cols[0]:
        if st.button("⬅️ Zurück"):
            set_page("eastereggs")

    with cols[1]:
        if st.button("🎄 Karte final anzeigen", disabled=not reveal_enabled):
            st.balloons()

            # A slightly more emotional "letter style" output
            letter = (
                f"### 💌 Liebe {recipient}\n\n"
                f"{message.strip()}\n\n"
                "_Frohe Weihnachten 🎄✨_"
            )
            typing_effect(letter, speed=0.02)

            if st.session_state.secret_unlocked:
                st.divider()
                st.markdown("### 🗝️ Bonus (Secret Mode)")
                st.info("Du hast ein Easter Egg gefunden – du bist offiziell Weihnachtskarten-Profi 😄")
                st.markdown("**Bonus-Idee:** Drucke einen QR-Code mit dem Streamlit-Link und kleb ihn ans Geschenk.")


# =============================================================================
# App router
# =============================================================================
def main() -> None:
    init_session_state()

    # Sidebar navigation (keeps UX simple; users can always recover from wrong clicks)
    with st.sidebar:
        st.header("Navigation")
        st.write("Du kannst jederzeit zwischen den Seiten wechseln.")

        page_choice = st.radio(
            "Seite wählen",
            options=["start", "eastereggs", "final"],
            format_func=lambda p: {"start": "Start", "eastereggs": "Easter Eggs", "final": "Final Reveal"}[p],
            index=["start", "eastereggs", "final"].index(st.session_state.page),
        )
        st.session_state.page = page_choice

        st.divider()
        st.caption("Status")
        st.write(f"Secret Mode: {'✅' if st.session_state.secret_unlocked else '❌'}")
        st.write(f"✨ Klicks: {st.session_state.sparkle_clicks}/5")
        if st.session_state.quiz_done:
            st.write(f"Quiz: {st.session_state.quiz_score}/3")

    # Render current page
    if st.session_state.page == "start":
        page_start()
    elif st.session_state.page == "eastereggs":
        page_eastereggs()
    elif st.session_state.page == "final":
        page_final()
    else:
        # Safety fallback if a state is corrupted
        st.error("Unbekannte Seite – zurück zum Start.")
        set_page("start")


if __name__ == "__main__":
    main()
