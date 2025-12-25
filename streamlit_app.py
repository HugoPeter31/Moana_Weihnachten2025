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
    "IMG_2873.jpeg",
    "IMG_5603.jpeg",
    "IMG_7753.jpeg",
    "IMG_0634.jpeg",
    "IMG_8238.jpeg",
]

PHOTO_CAPTIONS: List[str] = [
    "Mier hends scho als chlini chindli immer guet gha und zeme döffe e wunderschöni Chindheit gnüsse 😄",
    "Im Trio hemer vieli schöni Moment döffe zeme ha ❤️",
    "Gmeinsami Erlebnis weg vo deheime – Sprachufenthalt Eastbourne oder ✨",
    "Interrail vo Wien bis Bologna 🇮🇹",
    "Ich freue mich uf witeri sportlichi & abenteurlustigi Ziite 🤸‍♀️",
]

FINAL_PERSONAL_TEXT = (
    "Liebi Moana\n\n"
    "Danke für all die schöne Moment womer bisher hend döffe zeme ha "
    "und dafür, dass du immer da bisch, wemer dich bruucht.\n\n"
    "Du döfsch stolz sii uf alles, was du bisher erreicht hesch.\n"
    "Bliib wie du bisch.\n\n"
    "Ich freue mich uf alles, was chund und uf vieli witeri "
    "schöni Moment zeme mit dir ❤️\n\n"
    "Frohe Weihnachten! 🎄✨"
)

COUPONS: List[Tuple[str, str]] = [
    ("☕ Kaffee-Date", "Gömer zeme im Magdalena go käffele."),
    ("🍪 Guetzli-Abend", "Guetzli backe oder Lebkuechehuus."),
    ("🏃 Squash-Match", "Squash oder im Frühlig Tennis spiele."),
]

# =============================================================================
# 🎨 DARK GREEN CHRISTMAS THEME + BALLOONS
# =============================================================================
def apply_festive_theme() -> None:
    """Dark green Christmas background with bright content cards."""
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 20% 0%, rgba(40, 90, 60, 0.35), transparent 55%),
                radial-gradient(circle at 80% 10%, rgba(20, 60, 40, 0.35), transparent 55%),
                linear-gradient(180deg, #0f2e1f 0%, #143d2b 100%);
        }

        h1, h2, h3, p, span, label {
            color: #f5f5f5;
        }

        .xmas-card {
            padding: 18px;
            border-radius: 20px;
            background: rgba(255,255,255,0.92);
            box-shadow: 0 18px 40px rgba(0,0,0,0.35);
            margin-bottom: 14px;
            color: #222;
        }

        .xmas-card p, .xmas-card h1, .xmas-card h2, .xmas-card h3 {
            color: #222;
        }

        div.stButton > button {
            border-radius: 14px;
            padding: 0.65rem 1.05rem;
            background: linear-gradient(180deg, #f5f5f5, #eaeaea);
            box-shadow: 0 8px 20px rgba(0,0,0,0.30);
        }

        div.stButton > button:hover {
            background: linear-gradient(180deg, #ffffff, #f0f0f0);
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
            position:absolute; bottom:-120px; width:52px; height:72px;
            border-radius:50%;
            animation:fly 2.2s ease-out forwards;
            opacity:0.9;
        }
        .b:nth-child(1){ left:20%; background:#c62828; }
        .b:nth-child(2){ left:50%; background:#2e7d32; animation-delay:.2s; }
        .b:nth-child(3){ left:80%; background:#f9a825; animation-delay:.4s; }

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
    st.session_state.setdefault("final_shown", False)
    st.session_state.setdefault("show_balloons_once", False)
    st.session_state.setdefault("coupon", None)


# =============================================================================
# 🎁 FEATURES
# =============================================================================
def show_coupon_generator() -> None:
    st.subheader("🎁 Zieh deinen Gutschein")
    if st.button("🎟️ Gutschein ziehen"):
        title, detail = random.choice(COUPONS)
        st.session_state.coupon = title
        st.caption(detail)

    if st.session_state.get("coupon"):
        st.success(st.session_state.coupon)


# =============================================================================
# 🎁 PAGE 1
# =============================================================================
def render_card_page() -> None:
    st.title(APP_TITLE)
    st.subheader(f"Eine kleine digitale Überraschung für {RECIPIENT_RELATION} ❤️")

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    name = st.text_input("Wie heisst du?")
    st.markdown("</div>", unsafe_allow_html=True)

    if not name or not validate_name(name):
        return

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    message = (
        f"Liebe {name},\n\n"
        "ich wünsche dir von Herzen wunderschöne Weihnachten 🎄✨\n"
        "voller Wärme, Lachen und ganz vielen schönen Momenten.\n\n"
        "Danke, dass es dich gibt ❤️"
    )
    if not st.session_state.message_shown:
        typing_effect(message)
        st.session_state.message_shown = True
    else:
        st.markdown(message)

    st.info(f"⏳ Noch {days_until_christmas()} Tage bis Weihnachten")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="xmas-card">', unsafe_allow_html=True)
    show_coupon_generator()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("let’s continue ➜"):
        goto_page("gallery")
        st.rerun()


# =============================================================================
# 📸 PAGE 2
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
# 💌 PAGE 3
# =============================================================================
def render_final_page() -> None:
    st.title("🎁 Für Moana")

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
