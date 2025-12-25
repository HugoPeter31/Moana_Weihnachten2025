import random
import re
import time
from datetime import date
from typing import List

import streamlit as st


# =============================================================================
# 🎄 INTERAKTIVE WEIHNACHTSKARTE (Streamlit Wizard, 3 Seiten)
# =============================================================================
# Why this design:
# - A wizard (step-by-step flow) feels like opening a real card: intro → memories → message.
# - Session State keeps navigation stable (no fragile global variables / rerun surprises).
# - Input validation avoids crashes and creates a smooth experience (especially for gifts).
# =============================================================================


# ----------------------------
# Configuration (easy to tweak)
# ----------------------------
APP_TITLE = "🎄 Frohe Weihnachten 🎄"
MAX_PHOTOS = 5

DEFAULT_APPRECIATION_POINTS = [
    "Du bist immer für mich da – auch wenn’s stressig wird.",
    "Dein Humor rettet jeden Tag.",
    "Du hast ein riesiges Herz und denkst an andere.",
    "Mit dir wird’s nie langweilig.",
    "Du gibst mir das Gefühl von Zuhause.",
]


# ----------------------------
# Session state helpers
# ----------------------------
def init_state() -> None:
    """
    Initialize session variables once.
    This prevents accidental KeyErrors and keeps the app flow deterministic.
    """
    defaults = {
        "page": 1,
        "recipient_name": "",
        "easter_clicks": 0,
        "photos": [],
        "appreciation_points": DEFAULT_APPRECIATION_POINTS.copy(),
        "final_message": "",
        "signature": "Mit Liebe, Hugo",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to_page(page_number: int) -> None:
    """Small helper to keep navigation logic in one place."""
    st.session_state.page = max(1, min(3, page_number))


# ----------------------------
# Validation & small utilities
# ----------------------------
def validate_name(name: str) -> bool:
    """
    Validate the recipient name input.
    We only allow letters and spaces to keep greetings clean and avoid weird formatting.
    """
    return bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß ]+", name.strip()))


def typing_effect(text: str, speed: float = 0.03) -> None:
    """
    Render text character-by-character.
    WHY: A typing animation adds emotional "unwrapping" and feels more personal.
    """
    placeholder = st.empty()
    out = ""
    for ch in text:
        out += ch
        placeholder.markdown(out)
        time.sleep(speed)


def days_until_next_christmas() -> int:
    """
    Calculate days until next Christmas (Dec 25).
    Handles 'after Christmas' case by rolling into next year.
    """
    today = date.today()
    christmas = date(today.year, 12, 25)
    if today > christmas:
        christmas = date(today.year + 1, 12, 25)
    return (christmas - today).days


# ----------------------------
# Styling helpers
# ----------------------------
def card_container_start() -> None:
    """Simple premium-looking card container (lightweight HTML/CSS)."""
    st.markdown(
        """
        <div style="
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 18px;
            padding: 18px;
            background: rgba(255,255,255,0.05);
            box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        ">
        """,
        unsafe_allow_html=True,
    )


def card_container_end() -> None:
    """Close the card container."""
    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------
# Common UI sections
# ----------------------------
def render_header() -> None:
    st.title(APP_TITLE)
    st.caption("Eine kleine interaktive Weihnachtskarte ❤️")


def render_navigation() -> None:
    """
    Minimal navigation:
    - Keeps user oriented (page indicator)
    - Still feels like a 'card flow' rather than an app
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.button(
            "⬅️ Zurück",
            disabled=st.session_state.page == 1,
            on_click=lambda: go_to_page(st.session_state.page - 1),
        )

    with col2:
        st.write(f"**Seite {st.session_state.page} / 3**")

    with col3:
        st.button(
            "Weiter ➡️",
            disabled=st.session_state.page == 3,
            on_click=lambda: go_to_page(st.session_state.page + 1),
        )


# =============================================================================
# Page 1 — Intro (complete)
# =============================================================================
def render_page_1() -> None:
    """
    Page 1:
    - Name input with validation
    - Warm intro with typing effect
    - Small surprise button + countdown
    """
    card_container_start()
    st.subheader("✨ Willkommen")

    name_input = st.text_input(
        "Wie heisst du?",
        value=st.session_state.recipient_name,
        placeholder="z.B. Lea",
    )

    if name_input:
        if validate_name(name_input):
            st.session_state.recipient_name = name_input.strip()

            st.success(f"Hi {st.session_state.recipient_name} 😊")
            st.write("Wenn du bereit bist, geht’s weiter zu unseren Momenten ❤️")

            st.write("")  # spacing
            typing_effect(
                "Ich hab dir eine kleine digitale Weihnachtskarte gebaut 🎄✨\n"
                "Nicht perfekt, aber hoffentlich fühlt sie sich nach *uns* an.",
                speed=0.02,
            )
        else:
            st.warning("Bitte nur Buchstaben verwenden (keine Zahlen oder Sonderzeichen).")

    st.divider()

    col_a, col_b = st.columns([1, 2])
    with col_a:
        if st.button("🎁 Mini-Überraschung"):
            st.info(
                random.choice(
                    [
                        "🎄 Du bist wunderbar.",
                        "✨ Heute ist dein Tag.",
                        "❤️ Schön, dass es dich gibt.",
                        "☕ Ich schulde dir einen Kaffee (oder Glühwein).",
                        "🌟 Danke, dass du immer du bist.",
                    ]
                )
            )

    with col_b:
        st.caption(f"⏳ Noch {days_until_next_christmas()} Tage bis Weihnachten")

    card_container_end()


# =============================================================================
# Page 2 — Photos + appreciation + Easter Eggs
# =============================================================================
def render_photo_grid(photos: List) -> None:
    """
    Show up to 5 photos in a clean layout (3 top, 2 bottom).
    WHY: This layout stays readable on laptops and doesn't feel cluttered.
    """
    if not photos:
        st.info("Noch keine Fotos ausgewählt. Unten kannst du bis zu 5 Bilder hochladen.")
        return

    photos = photos[:MAX_PHOTOS]
    top = photos[:3]
    bottom = photos[3:]

    cols = st.columns(3)
    for i, img in enumerate(top):
        cols[i].image(img, use_container_width=True)

    if bottom:
        cols2 = st.columns(2)
        for i, img in enumerate(bottom):
            cols2[i].image(img, use_container_width=True)


def render_page_2() -> None:
    """
    Page 2:
    - Upload up to 5 photos
    - Editable "what I appreciate" list
    - Two Easter Eggs:
      1) Click ✨ 3 times -> secret message
      2) Slider >= 95 -> balloons + message
    """
    card_container_start()
    st.subheader("📸 Unsere Momente")

    st.write("Wähle bis zu **5 Fotos** von uns aus – sie werden direkt schön angezeigt.")

    uploaded = st.file_uploader(
        "Fotos hochladen (max. 5)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    # Keep only first 5 images so the card always stays elegant.
    if uploaded:
        st.session_state.photos = uploaded[:MAX_PHOTOS]

    render_photo_grid(st.session_state.photos)

    st.divider()
    st.subheader("💛 Was ich an dir schätze")

    for idx, point in enumerate(st.session_state.appreciation_points):
        st.session_state.appreciation_points[idx] = st.text_input(
            f"Punkt {idx + 1}",
            value=point,
            key=f"app_point_{idx}",
        )

    # ----------------------------
    # Easter Egg #1 — secret click
    # ----------------------------
    st.divider()
    col_a, col_b = st.columns([1, 5])
    with col_a:
        if st.button("✨"):
            st.session_state.easter_clicks += 1

    with col_b:
        st.caption("Kleiner Hinweis: manchmal lohnt es sich, Dinge mehrmals anzuklicken… 😄")

    if st.session_state.easter_clicks >= 3:
        st.success("🎁 Easter Egg: Du bist (wirklich) meine Lieblingsperson. ❤️")

    # ----------------------------
    # Easter Egg #2 — sister score
    # ----------------------------
    st.divider()
    st.subheader("🏆 Schwester-Score (nur zum Spass)")
    score = st.slider("Wie fest bist du die Beste?", min_value=0, max_value=100, value=98)

    if score >= 95:
        st.balloons()
        st.info("Okay… das ist unfair hoch. Aber korrekt 😄")

    card_container_end()


# =============================================================================
# Page 3 — Final message + preview + "Open when..."
# =============================================================================
def render_page_3() -> None:
    """
    Page 3:
    - Write final personal message
    - Show a nice preview in a card style
    - Add 'Open when...' expandable mini messages
    """
    card_container_start()
    st.subheader("💌 Deine persönliche Weihnachtsbotschaft")

    st.session_state.final_message = st.text_area(
        "Schreibe hier deine persönliche Nachricht",
        value=st.session_state.final_message,
        height=170,
        placeholder="Liebe ..., ich wünsche dir ...",
    )

    st.session_state.signature = st.text_input(
        "Signatur (optional)",
        value=st.session_state.signature,
    )

    st.divider()
    st.subheader("👀 Vorschau")

    preview_name = st.session_state.recipient_name.strip() or "du"
    preview_text = st.session_state.final_message.strip()

    if not preview_text:
        st.info("Schreib eine Nachricht – dann erscheint hier die Vorschau.")
    else:
        st.markdown(
            f"""
            <div style="
                border-radius: 18px;
                padding: 18px;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.22);
            ">
                <h4 style="margin-top:0;">Liebe {preview_name} 🎄</h4>
                <p style="white-space: pre-wrap; margin-bottom: 10px;">{preview_text}</p>
                <p style="opacity:0.85; margin:0;">{st.session_state.signature}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("📬 Open when… (Mini-Überraschungen)")

    with st.expander("Open when du lachst 😄"):
        st.write("Dann weiss ich, dass alles gut ist. Und falls nicht: ich bringe Snacks.")
    with st.expander("Open when du gestresst bist 🫶"):
        st.write("Atme. Du schaffst das. Und ich bin da.")
    with st.expander("Open when du mich vermisst ❤️"):
        st.write("Ich dich auch. Immer.")

    card_container_end()


# =============================================================================
# App entry point
# =============================================================================
def main() -> None:
    """
    Main orchestrator:
    - Initializes state
    - Renders the current wizard page
    - Keeps navigation consistent
    """
    st.set_page_config(page_title="Weihnachtskarte", page_icon="🎄", layout="centered")
    init_state()

    render_header()
    render_navigation()
    st.write("")  # small spacing

    if st.session_state.page == 1:
        render_page_1()
    elif st.session_state.page == 2:
        render_page_2()
    else:
        render_page_3()


if __name__ == "__main__":
    main()
