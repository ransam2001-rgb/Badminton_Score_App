import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Badminton Score",
    page_icon="🏸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# CUSTOM MOBILE STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }

    .score {
        font-size: 80px;
        font-weight: 700;
        text-align: center;
        line-height: 1;
    }

    .player {
        font-size: 22px;
        font-weight: 700;
        text-align: center;
    }

    .games {
        text-align: center;
        font-size: 25px;
        font-weight: 700;
    }

    .serve {
        text-align: center;
        font-size: 18px;
        padding: 8px;
    }

    div.stButton > button {
        width: 100%;
        min-height: 65px;
        font-size: 20px;
        font-weight: 700;
        border-radius: 14px;
    }

    .history-card {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

defaults = {
    "a": 0,
    "b": 0,
    "ga": 0,
    "gb": 0,
    "server": "A",
    "history": [],
    "matches": [],
    "game_scores": [],
    "match_finished": False,
    "match_started": datetime.now().strftime("%Y-%m-%d %H:%M"),
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------------
# PLAYER NAMES
# ---------------------------------------------------------

st.title("🏸 Badminton Score")

name_a = st.text_input(
    "Player A",
    value="Player A",
)

name_b = st.text_input(
    "Player B",
    value="Player B",
)

# ---------------------------------------------------------
# BADMINTON RULES
# ---------------------------------------------------------

def game_won(score, other):
    """
    Standard badminton game:
    - First to 21
    - At 20-20, must win by 2
    - At 29-29, next point wins
    """
    if score >= 30:
        return True

    if score < 21:
        return False

    return score >= other + 2


# ---------------------------------------------------------
# SAVE CURRENT STATE FOR UNDO
# ---------------------------------------------------------

def save_undo():
    st.session_state.history.append(
        {
            "a": st.session_state.a,
            "b": st.session_state.b,
            "ga": st.session_state.ga,
            "gb": st.session_state.gb,
            "server": st.session_state.server,
            "game_scores": list(st.session_state.game_scores),
            "match_finished": st.session_state.match_finished,
        }
    )


# ---------------------------------------------------------
# RECORD COMPLETED MATCH
# ---------------------------------------------------------

def save_completed_match(winner):
    match = {
        "date": st.session_state.match_started,
        "player_a": name_a,
        "player_b": name_b,
        "score": ", ".join(st.session_state.game_scores),
        "winner": winner,
    }

    st.session_state.matches.insert(0, match)


# ---------------------------------------------------------
# ADD POINT
# ---------------------------------------------------------

def point(player):
    if st.session_state.match_finished:
        return

    save_undo()

    if player == "A":
        st.session_state.a += 1
        st.session_state.server = "A"
    else:
        st.session_state.b += 1
        st.session_state.server = "B"

    # Player A wins game
    if game_won(st.session_state.a, st.session_state.b):

        st.session_state.game_scores.append(
            f"{st.session_state.a}-{st.session_state.b}"
        )

        st.session_state.ga += 1
        st.session_state.a = 0
        st.session_state.b = 0
        st.session_state.server = "A"

        if st.session_state.ga == 2:
            st.session_state.match_finished = True
            save_completed_match(name_a)

    # Player B wins game
    elif game_won(st.session_state.b, st.session_state.a):

        st.session_state.game_scores.append(
            f"{st.session_state.a}-{st.session_state.b}"
        )

        st.session_state.gb += 1
        st.session_state.a = 0
        st.session_state.b = 0
        st.session_state.server = "B"

        if st.session_state.gb == 2:
            st.session_state.match_finished = True
            save_completed_match(name_b)


# ---------------------------------------------------------
# UNDO
# ---------------------------------------------------------

def undo():
    if not st.session_state.history:
        return

    previous = st.session_state.history.pop()

    st.session_state.a = previous["a"]
    st.session_state.b = previous["b"]
    st.session_state.ga = previous["ga"]
    st.session_state.gb = previous["gb"]
    st.session_state.server = previous["server"]
    st.session_state.game_scores = previous["game_scores"]
    st.session_state.match_finished = previous["match_finished"]


# ---------------------------------------------------------
# NEW MATCH
# ---------------------------------------------------------

def new_match():
    st.session_state.a = 0
    st.session_state.b = 0
    st.session_state.ga = 0
    st.session_state.gb = 0
    st.session_state.server = "A"
    st.session_state.history = []
    st.session_state.game_scores = []
    st.session_state.match_finished = False
    st.session_state.match_started = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )


# ---------------------------------------------------------
# HEADER IMAGE
# ---------------------------------------------------------

try:
    st.image(
        "https://commons.wikimedia.org/wiki/Special:FilePath/Badminton_court_view.jpg",
        use_container_width=True,
    )
except Exception:
    pass

# ---------------------------------------------------------
# MATCH SCORE
# ---------------------------------------------------------

st.markdown(
    f'<div class="games">Games&nbsp;&nbsp; {st.session_state.ga} '
    f'– {st.session_state.gb}</div>',
    unsafe_allow_html=True,
)

st.write("")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f'<div class="player">🏸 {name_a}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="score">{st.session_state.a}</div>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f'<div class="player">🏸 {name_b}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="score">{st.session_state.b}</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# SERVER
# ---------------------------------------------------------

server_name = name_a if st.session_state.server == "A" else name_b

st.markdown(
    f'<div class="serve">🏸 <b>{server_name}</b> is serving</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# POINT BUTTONS
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    if st.button(
        f"➕ {name_a} POINT",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.match_finished,
    ):
        point("A")
        st.rerun()

with col2:
    if st.button(
        f"➕ {name_b} POINT",
        use_container_width=True,
        disabled=st.session_state.match_finished,
    ):
        point("B")
        st.rerun()

# ---------------------------------------------------------
# MATCH COMPLETE
# ---------------------------------------------------------

if st.session_state.match_finished:

    if st.session_state.ga == 2:
        winner = name_a
    else:
        winner = name_b

    st.success(
        f"🏆 {winner} wins the match!"
    )

    st.write(
        "Game scores: "
        + "  •  ".join(st.session_state.game_scores)
    )

# ---------------------------------------------------------
# CONTROL BUTTONS
# ---------------------------------------------------------

st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "↩️ UNDO",
        use_container_width=True,
        disabled=not st.session_state.history,
    ):
        undo()
        st.rerun()

with col2:
    if st.button(
        "🔄 NEW MATCH",
        use_container_width=True,
    ):
        new_match()
        st.rerun()

# ---------------------------------------------------------
# HISTORY
# ---------------------------------------------------------

st.divider()

st.subheader("📜 Match History")

if not st.session_state.matches:

    st.info(
        "No completed matches yet. "
        "Finish a match and it will appear here."
    )

else:

    for i, match in enumerate(st.session_state.matches):

        st.markdown(
            f"""
            **🏸 {match['player_a']} vs {match['player_b']}**

            🏆 Winner: **{match['winner']}**

            🎯 {match['score']}

            📅 {match['date']}
            """
        )

        st.divider()

    # -----------------------------------------------------
    # DOWNLOAD HISTORY
    # -----------------------------------------------------

    history_df = pd.DataFrame(
        st.session_state.matches
    )

    csv = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Match History",
        data=csv,
        file_name="badminton_match_history.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # -----------------------------------------------------
    # CLEAR HISTORY
    # -----------------------------------------------------

    if st.button(
        "🗑️ Clear Match History",
        use_container_width=True,
    ):
        st.session_state.matches = []
        st.rerun()

# ---------------------------------------------------------
# RULES
# ---------------------------------------------------------

with st.expander("📖 Badminton scoring rules"):

    st.write(
        """
        **Standard rally scoring**

        • A game is normally played to 21 points.

        • At 20–20, a player must lead by 2 points.

        • At 29–29, the next point wins the game.

        • A match is normally best of 3 games.

        • The first player/team to win 2 games wins the match.
        """
    )

st.caption(
    "🏸 Badminton Score • Made for mobile"
)