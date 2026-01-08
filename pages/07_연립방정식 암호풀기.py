

import streamlit as st

if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'solved_problem_1' not in st.session_state:
    st.session_state.solved_problem_1 = False
if 'solved_problem_2' not in st.session_state:
    st.session_state.solved_problem_2 = False
if 'show_next_btn_1' not in st.session_state:
    st.session_state.show_next_btn_1 = False
if 'show_next_btn_2' not in st.session_state:
    st.session_state.show_next_btn_2 = False
if 'show_next_btn_3' not in st.session_state:
    st.session_state.show_next_btn_3 = False

def check_answer_problem1(x, y):
    """첫 번째 문제의 정답을 확인하는 함수"""
    # 문제: x + y = 15, x - y = 3
    if x == 9 and y == 6:
        st.success("🎉 정답입니다! 첫 번째 암호를 해독했어요.")
        st.balloons()
        st.session_state.solved_problem_1 = True
        st.session_state.show_next_btn_1 = True
    else:
        st.error("😭 다시 생각해 보세요. 해답은 두 식을 모두 만족해야 해요.")

def check_answer_problem2(adults, youths):
    """두 번째 문제의 정답을 확인하는 함수"""
    # 문제: 4000x + 2000y = 34000, y = x + 2
    if adults == 5 and youths == 7:
        st.success("🎉 완벽해요! 두 번째 암호를 해독했어요!")
        st.balloons()
        st.session_state.solved_problem_2 = True
        st.session_state.show_next_btn_2 = True
    else:
        st.error("😭 다시 한번 확인해 보세요. 방정식에 올바른 값을 넣었나요?")

def check_answer_problem3(five_hundred, one_hundred):
    # 문제: 500원짜리 동전 5개, 100원짜리 동전 5개
    if five_hundred == 5 and one_hundred == 5:
        st.success("🎉 모든 암호를 해독했습니다! 진짜 보물은 바로 여러분입니다!")
        st.balloons()
        st.session_state.show_next_btn_3 = True
    else:
        st.error("😭 다시 한번 확인해 보세요. 조건을 모두 만족해야 해요.")

st.title("🕵️‍♂️ 수학 탐정: 암호 해독 미션")
st.subheader("연립방정식으로 숨겨진 비밀을 밝혀내세요!")
st.markdown("---")

# 첫 번째 문제
if st.session_state.page == 'intro':
    st.header("🔑 첫 번째 암호")
    st.write("두 숫자 $x$와 $y$의 **합은 15**이고, **차는 3**입니다. $x$와 $y$를 찾아 첫 번째 암호를 해독하세요.")

    col1, col2 = st.columns(2)
    with col1:
        x_val = st.number_input('x의 값', min_value=0, step=1, key='x1')
    with col2:
        y_val = st.number_input('y의 값', min_value=0, step=1, key='y1')

    if st.button('첫 번째 암호 해독'):
        check_answer_problem1(x_val, y_val)
    if st.session_state.show_next_btn_1:
        if st.button('다음 문제로 이동', key='next1'):
            st.session_state.clear()
            st.session_state.page = 'problem2'
            st.session_state.solved_problem_1 = True

# 두 번째 문제
elif st.session_state.page == 'problem2':
    st.header("🔐 두 번째 암호")
    st.write("어떤 박물관의 입장료는 성인 $x$명과 청소년 $y$명에게 총 34,000원을 받았습니다. 성인 입장료는 4,000원, 청소년 입장료는 2,000원이며, 청소년이 성인보다 2명 더 많았습니다. 각각 몇 명이었을까요?")

    col3, col4 = st.columns(2)
    with col3:
        adults_val = st.number_input('성인 수', min_value=0, step=1, key='adults')
    with col4:
        youths_val = st.number_input('청소년 수', min_value=0, step=1, key='youths')

    if st.button('두 번째 암호 해독'):
        check_answer_problem2(adults_val, youths_val)
    if st.session_state.show_next_btn_2:
        if st.button('다음 문제로 이동', key='next2'):
            st.session_state.clear()
            st.session_state.page = 'problem3'
            st.session_state.solved_problem_1 = True
            st.session_state.solved_problem_2 = True

# 세 번째 문제
elif st.session_state.page == 'problem3':
    st.header("💎 세 번째 암호")
    st.write("마지막 단서입니다! 주머니에는 500원짜리 동전과 100원짜리 동전이 총 **10개** 들어 있고, 전체 금액은 **3,000원**입니다. 500원짜리 동전과 100원짜리 동전은 각각 몇 개일까요?")

    col5, col6 = st.columns(2)
    with col5:
        five_hundred_val = st.number_input('500원짜리 동전 개수', min_value=0, step=1, key='500')
    with col6:
        one_hundred_val = st.number_input('100원짜리 동전 개수', min_value=0, step=1, key='100')

    if st.button('세 번째 암호 해독'):
        check_answer_problem3(five_hundred_val, one_hundred_val)
    if st.session_state.show_next_btn_3:
        if st.button('보물 상자 열기', key='next3'):
            st.session_state.page = 'completed'

# 모든 문제를 해결했을 경우
if st.session_state.page == 'completed':
    st.markdown("---")
    st.write("선생님한테 가서 보물을 받으세요!")