import random
import math
import streamlit as st

# ===== 🎒 중학교 수학 교실용 헤더 =====
st.markdown("""
        <style>
            .title-wrap { text-align:center; margin-top:-14px; margin-bottom:6px; }
            .class-title { font-size: 2.1em; font-weight: 800; color: #2a6fb2; margin: 0; letter-spacing: 0.5px; }
            .class-title .accent { color: #f2a900; }
            .subtitle { font-size: 1.05em; color: #5b6b7a; margin-top: 4px; }

            /* ✅ 교실 미션 박스 */
            .chalkboard {
                background: #f9fcff; 
                border: 1px solid #e4eef8; 
                border-radius: 14px; 
                padding: 10px 14px; 
                margin: 8px auto 12px auto;
                width: 15cm;
                text-align: center;
            }

            /* 중앙 래퍼 */
            .center-wrap { width: 10cm; margin: 0 auto; text-align: center; }

            /* 단계 라벨 배지 */
            .stage-badge { padding:5px 12px; border-radius:999px; background:#eef6ff; border:1px solid #d5e9ff; color: #244e75; }

            /* 입력창 */
            div[data-testid="stNumberInput"] { width: 10cm !important; margin: 0 auto; }

            /* 안내 박스 */
            .ui-box { width: 10cm; margin: 8px auto; padding: 10px 12px; border-radius: 10px; text-align: center; }
            .ui-info { background: #eef6ff; border: 1px solid #d5e9ff; color: #244e75; }
            .ui-success { background: #eef9f1; border: 1px solid #cfeeda; color: #24623d; }
            .ui-warning { background: #fff7e6; border: 1px solid #ffe0a3; color: #6a4b14; }

            /* ✅ 버튼 영역 */
            .btn-area {
                width: 10cm;
                margin: 10px auto 6px auto;
                display: flex;
                justify-content: flex-start;
            }
            .btn-area button {
                width: 5cm !important;
                height: 2.5em;
                font-size: 1.0rem;
                font-weight: 600;
            }

            /* 단계 시각 효과 */
            .pulse { animation: pulse 1.4s infinite; display:inline-block; }
            .bounce { animation: bounce 1.2s infinite; display:inline-block; }
            .shake { animation: shake 0.8s ease-in-out infinite; display:inline-block; }
            .pop  { animation: pop 0.9s ease-in-out infinite; display:inline-block; }
            @keyframes pulse { 0%{transform:scale(1)} 50%{transform:scale(1.12)} 100%{transform:scale(1)} }
            @keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
            @keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-3px)} 50%{transform:translateX(3px)} 75%{transform:translateX(-2px)} }
            @keyframes pop { 0%,100%{transform:scale(1)} 50%{transform:scale(1.18)} }

            /* 단계 상자 */
            .stage-box { margin:4px auto 12px auto; padding:10px 12px; border:1px dashed #e1e1e1; border-radius:10px; background:#fafafa; width: 10cm; }

            /* ✅ 큰 분수 표시 */
            .big-fraction { font-size: 200%; text-align:center; margin-bottom: 8px; }

            /* 다크 모드 감지 및 스타일 오버라이드 */
            @media (prefers-color-scheme: dark) {
                .class-title { color: #9ecfff !important; }
                .class-title .accent { color: #ffbf69 !important; }
                .subtitle { color: #c7d7e6 !important; }
                .chalkboard {
                    background: #071025 !important;
                    border: 1px solid #15314a !important;
                    color: #e6f4ff !important;
                }
                .ui-box { background: transparent !important; }
                .ui-info { background: #072034 !important; border: 1px solid #0b3f59 !important; color: #cbe9ff !important; }
                .ui-success { background: #032515 !important; border: 1px solid #0c3b22 !important; color: #bff0c8 !important; }
                .ui-warning { background: #2b1606 !important; border: 1px solid #4b2b0f !important; color: #ffdca3 !important; }
                .stage-box { background: #071722 !important; border-color: #17393f !important; color: #e7f6ff !important; }
                .big-fraction { color: #e8f3ff !important; }
                .center-wrap { color: #dfefff !important; }
                .btn-area button { background-color: #0f2a3a !important; color: #e6f6ff !important; border: 1px solid #15455a !important; }
                div[data-testid="stNumberInput"] input, .stTextInput>div>input, .stTextArea>div>textarea { background: #071622 !important; color: #e6f6ff !important; border: 1px solid #153647 !important; }
                /* 링크/강조 색상 */
                a { color: #4fd1ff !important; }
            }
        </style>
        <div class="title-wrap">
                <h1 class="class-title">🧮 분수의 약분 <span class="accent">마스터 👑</span></h1>
                <div class="chalkboard">
                    <div class="subtitle">교실 미션: 공약수를 찾아 분수를 <b>기약분수</b>로 만들자! ✏️📐</div>
                </div>
        </div>
""", unsafe_allow_html=True)

# -------------------------------
# Helpers
# -------------------------------
def generate_fraction():
    while True:
        n = random.randint(2, 50)
        d = random.randint(2, 50)
        if n < d and math.gcd(n, d) != 1:
            return n, d

def get_divisors(n, d):
    return [i for i in range(2, min(n, d) + 1) if n % i == 0 and d % i == 0]

def goto(step):
    st.session_state.step = step
    st.rerun()

def set_fraction(n, d):
    st.session_state.numerator = n
    st.session_state.denominator = d

def ensure_state():
    ss = st.session_state
    if 'step' not in ss:
        ss.step = 1
    if 'numerator' not in ss or 'denominator' not in ss:
        ss.numerator, ss.denominator = generate_fraction()
    if 'current_divisor' not in ss:
        ss.current_divisor = None

# 안내 박스
def ui_info(text): st.markdown(f'<div class="ui-box ui-info">{text}</div>', unsafe_allow_html=True)
def ui_success(text): st.markdown(f'<div class="ui-box ui-success">{text}</div>', unsafe_allow_html=True)
def ui_warning(text): st.markdown(f'<div class="ui-box ui-warning">{text}</div>', unsafe_allow_html=True)

# 단계 표시
def show_progress(step):
    labels = {1:"① 공약수 찾기 단계", 2:"② 약분 계산 단계", 2.5:"③ 다시 약분하기 단계", 3:"④ 기약분수 완성 단계"}
    st.markdown(f"""
    <div class="center-wrap">
      <div style="display:flex;gap:8px;align-items:center;justify-content:center;margin:8px 0 6px 0;">
        <span style="font-weight:700;font-size:1.0rem;">📘 현재 학습 단계</span>
                <span class="stage-badge">
                    {labels.get(step, '시작')}
                </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

def show_stage_visual(step):
    if step == 1:
        st.markdown('<div class="stage-box">🔍 <span class="bounce">공약수 찾기!</span> 가능한 수를 탐색해봐요.</div>', unsafe_allow_html=True)
    elif step == 2:
        st.markdown('<div class="stage-box">➗ <span class="pulse">약분 계산 중</span> — 분자와 분모를 같은 수로 나눠요.</div>', unsafe_allow_html=True)
    elif step == 2.5:
        st.markdown('<div class="stage-box">🔁 <span class="shake">기약분수가 아니에요</span> — 한 번 더 약분해봐요.</div>', unsafe_allow_html=True)
    elif step == 3:
        st.markdown('<div class="stage-box">🏆 <span class="pop">기약분수 달성!</span> 잘했어요 👏</div>', unsafe_allow_html=True)

# -------------------------------
# Init
# -------------------------------
ensure_state()
n = st.session_state.numerator
d = st.session_state.denominator

st.markdown('<div class="center-wrap">', unsafe_allow_html=True)
show_progress(st.session_state.step)
show_stage_visual(st.session_state.step)

# -------------------------------
# STEP 1
# -------------------------------
if st.session_state.step == 1:
    st.markdown("<div class='big-fraction'>", unsafe_allow_html=True)
    st.latex(f"\\Large \\frac{{{n}}}{{{d}}}")
    st.markdown("</div>", unsafe_allow_html=True)

    ui_info("분수를 보고, 어떤 수로 나눌 수 있는지 직접 입력하세요.")
    user_div = st.number_input("어떤 수로 나눌 수 있나요? (2~50)", min_value=1, max_value=50, step=1,
                               key="user_div_input", format="%d")

    st.markdown('<div class="btn-area">', unsafe_allow_html=True)
    if st.button("완료", key="btn_div"):
        if user_div in get_divisors(n, d):
            st.session_state.current_divisor = int(user_div)
            goto(2)
        else:
            ui_warning("답이 맞지 않아요. 다시 생각해보세요.")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# STEP 2
# -------------------------------
elif st.session_state.step == 2:
    ui_success(f"좋아요! 이제 {st.session_state.current_divisor}로 약분해봅시다.")
    st.markdown(f"<p style='text-align:center;'>문제로 제시한 분수</p>", unsafe_allow_html=True)
    st.latex(f"\\Large \\frac{{{n}}}{{{d}}}")
    st.markdown(f"<p style='text-align:center;'>를 {st.session_state.current_divisor}로 나누세요.</p>", unsafe_allow_html=True)

    num = st.number_input("분자(나눈 결과)", min_value=1, max_value=n, step=1, key=f"num_{n}_{d}")
    den = st.number_input("분모(나눈 결과)", min_value=1, max_value=d, step=1, key=f"den_{n}_{d}")

    st.markdown('<div class="btn-area">', unsafe_allow_html=True)
    if st.button("완료", key=f"btn_reduce_{n}_{d}"):
        div = st.session_state.current_divisor
        cn, cd = n // div, d // div
        if num == cn and den == cd:
            set_fraction(cn, cd)
            goto(3 if math.gcd(cn, cd) == 1 else 2.5)
        else:
            ui_warning("답이 틀렸습니다. 다시 약분해보세요.")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# STEP 2.5
# -------------------------------
elif st.session_state.step == 2.5:
    ui_info("기약분수가 아니네요. 다시 약분해 봅시다.")
    st.latex(f"\\Large \\frac{{{st.session_state.numerator}}}{{{st.session_state.denominator}}}")
    st.markdown('<div class="btn-area">', unsafe_allow_html=True)
    if st.button("다음", key="btn_next"):
        st.session_state.current_divisor = None
        goto(1)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# STEP 3
# -------------------------------
elif st.session_state.step == 3:
    ui_success("정답이에요! 기약분수를 완성했습니다 👏")
    st.latex(f"\\Large \\frac{{{st.session_state.numerator}}}{{{st.session_state.denominator}}}")
    st.markdown('<div class="btn-area">', unsafe_allow_html=True)
    if st.button("새로운 문제 풀기", key="btn_new"):
        set_fraction(*generate_fraction())
        st.session_state.current_divisor = None
        goto(1)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)