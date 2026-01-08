# ...existing code...
import streamlit as st
import random

st.title("💡 2진수를 10진수로 변환하는 앱")

# =========================
# 문제 식별자 (위젯 key 분리용)
# =========================
if 'problem_id' not in st.session_state:
    st.session_state.problem_id = 0
pid = st.session_state.problem_id

# 1. 1~10비트 길이의 랜덤 2진수 생성 (1이 최소 하나 포함되도록)
if 'bit_len' not in st.session_state:
    st.session_state.bit_len = random.randint(1, 10)

if 'binary' not in st.session_state:
    while True:
        bits = [random.choice([0, 1]) for _ in range(st.session_state.bit_len)]
        if bits.count(1) >= 1:  # 1이 한 개 이상 포함되어 있으면 OK
            st.session_state.binary = bits
            break

bit_len = st.session_state.bit_len
binary = st.session_state.binary

# 2진수 표시 (MSB ~ LSB)
bin_str = ''.join(str(b) for b in binary)
st.write(
    f"랜덤 2진수: <span style='font-size:1.5em; letter-spacing:0.2em'><b>{bin_str}</b></span>",
    unsafe_allow_html=True
)

# 각 비트별로 입력 칸 생성 (MSB~LSB)
st.write("각 비트 아래 칸에 1로 표현된 자리의 가중치를 입력하세요. (해당 비트가 1일 때는 숫자, 0일 때는 0 또는 빈칸)")
cols = st.columns(bit_len)

# user_weights 초기화
if 'user_weights' not in st.session_state or len(st.session_state.user_weights) != bit_len:
    st.session_state.user_weights = [''] * bit_len

for i, col in enumerate(cols):
    with col:
        # 비트값 가운데 정렬
        st.markdown(
            f"<div style='text-align:center; font-weight:bold'>{binary[i]}</div>",
            unsafe_allow_html=True
        )
        # 입력 칸 가운데 정렬 스타일
        st.markdown("""
        <style>
        .stTextInput>div>div>input {
            text-align: center !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # 각 입력은 problem_id를 포함한 고유 key로 관리
        st.session_state.user_weights[i] = st.text_input(
            label=" ",
            value=st.session_state.user_weights[i],
            key=f"weight_input_{pid}_{i}",     # ★ pid 포함
            placeholder=""
        )

# 정답 가중치 계산 함수 (LSB에 2^0)
def get_weights(bits):
    return [2**i for i, b in enumerate(reversed(bits)) if b == 1]

answer_weights = get_weights(binary)
decimal_value = sum(answer_weights)

# 가중치 확인 버튼
if st.button("정답 확인", key=f"check_weights_btn_{pid}"):
    try:
        user_weights = [
            int(st.session_state.user_weights[i])
            for i in range(bit_len)
            if binary[i] == 1 and st.session_state.user_weights[i].strip() != ""
        ]
        if sorted(user_weights) == sorted(answer_weights):
            st.success("정답입니다! 이제 각 가중치의 합을 계산해보세요.")
            st.session_state.show_calc = True
        else:
            st.error(f"틀렸습니다. 정답 가중치: {answer_weights}")
            st.session_state.show_calc = False
    except Exception:
        st.error("입력 형식이 올바르지 않습니다. 숫자만 입력하세요.")

# 항상 10진수 입력 칸과 최종 확인 버튼을 표시
st.markdown("<span style='font-size:1.1em'>각 가중치를 더해 10진수 값을 입력하세요!</span>", unsafe_allow_html=True)

# number_input에 problem_id를 포함한 key 사용
if 'user_decimal' not in st.session_state:
    st.session_state.user_decimal = 0

st.session_state.user_decimal = st.number_input(
    "10진수 값 입력",
    min_value=0, step=1,
    value=st.session_state.user_decimal,
    key=f"user_decimal_input_{pid}"         # ★ pid 포함
)

if st.button("최종 정답 확인", key=f"final_check_btn_{pid}"):
    if st.session_state.user_decimal == decimal_value:
        st.success(f"정답! 2진수 {bin_str}의 10진수 값은 {decimal_value}입니다.")
    else:
        st.error(f"틀렸습니다. 정답은 {decimal_value}입니다.")

# =========================
# 새 문제 버튼: 문제 ID 증가
# =========================
if st.button("새 문제", key=f"new_problem_btn_{pid}"):
    # 다음 문제용 최소 상태만 reset
    st.session_state.problem_id += 1          # ★ 새로운 문제 id
    for k in ['bit_len', 'binary', 'show_calc', 'user_weights', 'user_decimal']:
        st.session_state.pop(k, None)
    st.rerun()
# ...existing code...