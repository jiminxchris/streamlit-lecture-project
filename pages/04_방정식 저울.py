
import streamlit as st
import re

# --------------------------------------------------------------------------
# 페이지 기본 설정
# --------------------------------------------------------------------------
import streamlit as st
import re

# --------------------------------------------------------------------------
# 페이지 기본 설정
# --------------------------------------------------------------------------
st.set_page_config(page_title="방정식 저울", page_icon="⚖️")

st.title("⚖️ 인터랙티브 방정식 저울")
st.write("""
일차방정식을 입력하고, '등식의 성질'을 이용해 저울의 균형을 맞추며 문제를 풀어보세요.
최종 목표는 저울의 한쪽에 **'x' 상자 하나**만 남기는 것입니다!
""")

# --------------------------------------------------------------------------
# 핵심 기능: 세션 상태(Session State) 초기화
# --------------------------------------------------------------------------
if 'parts' not in st.session_state:
    st.session_state.parts = {
        'lhs_x': 0, 'lhs_c': 0, 'rhs_x': 0, 'rhs_c': 0
    }

# --------------------------------------------------------------------------
# 도우미 함수 (Helper Functions)
# --------------------------------------------------------------------------

def parse_term(term_str):
    term_str = term_str.strip()
    if not term_str: return 0, None
    if 'x' in term_str:
        coeff_str = term_str.replace('x', '').strip()
        if coeff_str == '' or coeff_str == '+': return 1, 'x'
        elif coeff_str == '-': return -1, 'x'
        else: return int(coeff_str), 'x'
    else:
        return int(term_str), 'c'

def parse_side(side_str):
    side_str = side_str.replace('+', ' +').replace('-', ' -')
    terms = re.split(r'\s+', side_str)
    if terms[0] == '': terms = terms[1:]
    x_total, c_total = 0, 0
    current_term = ""
    for term in terms:
        if term in ['+', '-']:
            if current_term:
                coeff, var = parse_term(current_term)
                if var == 'x': x_total += coeff
                else: c_total += coeff
            current_term = term
        else:
            current_term += term
    if current_term:
        coeff, var = parse_term(current_term)
        if var == 'x': x_total += coeff
        else: c_total += coeff
    return x_total, c_total

def display_scale():
    parts = st.session_state.parts
    st.markdown("---")
    left_col, right_col = st.columns(2)

    # 항상 int()로 변환하여 오류 원천 방지
    lhs_x_val, lhs_c_val = parts.get('lhs_x', 0), parts.get('lhs_c', 0)
    rhs_x_val, rhs_c_val = parts.get('rhs_x', 0), parts.get('rhs_c', 0)

    with left_col:
        st.subheader("왼쪽")
        st.latex(f"{lhs_x_val}x + {lhs_c_val}")
        x_display = '📦' * int(lhs_x_val) if lhs_x_val > 0 and float(lhs_x_val).is_integer() else ''
        c_display = '⚪' * int(lhs_c_val) if lhs_c_val > 0 and float(lhs_c_val).is_integer() else ''
        st.markdown(f"<p style='font-size: 24px; letter-spacing: 4px;'>{x_display} {c_display}</p>", unsafe_allow_html=True)

    with right_col:
        st.subheader("오른쪽")
        st.latex(f"{rhs_x_val}x + {rhs_c_val}")
        x_display = '📦' * int(rhs_x_val) if rhs_x_val > 0 and float(rhs_x_val).is_integer() else ''
        c_display = '⚪' * int(rhs_c_val) if rhs_c_val > 0 and float(rhs_c_val).is_integer() else ''
        st.markdown(f"<p style='font-size: 24px; letter-spacing: 4px;'>{x_display} {c_display}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if (lhs_x_val == 1 and rhs_x_val == 0 and lhs_c_val == 0) or \
       (rhs_x_val == 1 and lhs_x_val == 0 and rhs_c_val == 0):
        st.balloons()
        st.success(f"정답을 찾았습니다! x = {rhs_c_val if lhs_x_val == 1 else lhs_c_val}")

# --------------------------------------------------------------------------
# 사용자 인터페이스 (UI) 부분
# --------------------------------------------------------------------------

st.subheader("1. 방정식 설정하기")
equation_str = st.text_input("일차방정식을 입력하세요:", "2x + 3 = 9")

if st.button("저울에 올리기"):
    try:
        lhs_str, rhs_str = equation_str.split('=')
        lhs_x, lhs_c = parse_side(lhs_str)
        rhs_x, rhs_c = parse_side(rhs_str)
        st.session_state.parts = {'lhs_x': lhs_x, 'lhs_c': lhs_c, 'rhs_x': rhs_x, 'rhs_c': rhs_c}
    except Exception as e:
        st.error(f"방정식 형식이 올바르지 않습니다. 'ax + b = cx + d' 형태로 입력해주세요. (오류: {e})")

if any(st.session_state.parts.values()):
    display_scale()
    st.subheader("2. 등식의 성질 적용하기")
    op_col1, op_col2 = st.columns([1, 2])
    with op_col1:
        operation = st.radio("연산 선택", ["상수 더하기/빼기", "x항 더하기/빼기", "양변 곱하기/나누기"])
    with op_col2:
        if operation == "상수 더하기/빼기":
            val = st.number_input("상수 값:", value=1, step=1)
            if st.button(f"양변에 상수 '{val}' 더하기"):
                st.session_state.parts['lhs_c'] += val
                st.session_state.parts['rhs_c'] += val
                st.rerun()
            if st.button(f"양변에서 상수 '{val}' 빼기"):
                st.session_state.parts['lhs_c'] -= val
                st.session_state.parts['rhs_c'] -= val
                st.rerun()
        elif operation == "x항 더하기/빼기":
            val = st.number_input("x의 계수:", value=1, step=1)
            if st.button(f"양변에 '{val}x' 더하기"):
                st.session_state.parts['lhs_x'] += val
                st.session_state.parts['rhs_x'] += val
                st.rerun()
            if st.button(f"양변에서 '{val}x' 빼기"):
                st.session_state.parts['lhs_x'] -= val
                st.session_state.parts['rhs_x'] -= val
                st.rerun()
        elif operation == "양변 곱하기/나누기":
            val = st.number_input("값:", value=2.0, step=0.1, min_value=0.0, format="%0.2f")
            if st.button(f"양변에 '{val}' 곱하기"):
                for k in st.session_state.parts:
                    st.session_state.parts[k] = float(st.session_state.parts[k]) * float(val)
                st.rerun()
            if st.button(f"양변을 '{val}'(으)로 나누기"):
                if val == 0:
                    st.warning("0으로 나눌 수 없습니다.")
                else:
                    for k in st.session_state.parts:
                        st.session_state.parts[k] = float(st.session_state.parts[k]) / float(val)
                    st.rerun()

if st.sidebar.button("처음부터 시작하기"):
    st.session_state.parts = {'lhs_x': 0, 'lhs_c': 0, 'rhs_x': 0, 'rhs_c': 0}
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("도움말")
st.sidebar.info(
    """
    - **📦 (상자):** 미지수 x
    - **⚪ (흰 구슬):** 양수(+) 1
    - **🔻 (역삼각형):** -x
    - **🔴 (붉은 구슬):** 음수(-) 1
    """
)