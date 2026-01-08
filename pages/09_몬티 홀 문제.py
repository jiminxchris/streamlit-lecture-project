import streamlit as st
import random
import pandas as pd

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="몬티 홀 문제 시뮬레이터",
    page_icon="🧠"
)

# --- 제목과 설명 ---
st.title("🧠 몬티 홀 문제 시뮬레이터")
st.markdown("""
세 개의 문 뒤에는 **자동차 🚗** 한 대와 **염소 🐐** 두 마리가 있습니다.
1.  당신이 문 하나를 선택합니다.
2.  정답을 아는 진행자가 남은 문 중에서 염소가 있는 문을 열어 보여줍니다.
3.  이제 당신에게 마지막 기회가 주어집니다. 처음 선택을 **유지**하시겠습니까, 아니면 남은 문으로 **바꾸**시겠습니까?

이 시뮬레이터는 수많은 게임을 대신 플레이하여 어떤 전략이 자동차를 얻을 확률이 더 높은지 보여줍니다!
""")

# --- 사용자 입력 (사이드바) ---
st.sidebar.header("🕹️ 게임 설정")
num_simulations = st.sidebar.number_input(
    label="시뮬레이션 횟수를 입력하세요",
    min_value=100,
    max_value=100000,
    value=1000, # 기본값
    step=100
)

# --- 시뮬레이션 함수 ---
def run_simulation(strategy_to_switch):
    wins = 0
    for _ in range(num_simulations):
        doors = [1, 2, 3]
        car_door = 1 # 자동차는 항상 1번에 있다고 가정
        player_choice = random.choice(doors)
        doors_to_open = [door for door in doors if door != car_door and door != player_choice]
        opened_door = random.choice(doors_to_open)
        if strategy_to_switch:
            final_choice = [door for door in doors if door != player_choice and door != opened_door][0]
        else:
            final_choice = player_choice
        if final_choice == car_door:
            wins += 1
    return wins

# --- 실행 버튼 ---
if st.button("🚀 시뮬레이션 시작!"):
    stay_wins = run_simulation(strategy_to_switch=False)
    switch_wins = run_simulation(strategy_to_switch=True)
    st.header("📊 시뮬레이션 결과")
    results_df = pd.DataFrame({
        '전략': ['선택을 유지하기', '선택을 바꾸기'],
        '승리 횟수': [stay_wins, switch_wins]
    }).set_index('전략')
    stay_win_rate = round((stay_wins / num_simulations) * 100, 2)
    switch_win_rate = round((switch_wins / num_simulations) * 100, 2)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("선택을 유지했을 때")
        st.metric(label="🏆 승률", value=f"{stay_win_rate}%")
        st.write(f"({num_simulations}번 중 {stay_wins}번 승리)")
    with col2:
        st.subheader("선택을 바꿨을 때")
        st.metric(label="🏆 승률", value=f"{switch_win_rate}%")
        st.write(f"({num_simulations}번 중 {switch_wins}번 승리)")
    st.subheader("📈 전체 결과 비교")
    st.bar_chart(results_df)
    st.info("결과가 놀랍지 않나요? 선택을 바꾸는 것이 승리할 확률이 약 **두 배**나 높습니다!")
else:
    st.info("게임 횟수를 설정하고 '시뮬레이션 시작' 버튼을 눌러 결과를 확인해보세요.")

import streamlit as st

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="몬티 홀 문제의 비밀",
    page_icon="🤔",
    layout="wide"
)

# --- 1. 제목 및 핵심 질문 ---
st.title("🤔 몬티 홀 문제, 왜 바꿔야만 할까?")
st.markdown("---")
st.info("""
시뮬레이터를 돌려보면 **선택을 바꾸는 것이 약 2/3 (66.7%) 확률로 승리**한다는 충격적인 결과를 볼 수 있습니다.  
하지만 머리로는 여전히 "남은 문이 2개니 확률은 1/2 아닌가?"라는 생각이 듭니다.  
이 페이지에서 그 비밀을 파헤쳐 봅시다!
""")

# --- 2. 흔한 함정 ---
st.header("❌ 우리가 빠지는 생각의 함정")
st.error("""
**"진행자가 염소가 있는 문을 하나 열었으니, 남은 두 개의 문 중에 자동차가 있을 확률은 각각 1/2이다."**
""")
st.write("""
이 생각이 바로 가장 흔하게 하는 실수입니다. 왜 틀렸을까요?  
핵심은, **진행자가 아무 문이나 막 여는 것이 아니라는 점**입니다. 진행자는 아래 두 가지 규칙을 모두 알고 있습니다.
1.  **자동차가 어디 있는지 안다.**
2.  **참가자가 선택한 문은 열 수 없다.**

이 '정보'를 가진 진행자의 행동 때문에 확률이 더 이상 1/2로 공평하지 않게 됩니다.
""")
st.markdown("---")

# --- 3. 관점을 바꿔서 확률 이해하기 ---
st.header("💡 관점을 바꾸면 진실이 보인다: 문 2개를 한 팀으로!")
st.markdown("""
자, 이제 생각의 방식을 완전히 바꿔봅시다.  
내가 문 1개를 선택한 순간, 세상은 두 부분으로 나뉩니다.
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("A팀: 내가 선택한 문 1개")
    st.success("""
    -   이 문 뒤에 자동차가 있을 확률: **1/3**
    """)
    st.code("🚪", language="text")


with col2:
    st.subheader("B팀: 내가 선택하지 않은 문 2개")
    st.warning("""
    -   이 **두 개의 문 어딘가에** 자동차가 있을 확률: **2/3**
    """)
    st.code("🚪 🚪", language="text")

st.markdown("""
여기까지는 모두가 동의할 것입니다. **그런데 여기서 진행자가 마법을 보여줍니다!**

진행자는 B팀(내가 고르지 않은 문 2개) 중에서 **꽝(염소)인 문을 반드시 찾아서 열어줍니다.** 이것은 B팀의 확률 2/3를 없애는 행동이 아니라, **B팀의 확률 2/3를 남은 문 하나에 전부 몰아주는** 것과 같습니다.
""")

st.subheader("진행자의 마법 후...")
col3, col4 = st.columns(2)
with col3:
    st.subheader("A팀: 나의 첫 선택 (바꾸지 않음)")
    st.success("""
    -   여전히 자동차가 있을 확률: **1/3** (바뀐 것이 없음)
    """)
    st.code("🚪", language="text")

with col4:
    st.subheader("B팀: 진행자가 남겨준 문 (바꿈)")
    st.warning("""
    -   원래 B팀이 가졌던 확률 **2/3**를 이 문 하나가 **전부 가져오게 됩니다!**
    """)
    st.code("🚪", language="text")
st.markdown("---")


# --- 4. 극단적인 예시로 확인하기 ---
st.header("💯 문이 100개라면? (극단적 예시)")
st.markdown("""
아직도 헷갈린다면, 문이 100개인 상황을 상상해봅시다.
-   100개의 문 중에 자동차는 단 1대, 나머지 99개는 모두 염소입니다.
-   당신이 1개의 문(예: 1번 문)을 선택했습니다.
""")

st.subheader("나의 첫 선택 (1번 문)")
st.success("1번 문에 자동차가 있을 확률은 얼마일까요? 당연히 **1/100** 입니다. (거의 꽝이죠)")

st.subheader("내가 선택하지 않은 나머지 99개의 문")
st.warning("나머지 99개 문 어딘가에 자동차가 있을 확률은 얼마일까요? 무려 **99/100** 입니다.")

st.markdown("""
이때, 모든 정답을 아는 진행자가 당신이 고르지 않은 99개의 문 중에서 **염소가 있는 문 98개를 모두 열어버립니다.** 그리고 당신에게 묻습니다.
""")
st.info("**\"처음에 고른 1번 문을 고수하시겠습니까, 아니면 제가 남겨둔 단 하나의 문으로 바꾸시겠습니까?\"**")

st.write("""
이제 어떤 선택이 더 현명하게 느껴지나요?

-   **고수하는 선택:** 나의 첫 선택이 처음부터 정답이었을 희박한 확률(**1/100**)에 거는 것입니다.
-   **바꾸는 선택:** 내가 고르지 않은 99개의 문에 있던 압도적인 확률(**99/100**)을 남은 문 하나가 모두 가져온 것입니다.

**당연히 바꾸는 것이 압도적으로 유리합니다.** 문이 3개일 때의 몬티 홀 문제도 이와 똑같은 원리입니다.
""")
st.balloons()
