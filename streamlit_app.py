import streamlit as st

st.set_page_config(
    page_title="Badminton Score",
    page_icon="🏸",
    layout="centered"
)

if "a" not in st.session_state:
    st.session_state.a = 0
    st.session_state.b = 0
    st.session_state.ga = 0
    st.session_state.gb = 0
    st.session_state.server = "A"
    st.session_state.history = []

def save():
    st.session_state.history.append((
        st.session_state.a,
        st.session_state.b,
        st.session_state.ga,
        st.session_state.gb,
        st.session_state.server
    ))

def game_won(x, y):
    return x >= 30 or (x >= 21 and x >= y + 2)

def point(player):
    save()

    if player == "A":
        st.session_state.a += 1
        st.session_state.server = "A"
    else:
        st.session_state.b += 1
        st.session_state.server = "B"

    if game_won(st.session_state.a, st.session_state.b):
        st.session_state.ga += 1
        st.session_state.a = 0
        st.session_state.b = 0

    elif game_won(st.session_state.b, st.session_state.a):
        st.session_state.gb += 1
        st.session_state.a = 0
        st.session_state.b = 0

def undo():
    if st.session_state.history:
        a, b, ga, gb, server = st.session_state.history.pop()
        st.session_state.a = a
        st.session_state.b = b
        st.session_state.ga = ga
        st.session_state.gb = gb
        st.session_state.server = server

def new_match():
    st.session_state.a = 0
    st.session_state.b = 0
    st.session_state.ga = 0
    st.session_state.gb = 0
    st.session_state.server = "A"
    st.session_state.history = []

st.title("🏸 Badminton Score")

col1, col2 = st.columns(2)

with col1:
    name_a = st.text_input("Player A", "Player A")
    st.metric("SCORE", st.session_state.a)

with col2:
    name_b = st.text_input("Player B", "Player B")
    st.metric("SCORE", st.session_state.b)

st.divider()

st.subheader(
    f"Games  {st.session_state.ga}  –  {st.session_state.gb}"
)

st.info(
    f"🏸 {name_a if st.session_state.server == 'A' else name_b} serves"
)

col1, col2 = st.columns(2)

with col1:
    if st.button(
        f"➕ {name_a}",
        use_container_width=True,
        type="primary"
    ):
        point("A")
        st.rerun()

with col2:
    if st.button(
        f"➕ {name_b}",
        use_container_width=True
    ):
        point("B")
        st.rerun()

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("↩️ UNDO", use_container_width=True):
        undo()
        st.rerun()

with col2:
    if st.button("🔄 NEW MATCH", use_container_width=True):
        new_match()
        st.rerun()

if st.session_state.ga == 2:
    st.success(f"🏆 {name_a} wins the match!")

if st.session_state.gb == 2:
    st.success(f"🏆 {name_b} wins the match!")

st.caption(
    "21-point rally scoring • 20–20 requires a 2-point lead • "
    "29–29 is decided by the next point"
)