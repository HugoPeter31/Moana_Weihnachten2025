import random
import re
import time
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

import streamlit as st
import streamlit.components.v1 as components


# =============================================================================
# 🎄 CONFIGURATION
# =============================================================================
APP_TITLE = "🎄 Frohe Weihnachten 🎄"
RECIPIENT_RELATION = "eine meiner Lieblingsschwestern"

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


# =============================================================================
# 🎨 FESTIVE THEME + CELEBRATION ANIMATIONS
# =============================================================================
def apply_festive_theme() -> None:
    """
    Inject a more festive Christmas theme (background, glow, ribbons, cards).
    WHY: A strong visual style makes the app feel like a real "digital gift".
    """
    st.markdown(
        """
        <style>
        /* ---------- Page background (soft festive gradient + subtle sparkle) ---------- */
        .stApp {
            background:
                radial-gradient(circle at 15% 5%, rgba(205, 0, 0, 0.14), transparent 45%),
                radial-gradient(circle at 85% 10%, rgba(0, 130, 0, 0.14), transparent 45%),
                radial-gradient(circle at 40% 0%, rgba(230, 200, 0, 0.10), transparent 38%),
                linear-gradient(180deg, rgba(255,255,255,0.98), rgba(252,252,252,0.98));
        }

        /* ---------- Make the top header spacing feel like a "card" ---------- */
        header[data-testid="stHeader"] {
            background: transparent;
        }

        /* ---------- Typography tweaks ---------- */
        h1, h2, h3 {
            letter-spacing: 0.25px;
        }
        h1 {
            text-shadow: 0 10px 30px rgba(200,0,0,0.10);
        }

        /* ---------- Card container ---------- */
        .xmas-card {
            position: relative;
            padding: 18px 18px;
            border-radius: 20px;
            border: 1px solid rgba(210,210,210,0.55);
            background: rgba(255,255,255,0.78);
            box-shadow: 0 16px 36px rgba(0,0,0,0.08);
            backdrop-filter: blur(7px);
            margin-bottom: 14px;
            overflow: hidden;
        }

        /* Ribbon on top-left corner */
        .xmas-card::before{
            content:"";
            position:absolute;
            top:-16px;
            left:-16px;
            width: 90px;
            height: 90px;
            background: radial-gradient(circle at 30% 30%, rgba(220,0,0,0.85), rgba(150,0,0,0.65));
            transform: rotate(12deg);
            border-radius: 18px;
            filter: drop-shadow(0 10px 12px rgba(0,0,0,0.10));
            opacity: 0.28;
        }

        /* Subtle golden glitter line */
        .xmas-divider {
            height: 1px;
            width: 100%;
            margin: 14px 0;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(210,160,0,0.35),
                rgba(200,0,0,0.30),
                rgba(0,120,0,0.30),
                rgba(210,160,0,0.35),
                transparent
            );
        }

        /* ---------- Buttons: "gift tag" look ---------- */
        div.stButton > button {
            border-radius: 14px;
            padding: 0.65rem 1.05rem;
            border: 1px solid rgba(0,0,0,0.10);
            background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(245,245,245,0.95));
            box-shadow: 0 10px 22px rgba(0,0,0,0.10);
            transition: transform 120ms ease, box-shadow 120ms ease;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 28px rgba(0,0,0,0.12);
        }

        /* ---------- Snow-like subtle animation on background (lightweight) ---------- */
        .xmas-sparkle {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 1;
            background-image:
                radial-gradient(rgba(255,255,255,0.65) 1px, transparent 1px),
                radial-gradient(rgba(255,255,255,0.45) 1px, transparent 1px);
            background-size: 110px 110px, 160px 160px;
            background-position: 0 0, 40px 60px;
            opacity: 0.30;
            animation: sparkleMove 12s linear infinite;
        }
        @keyframes sparkleMove {
            0% { transform: translateY(0); }
            100% { transform: translateY(40px); }
        }

        /* Ensure Sparkle overlay doesn't block content */
        section.main > div { position: relative; z-index: 2; }
        </style>

        <div class="xmas-sparkle"></div>
        """,
        unsafe_allow_html=True,
    )


def trigger_balloons() -> None:
    """
    Set a one-shot flag so balloons show once on the next page render.
    WHY: Streamlit reruns on any interaction; session_state is the clean control mechanism.
    """
    st.session_state.show_balloons_once = True


def maybe_show_balloons() -> None:
    """
    Render a fun balloon celebration only once after navigation.
    Cleared immediately so it won't replay on other reruns.
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
      <div class="balloon b7"></div>
      <div class="balloon b8"></div>
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
        bottom: -140px;
        width: 54px;
        height: 76px;
        border-radius: 50% 50% 45% 45%;
        opacity: 0.93;
        filter: drop-shadow(0 14px 16px rgba(0,0,0,0.14));
        animation: flyUp 2.4s cubic-bezier(.2,.9,.2,1) forwards;
      }

      .balloon::before{
        content:"";
        position:absolute;
        inset: 10px 12px auto auto;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: rgba(255,255,255,0.22);
        transform: rotate(18deg);
      }

      .balloon::after{
        content:"";
        position:absolute;
        left: 50%;
        top: 74px;
        width: 2px;
        height: 62px;
        background: rgba(0,0,0,0.14);
        transform: translateX(-50%);
      }

      /* More balloons + varied sizes for a richer effect */
      .b1{ left: 6%;  background: rgba(200,  0,  0, 0.86); animation-delay: 0.00s; transform: scale(0.95); }
      .b2{ left: 16%; background: rgba(  0,120,  0, 0.86); animation-delay: 0.08s; transform: scale(1.05); }
      .b3{ left: 28%; background: rgba(220,180,  0, 0.86); animation-delay: 0.16s; transform: scale(0.90); }
      .b4{ left: 40%; background: rgba(180,  0,120, 0.82); animation-delay: 0.05s; transform: scale(1.00); }
      .b5{ left: 52%; background: rgba(  0, 90,160, 0.82); animation-delay: 0.12s; transform: scale(0.92); }
      .b6{ left: 64%; background: rgba(230, 60, 60, 0.78); animation-delay: 0.20s; transform: scale(1.08); }
      .b7{ left: 78%; background: rgba( 40,150,120, 0.78); animation-delay: 0.10s; transform: scale(0.96); }
      .b8{ left: 90%; background: rgba(240,200, 60, 0.78); animation-delay: 0.22s; transform: scale(1.02); }

      @keyframes flyUp{
        0%   { transform: translateY(0) translateX(0) rotate(-3deg) scale(var(--s,1)); }
        25%  { transform: translateY(-28vh) translateX(12px) rotate(3deg) scale(var(--s,1)); }
        60%  { transform: translateY(-78vh) translateX(-10px) rotate(-2deg) scale(var(--s,1)); }
        100% { transform: translateY(-125vh) translateX(6px) rotate(2deg) scale(var(--s,1)); opacity: 0; }
      }
    </style>
    """
    components.html(balloons_html, height=0)


# =============================================================================
# 🧩 HELPER FUNCTIONS
# =============================================================================
def validate_name(name: str) -> bool:
    """
    Validate the user's name input.
    Only letters and spaces are allowed to keep the greeting personal and clean.
    """
    return bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß ]+", name.strip()))


def typing_effect(text: str, speed: float = 0.04) -> None:
    """
    Display text character by character to create a typing animation.
    WHY: Feels like a personal message being written live.
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
    WHY: Missing files should not crash the app (robustness for grading/demo).
    """
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url

    path = Path(path_or_url)
    return str(path) if path.exists() else None


def goto_page(page: str) -> None:
    """
    Navigate to another page and trigger balloons exactly once.
    """
    st.session_state.page = page
    trigger_balloons()


def init_state() -> None:
    """
    Initialize session_state defaults once.
    Prevents KeyErrors and keeps behavior stable across reruns.
    """
    st.session_state.setdefault("page", "card")
    st.session_state.setdefault("message_shown", False)
    st.session_state.setdefault("last_surprise", None)
    st.session_state.setdefault("validated_name", None)
    st.session_state.setdefault("final_shown", False)
    st.session_state.setdefault("show_balloons_once", False)


# =============================================================================
# 🎁 PAGE 1: CARD
# =============================================================================
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
    """First page: card + continue button."""
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


# =============================================================================
# 📸 PAGE 2: GALLERY
# =============================================================================
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


# =============================================================================
# 💌 PAGE 3: FINAL MESSAGE
# =============================================================================
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


# =============================================================================
# 🚀 MAIN
# =============================================================================
def main() -> None:
    """
    Main entry point.
    Uses a simple router for a clean single-file "multi-page" app.
    """
    st.set_page_config(page_title=APP_TITLE, page_icon="🎄", layout="centered")
    init_state()

    apply_festive_theme()
    maybe_show_balloons()

    page = st.session_state.page
    if page == "card":
        render_card_page()
    elif page == "gallery":
        render_gallery_page()
    elif page == "final":
        render_final_page()
    else:
        goto_page("card")
        st.rerun()


if __name__ == "__main__":
    main()
