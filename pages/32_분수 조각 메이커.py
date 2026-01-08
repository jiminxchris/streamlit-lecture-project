import math
import random
import streamlit as st
import html

st.set_page_config(page_title="뚝딱! 분수 조각 메이커", page_icon="🧁", layout="wide")

# --- 스타일 (디저트 가게 테마 + 다크 모드 대응) ---
st.markdown(
    """
    <style>
    :root {
        --bg-light: linear-gradient(180deg, #FFF6F0 0%, #FFF0E6 100%);
        --bg-dark: linear-gradient(180deg, #1a1a1a 0%, #2a2a2a 100%);
        --text-light: #333;
        --text-dark: #e0e0e0;
        --title-light: #7A2F8A;
        --title-dark: #d4a5f8;
        --highlight-light: #FFF1CC;
        --highlight-dark: #3d3333;
        --note-light: #D35400;
        --note-dark: #ffb366;
        --card-light: #FFF8F2;
        --card-dark: #2a2a2a;
        --border-light: #F0D9C3;
        --border-dark: #404040;
        --btn-light: #FFD699;
        --btn-dark: #5a5a5a;
        --dashed-light: #F0D9C3;
        --dashed-dark: #505050;
    }
    
    /* 라이트 모드 (기본값) */
    @media (prefers-color-scheme: light) {
        .stApp { background: var(--bg-light) !important; }
        body { background: var(--bg-light) !important; }
        .title { color: var(--title-light); font-family: 'Comic Sans MS', cursive; }
        .big { font-size:20px; font-weight:700; color: var(--text-light); }
        .highlight { background: var(--highlight-light); padding:8px; border-radius:8px; color: var(--text-light); }
        .fraction-note { font-size:18px; font-weight:700; color: var(--note-light); }
    }
    
    /* 다크 모드 */
    @media (prefers-color-scheme: dark) {
        .stApp { background: var(--bg-dark) !important; }
        body { background: var(--bg-dark) !important; }
        .title { color: var(--title-dark); font-family: 'Comic Sans MS', cursive; }
        .big { font-size:20px; font-weight:700; color: var(--text-dark); }
        .highlight { background: var(--highlight-dark); padding:8px; border-radius:8px; color: var(--text-dark); }
        .fraction-note { font-size:18px; font-weight:700; color: var(--note-dark); }
    }
    
    /* 공통 스타일 */
    .title { font-family: 'Comic Sans MS', cursive; }
    .big { font-size:20px; font-weight:700; }
    .highlight { padding:8px; border-radius:8px; }
    .fraction-note { font-size:18px; font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# 🧁 뚝딱! 분수 조각 메이커")

# 다크 모드 감지 스크립트 추가
st.markdown("""
<script>
// 시스템 다크 모드 감지 및 HTML에 속성 추가
function updateDarkModeAttr() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-dark-mode', isDark ? 'true' : 'false');
}
updateDarkModeAttr();
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateDarkModeAttr);
</script>
""", unsafe_allow_html=True)

# 다크 모드 상태 확인 (JavaScript에서 감지)
dark_mode = False  # 기본값은 라이트 모드
# Streamlit 클라이언트를 통해 다크 모드 감지하려면 JavaScript를 사용해야 합니다

# --- 유틸리티: SVG 생성 ---

def svg_pizza(denominator: int, numerator: int, size: int = 300, fill_color="#FF8A80", dark_mode: bool = False) -> str:
    """좀 더 현실감 있는 피자 SVG를 반환합니다: 크러스트(테두리), 치즈, 토핑(페퍼로니)과 음영을 추가했습니다."""
    # 다크 모드 색상
    if dark_mode:
        crust_light = "#8B6F47"
        crust_dark = "#5C4A36"
        cheese_light = "#C4A876"
        cheese_dark = "#9A8060"
        empty_color = "#3a3a3a"
        pepperoni_light = "#E67E7E"
        pepperoni_dark = "#A03030"
        border_color = "#4a4a4a"
    else:
        crust_light = "#F4C27A"
        crust_dark = "#D18B3B"
        cheese_light = "#FFE0A3"
        cheese_dark = "#FFD08A"
        empty_color = "#FFF5E6"
        pepperoni_light = "#FF8A80"
        pepperoni_dark = "#BF360C"
        border_color = "#8B5A3A"
    
    cx = size // 2
    cy = size // 2
    r = size // 2 - 6
    # defs: gradients & shadow
    svg_parts = [f'''<svg width="{size}px" height="{size}px" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="crustGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="{crust_light}" />
          <stop offset="100%" stop-color="{crust_dark}" />
        </linearGradient>
        <radialGradient id="cheeseGrad" cx="50%" cy="30%" r="70%">
          <stop offset="0%" stop-color="{cheese_light}" />
          <stop offset="100%" stop-color="{cheese_dark}" />
        </radialGradient>
        <radialGradient id="pepperoniGrad" cx="30%" cy="30%" r="60%">
          <stop offset="0%" stop-color="{pepperoni_light}" />
          <stop offset="100%" stop-color="{pepperoni_dark}" />
        </radialGradient>
        <filter id="softShadow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.15"/>
        </filter>
      </defs>
      <!-- crust -->
      <circle cx="{cx}" cy="{cy}" r="{r + 8}" fill="url(#crustGrad)" stroke="{border_color}" stroke-width="2" />
      <!-- cheese -->
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#cheeseGrad)" stroke="{border_color}" stroke-width="1" />''']

    # slices and toppings
    for i in range(denominator):
        start = (2 * math.pi / denominator) * i - math.pi / 2
        end = (2 * math.pi / denominator) * (i + 1) - math.pi / 2
        x1 = cx + r * math.cos(start)
        y1 = cy + r * math.sin(start)
        x2 = cx + r * math.cos(end)
        y2 = cy + r * math.sin(end)
        large_arc = 1 if (end - start) > math.pi else 0
        d = f"M {cx} {cy} L {x1} {y1} A {r} {r} 0 {large_arc} 1 {x2} {y2} Z"
        if i < numerator:
            fill = "url(#cheeseGrad)"
            # add a pepperoni on this slice
            mid = (start + end) / 2
            px = cx + r * 0.45 * math.cos(mid)
            py = cy + r * 0.45 * math.sin(mid)
            pep = f'<circle class="topping" cx="{px}" cy="{py}" r="{max(4, size*0.06):.1f}" fill="url(#pepperoniGrad)" stroke="{border_color}" stroke-width="0.8" />'
            filled_flag = 1
        else:
            fill = empty_color
            pep = ''
            filled_flag = 0
        # add class/data attributes so JS can interact with slices
        svg_parts.append(f'<path class="slice" data-index="{i}" data-filled="{filled_flag}" d="{d}" fill="{fill}" stroke="{border_color}" stroke-width="0.8"/>')
        if pep:
            svg_parts.append(pep)

    # subtle highlight
    svg_parts.append(f'<circle cx="{cx}" cy="{cy - r*0.2}" r="{r*0.4:.1f}" fill="#FFFFFF" opacity="0.06" />')
    svg_parts.append('</svg>')
    return "".join(svg_parts)


def svg_chocolate(denominator: int, numerator: int, width: int = 320, height: int = 200, fill_color="#6D4C41", dark_mode: bool = False) -> str:
    """현실감 있는 초콜릿 바 SVG: 그라데이션과 광택, 여러 칸으로 나눈 초콜릿 모양을 그립니다."""
    # 다크 모드 색상
    if dark_mode:
        choco_light = "#5C4736"
        choco_dark = "#3d322a"
        shine_color = "#FFFFFF"
        empty_color = "#4a4a4a"
        border_color = "#2a2420"
    else:
        choco_light = "#7B4F3C"
        choco_dark = "#51342A"
        shine_color = "#FFFFFF"
        empty_color = "#EDE0D6"
        border_color = "#3F2A20"
    
    w = width
    h = height
    col_w = w / denominator
    rows = 2  # 살짝 높이를 나눠서 블록 느낌을 줌

    svg_parts = [f'''<svg width="{w}px" height="{h}px" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="chocoGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="{choco_light}" />
          <stop offset="100%" stop-color="{choco_dark}" />
        </linearGradient>
        <linearGradient id="shine" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="{shine_color}" stop-opacity="0.15" />
          <stop offset="100%" stop-color="{shine_color}" stop-opacity="0" />
        </linearGradient>
      </defs>
      <!-- rounded chocolate bar -->
      <rect x="2" y="2" rx="12" ry="12" width="{w-4}" height="{h-4}" fill="url(#chocoGrad)" stroke="{border_color}" stroke-width="2" />
      <!-- inner shine -->
      <rect x="6" y="6" rx="10" ry="10" width="{w-12}" height="{h-12}" fill="url(#shine)" opacity="0.35" />''']

    # blocks
    idx = 0
    for row in range(rows):
        block_h = (h - 12) / rows
        for col in range(denominator):
            x = 8 + col * col_w
            y = 8 + row * block_h
            idx += 1
            # 채워야 할 블록 수는 분자 비율에 따라 좌에서 우로 채움
            filled = col < numerator
            fill = "url(#chocoGrad)" if filled else empty_color
            data_index = col + row * denominator
            filled_flag = 1 if filled else 0
            svg_parts.append(f'<rect class="block" data-index="{data_index}" data-filled="{filled_flag}" x="{x}" y="{y}" width="{col_w - 6:.2f}" height="{block_h - 6:.2f}" rx="6" ry="6" fill="{fill}" stroke="{border_color}" stroke-width="1" />')

    svg_parts.append('</svg>')
    return "".join(svg_parts)


def render_svg(svg: str, height: int = 320):
    """안전하게 SVG를 렌더링합니다."""
    # st.markdown에 raw svg를 넣으면 안전 설정 때문에 보이지 않을 수 있어 컴포넌트를 사용합니다.
    st.components.v1.html(svg, height=height)


# --- 공통 UI helper ---

def fraction_inputs(prefix: str = "", initial_d: int = 4, initial_n: int = 1):
    col1, col2 = st.columns(2)
    with col1:
        d = st.number_input(f"{prefix}분모 (2~12)", min_value=2, max_value=12, value=initial_d, step=1, key=f"{prefix}d")
    # 분모에 따라 분자 최대값을 자동 제한
    with col2:
        n = st.number_input(f"{prefix}분자 (1~{d})", min_value=1, max_value=d, value=min(initial_n, d), step=1, key=f"{prefix}n")
    return d, n


# --- 모드: 탐색 모드 ---

def exploration_mode():
    st.header("탐색 모드: 분수를 만들어봐요! 🍰")
    shape = st.radio("모양을 골라요:", ("원(피자)", "사각형(초콜릿)"))
    d, n = fraction_inputs(prefix="")

    st.markdown(f"<div class='highlight fraction-note'>이 분수는 1/{d} 조각이 {n}개 모여서 만들어졌어요!</div>", unsafe_allow_html=True)

    svg = svg_pizza(d, n, dark_mode=dark_mode) if shape.startswith("원") else svg_chocolate(d, n, dark_mode=dark_mode)
    render_svg(svg)


# --- 모드: 비교 모드 ---

def compare_mode():
    st.header("비교 모드: 어느 쪽이 더 클까? 🤔")
    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader("왼쪽")
        d1, n1 = fraction_inputs(prefix="L_", initial_d=4, initial_n=1)
        shape1 = st.selectbox("왼쪽 모양", ("원(피자)", "사각형(초콜릿)"), key="shape1")
    with right_col:
        st.subheader("오른쪽")
        d2, n2 = fraction_inputs(prefix="R_", initial_d=6, initial_n=1)
        shape2 = st.selectbox("오른쪽 모양", ("원(피자)", "사각형(초콜릿)"), key="shape2")

    # 시각화
    colL, colR, colRsl = st.columns([1,1,0.5])
    with colL:
        st.markdown("**왼쪽 도형**")
        render_svg(svg_pizza(d1, n1, dark_mode=dark_mode) if shape1.startswith("원") else svg_chocolate(d1, n1, dark_mode=dark_mode))
        st.markdown(f"**{n1}/{d1}**")
    with colR:
        st.markdown("**오른쪽 도형**")
        render_svg(svg_pizza(d2, n2, dark_mode=dark_mode) if shape2.startswith("원") else svg_chocolate(d2, n2, dark_mode=dark_mode))
        st.markdown(f"**{n2}/{d2}**")

    # 비교
    val1 = n1 / d1
    val2 = n2 / d2
    if abs(val1 - val2) < 1e-9:
        res = "="
    elif val1 > val2:
        res = ">"
    else:
        res = "<"

    st.markdown(f"### 결과: 왼쪽 {res} 오른쪽")


# --- 모드: 퀴즈 모드 ---

def ensure_quiz_state():
    if "quiz" not in st.session_state:
        st.session_state.quiz = {}


def new_quiz():
    # ensure denominator is within allowed range (2~12)
    d = random.randint(2, 12)
    d = max(2, min(12, int(d)))
    n = random.randint(1, d)
    shape = random.choice(["원(피자)", "사각형(초콜릿)"])
    st.session_state.quiz = {"d": d, "n": n, "shape": shape, "tries": 0}
    # For student engagement, show different example numbers (distractors) in the input fields
    # pick a denominator different from the correct one
    possible_ds = [x for x in range(2, 13) if x != d]
    distractor_d = random.choice(possible_ds)
    # pick a numerator valid for distractor_d
    distractor_n = random.randint(1, distractor_d)
    # ensure distractor pair is not accidentally the same as the answer
    if distractor_d == d and distractor_n == n:
        distractor_n = min(distractor_d, 1 if 1 != n else 2)
    st.session_state['quiz_d'] = distractor_d
    st.session_state['quiz_n'] = distractor_n


def quiz_mode():
    st.header("퀴즈 모드: 도전! 분수를 맞혀보세요 🎯")
    ensure_quiz_state()
    if st.button("새 문제 생성"):  # 새 문제 버튼
        new_quiz()

    if not st.session_state.quiz:
        new_quiz()

    q = st.session_state.quiz
    # safety: ensure quiz denominator never exceeds 12 (in case of unexpected mutation)
    if 'd' in q:
        q['d'] = max(2, min(12, int(q['d'])))
    if 'n' in q and 'd' in q:
        q['n'] = max(1, min(int(q['n']), int(q['d'])))
    st.session_state.quiz = q
    st.markdown("**도형을 보고 분모와 분자를 입력하세요.**")
    # 도형 제시
    svg = svg_pizza(q["d"], q["n"], dark_mode=dark_mode) if q["shape"].startswith("원") else svg_chocolate(q["d"], q["n"], dark_mode=dark_mode)
    render_svg(svg)

    col1, col2 = st.columns(2)
    with col1:
        # 기본값은 새 문제 생성 시 세션에 저장된 distractor 값을 사용합니다 (정답과 다르게 표시)
        default_d = st.session_state.get('quiz_d', q["d"])
        d_input = st.number_input("분모 (정수)", min_value=2, max_value=12, value=int(default_d), step=1, key="quiz_d")
    with col2:
        default_n = st.session_state.get('quiz_n', 1)
        # 분모에 따라 분자 최대값을 제한하고, 기본값은 distractor를 사용하되 분모보다 크지 않게
        n_input = st.number_input("분자 (정수)", min_value=1, max_value=d_input, value=min(int(default_n), d_input), step=1, key="quiz_n")

    if st.button("정답 제출"):
        # 안정성을 위해 정수로 변환하여 비교
        d_input = int(d_input)
        n_input = int(n_input)
        st.session_state.quiz["tries"] += 1
        tries = st.session_state.quiz["tries"]
        if d_input == int(q["d"]) and n_input == int(q["n"]):
            st.balloons()
            st.success("정답이에요! 🎉 잘했어요!")
            # Reveal answer only when 학생/선생님이 원할 때 확인할 수 있게 버튼을 제공합니다.
            if st.button("정답 보기"):
                st.markdown(f"**정답: {q['n']}/{q['d']}**")
                st.markdown(f"<div class='highlight fraction-note'>이 분수는 1/{q['d']} 조각이 {q['n']}개 모여서 만들어졌어요!</div>", unsafe_allow_html=True)
            # 문제 초기화(다음 문제를 원하면 '새 문제 생성' 버튼을 눌러주세요)
            st.session_state.quiz = {}
            # remove the input distractors so the next problem can set fresh distractors
            st.session_state.pop('quiz_d', None)
            st.session_state.pop('quiz_n', None)
        else:
            # show what the student submitted (non-revealing)
            st.info(f"입력: {n_input}/{d_input} — 도형을 다시 확인해보세요.")
            # 지능형 힌트 단계적 제공
            if tries == 1:
                st.info("힌트: 전체 조각(분모)을 먼저 세어봐요! 🎯")
            elif tries == 2:
                st.info("힌트: 색칠된 조각(분자)은 몇 개인지 세어보세요! ✋")
            else:
                st.warning("아직 틀렸어요. 다시 시도해보세요 — 필요한 경우 '새 문제 생성' 버튼으로 다음 문제로 넘어갈 수 있어요.")


# --- 모드: 웹 전용 체험 모드 (인터랙티브) ---

def interactive_mode():
    st.header("웹 체험 모드: 디지털 체험으로 직접 만져보세요! 🖐️")
    st.markdown("투명도 겹치기, 무한 쪼개기, 분수 저울, 남은 조각 반전 등 디지털 전용 체험을 해보세요. 도형을 드래그해서 겹쳐보세요.")

    dL, nL = fraction_inputs(prefix="IL_", initial_d=4, initial_n=1)
    shapeL = st.selectbox("왼쪽 모양", ("원(피자)", "사각형(초콜릿)"), key="I_shapeL")
    dR, nR = fraction_inputs(prefix="IR_", initial_d=6, initial_n=1)
    shapeR = st.selectbox("오른쪽 모양", ("원(피자)", "사각형(초콜릿)"), key="I_shapeR")

    left_svg = svg_pizza(dL, nL) if shapeL.startswith("원") else svg_chocolate(dL, nL)
    right_svg = svg_pizza(dR, nR) if shapeR.startswith("원") else svg_chocolate(dR, nR)

def interactive_mode():
    st.header("웹 체험 모드: 디지털 체험으로 직접 만져보세요! 🖐️")
    st.markdown("투명도 겹치기, 무한 쪼개기, 분수 저울, 남은 조각 반전 등 디지털 전용 체험을 해보세요. 도형을 드래그해서 겹쳐보세요.")

    dL, nL = fraction_inputs(prefix="IL_", initial_d=4, initial_n=1)
    shapeL = st.selectbox("왼쪽 모양", ("원(피자)", "사각형(초콜릿)"), key="I_shapeL")
    dR, nR = fraction_inputs(prefix="IR_", initial_d=6, initial_n=1)
    shapeR = st.selectbox("오른쪽 모양", ("원(피자)", "사각형(초콜릿)"), key="I_shapeR")

    left_svg = svg_pizza(dL, nL, dark_mode=dark_mode) if shapeL.startswith("원") else svg_chocolate(dL, nL, dark_mode=dark_mode)
    right_svg = svg_pizza(dR, nR, dark_mode=dark_mode) if shapeR.startswith("원") else svg_chocolate(dR, nR, dark_mode=dark_mode)

    opL = st.slider("왼쪽 투명도", 0.0, 1.0, 0.9, 0.05, key="I_opL")
    opR = st.slider("오른쪽 투명도", 0.0, 1.0, 0.6, 0.05, key="I_opR")

    # Build an interactive HTML area with JS to handle drag, split, invert, scale
    # 다크 모드 색상 정의
    if dark_mode:
        playground_bg = "#2a2a2a"
        stage_border = "#505050"
        control_btn_bg = "#5a5a5a"
        control_btn_text = "#e0e0e0"
        info_text = "#e0e0e0"
        scale_wrap_light = "linear-gradient(180deg, #3a3a3a 0%, #2a2a2a 100%)"
        scale_wrap_left_shadow = "0 6px 14px rgba(255,100,100,0.15)"
        scale_wrap_right_shadow = "0 6px 14px rgba(100,200,255,0.15)"
        scale_text_color = "#c0c0c0"
        scale_explain_color = "#a0a0a0"
        beam_color = "#a0a0a0"
        beam_light_color = "#ff8888"
        beam_dark_color = "#8888ff"
    else:
        playground_bg = "#FFF8F2"
        stage_border = "#F0D9C3"
        control_btn_bg = "#FFD699"
        control_btn_text = "#333"
        info_text = "#333"
        scale_wrap_light = "linear-gradient(180deg, #FFF6F6 0%, #FFF1F0 100%)"
        scale_wrap_left_shadow = "0 6px 14px rgba(255,170,160,0.15)"
        scale_wrap_right_shadow = "0 6px 14px rgba(160,210,255,0.15)"
        scale_text_color = "#5D4037"
        scale_explain_color = "#6B4F3F"
        beam_color = "#8E7A66"
        beam_light_color = "#FFB3A7"
        beam_dark_color = "#B3E5FF"

    html = (f"""
    <style>
    .playground {{ background:{playground_bg}; border-radius:12px; padding:12px; }}
    .stage {{ position:relative; width:100%; height:420px; border:2px dashed {stage_border}; border-radius:8px; overflow:hidden; }}
    .piece {{ position:absolute; cursor:grab; user-select:none; }}
    .controls {{ margin-top:8px; }}
    .control-btn {{ background:{control_btn_bg}; color:{control_btn_text}; border:none; padding:8px 12px; margin-right:8px; border-radius:8px; cursor:pointer; }}
    .info {{ margin-top:8px; font-weight:600; color:{info_text}; }}
    .scale-wrap {{ position:absolute; right:12px; top:8px; width:320px; height:200px; background:#fff; border-radius:8px; padding:8px; box-shadow:0 2px 6px rgba(0,0,0,0.08); transition: background 0.35s ease, box-shadow 0.35s ease; }}
    #beam {{ transition: transform 0.5s ease, fill 0.35s ease; }}
    .scale-wrap.left {{ background: {scale_wrap_light}; box-shadow:{scale_wrap_left_shadow}; }}
    .scale-wrap.right {{ background: {scale_wrap_light}; box-shadow:{scale_wrap_right_shadow}; }}
    </style> 

    <div class="playground">
      <div class="controls">
        <button id="resetBtn" class="control-btn">초기 위치로</button>
        <button id="splitBtn" class="control-btn">무한 쪼개기 ✨</button>
        <button id="undoSplitBtn" class="control-btn">쪼개기 되돌리기 ⤺</button>
        <button id="resetSplitBtn" class="control-btn">초기화(분할 초기값) ⤵</button>
        <button id="invertBtn" class="control-btn">남은 조각 보기 ↔</button>
      </div>
      <div id="stage" class="stage">
        <div id="leftPiece" class="piece" data-d="{dL}" data-n="{nL}" data-orig-d="{dL}" data-orig-n="{nL}" data-split-count="0" data-shape="{shapeL}" style="left:60px; top:40px; opacity:{opL}; z-index:3">{left_svg}</div>
        <div id="rightPiece" class="piece" data-d="{dR}" data-n="{nR}" data-orig-d="{dR}" data-orig-n="{nR}" data-split-count="0" data-shape="{shapeR}" style="left:220px; top:140px; opacity:{opR}; z-index:2">{right_svg}</div>
        <div class="scale-wrap" id="scaleWrap">
          <svg id="scaleSVG" viewBox="0 0 320 200" width="320" height="200" xmlns="http://www.w3.org/2000/svg">
            <line x1="160" y1="100" x2="160" y2="108" stroke="#3F2A20" stroke-width="6" />
            <rect id="beam" x="40" y="86" width="240" height="12" rx="6" fill="{beam_color}" transform-origin="160px 94px" />
            <circle cx="160" cy="108" r="8" fill="#3F2A20" />
            <text id="scaleText" x="160" y="28" fill="{scale_text_color}" font-size="14" text-anchor="middle" font-weight="700">분수 저울</text>
          </svg>
          <div id="scaleValues" style="text-align:center; font-size:13px; color:{scale_text_color}; margin-top:6px;"></div>
          <div id="scaleExplain" style="font-size:12px; color:{scale_explain_color}; margin-top:6px;">저울은 색칠된 부분(분수)이 큰 쪽으로 기울어요 — 빔이 거의 수평이면 두 분수가 거의 같아요.</div>
        </div> 
      </div>
      <div class="info">남은 조각: <span id="remaining">-</span></div>
    </div>

    <script>
    (function(){{
      // helpers
      function $(s, root=document){{return root.querySelector(s)}}
      function $all(s, root=document){{return Array.from(root.querySelectorAll(s))}}

      const left = $('#leftPiece');
      const right = $('#rightPiece');
      const stage = $('#stage');
      const remaining = $('#remaining');
      const beamLightColor = '{beam_light_color}';
      const beamDarkColor = '{beam_dark_color}';

      // make elements draggable
      function makeDraggable(el){{
        let isDown=false, startX=0, startY=0, origX=0, origY=0;
        el.addEventListener('pointerdown', (e)=>{{
          isDown=true; el.setPointerCapture(e.pointerId);
          startX = e.clientX; startY = e.clientY;
          const rect = el.getBoundingClientRect();
          const srect = stage.getBoundingClientRect();
          origX = rect.left - srect.left; origY = rect.top - srect.top;
          el.style.cursor='grabbing';
          el.style.zIndex = 999;
        }});
        window.addEventListener('pointermove', (e)=>{{
          if(!isDown) return;
          const srect = stage.getBoundingClientRect();
          let nx = origX + (e.clientX - startX);
          let ny = origY + (e.clientY - startY);
          nx = Math.max(0, Math.min(srect.width - el.offsetWidth, nx));
          ny = Math.max(0, Math.min(srect.height - el.offsetHeight, ny));
          el.style.left = nx + 'px';
          el.style.top = ny + 'px';
        }});
        window.addEventListener('pointerup', ()=>{{ if(isDown){{ isDown=false; el.style.cursor='grab'; el.style.zIndex=''; }}}});
      }}
      makeDraggable(left); makeDraggable(right);

      // reset position
      $('#resetBtn').addEventListener('click', ()=>{{
        left.style.left='60px'; left.style.top='40px'; left.style.zIndex=3;
        right.style.left='220px'; right.style.top='140px'; right.style.zIndex=2;
      }});

      // compute remaining and update scale
      function updateStatus(){{
        const dL = parseInt(left.dataset.d,10); const nL = parseInt(left.dataset.n,10);
        const dR = parseInt(right.dataset.d,10); const nR = parseInt(right.dataset.n,10);
        remaining.innerText = (dL - nL) + '/' + dL + ' , ' + (dR - nR) + '/' + dR;
        const valL = nL / dL; const valR = nR / dR;
        // show numeric values for clarity
        const sv = $('#scaleValues'); if(sv) sv.innerText = '왼쪽: ' + nL + '/' + dL + ' = ' + (valL*100).toFixed(1) + '%  ·  오른쪽: ' + nR + '/' + dR + ' = ' + (valR*100).toFixed(1) + '%';
        // angle calculation with slightly higher sensitivity for clarity
        const baseAngle = (valR - valL) * 50;
        const angle = Math.max(-40, Math.min(40, baseAngle));
        const beam = $('#beam');
        beam.style.transform = 'rotate(' + angle + 'deg)';
        // color / highlight based on which side is heavier
        const wrap = $('#scaleWrap');
        const explain = $('#scaleExplain');
        if(Math.abs(valL - valR) < 1e-9){{
          beam.style.fill = '{beam_color}';
          if(wrap){{ wrap.classList.remove('left'); wrap.classList.remove('right'); }}
          if(explain) explain.innerText = '두 분수는 거의 같습니다! 빔이 수평이에요.';
        }} else if(valL > valR){{
          beam.style.fill = beamLightColor;
          if(wrap){{ wrap.classList.add('left'); wrap.classList.remove('right'); }}
          if(explain) explain.innerText = '왼쪽이 더 큽니다 — 저울이 왼쪽으로 기울어요.';
        }} else {{
          beam.style.fill = beamDarkColor;
          if(wrap){{ wrap.classList.add('right'); wrap.classList.remove('left'); }}
          if(explain) explain.innerText = '오른쪽이 더 큽니다 — 저울이 오른쪽으로 기울어요.';
        }}
      }}
      updateStatus();

      // infinite split: doubles visible cut-lines (keeps fills)
      $('#splitBtn').addEventListener('click', ()=>{{
        [$all('.piece')].forEach(()=>{{}}); // no-op to silence linter
        [$('#leftPiece'), $('#rightPiece')].forEach(piece=>{{
          const svg = piece.querySelector('svg');
          if(!svg) return;
          // initialize origD if not present
          const origD = parseInt(piece.dataset.origD || piece.dataset.d,10);
          let splitCount = parseInt(piece.dataset.splitCount || '0',10);
          splitCount += 1; piece.dataset.splitCount = splitCount;
          const newD = origD * Math.pow(2, splitCount);
          piece.dataset.d = newD;

          // remove old overlay if present
          const prev = svg.querySelector('.split-lines'); if(prev) prev.remove();
          const g = document.createElementNS('http://www.w3.org/2000/svg','g'); g.setAttribute('class','split-lines');

          if(piece.dataset.shape.startsWith('원')){{
            // pizza: add lines by new denominator
            const w = svg.viewBox.baseVal.width; const h = svg.viewBox.baseVal.height;
            const cx = w/2, cy = h/2; const r = Math.min(w,h)/2 - 6;
            for(let i=0;i<newD;i++){{
              const ang = (2*Math.PI/newD)*i - Math.PI/2;
              const x2 = cx + r*Math.cos(ang);
              const y2 = cy + r*Math.sin(ang);
              const line = document.createElementNS('http://www.w3.org/2000/svg','line');
              line.setAttribute('x1',cx); line.setAttribute('y1',cy); line.setAttribute('x2',x2); line.setAttribute('y2',y2);
              line.setAttribute('stroke','#BDBDBD'); line.setAttribute('stroke-width','0.8'); line.setAttribute('stroke-opacity','0');
              g.appendChild(line);
            }}
          }} else {{
            // chocolate: add midlines
            const w = svg.viewBox.baseVal.width; const h = svg.viewBox.baseVal.height;
            const innerW = w - 20; // approximate inner area
            for(let i=1;i<newD;i++){{
              const x = 8 + (i)*(innerW/newD);
              const line = document.createElementNS('http://www.w3.org/2000/svg','line');
              line.setAttribute('x1',x); line.setAttribute('y1',8); line.setAttribute('x2',x); line.setAttribute('y2',h-8);
              line.setAttribute('stroke','#BDBDBD'); line.setAttribute('stroke-width','0.8'); line.setAttribute('stroke-opacity','0');
              g.appendChild(line);
            }}
          }}
          svg.appendChild(g);
          // animate lines in
          const lines = g.querySelectorAll('line');
          lines.forEach((ln,idx)=> setTimeout(()=> ln.setAttribute('stroke-opacity','1'), idx*8));
        }});
        updateStatus();
      }});

      // undo split (한 단계 되돌리기)
      $('#undoSplitBtn').addEventListener('click', ()=>{{
        [$('#leftPiece'), $('#rightPiece')].forEach(piece=>{{
          const svg = piece.querySelector('svg'); if(!svg) return;
          let splitCount = parseInt(piece.dataset.splitCount || '0',10);
          const origD = parseInt(piece.dataset.origD || piece.dataset.d,10);
          if(splitCount > 0){{
            splitCount -= 1; piece.dataset.splitCount = splitCount;
            const newD = origD * Math.pow(2, splitCount);
            piece.dataset.d = newD;
            const prev = svg.querySelector('.split-lines'); if(prev) prev.remove();
            if(splitCount > 0){{
              const g = document.createElementNS('http://www.w3.org/2000/svg','g'); g.setAttribute('class','split-lines');
              if(piece.dataset.shape.startsWith('원')){{
                const w = svg.viewBox.baseVal.width; const h = svg.viewBox.baseVal.height; const cx = w/2, cy = h/2; const r = Math.min(w,h)/2 - 6;
                for(let i=0;i<newD;i++){{ const ang = (2*Math.PI/newD)*i - Math.PI/2; const x2 = cx + r*Math.cos(ang); const y2 = cy + r*Math.sin(ang); const line = document.createElementNS('http://www.w3.org/2000/svg','line'); line.setAttribute('x1',cx); line.setAttribute('y1',cy); line.setAttribute('x2',x2); line.setAttribute('y2',y2); line.setAttribute('stroke','#BDBDBD'); line.setAttribute('stroke-width','0.8'); line.setAttribute('stroke-opacity','0'); g.appendChild(line); }}
              }} else {{
                const w = svg.viewBox.baseVal.width; const h = svg.viewBox.baseVal.height; const innerW = w - 20; for(let i=1;i<newD;i++){{ const x = 8 + (i)*(innerW/newD); const line = document.createElementNS('http://www.w3.org/2000/svg','line'); line.setAttribute('x1',x); line.setAttribute('y1',8); line.setAttribute('x2',x); line.setAttribute('y2',h-8); line.setAttribute('stroke','#BDBDBD'); line.setAttribute('stroke-width','0.8'); line.setAttribute('stroke-opacity','0'); g.appendChild(line); }}
              }}
              svg.appendChild(g);
              const lines = g.querySelectorAll('line'); lines.forEach((ln,idx)=> setTimeout(()=> ln.setAttribute('stroke-opacity','1'), idx*6));
            }}
          }}
        }});
        updateStatus();
      }});

      // reset split to original denominator
      $('#resetSplitBtn').addEventListener('click', ()=>{{
        [$('#leftPiece'), $('#rightPiece')].forEach(piece=>{{
          const svg = piece.querySelector('svg'); if(!svg) return;
          const origD = parseInt(piece.dataset.origD || piece.dataset.d,10);
          piece.dataset.splitCount = 0;
          piece.dataset.d = origD;
          const prev = svg.querySelector('.split-lines'); if(prev) prev.remove();
        }});
        updateStatus();
      }});

      // invert remaining: swap filled/unfilled on slices/blocks
      let inverted = false;
      $('#invertBtn').addEventListener('click', ()=>{{
        inverted = !inverted;
        [$('#leftPiece'), $('#rightPiece')].forEach(piece=>{{
          const svg = piece.querySelector('svg'); if(!svg) return;
          if(piece.dataset.shape.startsWith('원')){{
            const slices = svg.querySelectorAll('.slice');
            slices.forEach(s=>{{
              const filled = s.getAttribute('data-filled') === '1';
              if(!inverted){{ // restore original
                if(filled){{ s.setAttribute('fill','url(#cheeseGrad)'); s.setAttribute('data-filled','1'); }}
                else {{ s.setAttribute('fill','#FFF5E6'); s.setAttribute('data-filled','0'); }}
              }} else {{
                if(filled){{ s.setAttribute('fill','#FFF5E6'); s.setAttribute('data-filled','0'); }}
                else {{ s.setAttribute('fill','url(#cheeseGrad)'); s.setAttribute('data-filled','1'); }}
              }}
            }});
          }} else {{
            const blocks = svg.querySelectorAll('.block');
            blocks.forEach(b=>{{
              const filled = b.getAttribute('data-filled') === '1';
              if(!inverted){{ if(filled){{ b.setAttribute('fill','url(#chocoGrad)'); b.setAttribute('data-filled','1'); }} else {{ b.setAttribute('fill','#EDE0D6'); b.setAttribute('data-filled','0'); }}}}
              else {{ if(filled){{ b.setAttribute('fill','#EDE0D6'); b.setAttribute('data-filled','0'); }} else {{ b.setAttribute('fill','url(#chocoGrad)'); b.setAttribute('data-filled','1'); }}}}
            }});
          }}
        }});
        updateStatus();
      }});

    }})();
    </script>
    """)

    st.components.v1.html(html, height=680)

# --- 사이드바 및 모드 선택 ---
mode = st.sidebar.selectbox("모드 선택", ("탐색 모드", "비교 모드", "퀴즈 모드", "웹 체험 모드"))

if mode == "탐색 모드":
    exploration_mode()
elif mode == "비교 모드":
    compare_mode()
elif mode == "퀴즈 모드":
    quiz_mode()
else:
    interactive_mode()


