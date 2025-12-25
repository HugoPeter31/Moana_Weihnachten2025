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
    "Mier hends scho als chlini gschwüsterti immer guet gha😄",
    "Unser Moment 2 – einfach typisch wir ❤️",
    "Unser Moment 3 – ein kleines Abenteuer ✨",
    "Unser Moment 4 – das war so schön 🥹",
    "Unser Moment 5 – und davon bitte mehr! 🎁",
]

FINAL_PERSONAL_TEXT = (
    "Liebi Moana\n\n"
    "Danke für all die schöne Moment womer bisher hend döffe zeme ha "
    "und dafür, dass du immer da bist, wemer dich bruucht.\n\n"
    "Du döfsch Stolz sie uf alles was du bisher erreicht hesch."
    "Bliib wie du bisch..\n\n"
    "Ich freue mich auf alles, was chund und uf viele witeri schöni Moment zeme mit Dir❤️\n\n"
    "Frohe Weihnachten! 🎄✨"
)

# 🎁 Gutschein-Generator
COUPONS: List[Tuple[str, str]] = [
    ("☕ Kaffee-Date", "Gömer mal zeme im Magdalena go käffele."),
    ("🍪 Guetzli-Abend", "Gemeinsam Guetzli backen oder Lebkuechehuus."),
    ("🏃 Squash-Match", "Gömer doch mal zeme go squashe oder im Früehlig wieder go Tennis spiele"),
]

# 🧡 Kompliment-Maschine
COMPLIMENT_BANK = {
    "Motivation": [
        "Du packsch das. Du hesch scho so viel gschafft 💪",
        "Ich glaub fest a dich. ✨",
        "Du bisch stärker als du meinst.",
    ],
    "Humor": [
        "Wenn Weihnachten e Sport wär, wärsch du MVP im Guetzli-Nasche 😄🍪",
    ],
    "Herz": [
        "Ich bi mega dankbar für dich. Du bisch e grossi Bereicherung ❤️",
        "Uf dich chamer immer zähle",
        "Du hesch es grosses Herz – und das merkt jede.",
    ],
}


# =============================================================================
# 🎨 FESTIVE THEME + BALLOONS
# =============================================================================
def apply_festive_theme() -> None:
    """Apply a festive Christmas theme via CSS."""
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 5%, rgba(205, 0, 0, 0.14), transparent 45%),
                radial-gradient(circle at 85% 10%, rgba(0, 130, 0, 0.14), transparent 45%),
                linear-gradient(180deg, rgba(255,255,255,0.98), rgba(252,252,252,0.98));
        }

        .xmas-card {
            padding: 18px;
            border-radius: 20px;
            background: rgba(255,255,255,0.80);
            box-shadow: 0 16px 36px rgba(0,0,0,0.08);
            margin-bottom: 14px;
        }

        div.stButton > button {
            border-radius: 14px;
            padding: 0.65rem 1.05rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.10);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def trigger_balloons() -> None:
    st.session_state.show_balloons_once = True


def maybe_show_balloons() -> None:
    if not st.session_state.get("show_balloons_once", False):
        return

    st.session_state.show_balloons_once = False

    components.html(
        """
        <div id="balloons">
          <div class="b"></div><div class="b"></div><div class="b"></div>
        </div>
        <style>
        #balloons { position:fixed; inset:0; pointer-events:none; z-index:9999; }
        .b {
            position:absolute; bottom:-100px; width:50px; height:70px;
            border-radius:50%; background:red; animation:fly 2s ease-out forwards;
        }
        .b:nth-child(1){ left:20%; background:#c00; }
        .b:nth-child(2){ left:50%; background:#0a7; animation-delay:.2s; }
        .b:nth-child(3){ left:80%; background:#da0; animation-delay:.4s; }

        @keyframes fly {
            to { transform:translateY(-120vh); opacity:0; }
        }
        </style>
        """,
        height=0,
    )


# =============================================================================
# 🧩 HELPERS
# =============================================================================
def validate_name(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß ]+", name.strip()))


def typing_effect(text: str, speed: float = 0.04) -> None:
    placeholder = st.empty()
    rendered = ""
    for char in text:
        rendered += char
        placeholder.markdown(rendered)
        time.sleep(speed)


def days_until_christmas() -> int:
    today = date.today()
    christmas = date(today.year, 12, 25)
    if today > christmas:
        christmas = date(today.year + 1, 12, 25)
    return (christmas - today).days


def safe_image(path: str) -> Optional[str]:
    p = Path(path)
    return str(p) if p.exists() else None


def goto_page(page: str) -> None:
    st.session_state.page = page
    trigger_balloons()


def init_state() -> None:
    st.session_state.setdefault("page", "card")
    st.session_state.setdefault("message_shown", False)
    st.session_state.setdefault("validated_name", None)
    st.session_state.setdefault("final_shown", False)
    st.session_state.setdefault("show_balloons_once", False)
    st.session_state.setdefault("coupon", None)
    st.session_state.setdefault("coupon_details", None)
    st.session_state.setdefault("compliment", None)


# =============================================================================
# 🎁 FEATURES
# =============================================================================
def show_coupon_generator() -> None:
    st.subheader("🎁 Zieh deinen Gutschein")
    if st.button("🎟️ Gutschein ziehen"):
        title, detail = random.choice(COUPONS)
        st.session_state.coupon = title
        st.session_state.coupon_details = detail

    if st.session_state.get("coupon"):
        st.success(st.session_state.coupon)
        st.caption(st.session_state.coupon_details)


def show_compliment_machine() -> None:
    st.subheader("🧡 Kompliment-Maschine")
    mode = st.selectbox("Was brauchst du heute?", list(COMPLIMENT_BANK.keys()))

    if st.button("✨ Gib mir eins!"):
        st.session_state.compliment = random.choice(COMPLIMENT_BANK[mode])

    if st.session_state.get("compliment"):
        st.success(st.session_state.compliment)


# =============================================================================
# 🎁 PAGE 1: CARD
# =============================================================================
def render_card_page() -> None:
    st.title(APP_TITLE)
    st.subheader(f"Eine kleine digitale Überraschung für {RECIPIENT_RELATION} ❤️")

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    name = st.text_input("Wie heisst du?")
    st.markdown("</div>", unsafe_allow_html=True)

    if not name or not validate_name(name):
        return

    st.session_state.validated_name = name.strip()

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    show_message = (
        f"Liebe {name},\n\n"
        "ich wünsche dir von Herzen wunderschöne Weihnachten 🎄✨\n"
        "voller Wärme, Lachen und ganz vielen schönen Momenten.\n\n"
        "Danke, dass es dich gibt ❤️"
    )
    
    if not st.session_state.message_shown:
        typing_effect(show_message)
        st.session_state.message_shown = True
    else:
        st.markdown(show_message)

    st.info(f"⏳ Noch {days_until_christmas()} Tage bis Weihnachten")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    show_coupon_generator()
    show_compliment_machine()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("let’s continue ➜"):
        goto_page("gallery")
        st.rerun()


# =============================================================================
# 📸 PAGE 2: GALLERY
# =============================================================================
def render_gallery_page() -> None:
    st.title("📸 Kleine Erinnerungen")

    for path, caption in zip(PHOTO_PATHS, PHOTO_CAPTIONS):
        st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
        img = safe_image(path)
        if img:
            st.image(img, use_container_width=True)
        st.write(caption)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Weiter zur Weihnachtskarte ➜"):
        goto_page("final")
        st.rerun()


# =============================================================================
# 💌 PAGE 3: FINAL
# =============================================================================
def render_final_page() -> None:
    st.title("🎁 Deine Weihnachtskarte")

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    if not st.session_state.final_shown:
        typing_effect(FINAL_PERSONAL_TEXT)
        st.session_state.final_shown = True
    else:
        st.markdown(FINAL_PERSONAL_TEXT)
    st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# 🚀 MAIN
# =============================================================================
def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🎄", layout="centered")
    init_state()
    apply_festive_theme()
    maybe_show_balloons()

    if st.session_state.page == "card":
        render_card_page()
    elif st.session_state.page == "gallery":
        render_gallery_page()
    else:
        render_final_page()


if __name__ == "__main__":
    main()
