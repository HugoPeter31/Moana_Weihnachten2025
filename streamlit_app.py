import base64
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

# Gift / coupon pool (Point 2)
COUPONS: List[Tuple[str, str]] = [
    ("☕ 1x Kaffee geht auf mich", "Ein Kaffee-Date – du wählst Ort & Zeit."),
    ("🍪 Guetzli-Abend", "Wir backen zusammen Guetzli (inkl. Naschen 😄)."),
    ("🎬 Filmabend", "Film deiner Wahl + Snacks deiner Wahl."),
    ("🥐 Brunch", "Gemütlicher Brunch – ich lade ein."),
    ("🏃 Squash-Match", "Revanche! (oder freundschaftlich… 🤭)"),
    ("🚶 Winterspaziergang", "Spaziergang + heisse Schoggi / Glühwein."),
]

# Ornament messages (Point 5)
ORNAMENTS: List[Tuple[str, str]] = [
    ("🎄", "Ich schätze an dir, dass du immer ehrlich bist – auch wenn’s unbequem ist."),
    ("⭐", "Du bringst so viel Humor rein. Mit dir fühlt sich alles leichter an."),
    ("🧡", "Dein Herz ist riesig. Du bist für andere da, ohne viel Lärm darum."),
    ("🎁", "Mit dir kann man einfach Zeit verbringen – ohne Plan, ohne Druck, einfach gut."),
    ("❄️", "Du hast eine ruhige Stärke. Das beeindruckt mich immer wieder."),
    ("🔔", "Du machst unser Family-Team besser. Punkt."),
]

# Soundboard assets (Point 6) — optional local files
# If files are missing, the app will show a friendly info instead of crashing.
SOUNDS = {
    "🔔 Jingle": "assets/sounds/jingle.mp3",
    "🎅 Ho Ho Ho": "assets/sounds/hohoho.mp3",
    "🔥 Fireplace": "assets/sounds/fireplace.mp3",
    "🚨 Guetzli-Alarm": "assets/sounds/guetzli_alarm.mp3",
}

# Compliment generator (Point 8)
COMPLIMENT_BANK = {
    "Motivation": [
        "Du packsch das. Wirklich. Du hesch scho so viel gschafft – und das chunnt vo dim Drive. 💪",
        "Wenn du dir selber würdisch zuehöre wie ich über dich rede, würdisch du sofort wieder an dich glaube. ✨",
        "Du bisch stärker als du meinst – und ich glaub fix a dich. ❤️",
    ],
    "Humor": [
        "Wenn Weihnachten e Sport wär, wärsch du safe MVP im Guetzli-Nasche. 😄🍪",
        "Ich wünsch dir e Tag ohni Stress – und falls doch: druck eifach 'Reset' wie bi mir. 😌",
        "Du bisch wie Lametta: unnötig, aber ohne di gsehds eifach nöd so guet us. 😆✨",
    ],
    "Herz": [
        "Du bisch e Mensch, wo me gern um sich hät. Danke, dass du so bisch wie du bisch. 🧡",
        "Ich bi mega dankbar für dich. Du gisch so viel, ohni’s gross z’zeige. ❤️",
        "Wenn’s e 'warm & safe'-Gefühl gäb zum usdrucke: das bisch du. 🕯️",
    ],
}


# =============================================================================
# 🎨 FESTIVE THEME + PAGE-CHANGE BALLOONS
# =============================================================================
def apply_festive_theme() -> None:
    """Inject a festive holiday theme via CSS (background, cards, sparkle)."""
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 5%, rgba(205, 0, 0, 0.14), transparent 45%),
                radial-gradient(circle at 85% 10%, rgba(0, 130, 0, 0.14), transparent 45%),
                radial-gradient(circle at 40% 0%, rgba(230, 200, 0, 0.10), transparent 38%),
                linear-gradient(180deg, rgba(255,255,255,0.98), rgba(252,252,252,0.98));
        }
        header[data-testid="stHeader"] { background: transparent; }
        h1, h2, h3 { letter-spacing: 0.25px; }
        h1 { text-shadow: 0 10px 30px rgba(200,0,0,0.10); }

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
        .xmas-card::before{
            content:"";
            position:absolute;
            top:-16px; left:-16px;
            width: 90px; height: 90px;
            background: radial-gradient(circle at 30% 30%, rgba(220,0,0,0.85), rgba(150,0,0,0.65));
            transform: rotate(12deg);
            border-radius: 18px;
            filter: drop-shadow(0 10px 12px rgba(0,0,0,0.10));
            opacity: 0.28;
        }
        .xmas-divider {
            height: 1px;
            width: 100%;
            margin: 14px 0;
            background: linear-gradient(
                90deg, transparent,
                rgba(210,160,0,0.35),
                rgba(200,0,0,0.30),
                rgba(0,120,0,0.30),
                rgba(210,160,0,0.35),
                transparent
            );
        }
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
            opacity: 0.28;
            animation: sparkleMove 12s linear infinite;
        }
        @keyframes sparkleMove {
            0% { transform: translateY(0); }
            100% { transform: translateY(40px); }
        }
        section.main > div { position: relative; z-index: 2; }
        </style>

        <div class="xmas-sparkle"></div>
        """,
        unsafe_allow_html=True,
    )


def trigger_balloons() -> None:
    """One-shot flag: show balloons exactly once after a navigation event."""
    st.session_state.show_balloons_once = True


def maybe_show_balloons() -> None:
    """Render balloon overlay only once; cleared immediately to avoid replay on reruns."""
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

      .b1{ left: 6%;  background: rgba(200,  0,  0, 0.86); animation-delay: 0.00s; }
      .b2{ left: 16%; background: rgba(  0,120,  0, 0.86); animation-delay: 0.08s; }
      .b3{ left: 28%; background: rgba(220,180,  0, 0.86); animation-delay: 0.16s; }
      .b4{ left: 40%; background: rgba(180,  0,120, 0.82); animation-delay: 0.05s; }
      .b5{ left: 52%; background: rgba(  0, 90,160, 0.82); animation-delay: 0.12s; }
      .b6{ left: 64%; background: rgba(230, 60, 60, 0.78); animation-delay: 0.20s; }
      .b7{ left: 78%; background: rgba( 40,150,120, 0.78); animation-delay: 0.10s; }
      .b8{ left: 90%; background: rgba(240,200, 60, 0.78); animation-delay: 0.22s; }

      @keyframes flyUp{
        0%   { transform: translateY(0) translateX(0) rotate(-3deg); }
        25%  { transform: translateY(-28vh) translateX(12px) rotate(3deg); }
        60%  { transform: translateY(-78vh) translateX(-10px) rotate(-2deg); }
        100% { transform: translateY(-125vh) translateX(6px) rotate(2deg); opacity: 0; }
      }
    </style>
    """
    components.html(balloons_html, height=0)


# =============================================================================
# 🧩 GENERIC HELPERS
# =============================================================================
def validate_name(name: str) -> bool:
    """Allow only letters/spaces to keep the greeting clean and personal."""
    return bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß ]+", name.strip()))


def typing_effect(text: str, speed: float = 0.04) -> None:
    """Typewriter effect for emotional impact."""
    placeholder = st.empty()
    rendered_text = ""
    for char in text:
        rendered_text += char
        placeholder.markdown(rendered_text)
        time.sleep(speed)


def days_until_christmas() -> int:
    """Days until next Christmas (handles passed Christmas)."""
    today = date.today()
    christmas = date(today.year, 12, 25)
    if today > christmas:
        christmas = date(today.year + 1, 12, 25)
    return (christmas - today).days


def safe_image(path_or_url: str) -> Optional[str]:
    """Resolve image path safely (no crash if file missing)."""
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    path = Path(path_or_url)
    return str(path) if path.exists() else None


def read_audio_as_base64(path: str) -> Optional[str]:
    """
    Load audio file and return base64 string for safe embedding.
    WHY: Works reliably for local mp3/wav without external dependencies.
    """
    audio_path = Path(path)
    if not audio_path.exists():
        return None
    data = audio_path.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def goto_page(page: str) -> None:
    """Navigate to another page and trigger balloons exactly once."""
    st.session_state.page = page
    trigger_balloons()


def init_state() -> None:
    """Initialize session_state defaults (stable reruns, no KeyErrors)."""
    st.session_state.setdefault("page", "card")
    st.session_state.setdefault("message_shown", False)
    st.session_state.setdefault("last_surprise", None)
    st.session_state.setdefault("validated_name", None)
    st.session_state.setdefault("final_shown", False)
    st.session_state.setdefault("show_balloons_once", False)

    # Feature states
    st.session_state.setdefault("coupon", None)
    st.session_state.setdefault("coupon_details", None)
    st.session_state.setdefault("ornament_message", None)
    st.session_state.setdefault("compliment", None)


# =============================================================================
# 🎁 FEATURE: Coupon generator (Point 2)
# =============================================================================
def show_coupon_generator() -> None:
    """Random coupon draw + persistent display."""
    st.subheader("🎁 Zieh deinen Gutschein")

    if st.button("🎟️ Gutschein ziehen"):
        title, details = random.choice(COUPONS)
        st.session_state.coupon = title
        st.session_state.coupon_details = details

    if st.session_state.get("coupon"):
        st.success(st.session_state.coupon)
        st.caption(st.session_state.coupon_details)


# =============================================================================
# 🎄 FEATURE: Wish tree ornaments (Point 5)
# =============================================================================
def show_wish_tree() -> None:
    """Clickable ornaments reveal warm messages."""
    st.subheader("🎄 Wunschbaum")
    st.caption("Klick auf ein Ornament – dahinter steckt etwas für dich ❤️")

    cols = st.columns(6)
    for i, (icon, text) in enumerate(ORNAMENTS):
        with cols[i]:
            if st.button(icon, key=f"ornament_{i}"):
                st.session_state.ornament_message = text

    if st.session_state.get("ornament_message"):
        st.info(st.session_state.ornament_message)


# =============================================================================
# 🎶 FEATURE: Soundboard (Point 6)
# =============================================================================
def show_soundboard() -> None:
    """
    Simple soundboard (plays local mp3 files if present).
    If files are missing, show a friendly note instead of errors.
    """
    st.subheader("🎶 Mini-Soundboard")
    st.caption("Optional: Lege MP3-Dateien in `assets/sounds/` ab (siehe SOUNDS-Dict).")

    cols = st.columns(4)
    buttons = list(SOUNDS.items())

    for col, (label, path) in zip(cols, buttons):
        with col:
            if st.button(label):
                audio_b64 = read_audio_as_base64(path)
                if audio_b64 is None:
                    st.info(f"Audio-Datei fehlt: `{path}`")
                else:
                    st.audio(base64.b64decode(audio_b64), format="audio/mp3")


# =============================================================================
# 🧡 FEATURE: Compliment machine (Point 8)
# =============================================================================
def show_compliment_machine() -> None:
    """Generate a themed compliment (motivation / humor / heart)."""
    st.subheader("🧡 Kompliment-Maschine")
    mode = st.selectbox("Was brauchst du heute?", ["Motivation", "Humor", "Herz"])

    if st.button("✨ Gib mir eins!"):
        st.session_state.compliment = random.choice(COMPLIMENT_BANK[mode])

    if st.session_state.get("compliment"):
        st.success(st.session_state.compliment)


# =============================================================================
# 🎁 PAGE 1: CARD
# =============================================================================
def show_header() -> None:
    st.title(APP_TITLE)
    st.subheader(f"Eine kleine digitale Überraschung für {RECIPIENT_RELATION} ❤️")


def show_personal_message(name: str) -> None:
    """Animated message only once; afterwards static markdown."""
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
    """Small surprise (stored so it stays stable)."""
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

    # Extra features on page 1 (fun + festive)
    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    show_coupon_generator()       # Point 2
    st.markdown('<div class="xmas-divider"></div>', unsafe_allow_html=True)
    show_wish_tree()              # Point 5
    st.markdown('<div class="xmas-divider"></div>', unsafe_allow_html=True)
    show_soundboard()             # Point 6
    st.markdown('<div class="xmas-divider"></div>', unsafe_allow_html=True)
    show_compliment_machine()     # Point 8
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    if st.button("let’s continue ➜"):
        goto_page("gallery")
        st.rerun()


# =============================================================================
# 📸 PAGE 2: GALLERY
# =============================================================================
def render_gallery_page() -> None:
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
