import datetime
import json

import boto3
import streamlit as st

R2_PREFIX = "invites/"


def get_r2_client():
    try:
        secrets = st.secrets
        account_id = secrets["R2_ACCOUNT_ID"]
        access_key = secrets["R2_ACCESS_KEY_ID"]
        secret_key = secrets["R2_SECRET_ACCESS_KEY"]
    except (KeyError, FileNotFoundError):
        return None
    return boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )


def log_invite(movie_title, date_label, time_label):
    client = get_r2_client()
    if client is None:
        return
    now = datetime.datetime.now()
    key = f"{R2_PREFIX}{now.strftime('%Y%m%dT%H%M%S')}.json"
    body = json.dumps({
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "movie": movie_title,
        "date": date_label,
        "time": time_label,
    })
    client.put_object(Bucket=st.secrets["R2_BUCKET"], Key=key, Body=body.encode("utf-8"))


def get_invite_history():
    client = get_r2_client()
    if client is None:
        return None
    bucket = st.secrets["R2_BUCKET"]
    resp = client.list_objects_v2(Bucket=bucket, Prefix=R2_PREFIX)
    entries = []
    for obj in resp.get("Contents", []):
        data = client.get_object(Bucket=bucket, Key=obj["Key"])
        entries.append(json.loads(data["Body"].read()))
    entries.sort(key=lambda e: e["timestamp"], reverse=True)
    return entries

MOVIES = [
    {
        "emoji": "",
        "title": "Прошлые жизни",
        "genre": "Драма",
        "time": "2ч 31м",
        "link": "https://www.youtube.com/watch?v=79kM10MCPsE",
    },
    {
        "emoji": "",
        "title": "Дамы вперед",
        "genre": "Комедия",
        "time": "1ч 30м",
        "link": "https://www.youtube.com/watch?v=rW-8maecA_E",
    },
    {
        "emoji": "",
        "title": "Марти Великолепный",
        "genre": "Драма",
        "time": "2ч 30м",
        "link": "https://www.youtube.com/watch?v=Nv1mD57tl8Q",
    },
    {
        "emoji": "",
        "title": "Престиж",
        "genre": "Детектив",
        "time": "2ч 10м",
        "link": "https://www.youtube.com/watch?v=0B6O17m9sWE",
    },
]

WEEKDAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
MONTHS_RU = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]


def build_dates(n=14):
    today = datetime.date.today()
    labels = []
    for i in range(n):
        d = today + datetime.timedelta(days=i)
        tag = "Сегодня" if i == 0 else ("Завтра" if i == 1 else WEEKDAYS_RU[d.weekday()])
        labels.append(f"{tag}, {d.day} {MONTHS_RU[d.month - 1]}")
    return labels


#DATES = build_dates(14)
DATES = ["Вт, 28 июл", "Ср, 29 июл", "Чт, 30 июл"]
TIMES = ["17:30", "18:00", "19:00", "20:00"]

st.set_page_config(page_title="Валера приглашает", page_icon="💌", layout="wide")

CSS = """
<style>
@keyframes bgShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pop {
    0%   { transform: scale(0.9); opacity: 0; }
    60%  { transform: scale(1.03); opacity: 1; }
    100% { transform: scale(1); }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-6px); }
}
@keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}
@keyframes confettiFall {
    0%   { transform: translateY(-20px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(160px) rotate(360deg); opacity: 0; }
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a40);
    background-size: 400% 400%;
    animation: bgShift 18s ease infinite;
}
[data-testid="stHeader"] { background: transparent; }

#hero {
    text-align: center;
    padding: 20px 10px 4px 10px;
    animation: fadeUp 0.8s ease both;
}
#hero h1 {
    font-size: 2.4rem;
    margin-bottom: 6px;
    background: linear-gradient(90deg, #ff9966, #ff5e62, #8e2de2, #4a00e0, #00c6ff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shimmer 6s linear infinite;
}
#hero p { color: #cfd0ff; font-size: 1.05rem; opacity: 0.85; }

.section-title {
    color: #fff;
    font-size: 1.15rem;
    font-weight: 600;
    margin: 18px 0 8px 0;
    animation: fadeUp 0.6s ease both;
}

.stButton > button, .stLinkButton > a {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    background: rgba(255,255,255,0.06) !important;
    color: #fff !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease !important;
    animation: fadeUp 0.5s ease both;
}
.stButton > button:hover, .stLinkButton > a:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 10px 24px rgba(138,58,226,0.35);
    background: rgba(255,255,255,0.14) !important;
}
.stButton > button[kind="primary"] {
    border-color: #ff5e62 !important;
    background: linear-gradient(135deg, rgba(255,94,98,0.35), rgba(142,45,226,0.35)) !important;
    box-shadow: 0 0 0 2px rgba(255,94,98,0.55), 0 10px 24px rgba(255,94,98,0.25) !important;
}
.stLinkButton > a {
    background: linear-gradient(135deg, rgba(0,198,255,0.9), rgba(0,114,255,0.9)) !important;
    border: none !important;
    font-weight: 600 !important;
    text-align: center;
    justify-content: center;
}
.stLinkButton > a:hover {
    box-shadow: 0 6px 16px rgba(0,114,255,0.5) !important;
}

#invite-btn .stButton > button {
    background: linear-gradient(135deg, #ff5e62, #ff9966) !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 12px !important;
    animation: float 3s ease-in-out infinite;
}
#invite-btn .stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 26px rgba(255,94,98,0.45) !important;
}

.result-card {
    animation: pop 0.55s cubic-bezier(.26,1.4,.44,1) both;
    border-radius: 20px;
    padding: 22px;
    background: linear-gradient(135deg, rgba(142,45,226,0.25), rgba(0,198,255,0.18));
    border: 1px solid rgba(255,255,255,0.18);
    position: relative;
    overflow: hidden;
    color: #fff;
}
.result-card::before {
    content: "🎉";
    position: absolute;
    left: 10%;
    font-size: 22px;
    animation: confettiFall 1.6s ease-in forwards;
}
.result-card::after {
    content: "🍿";
    position: absolute;
    right: 15%;
    font-size: 22px;
    animation: confettiFall 1.9s ease-in forwards;
}

.stButton > button, .stLinkButton > a {
    min-height: 44px;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        padding-top: 1rem !important;
    }
    #hero h1 { font-size: 1.6rem; }
    #hero p { font-size: 0.9rem; }
    .section-title { font-size: 1rem; margin: 14px 0 6px 0; }

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 8px !important;
    }
    [data-testid="stHorizontalBlock"] [data-testid="column"] {
        flex: 1 1 45% !important;
        min-width: 0 !important;
        width: 45% !important;
    }
    .stButton > button, .stLinkButton > a {
        font-size: 0.85rem !important;
        padding: 8px 6px !important;
    }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div id="hero">
        <h1> Валерий приглашает Анжелу</h1>
        <p>Выбери фильм, день и время</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "movie_idx" not in st.session_state:
    st.session_state.movie_idx = 0
if "date_idx" not in st.session_state:
    st.session_state.date_idx = 0
if "time_idx" not in st.session_state:
    st.session_state.time_idx = 2
if "show_invite" not in st.session_state:
    st.session_state.show_invite = False

st.markdown('<div class="section-title">🎥 Выбери фильм</div>', unsafe_allow_html=True)
movie_cols = st.columns(len(MOVIES))
for i, (col, m) in enumerate(zip(movie_cols, MOVIES)):
    with col:
        selected = st.session_state.movie_idx == i
        if st.button(
            f"{m['emoji']}  {m['title']}",
            key=f"movie_{i}",
            use_container_width=True,
            type="primary" if selected else "secondary",
        ):
            st.session_state.movie_idx = i
            st.rerun()
        st.caption(f"{m['genre']} · {m['time']}")
        if m.get("link"):
            st.link_button("▶ Трейлер", m["link"], use_container_width=True)

st.markdown('<div class="section-title">📅 Выбери дату</div>', unsafe_allow_html=True)
for row_start in range(0, len(DATES), 7):
    row = DATES[row_start:row_start + 7]
    date_cols = st.columns(7)
    for j, label in enumerate(row):
        idx = row_start + j
        with date_cols[j]:
            selected = st.session_state.date_idx == idx
            if st.button(
                label,
                key=f"date_{idx}",
                use_container_width=True,
                type="primary" if selected else "secondary",
            ):
                st.session_state.date_idx = idx
                st.rerun()

st.markdown('<div class="section-title">🕒 Выбери время сеанса</div>', unsafe_allow_html=True)
time_cols = st.columns(len(TIMES))
for i, (col, t) in enumerate(zip(time_cols, TIMES)):
    with col:
        selected = st.session_state.time_idx == i
        if st.button(
            t,
            key=f"time_{i}",
            use_container_width=True,
            type="primary" if selected else "secondary",
        ):
            st.session_state.time_idx = i
            st.rerun()

current_movie = MOVIES[st.session_state.movie_idx]
current_date = DATES[st.session_state.date_idx]
current_time = TIMES[st.session_state.time_idx]

st.markdown(
    f"""
    <p style="color:#cfd0ff; margin:6px 0 14px 0;">
    Выбрано сейчас: <b>{current_movie['emoji']} {current_movie['title']}</b>
    &nbsp;·&nbsp; 📅 <b>{current_date}</b> &nbsp;·&nbsp; 🕒 <b>{current_time}</b>
    </p>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.markdown('<div id="invite-btn">', unsafe_allow_html=True)
if st.button("✨ Подтверждаю", key="invite_btn", use_container_width=True):
    st.session_state.show_invite = True
    log_invite(current_movie["title"], current_date, current_time)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_invite:
    st.markdown(
        f"""
        <div class="result-card">
        <p><b>Валерий</b> приглашает <b>Анжелу</b> посмотреть онлайн:</p>
        <p><b>{current_movie['emoji']} {current_movie['title']}</b><br>{current_movie['genre']} · {current_movie['time']}</p>
        <p>📅 <b>{current_date}</b> &nbsp; 🕒 <b>{current_time}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

history = get_invite_history()
if history is None:
    st.caption("История приглашений: не настроен R2 (заполни .streamlit/secrets.toml)")
else:
    with st.expander("📋 История приглашений"):
        if not history:
            st.write("Пока пусто.")
        for entry in history:
            st.write(f"{entry['timestamp']} — **{entry['movie']}**, {entry['date']}, {entry['time']}")
