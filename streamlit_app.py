import streamlit as st
import time
import re
from typing import List, Optional


# =============================================================================
# Configuration (avoid hardcoding in logic)
# =============================================================================
APP_TITLE = "🎄 Interaktive Weihnachtskarte 🎄"
MAX_PHOTOS_PER_SECTION = 6


# =============================================================================
# Helpers (small, focused functions)
# =============================================================================
def validate_name(name: str) -> bool:
    """Allow only letters/spaces to keep greeting clean and avoid weird UI states."""
    return bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß ]+", name.strip()))


def init_state() -> None:
    """Initialize session state once to keep navigation predictable across reruns."""
    defaults = {
        "page": 1,
        "recipient_name": "",
        "santa_popup": False,
        "secret_unlocked": False,
        "secret_clicks": 0,
        "childhood_photos": [],
        "teen_photos": [],
        "today_photos": [],
        "final_photos": [],
        "final_message": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def trigger_santa_popup() -> None:
    """
    Show a short Santa+sled overlay after navigation.
    We store a flag in session_state to display it on the next render.
    """
    st.session_state.santa_popup = True


def show_santa_popup() -> None:
    """Render a temporary Santa+sled overlay if the flag is set."""
    if not st.session_state.santa_popup:
        return

    # WHY CSS: Streamlit has limited native animations; CSS allows a playful popup without extra deps.
    st.markdown(
        """
        <style>
        .santa-popup {
            position: fixed;
            top: 18px;
            right: 18px;
            z-index: 9999;
            background: rgba(0,0,0,0.75);
            color: white;
            padding: 14px 16px;
            border-radius: 14px;
            font-size: 18px;
            animation: fadeInOut 1.6s ease-in-out forwards;
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        }
        @keyframes fadeInOut {
            0%   { opacity: 0; transform: translateY(-10px); }
            15%  { opacity: 1; transform: translateY(0); }
            75%  { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-10px); }
        }
        </style>
        <div class="santa-popup">🎅🛷 Ho ho ho! Weiter geht’s…</div>
        """,
        unsafe_allow_html=True,
    )

    # Reset flag after rendering (avoid repeated popups on rerun)
    time.sleep(0.2)
    st.session_state.santa_popup = False


def go_next() -> None:
    """Advance page safely and show the Santa popup."""
    st.session_state.page = min(st.session_state.page + 1, 6)
    trigger_santa_popup()


def go_back() -> None:
    """Go back safely (no popup by default, but you can add it if you want)."""
    st.session_state.page = max(st.session_state.page - 1, 1)


def upload_photos(
    label: str, state_key: str, help_text: str, max_photos: int = MAX_PHOTOS_PER_SECTION
) -> None:
    """
    Store uploaded photos in session state.
    WHY: Session state prevents losing uploads when Streamlit reruns the script.
    """
    files = st.file_uploader(
        label,
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        help=help_text,
    )
    if files:
        st.session_state[state_key] = files[:max_photos]

    photos: List = st.session_state[state_key]
    if photos:
        st.caption(f"Ausgewählt: {len(photos)} Foto(s)")
        st.image(photos, use_container_width=True)


def secret_easter_egg() -> None:
    """
    A simple Easter egg:
    Click a button 5 times to unlock a secret card.
    WHY: Fun interaction without requiring key-capture libraries.
    """
    st.session_state.secret_clicks += 1
    if st.session_state.secret_clicks >= 5:
        st.session_state.secret_unlocked = True


# =============================================================================
# Pages
# =============================================================================
def page_1_intro() -> None:
    st.title(APP_TITLE)
    st.subheader("Seite 1/5 – Start ❤️")

    name_input = st.text_input("Wie heisst du?", value=st.session_state.recipient_name)

    if name_input:
        if validate_name(name_input):
            st.session_state.recipient_name = name_input.strip()
            st.success(f"Willkomme, {st.session_state.recipient_name} ✨")
        else:
            st.warning("Bitte nur Buchstaben verwenden (keine Zahlen/Sonderzeichen).")

    st.write("Wenn du bereit bisch: klick uf **Weiter** 😊")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("🎁 Easter Egg (psst…)", on_click=secret_easter_egg)
    with col2:
        # Only allow next if name is valid (keeps flow clean)
        can_continue = validate_name(st.session_state.recipient_name)
        st.button("➡️ Weiter", on_click=go_next, disabled=not can_continue)

    if st.session_state.secret_unlocked:
        st.info("🕵️ Secret unlocked: Du bisch mini Lieblings-Mitverschwörerin 😄")


def page_2_childhood() -> None:
    st.subheader("Seite 2/5 – Kindheit 🧸")
    st.write(
        "Chli e Reise zrugg: die Momente, wo alles eifach und schön gsi isch. "
        "Lad 1–3 Fotos vo eus als Chind uf (oder mehr)."
    )

    upload_photos(
        "📷 Kindheitsfotos hochladen",
        "childhood_photos",
        "Tip: Nimm die witzigste, chaotischte oder herzigste Bilder 😄",
    )

    st.markdown(
        """
        **Danke** für:
        - die unzählige Lacher
        - s Zämehalte (au wenn mer gstritte hend)
        - mini schönste Kindheits-Erinnerige mit dir
        """
    )

    nav_buttons()


def page_3_teen_years() -> None:
    st.subheader("Seite 3/5 – Teenie-Ziit 🌟")
    st.write(
        "Da sind d Insider entstanden 😄 "
        "Lad 1–3 Fotos vo eus i de Teenie-Ziit hoch."
    )

    upload_photos(
        "📷 Teenie-Fotos hochladen",
        "teen_photos",
        "Wenn’s mega cringe isch: perfekt. Genau drum 😂",
    )

    st.write("Mini Dankbarkeit i 1 Satz:")
    st.info("Mit dir het’s sich nie aagfühlt, als müessti ich alles allei packe.")

    nav_buttons()


def page_4_today_gratitude() -> None:
    st.subheader("Seite 4/5 – Hüt & ich ❤️")
    st.write(
        "Das isch mini Lieblings-Seite: was ich hüt a dir schätze – und wieso ich stolz bi, dini Schwester z si."
    )

    upload_photos(
        "📷 Aktuelli Fotos (optional)",
        "today_photos",
        "Optional: z.B. es Bild vo eus vo de letschte Ferie oder es Selfie.",
    )

    st.markdown(
        """
        **Was ich a dir so fescht schätze:**
        - dini Art, wie du Mensche zum lache bringsch
        - dini Loyalität und dini Wärme
        - dass du immer e Teil vo mim Dahei bisch
        """
    )

    nav_buttons()


def page_5_final() -> None:
    st.subheader("Seite 5/5 – Schlusskärtli 💌")
    st.write(
        "Jetzt chunt s Finale: Lad no es paar Lieblingsfotos hoch und schriib dini persönlich Botschaft."
    )

    upload_photos(
        "📷 Lieblingsfotos vo eus (Finale)",
        "final_photos",
        "Du chasch da meh als vorher neh – es wird wie es kleines Album.",
        max_photos=12,
    )

    message = st.text_area(
        "✍️ Dini persönliche Schlussbotschaft",
        value=st.session_state.final_message,
        placeholder="Liebe ..., ich bi mega dankbar, dass ...",
        height=180,
    )
    st.session_state.final_message = message

    if st.session_state.final_message.strip():
        st.divider()
        st.markdown("### 💖 Vorschau")
        st.markdown(st.session_state.final_message)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅️ Zurück", on_click=go_back)
    with col2:
        st.button("🎄 Fertig", on_click=go_next)

    st.caption("Tipp: Wenn du willst, mache ich dir als nächstes eine 'Download als PDF'-Variante.")


def page_6_done() -> None:
    st.title("✨ Frohi Wiehnachte ✨")
    st.write("Das isch dini fertigi digitale Weihnachtskarte 🎄❤️")

    if st.session_state.final_photos:
        st.image(st.session_state.final_photos, use_container_width=True)

    if st.session_state.final_message.strip():
        st.markdown("## 💌 Dini Botschaft")
        st.markdown(st.session_state.final_message)

    st.success("Fertig! Du chasch die App jetzt eifach im Browser zeige oder hoste (Streamlit Cloud).")
    st.button("🔄 Nochmal vo vorn", on_click=lambda: st.session_state.update({"page": 1}))


def nav_buttons() -> None:
    """Navigation controls used on pages 2–4."""
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅️ Zurück", on_click=go_back)
    with col2:
        st.button("➡️ Weiter", on_click=go_next)


# =============================================================================
# Main
# =============================================================================
def main() -> None:
    init_state()
    show_santa_popup()

    page = st.session_state.page

    # WHY: Simple routing keeps the app easy to understand and maintain.
    if page == 1:
        page_1_intro()
    elif page == 2:
        page_2_childhood()
    elif page == 3:
        page_3_teen_years()
    elif page == 4:
        page_4_today_gratitude()
    elif page == 5:
        page_5_final()
    else:
        page_6_done()


if __name__ == "__main__":
    main()
