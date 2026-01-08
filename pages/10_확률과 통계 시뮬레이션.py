import streamlit as st
import random
import itertools
from collections import Counter
import math

# --- 페이지 설정 ---
st.set_page_config(
    page_title="확률 마스터: 시뮬레이션 학습 앱",
    layout="wide"
)

st.title("확률 마스터: 시뮬레이션으로 배우는 확률과 통계")
st.markdown("학생들이 어려워하는 **조건부 확률, 독립/종속 사건, 순열** 개념을 시뮬레이션을 통해 직관적으로 이해해 보세요.")

# --- 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["1. 조건부 확률 (베이즈)", "2. 독립 vs 종속 사건", "3. 순열 (순서가 있는 경우)"])


# =================================================================
# 1. 조건부 확률 (베이즈 정리) 시뮬레이션
# =================================================================
def simulate_bayes(config, num_trials):
    """조건부 확률 시뮬레이션 실행"""
    
    # 설정값 추출
    a_red = config['a_red']
    a_blue = config['a_blue']
    b_red = config['b_red']
    b_blue = config['b_blue']
    
    # 전체 공 개수
    total_a = a_red + a_blue
    total_b = b_red + b_blue
    
    # 결과 카운터
    red_count = 0        # 전체 빨간 공 나온 횟수 (사건 B)
    red_from_a_count = 0 # A 주머니에서 빨간 공 나온 횟수 (사건 A ∩ B)

    for _ in range(num_trials):
        # 1단계: 주머니 선택 (동전 던지기, A 또는 B 선택 확률 1/2)
        selected_pouch = random.choice(['A', 'B'])
        
        # 2단계: 공 뽑기
        pouch_config = []
        if selected_pouch == 'A':
            pouch_config = ['Red'] * a_red + ['Blue'] * a_blue
        else: # 'B'
            pouch_config = ['Red'] * b_red + ['Blue'] * b_blue
            
        if not pouch_config: # 빈 주머니 방지
            continue
            
        drawn_ball = random.choice(pouch_config)
        
        # 3단계: 결과 기록
        if drawn_ball == 'Red':
            red_count += 1
            if selected_pouch == 'A':
                red_from_a_count += 1
                
    # 실험적 조건부 확률 계산
    experimental_prob = red_from_a_count / red_count if red_count > 0 else 0
    
    return red_count, red_from_a_count, experimental_prob

def calculate_theoretical_bayes(config):
    """베이즈 정리 공식으로 이론적 확률 계산"""
    a_red = config['a_red']
    a_blue = config['a_blue']
    b_red = config['b_red']
    b_blue = config['b_blue']
    
    total_a = a_red + a_blue
    total_b = b_red + b_blue
    
    if total_a == 0 or total_b == 0:
        return 0, 0, 0
    
    # P(A): A 주머니 선택 확률 = 0.5
    p_a = 0.5
    # P(B): 빨간 공이 나올 확률 = P(B|A)P(A) + P(B|B')P(B')
    p_red_if_a = a_red / total_a
    p_red_if_b = b_red / total_b
    
    p_b = p_red_if_a * 0.5 + p_red_if_b * 0.5
    
    # P(A ∩ B): A 주머니 선택하고 빨간 공 나올 확률 = P(B|A)P(A)
    p_a_and_red = p_red_if_a * p_a
    
    # P(A | B): 빨간 공이 나왔을 때 A 주머니에서 나왔을 확률 = P(A ∩ B) / P(B)
    theoretical_prob = p_a_and_red / p_b if p_b > 0 else 0
    
    return p_a_and_red, p_b, theoretical_prob

with tab1:
    st.header("1. 조건부 확률 이해하기: '두 개의 주머니' 게임")
    st.markdown("문제: **뽑은 공이 빨간색이었을 때, 그 공이 A 주머니에서 나왔을 확률**($P(A|R)$)은 얼마일까요? (주머니 선택 확률은 각각 50%입니다)")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("주머니 A 설정")
        a_red = st.number_input("A 주머니 빨간 공 개수", min_value=0, value=3, key='ar')
        a_blue = st.number_input("A 주머니 파란 공 개수", min_value=0, value=7, key='ab')
        st.subheader("주머니 B 설정")
        b_red = st.number_input("B 주머니 빨간 공 개수", min_value=0, value=8, key='br')
        b_blue = st.number_input("B 주머니 파란 공 개수", min_value=0, value=2, key='bb')

    with col2:
        num_trials = st.slider("시뮬레이션 반복 횟수", min_value=100, max_value=10000, value=5000, step=100)
        
        config = {'a_red': a_red, 'a_blue': a_blue, 'b_red': b_red, 'b_blue': b_blue}
        
        # 이론값 계산
        p_a_and_red, p_b, theoretical_prob = calculate_theoretical_bayes(config)
        st.subheader("💡 이론적 확률 (베이즈 정리)")
        st.latex(r"P(A|R) = \frac{P(R|A)P(A)}{P(R)}")
        st.markdown(f"**이론값 $P(A|R)$:** `{theoretical_prob:.4f}`")
        st.caption(f"$P(R|A)P(A)$ (분자) = {p_a_and_red:.4f} / $P(R)$ (분모) = {p_b:.4f}")

        if st.button("시뮬레이션 시작 (조건부 확률)"):
            red_count, red_from_a_count, experimental_prob = simulate_bayes(config, num_trials)
            
            st.subheader("🧪 시뮬레이션 결과")
            st.metric("총 반복 횟수", num_trials)
            st.metric("빨간 공이 나온 총 횟수 (P(R))", red_count)
            st.metric("A에서 빨간 공 나온 횟수 (P(A∩R))", red_from_a_count)
            
            st.success(f"**실험적 조건부 확률 $P(A|R)$:** `{experimental_prob:.4f}`")
            st.caption(f"계산: {red_from_a_count} / {red_count}")
            st.markdown("---")
            st.markdown("시뮬레이션 횟수를 늘릴수록 실험값은 **이론값**에 수렴합니다.")


# =================================================================
# 2. 독립 vs 종속 사건 시뮬레이션
# =================================================================
def simulate_extraction(config, num_trials, is_replacement):
    """복원/비복원 추출 시뮬레이션 실행"""
    initial_red = config['red']
    initial_blue = config['blue']
    
    # 2번 뽑을 때 모두 빨간 공일 확률을 계산
    red_red_count = 0
    
    for _ in range(num_trials):
        pouch = ['Red'] * initial_red + ['Blue'] * initial_blue
        
        if len(pouch) < 2: # 최소 2개 필요
            continue
            
        # 1차 추출
        ball1 = random.choice(pouch)
        
        # 공 재구성 (복원 또는 비복원)
        if not is_replacement: # 비복원 추출 (종속 사건)
            pouch.remove(ball1) # 뽑은 공 제거
            if not pouch: # 두 번째 뽑을 공이 없으면
                 continue
        
        # 2차 추출
        ball2 = random.choice(pouch)
        
        if ball1 == 'Red' and ball2 == 'Red':
            red_red_count += 1
            
    experimental_prob = red_red_count / num_trials if num_trials > 0 else 0
    return red_red_count, experimental_prob

def calculate_theoretical_extraction(config, is_replacement):
    """복원/비복원 추출 이론적 확률 계산"""
    r, b = config['red'], config['blue']
    total = r + b
    
    if total < 2:
        return 0
    
    if is_replacement: # 복원 추출 (독립 사건)
        # P(R1) * P(R2) = (r / total) * (r / total)
        prob = (r / total) * (r / total)
        formula = r"\left(\frac{R}{R+B}\right) \times \left(\frac{R}{R+B}\right)"
    else: # 비복원 추출 (종속 사건)
        # P(R1) * P(R2|R1) = (r / total) * ((r-1) / (total-1))
        if r < 1: return 0
        prob = (r / total) * ((r - 1) / (total - 1))
        formula = r"\frac{R}{R+B} \times \frac{R-1}{R+B-1}"

    return prob, formula


with tab2:
    st.header("2. 독립 사건 vs 종속 사건: '공 다시 넣기' 옵션")
    st.markdown("문제: **공을 연속으로 두 번 뽑을 때, 모두 빨간색일 확률**($P(R_1 \cap R_2)$)은 얼마일까요?")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("공 주머니 설정")
        r = st.number_input("빨간 공 개수 (R)", min_value=1, value=4, key='r')
        b = st.number_input("파란 공 개수 (B)", min_value=1, value=6, key='b')
        is_replacement = st.checkbox("✅ 뽑은 공을 다시 넣기 (복원 추출 / 독립 사건)", value=True, key='is_rep')

    with col2:
        num_trials_ext = st.slider("시뮬레이션 반복 횟수", min_value=100, max_value=10000, value=5000, step=100, key='trials_ext')
        
        config_ext = {'red': r, 'blue': b}
        
        # 이론값 계산
        theoretical_prob_ext, formula_ext = calculate_theoretical_extraction(config_ext, is_replacement)
        
        st.subheader(f"💡 이론적 확률 ({'독립 사건' if is_replacement else '종속 사건'})")
        st.latex(formula_ext)
        st.markdown(f"**이론값 $P(R_1 \cap R_2)$:** `{theoretical_prob_ext:.4f}`")

        if st.button("시뮬레이션 시작 (독립/종속)"):
            red_red_count, experimental_prob_ext = simulate_extraction(config_ext, num_trials_ext, is_replacement)
            
            st.subheader("🧪 시뮬레이션 결과")
            st.metric("총 반복 횟수", num_trials_ext)
            st.metric("두 번 모두 빨간 공 나온 횟수", red_red_count)
            
            st.success(f"**실험적 확률 $P(R_1 \cap R_2)$:** `{experimental_prob_ext:.4f}`")
            st.caption(f"계산: {red_red_count} / {num_trials_ext}")
            st.markdown("---")
            st.markdown("옵션 변경 시 **공식과 이론값**이 어떻게 바뀌는지 비교해 보세요.")

# =================================================================
# 3. 순열 시뮬레이션
# =================================================================
def simulate_permutation(n, r, num_trials):
    """순열 시뮬레이션 실행"""
    
    cards = list(range(1, n + 1))
    
    # 짝수 순열 개수 카운터
    even_perm_count = 0
    
    for _ in range(num_trials):
        # r개의 카드를 무작위로 뽑아 순서대로 나열
        permutation = random.sample(cards, r)
        
        if not permutation:
            continue
            
        # '세 자리 자연수' 문제처럼, 마지막 숫자가 짝수인지 확인 (짝수 조건)
        if permutation[-1] % 2 == 0:
            even_perm_count += 1
            
    experimental_prob = even_perm_count / num_trials if num_trials > 0 else 0
    return even_perm_count, experimental_prob

def calculate_theoretical_permutation(n, r):
    """순열 이론적 확률 계산 (마지막 숫자가 짝수일 확률)"""
    if n < r:
        return 0, 0
    
    # 전체 순열의 수: nPr = n! / (n-r)!
    nPr_total = math.factorial(n) / math.factorial(n - r)
    
    # 특정 조건(마지막 자리가 짝수)을 만족하는 순열의 수
    
    # 1. 짝수 카드의 개수: E
    even_cards = [i for i in range(1, n + 1) if i % 2 == 0]
    num_even_cards = len(even_cards)
    
    # 2. 마지막 자리를 짝수(E)로 고정하는 경우의 수: num_even_cards
    # 3. 나머지 (r-1)자리를 나머지 (n-1)개의 카드 중에서 순열로 채우는 경우의 수: (n-1)P(r-1)
    if num_even_cards == 0 or r == 0:
        nPr_even = 0
    else:
        # 나머지 (n-1)개 중 (r-1)개를 순서대로 나열
        if n - 1 < r - 1: # 순열 불가능
            nPr_even = 0
        else:
            nPr_remaining = math.factorial(n - 1) / math.factorial((n - 1) - (r - 1))
            nPr_even = num_even_cards * nPr_remaining
            
    theoretical_prob = nPr_even / nPr_total if nPr_total > 0 else 0
    
    return nPr_total, nPr_even, theoretical_prob

with tab3:
    st.header("3. 순열 이해하기: '카드 순서대로 나열하기' 게임")
    st.markdown("문제: **1부터 N까지 카드 중 R장을 뽑아 나열했을 때, 만들어진 R자리 숫자가 짝수일 확률**은 얼마일까요? (즉, 마지막 숫자가 짝수일 확률)")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("카드 설정")
        n_cards = st.number_input("전체 카드 개수 (N, 1부터)", min_value=1, value=5, key='n_c')
        r_draw = st.number_input("뽑을 카드 개수 (R)", min_value=1, max_value=n_cards, value=3, key='r_d')
        st.caption(f"문제 상황: {n_cards}장의 카드 중 {r_draw}장을 뽑아 {r_draw}자리 숫자를 만듭니다.")

    with col2:
        num_trials_perm = st.slider("시뮬레이션 반복 횟수", min_value=100, max_value=10000, value=5000, step=100, key='trials_perm')
        
        # 이론값 계산
        nPr_total, nPr_even, theoretical_prob_perm = calculate_theoretical_permutation(n_cards, r_draw)
        
        st.subheader("💡 이론적 확률 (순열)")
        st.latex(r"P(\text{Event}) = \frac{\text{특정 조건을 만족하는 순열의 수}}{\text{전체 순열의 수} \ (^nP_r)}")
        st.markdown(f"**전체 순열 $P_r$:** `{int(nPr_total)}`")
        st.markdown(f"**짝수인 순열:** `{int(nPr_even)}`")
        st.markdown(f"**이론값 $P(짝수)$:** `{theoretical_prob_perm:.4f}`")

        if st.button("시뮬레이션 시작 (순열)"):
            even_perm_count, experimental_prob_perm = simulate_permutation(n_cards, r_draw, num_trials_perm)
            
            st.subheader("🧪 시뮬레이션 결과")
            st.metric("총 반복 횟수", num_trials_perm)
            st.metric("짝수 순열이 나온 횟수", even_perm_count)
            
            st.success(f"**실험적 확률 $P(짝수)$:** `{experimental_prob_perm:.4f}`")
            st.caption(f"계산: {even_perm_count} / {num_trials_perm}")
            st.markdown("---")
            st.markdown("**팁:** 뽑을 카드 개수(R)를 늘리거나 줄여보며 전체 경우의 수가 어떻게 변하는지 확인해 보세요.")