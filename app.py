import streamlit as st
import random
import time
import html as html_lib

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALIASES = [
    "SpicyTaco", "CaptainCrunch", "MightyMuffin", "SaltyPretzel",
    "CosmicBurrito", "NinjaNoodle", "FunkyFalafel", "TurboToast",
    "BlazeBean", "ChilliWaffle", "QuantumQuiche", "VelvetDonut",
    "AtomicAvocado", "RocketRamen", "SneakySpud", "ZenZiti",
]

PARTNER_ALIASES = [
    "GoldenGnocchi", "BraveBagel", "ElectricEclair", "MysticMango",
    "CozyCrepe", "DaringDumpling", "LuckyLasagna", "StellarSushi",
    "RadiantRisotto", "BoldBrioche", "PluckyPancake", "SwiftSamosa",
]

WINGMAN_PROMPTS = [
    "What's the wildest thing you've ever eaten?",
    "If you could only eat one cuisine forever, what would it be?",
    "What's your guilty-pleasure midnight snack?",
    "Have you ever tried cooking a dish and completely failed?",
    "Sweet or savoury breakfast — and why?",
    "What meal takes you back to childhood?",
    "Pineapple on pizza — yes or no? Defend your answer.",
    "If you opened a restaurant, what would you name it?",
]

AUTO_REPLIES = [
    "Ha, that's awesome! I totally agree.",
    "No way, tell me more!",
    "Haha I was just thinking the same thing.",
    "Interesting take... I'm the complete opposite!",
    "Okay that's a hot take but I respect it.",
    "LOL, you sound like my kind of dining buddy.",
    "Noted. Adding that to my food bucket list!",
    "Wait really?? That's wild.",
]

MOODS = ("Chatty", "Zen")
SPEEDS = ("Fast", "Slow")
CONVOS = ("Small Talk", "Deep Dive")

DISHES = [
    {"name": "Truffle Mushroom Pasta",      "img": "https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Spicy Tuna Poke Bowl",        "img": "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Classic Margherita Pizza",     "img": "https://images.pexels.com/photos/315755/pexels-photo-315755.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Grilled Salmon & Greens",      "img": "https://images.pexels.com/photos/842571/pexels-photo-842571.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Butter Chicken Curry",         "img": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Avocado Toast Deluxe",         "img": "https://images.pexels.com/photos/1351238/pexels-photo-1351238.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Thai Green Curry",             "img": "https://images.pexels.com/photos/699953/pexels-photo-699953.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "BBQ Pulled Pork Tacos",        "img": "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Sushi Platter",                "img": "https://images.pexels.com/photos/357756/pexels-photo-357756.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Mediterranean Bowl",           "img": "https://images.pexels.com/photos/1211887/pexels-photo-1211887.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Pancake Stack & Berries",      "img": "https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
    {"name": "Wagyu Beef Burger",            "img": "https://images.pexels.com/photos/1639557/pexels-photo-1639557.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"},
]


def get_partner_dish(partner_name: str) -> dict:
    idx = hash(partner_name) % len(DISHES)
    return DISHES[idx]


# ---------------------------------------------------------------------------
# CSS — everything inside a single <style> block
# ---------------------------------------------------------------------------

GLOBAL_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

:root {
    --c-primary: #D4552E;
    --c-primary-h: #BF4423;
    --c-accent: #F4A261;
    --c-accent-bg: #FFF3E6;
    --c-green: #2FA566;
    --bg-page: #FAF6F2;
    --bg-card: #FFFFFF;
    --bg-warm: #FFF8F3;
    --t-dark: #1E1E1E;
    --t-body: #3E3A37;
    --t-muted: #6E665E;
    --t-light: #8A8279;
    --b-default: #E8E0D8;
    --b-light: #F0EAE4;
    --r-sm: 10px;
    --r-md: 14px;
    --r-lg: 18px;
    --r-pill: 50px;
    --s-xs: 0 1px 2px rgba(0,0,0,0.04);
    --s-sm: 0 2px 8px rgba(0,0,0,0.06);
    --s-md: 0 4px 20px rgba(0,0,0,0.07);
}

html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--bg-page) !important;
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--t-body) !important;
}
header[data-testid="stHeader"] { background: var(--bg-page) !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden !important; }

.hero { text-align:center; padding:2.5rem 1rem 1.2rem; }
.hero-emoji { font-size:3rem; line-height:1; }
.hero h1 {
    font-size: clamp(2rem, 6vw, 2.6rem);
    font-weight: 700;
    color: var(--t-dark);
    margin: 0.25rem 0 0;
    letter-spacing: -0.5px;
}
.hero h1 em { font-style:normal; color:var(--c-primary); }
.hero .tagline {
    font-size: 0.95rem; font-weight: 500; color: var(--t-muted);
    text-transform: uppercase; letter-spacing: 1.5px; margin-top: 0.25rem;
}

.dots { display:flex; justify-content:center; align-items:center; gap:6px; padding:0.75rem 0 1.5rem; }
.dot-i { width:8px; height:8px; border-radius:50%; background:var(--b-default); transition:all .25s; }
.dot-i.on { width:26px; border-radius:8px; background:var(--c-primary); }

.dish-name {
    font-size:1rem; font-weight:700; color:var(--t-dark); margin-bottom:0.5rem;
}
.partner-name {
    display:inline-block; background:var(--c-primary); color:#fff; font-weight:700;
    font-size:0.95rem; padding:0.35rem 1.1rem; border-radius:var(--r-pill); margin-bottom:0.6rem;
}
[data-testid="stImage"] { border-radius:var(--r-md); overflow:hidden; }
[data-testid="stImage"] img { border-radius:var(--r-md) !important; }
.partner-tags { display:flex; flex-wrap:wrap; justify-content:center; gap:6px; }
.ptag {
    background:var(--c-accent-bg); color:#9B4420; font-size:0.75rem; font-weight:600;
    padding:0.28rem 0.65rem; border-radius:var(--r-pill); border:1px solid #F0DCC8;
}

.conn-bar {
    display:flex; align-items:center; gap:10px; background:var(--bg-card);
    border:1px solid var(--b-default); border-left:4px solid var(--c-green);
    border-radius:var(--r-md); padding:0.75rem 1.1rem; box-shadow:var(--s-xs);
    margin-bottom:1.25rem;
}
.conn-bar .live {
    width:10px; height:10px; background:var(--c-green); border-radius:50%;
    box-shadow:0 0 6px rgba(47,165,102,.45); animation:pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:.3;} }
.conn-bar .nm { font-weight:700; font-size:1rem; color:var(--t-dark); }
.conn-bar .sub { font-size:0.78rem; color:var(--t-muted); }

.alias-pill {
    display:inline-block; background:var(--c-primary); color:#fff; font-weight:700;
    font-size:1.2rem; padding:0.5rem 1.5rem; border-radius:var(--r-pill);
}
.alias-pill-sm {
    display:inline-block; background:var(--c-accent-bg); color:var(--c-primary);
    font-weight:600; font-size:0.82rem; padding:0.25rem 0.85rem; border-radius:var(--r-pill);
}

.chat-wrap { display:flex; flex-direction:column; gap:8px; padding:4px 0; }
.msg {
    max-width:80%; padding:8px 12px; border-radius:14px;
    font-size:0.87rem; line-height:1.5; word-wrap:break-word;
}
.msg-me {
    align-self:flex-end; background:var(--c-primary); color:#fff;
    border-bottom-right-radius:4px;
}
.msg-them {
    align-self:flex-start; background:#EDE8E3; color:var(--t-dark);
    border-bottom-left-radius:4px;
}
.msg-who { font-size:0.65rem; font-weight:700; opacity:0.7; margin-bottom:2px; }
.chat-placeholder { text-align:center; color:var(--t-light); font-size:0.85rem; padding:2.5rem 0.5rem; }

.q-label { font-size:0.92rem; font-weight:600; color:var(--t-dark); margin:0.75rem 0 0.3rem; }
.slabel {
    font-size:0.7rem; font-weight:700; text-transform:uppercase;
    letter-spacing:1.2px; color:var(--t-muted); margin-bottom:6px;
}

.search-hero { text-align:center; padding:3rem 1rem 1.5rem; }
.search-hero h2 { font-size:1.5rem; font-weight:700; color:var(--t-dark); margin:0 0 .3rem; }
.search-hero p { color:var(--t-muted); font-size:.92rem; }

/* === Streamlit widget overrides === */

[data-testid="stBaseButton-secondary"] > button,
.stButton > button {
    font-family:'DM Sans',sans-serif !important; font-weight:600 !important;
    font-size:0.88rem !important; border-radius:var(--r-sm) !important;
    padding:0.5rem 1.25rem !important; border:1px solid var(--b-default) !important;
    background:var(--bg-card) !important; color:var(--t-dark) !important;
    box-shadow:var(--s-xs) !important; transition:all 0.15s !important; cursor:pointer !important;
}
[data-testid="stBaseButton-secondary"] > button:hover,
.stButton > button:hover {
    border-color:var(--c-primary) !important; color:var(--c-primary) !important;
    box-shadow:var(--s-sm) !important;
}

[data-testid="stBaseButton-primary"] > button,
.stButton > button[kind="primary"] {
    background:var(--c-primary) !important; color:#fff !important;
    border:none !important; box-shadow:0 3px 12px rgba(212,85,46,0.28) !important;
}
[data-testid="stBaseButton-primary"] > button:hover,
.stButton > button[kind="primary"]:hover {
    background:var(--c-primary-h) !important; box-shadow:0 5px 18px rgba(212,85,46,0.38) !important;
}

[data-testid="stFormSubmitButton"] button {
    font-family:'DM Sans',sans-serif !important; font-weight:600 !important;
    font-size:0.88rem !important; background:var(--c-primary) !important;
    color:#fff !important; border:none !important; border-radius:var(--r-sm) !important;
    box-shadow:0 3px 12px rgba(212,85,46,0.28) !important; cursor:pointer !important;
}
[data-testid="stFormSubmitButton"] button:hover { background:var(--c-primary-h) !important; }

div[role="radiogroup"] { gap:8px !important; }
div[role="radiogroup"] > label,
div[role="radiogroup"] > div[role="radio"] {
    font-family:'DM Sans',sans-serif !important; background:var(--bg-warm) !important;
    border:1.5px solid var(--b-default) !important; border-radius:8px !important;
    padding:6px 14px !important; color:var(--t-body) !important; font-weight:500 !important;
    font-size:0.88rem !important; cursor:pointer !important;
    transition:border-color 0.15s, background 0.15s !important;
}
div[role="radiogroup"] > label:hover,
div[role="radiogroup"] > div[role="radio"]:hover {
    border-color:var(--c-primary) !important;
}
div[role="radiogroup"] > label[data-checked="true"],
div[role="radiogroup"] > label:has(input:checked),
div[role="radiogroup"] > div[role="radio"][aria-checked="true"] {
    background:var(--c-accent-bg) !important; border-color:var(--c-primary) !important;
    color:var(--c-primary) !important; font-weight:600 !important;
}

[data-testid="stTextInput"] input,
.stTextInput input {
    font-family:'DM Sans',sans-serif !important; background:var(--bg-card) !important;
    border:1.5px solid var(--b-default) !important; border-radius:var(--r-sm) !important;
    color:var(--t-dark) !important; font-size:0.9rem !important; padding:0.55rem 0.85rem !important;
}
[data-testid="stTextInput"] input::placeholder,
.stTextInput input::placeholder {
    color:var(--t-muted) !important; opacity:1 !important;
}
[data-testid="stTextInput"] input:focus,
.stTextInput input:focus {
    border-color:var(--c-primary) !important;
    box-shadow:0 0 0 3px rgba(212,85,46,0.1) !important; outline:none !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius:var(--r-md) !important; border-color:var(--b-light) !important;
}
.stAlert { border-radius:var(--r-sm) !important; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-inner) {
    background:var(--bg-card) !important; border:1px solid var(--b-default) !important;
    border-radius:var(--r-lg) !important; box-shadow:var(--s-sm) !important;
}
</style>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def init_state():
    defaults = {
        "step": 1,
        "alias": None,
        "partner": None,
        "partner_mood": None,
        "partner_speed": None,
        "partner_convo": None,
        "partner_dish_name": None,
        "partner_dish_img": None,
        "chat_history": [],
        "_wingman": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(step: int):
    st.session_state.step = step


def generate_partner():
    st.session_state.partner = random.choice(PARTNER_ALIASES)
    st.session_state.partner_mood = random.choice(MOODS)
    st.session_state.partner_speed = random.choice(SPEEDS)
    st.session_state.partner_convo = random.choice(CONVOS)
    dish = get_partner_dish(st.session_state.partner)
    st.session_state.partner_dish_name = dish["name"]
    st.session_state.partner_dish_img = dish["img"]
    st.session_state.chat_history = []


def progress_dots(current: int, total: int = 4):
    items = ""
    for i in range(1, total + 1):
        cls = "dot-i on" if i == current else "dot-i"
        items += f'<div class="{cls}"></div>'
    st.markdown(f'<div class="dots">{items}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Screen 1 — Welcome
# ---------------------------------------------------------------------------

def screen_welcome():
    progress_dots(1)

    st.markdown(
        '<div class="hero">'
        '<div class="hero-emoji">&#127860;</div>'
        '<h1>Co-<em>Dine</em></h1>'
        '<div class="tagline">Never eat alone</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 2, 1])
    with col:
        with st.container(border=True):
            st.markdown('<div class="card-inner">', unsafe_allow_html=True)
            if st.session_state.alias is None:
                st.markdown(
                    '<p style="color:var(--t-muted);margin:0 0 .5rem;font-size:.93rem;text-align:center;">'
                    'Get a secret food alias to start dining.</p>',
                    unsafe_allow_html=True,
                )
                if st.button("Generate My Alias", type="primary", use_container_width=True):
                    st.session_state.alias = random.choice(ALIASES)
                    st.rerun()
            else:
                st.markdown(
                    f'<div style="margin-bottom:.5rem;text-align:center;">'
                    f'<span class="alias-pill">{st.session_state.alias}</span></div>'
                    f'<p style="color:var(--t-muted);font-size:.88rem;margin:0 0 .5rem;text-align:center;">'
                    f'Your secret identity is ready.</p>',
                    unsafe_allow_html=True,
                )
                if st.button("Start Dining", type="primary", use_container_width=True):
                    go_to(2)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Screen 2 — Vibe Check
# ---------------------------------------------------------------------------

def screen_vibe_check():
    progress_dots(2)

    st.markdown(
        f'<div style="text-align:center;margin-bottom:.2rem;">'
        f'<span class="alias-pill-sm">{st.session_state.alias}</span></div>'
        f'<div style="text-align:center;margin-bottom:1.25rem;">'
        f'<h2 style="font-size:1.7rem;font-weight:700;color:var(--t-dark);margin:.4rem 0 .15rem;">Vibe Check</h2>'
        f'<p style="color:var(--t-muted);font-size:.9rem;margin:0;">Answer three quick questions to find your perfect match.</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 3, 1])
    with col:
        with st.container(border=True):
            st.markdown('<div class="q-label">What\'s your current mood?</div>', unsafe_allow_html=True)
            mood = st.radio("Current mood", MOODS, horizontal=True, label_visibility="collapsed")

            st.divider()

            st.markdown('<div class="q-label">How fast do you eat?</div>', unsafe_allow_html=True)
            speed = st.radio("Eating speed", SPEEDS, horizontal=True, label_visibility="collapsed")

            st.divider()

            st.markdown('<div class="q-label">What kind of conversation?</div>', unsafe_allow_html=True)
            convo = st.radio("Conversation type", CONVOS, horizontal=True, label_visibility="collapsed")

        st.markdown("")
        if st.button("Find My Dining Buddy", type="primary", use_container_width=True):
            st.session_state.user_mood = mood
            st.session_state.user_speed = speed
            st.session_state.user_convo = convo
            go_to(3)
            st.rerun()


# ---------------------------------------------------------------------------
# Screen 3 — Searching
# ---------------------------------------------------------------------------

def screen_search():
    progress_dots(3)
    st.markdown(
        '<div class="search-hero">'
        '<h2>Finding your match...</h2>'
        '<p>Scanning vibes, comparing cravings, picking the perfect table.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    with st.spinner("Searching for a dining buddy..."):
        time.sleep(3)
    generate_partner()
    go_to(4)
    st.rerun()


# ---------------------------------------------------------------------------
# Screen 4 — The Table
# ---------------------------------------------------------------------------

def screen_table():
    progress_dots(4)

    partner = st.session_state.partner

    st.markdown(
        f'<div class="conn-bar">'
        f'<div class="live"></div>'
        f'<div><div class="nm">{partner}</div>'
        f'<div class="sub">Connected &#8212; enjoy your meal together</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1], gap="medium")

    with left:
        st.markdown('<div class="slabel">Your Partner</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.image(st.session_state.partner_dish_img, use_container_width=True)
            st.markdown(
                f'<div style="text-align:center;padding:0.25rem 0 0.5rem;">'
                f'<div class="dish-name">{st.session_state.partner_dish_name}</div>'
                f'<div class="partner-name">{partner}</div>'
                f'<div class="partner-tags">'
                f'<span class="ptag">Mood: {st.session_state.partner_mood}</span>'
                f'<span class="ptag">Speed: {st.session_state.partner_speed}</span>'
                f'<span class="ptag">Convo: {st.session_state.partner_convo}</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown('<div class="slabel">Walkie-Talkie</div>', unsafe_allow_html=True)

        chat_box = st.container(height=260)
        with chat_box:
            if not st.session_state.chat_history:
                st.markdown(
                    '<div class="chat-placeholder">No messages yet &#8212; say hi!</div>',
                    unsafe_allow_html=True,
                )
            else:
                html = '<div class="chat-wrap">'
                for m in st.session_state.chat_history:
                    safe_text = html_lib.escape(m["text"])
                    if m["role"] == "user":
                        html += (
                            '<div class="msg msg-me">'
                            f'<div class="msg-who">You</div>{safe_text}</div>'
                        )
                    else:
                        html += (
                            '<div class="msg msg-them">'
                            f'<div class="msg-who">{partner}</div>{safe_text}</div>'
                        )
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input(
                "Chat message", label_visibility="collapsed", placeholder="Type a message..."
            )
            sent = st.form_submit_button("Send", use_container_width=True)

        if sent and user_msg.strip():
            st.session_state.chat_history.append({"role": "user", "text": user_msg.strip()})
            st.session_state.chat_history.append({"role": "partner", "text": random.choice(AUTO_REPLIES)})
            st.rerun()

        st.markdown(
            '<div class="slabel" style="margin-top:.6rem;">Quick Actions</div>',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("AI Wingman", use_container_width=True):
                st.session_state["_wingman"] = random.choice(WINGMAN_PROMPTS)
        with c2:
            if st.button("Shop This Plate", use_container_width=True):
                st.toast("Recipe added to Instacart!", icon="\U0001F6D2")

        if st.session_state.get("_wingman"):
            st.info(f"**Try asking:** {st.session_state['_wingman']}")
            st.session_state["_wingman"] = None

        if st.button("Find a New Buddy", use_container_width=True):
            go_to(3)
            st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Co-Dine", page_icon="🍽️", layout="centered")
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    init_state()

    step = st.session_state.step
    if step == 1:
        screen_welcome()
    elif step == 2:
        screen_vibe_check()
    elif step == 3:
        screen_search()
    elif step == 4:
        screen_table()


if __name__ == "__main__":
    main()
