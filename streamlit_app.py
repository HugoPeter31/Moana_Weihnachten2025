import streamlit as st
import time
import re
import random
from typing import List


# -----------------------------------------------------------------------------
# Why this structure:
# - A "wizard" (multi-step) makes the card feel like a story.
# - Session state avoids messy globals and keeps navigation predictable.
# - Validation prevents crashes and creates a smooth user experience.
# -----------------------------------------------------------------------------

APP_TITLE = "🎄 Frohe Weihnachten 🎄"
MAX_PHOTOS = 5


# ----------------------------
# Session state helpers
# ----------------------------
def init_state() -> None:
    """Initialize session variables once to keep the UI flow stable."""
    defaults = {
        "page": 1,
        "recipient_name": "",
        "photos": [],
        "easter_clicks": 0,
        "appreciation_points": [
            "Du bist immer für mich da – auch wenn’s stressig wird.",
            "Dein Humor rettet jeden Tag.",
            "Du hast ein riesiges Herz und denkst an andere.",
            "Mit dir wird’s nie langweilig.",
            "Du gibst mir das Gefühl von Zuhause.",
        ],
        "final_message": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to_page(page_number: int) -> None:
    """Navigate between pages without duplicating logic."""
    st.session_state.page = page_number


# ----------------------------
# Validation / UI utilities
# ----------------------------
def validate_name(name: str) -> bool:
    """Allow letters and spaces only (keeps the greeting clean)."""
    return bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß ]+", name.strip()))


def typing_effect(text: str, speed: float = 0.03) -> None:
    """Create a typing animation for emotional impact."""
    placeholder = st.empty()
    out = ""
    for ch in text:
        out += ch
        placeholder.markdown(out)
        time.sleep(speed)


def card_container_start() -> None:
    """A simple visual frame to make the card feel premium."""
    st.markdown(
        """
        <div style="
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 16px;
            padding: 18px;
            background: rgba(255,255,255,0.04);
        ">
        """,
        unsafe_allow_html=True,
    )


def card_container_end() -> None:
    """Close the HTML container."""
    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------
# Page renderers
# ----------------------------
def render_header() -> None:
    st.title(APP_TITLE)
    st.caption("Eine kleine interaktive Weihnachtskarte ❤️")


def render_navigation() -> None:
    """Top navigation that doesn't distract but gives control."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("⬅️ Zurück", disabled=st.session_state.page == 1, on_click=lambda: go_to_page(st.session_state.page - 1))

    with col2:
        st.write(f"**Seite {st.session_state.page} / 3**")

    with col3:
        st.button("Weiter ➡️", disabled=st.session_state.page == 3, on_click=lambda: go_to_page(st.session_state.page + 1))


def render_page_1() -> None:
    """
    Page 1: Intro (you can replace this with your existing version).
    Keeping it here as a working default.
    """
    card_container_start()
    st.subheader("✨ Willkommen")

    name_input = st.text_input("Wie heisst du?", value=st.session_state.recipient_name)

    if name_input:
        if validate_name(name_input):
            st.session_state.recipient_name = name_input.strip()
            st.success(f"Hi {st.session_state.recipient_name} 😊")
            st.write("Wenn du bereit bist, geht’s weiter zu unseren Momenten ❤️")
        else:
            st.warning("Bitte nur Buchstaben verwenden (keine Zahlen oder Sonderzeichen).")

    if st.button("🎁 Mini-Überraschung"):
        st.info(random.choice(["🎄 Du bist wunderbar.", "✨ Heute ist dein Tag.", "❤️ Schön, dass es dich gibt."]))

    card_container_end()


def render_photo_grid(photos: List) -> None:
    """Show up to 5 photos in a clean layout (3 top, 2 bottom)."""
    if not photos:
        st.info("Noch keine Fotos ausgewählt. Du kannst unten bis zu 5 Bilder hochladen.")
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
    """Page 2: photos + appreciation points + easter eggs."""
    card_container_start()
    st.subheader("📸 Unsere Momente")

    st.write("Hier kommen 5 Fotos von uns – einfach auswählen und es wird direkt schön angezeigt.")

    uploaded = st.file_uploader(
        "Fotos hochladen (max. 5)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    # Keep only first 5 photos to avoid layout issues and ensure the card remains tidy.
    if uploaded:
        st.session_state.photos = uploaded[:MAX_PHOTOS]

    render_photo_grid(st.session_state.photos)

    st.divider()
    st.subheader("💛 Was ich an dir schätze")

    # Editable list of appreciation points (personal touch).
    for idx, point in enumerate(st.session_state.appreciation_points):
        st.session_state.appreciation_points[idx] = st.text_input(
            f"Punkt {idx + 1}",
            value=point,
            key=f"app_point_{idx}",
        )

    # ----------------------------
    # Easter Egg #1: secret click
    # ----------------------------
    st.divider()
    col_a, col_b = st.columns([1, 5])
    with col_a:
        if st.button("✨"):
            st.session_state.easter_clicks += 1

    with col_b:
        st.caption("Kleiner Hinweis: manchmal lohnt es sich, auf Dinge mehrmals zu klicken… 😄")

    if st.session_state.easter_clicks >= 3:
        st.success("🎁 Easter Egg: Du bist (wirklich) meine Lieblingsperson. ❤️")

    # ----------------------------
    # Easter Egg #2: sister score
    # ----------------------------
    st.divider()
    st.subheader("🏆 Schwester-Score (nur zum Spass)")
    score = st.slider("Wie fest bist du die Beste?", min_value=0, max_value=100, value=98)

    if score >= 95:
        st.balloons()
        st.info("Okay… das ist unfair hoch. Aber korrekt 😄")

    card_container_end()


def render_page_3() -> None:
    """Page 3: final personal message with preview + optional 'open when' sections."""
    card_container_start()
    st.subheader("💌 Deine persönliche Weihnachtsbotschaft")

    st.session_state.final_message = st.text_area(
        "Schreibe hier deine persönliche Nachricht",
        value=st.session_state.final_message,
        height=160,
        placeholder="Liebe ..., ich wünsche dir ...",
    )

    signature = st.text_input("Signatur (optional)", value="Mit Liebe, Hugo")

    st.divider()
    st.subheader("👀 Vorschau")
    preview_name = st.session_state.recipient_name or "du"

    preview_text = st.session_state.final_message.strip()
    if not preview_text:
        st.info("Schreib eine Nachricht, dann erscheint hier die Vorschau.")
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
                <p style="white-space: pre-wrap;">{preview_text}</p>
                <p style="opacity:0.8; margin-bottom:0;">{signature}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Optional: "Open when..." small surprises
    st.divider()
    st.subheader("📬 Open when… (Mini-Überraschungen)")
    with st.expander("Open when du lachst 😄"):
        st.write("Dann weiss ich, dass alles gut ist. Und falls nicht: ich bringe Snacks.")
    with st.expander("Open when du gestresst bist 🫶"):
        st.write("Atme. Du schaffst das. Und ich bin da.")
    with st.expander("Open when du mich vermisst ❤️"):
        st.write("Ich dich auch. Immer.")

    card_container_end()


# ----------------------------
# App entry point
# ----------------------------
def main() -> None:
    """
    Main orchestrator:
    - Initializes state
    - Renders the correct page
