import random
import re
import time
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

import streamlit as st
import streamlit.components.v1 as components


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
# Styling & animations
# ----------------------------
def apply_christmas_theme() -> None:
    """
    Inject a subtle Christmas theme via CSS.
    WHY: Streamlit theming from code is limited; CSS ensures a consistent holiday look.
    """
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at 20% 0%, rgba(220, 0, 0, 0.10), transparent 40%),
                        radial-gradient(circle at 80% 0%, rgba(0, 130, 0, 0.10), transparent 40%),
                        linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.98));
        }

        h1, h2, h3 {
            letter-spacing: 0.2px;
        }

        .xmas-card {
            padding: 18px 18px;
            border-radius: 18px;
            border: 1px solid rgba(200,200,200,0.55);
            background: rgba(255,255,255,0.75);
            box-shadow: 0 10px 24px rgba(0,0,0,0.06);
            backdrop-filter: blur(6px);
            margin-bottom: 12px;
        }

        div.stButton > button {
            border-radius: 14px;
            padding: 0.6rem 1rem;
            border: 1px solid rgba(0,0,0,0.08);
            box-shadow: 0 6px 14px rgba(0,0,0,0.06);
        }

        .xmas-divider {
            height: 1px;
            width: 100%;
            margin: 14px 0;
            background: linear-gradient(90deg, transparent, rgba(200,0,0,0.35), rgba(0,120,0,0.35), transparent);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def trigger_balloons() -> None:
    """
    Set a one-shot flag so balloons show once on the next page render.
    WHY: Streamlit reruns; session_state is the reliable way to control animations.
    """
    st.session_state.show_balloons_once = True


def maybe_show_balloons() -> None:
    """
    Render balloon animation only once after navigation.
    The flag is cleared immediately so it won't replay on other reruns.
    """
    if not st.session_state.get("show_balloons_once", False):
        return

    st.session_state.show_balloons_once = False

    balloons_html = """
    <div id="balloons-overlay">
      <div class="balloon b1"></div>
      <div class="balloon b2"></div>
      <div class="balloon b3"></div>
      <div class="balloon b4"></div>
      <div class="balloon b5"></div>
      <div class="balloon b6"></div>
    </div>

    <style>
      #balloons-overlay{
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 9999;
        overflow: hidden;
      }
      .balloon{
        position: absolute;
        bottom: -120px;
        width: 52px;
        height: 70px;
        border-radius: 50% 50% 45% 45%;
        opacity: 0.92;
        filter: drop-shadow(0 10px 12px rgba(0,0,0,0.12));
        animation: flyUp 2.2s ease-in forwards;
      }
      .balloon::after{
        content:"";
        position:absolute;
        left: 50%;
        top: 68px;
        width: 2px;
        height: 52px;
        background: rgba(0,0,0,0.12);
        transform: translateX(-50%);
      }

      /* Christmas-ish palette */
      .b1{ left: 8%;  background: rgba(200,  0,  0, 0.85); animation-delay: 0.00s; }
      .b2{ left: 22%; background: rgba(  0,120,  0, 0.85); animation-delay: 0.10s; }
      .b3{ left: 40%; background: rgba(220,180,  0, 0.85); animation-delay: 0.18s; }
      .b4{ left: 58%; background: rgba(180,  0,120, 0.80); animation-delay: 0.06s; }
      .b5{ left: 76%; background: rgba(  0, 90,160, 0.80); animation-delay: 0.14s; }
      .b6{ left: 90%; background: rgba(230, 60, 60, 0.75); animation-delay: 0.22s; }

      @keyframes flyUp{
        0%   { transform: translateY(0) rotate(-2deg); }
        25%  { transform: translateY(-30vh) translateX(10px) rotate(2deg); }
        60%  { transform: translateY(-75vh) translateX(-8px) rotate(-2deg); }
        100% { transform: translateY(-120vh) translateX(4px) rotate(2deg); opacity: 0; }
      }
    </style>
    """
    components.html(balloons_html, height=0)


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
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url

    path = Path(path_or_url)
    return str(path) if path.exists() else None


def goto_page(page: str) -> None:
    """Navigate to another page and trigger a one-shot celebration animation."""
    st.session_state.page = page
    trigger_balloons()


def init_state() -> None:
    """
    Initialize session_state defaults once.
    This prevents KeyErrors and keeps app behavior predictable.
    """
    st.session_state.setdefault("page", "card")
    st.session_state.setdefault("message_shown", False)
    st.session_state.setdefault("last_surprise", None)
    st.session_state.setdefault("validated_name", None)
    st.session_state.setdefault("final_shown", False)
    st.session_state.setdefault("show_balloons_once", False)


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

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    name_input = st.text_input("Wie heisst du?")
    st.markdown("</div>", unsafe_allow_html=True)

    if not name_input:
        return

    if not validate_name(name_input):
        st.warning("Bitte gib einen gültigen Namen ein (nur Buchstaben, keine Zahlen).")
        return

    st.session_state.validated_name = name_input.strip()

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    show_personal_message(st.session_state.validated_name)
    st.markdown('<div class="xmas-divider"></div>', unsafe_allow_html=True)
    show_surprise()
    st.info(f"⏳ Noch {days_until_christmas()} Tage bis Weihnachten")
    st.markdown("</div>", unsafe_allow_html=True)

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

    pairs: List[Tuple[str, str]] = list(zip(PHOTO_PATHS, PHOTO_CAPTIONS))
    if len(pairs) < 5:
        st.warning("Hinweis: Du hast weniger als 5 Fotos/Captions definiert.")
    if len(pairs) > 5:
        pairs = pairs[:5]

    for idx, (path_or_url, caption) in enumerate(pairs, start=1):
        st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
        st.subheader(f"Moment {idx}")

        resolved = safe_image(path_or_url)
        if resolved is None:
            st.warning(f"Foto nicht gefunden: `{path_or_url}` (Pfad prüfen)")
        else:
            st.image(resolved, use_container_width=True)

        st.write(caption)
        st.markdown("</div>", unsafe_allow_html=True)

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

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    st.markdown(f"### {greeting}")

    if not st.session_state.get("final_shown", False):
        typing_effect(FINAL_PERSONAL_TEXT)
        st.session_state.final_shown = True
    else:
        st.markdown(FINAL_PERSONAL_TEXT)

    st.markdown("</div>", unsafe_allow_html=True)

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

    # Theme + one-shot balloons (on navigation)
    apply_christmas_theme()
    maybe_show_balloons()

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
