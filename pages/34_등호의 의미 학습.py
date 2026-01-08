import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import random
import time
import os

st.set_page_config(page_title="등호의 의미 배우기", layout="centered")

st.title("⚖️ 등호의 의미 배우기 앱")
st.write("등호(=)는 양변이 같다는 동치 관계를 나타내요. 숫자를 시소에 올려서 균형을 맞춰보세요!")

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'sub_step' not in st.session_state:
    st.session_state.sub_step = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'additional_quizzes' not in st.session_state:
    st.session_state.additional_quizzes = [
        {"question": "12 + 8 = ㅁ + 15", "answer": 5, "explanation": "12 + 8 = 20, ㅁ + 15 = 20, ㅁ = 5"},
        {"question": "14 + 9 = ㅁ + 16", "answer": 7, "explanation": "14 + 9 = 23, ㅁ + 16 = 23, ㅁ = 7"},
        {"question": "16 + 7 = ㅁ + 18", "answer": 5, "explanation": "16 + 7 = 23, ㅁ + 18 = 23, ㅁ = 5"},
        {"question": "45 + 32 = ㅁ + 50", "answer": 27, "explanation": "45 + 32 = 77, ㅁ + 50 = 77, ㅁ = 27"},
        {"question": "67 + 18 = ㅁ + 55", "answer": 30, "explanation": "67 + 18 = 85, ㅁ + 55 = 85, ㅁ = 30"}
    ]
if 'step3_problems' not in st.session_state:
    st.session_state.step3_problems = [
        {"question": r"56 + 24 = \Box + 37", "answer": 43, "explanation": "56 + 24 = 80, ㅁ + 37 = 80, ㅁ = 43"}
    ]

# 단계별 진행
if st.session_state.step == 1:
    if st.session_state.sub_step == 0:
        st.header("📚 단계 1-1: 등호에 대한 오개념 OX 퀴즈")
        st.write("등호(=)에 대해 얼마나 알고 있나요? 다음 OX 퀴즈에 답해보세요.")
        
        quiz1 = st.radio("1. 등호는 계산의 답을 나타낸다.", ["O", "X"], key="quiz1")
        quiz2 = st.radio("2. 등호는 양변이 같다는 동치 관계를 나타낸다.", ["O", "X"], key="quiz2")
        quiz3 = st.radio("3. 56 + 24 = □ + 37에서 □는 곧 계산의 답이다.", ["O", "X"], key="quiz3")
        
        if st.button("답 확인"):
            correct = 0
            if quiz1 == "X": correct += 1
            if quiz2 == "O": correct += 1
            if quiz3 == "X": correct += 1
            st.write(f"정답 수: {correct}/3")
            st.session_state.sub_step = 1
    else:
        st.header("📚 단계 1-2: 오개념 교정 및 등호 개념 설명")
        st.write("등호에 대한 오개념을 교정하고, 올바른 개념을 배워봅시다.")
        
        st.subheader("1. 등호는 계산의 답을 나타낸다? ❌")
        st.write("등호는 계산의 답이 아니라, 양변이 같다는 것을 나타냅니다. 예를 들어, 2 + 3 = 5에서 왼쪽과 오른쪽이 같아요.")
        
        st.subheader("2. 등호는 양변이 같다는 동치 관계를 나타낸다? ✅")
        st.write("맞아요! 등호는 '같다'는 의미로, 양변의 값이 동일하다는 것을 보여줍니다.")
        
        st.subheader("3. 56 + 24 = □ + 37에서 □는 곧 계산의 답이다? ❌")
        st.write("□는 계산의 답이 아니라, 등호를 만족시키는 값이에요. 56 + 24 = 80, □ + 37 = 80이므로 □ = 43입니다.")
        
        st.write("등호는 '균형'이나 '동치'를 나타내는 기호예요. 시소처럼 양변이 같아야 해요!")
        
        if st.button("다음 단계로"):
            st.session_state.step = 2

elif st.session_state.step == 2:
    st.header("⚖️ 단계 2: 시소로 등호의 의미 체험하기")
    st.write("숫자를 시소에 올려서 **균형을 맞춰보세요**! 균형이 맞으면 등호가 성립해요.")

    st.write("---")

    # 숫자 옵션
    numbers = list(range(10, 100))  # 10부터 99까지

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⬅️ 왼쪽 시소")
        left1 = st.slider("첫 번째 숫자", 10, 99, 10, key="left1")
        left2 = st.slider("두 번째 숫자", 10, 99, 11, key="left2")
        left_total = left1 + left2
        st.write(f"📌 왼쪽 합: {left1} + {left2} = {left_total}")

    with col2:
        st.subheader("오른쪽 시소 ➡️")
        right1 = st.slider("첫 번째 숫자", 10, 99, 12, key="right1")
        right2 = st.slider("두 번째 숫자", 10, 99, 13, key="right2")
        right_total = right1 + right2
        st.write(f"📌 오른쪽 합: {right1} + {right2} = {right_total}")

    st.write("---")

    # --- 균형 결과 ---
    st.header("📊 균형 결과")

    if left_total == right_total:
        st.success(f"🎉 균형이 맞아요!   {left_total} = {right_total}")
        if st.button("다음 단계로"):
            st.session_state.step = 3
    elif left_total > right_total:
        st.info(f"왼쪽이 더 무거워요. 왼쪽: {left_total}, 오른쪽: {right_total}")
    else:
        st.info(f"오른쪽이 더 무거워요. 왼쪽: {left_total}, 오른쪽: {right_total}")

    # --- 시소 시각화 ---
    st.write("### ⚖️ 시소 시각화")

    # 시소 그리기 함수
    def draw_seesaw(left_total, right_total, left_nums, right_nums):
        # 폰트 설정
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'NanumGothic-Bold.ttf')
        if os.path.exists(font_path):
            font_prop = fm.FontProperties(fname=font_path)
        else:
            font_prop = fm.FontProperties()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # 시소 바의 기울기 계산
        diff = left_total - right_total
        angle = min(max(diff * 0.05, -0.5), 0.5)  # 기울기 제한
        
        # 시소 바
        x = [-2, 2]
        y = [-angle, angle]
        ax.plot(x, y, 'saddlebrown', linewidth=8)
        
        # 지지대
        ax.plot([0, 0], [-1, 0], 'black', linewidth=6)
        
        # 왼쪽 숫자들 표시
        ax.text(-2.2, -angle - 0.1, f'{left_nums[0]}', fontsize=14, ha='center')
        ax.text(-1.8, -angle - 0.1, f'{left_nums[1]}', fontsize=14, ha='center')
        
        # 오른쪽 숫자들 표시
        ax.text(1.8, angle - 0.1, f'{right_nums[0]}', fontsize=14, ha='center')
        ax.text(2.2, angle - 0.1, f'{right_nums[1]}', fontsize=14, ha='center')
        
        # 합 표시
        ax.text(-2, -angle + 0.3, f'합: {left_total}', fontsize=12, ha='center', 
                fontproperties=font_prop, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        ax.text(2, angle + 0.3, f'합: {right_total}', fontsize=12, ha='center', 
                fontproperties=font_prop, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        
        ax.set_xlim(-3, 3)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
        ax.set_title("시소", fontsize=16, fontproperties=font_prop)
        
        return fig

    # 시소 그리기
    fig = draw_seesaw(left_total, right_total, [left1, left2], [right1, right2])
    st.pyplot(fig)

    # --- 확장 설명 ---
    st.write("---")
    st.write("""
💡 **활동 포인트**  
• 왼쪽과 오른쪽의 합이 같아질 수 있는 조합을 찾아보세요.  
• 숫자를 선택하는 과정 자체가 **균형의 개념을 이해하는 연습**이에요.  
• 친구와 서로 다른 조합을 만들어 보고 비교해 보세요!
""")

elif st.session_state.step == 3:
    st.header("🔍 단계 3: 다시 문제 풀기")
    st.write("이제 등호의 의미를 이해했으니, 처음 문제를 풀어보세요.")
    
    problem = st.session_state.step3_problems[0]
    st.latex(problem["question"])
    st.write("ㅁ에 들어갈 숫자를 입력하세요.")
    user_answer = st.number_input("ㅁ =", min_value=0, step=1, key="step3")
    if st.button("답 확인", key="check_step3"):
        if int(user_answer) == problem["answer"]:
            st.write(f"정답이에요! {problem['explanation']}")
            st.session_state.step = 4
        else:
            st.write("다시 생각해보세요. 등호는 양변이 같다는 뜻이에요.")

elif st.session_state.step == 4:
    st.header("🎯 단계 4: 추가 퀴즈")
    st.write("더 많은 문제를 풀어보세요!")
    
    if st.session_state.quiz_index < len(st.session_state.additional_quizzes):
        quiz = st.session_state.additional_quizzes[st.session_state.quiz_index]
        st.latex(quiz["question"])
        user_ans = st.number_input("ㅁ =", min_value=0, step=1, key=f"quiz_{st.session_state.quiz_index}")
        if st.button("답 확인", key=f"check_{st.session_state.quiz_index}"):
            if user_ans == quiz["answer"]:
                st.write(f"정답! {quiz['explanation']}")
                st.session_state.quiz_index += 1
            else:
                st.write("다시 시도해보세요.")
    else:
        st.success("모든 퀴즈를 완료했어요! 🎉")
        if st.button("수업 끝"):
            st.session_state.step = 5

elif st.session_state.step == 5:
    st.header("🎉 오늘의 수업 끝")
    st.write("등호의 의미를 잘 배웠어요! 다음 시간에 만나요.")
    st.balloons()
    if st.button("처음으로 돌아가기"):
        st.session_state.step = 1
        st.session_state.sub_step = 0
        st.session_state.quiz_answers = {}
        st.session_state.quiz_index = 0
        st.session_state.additional_quizzes = [
            {"question": "12 + 8 = ㅁ + 15", "answer": 5, "explanation": "12 + 8 = 20, ㅁ + 15 = 20, ㅁ = 5"},
            {"question": "14 + 9 = ㅁ + 16", "answer": 7, "explanation": "14 + 9 = 23, ㅁ + 16 = 23, ㅁ = 7"},
            {"question": "16 + 7 = ㅁ + 18", "answer": 5, "explanation": "16 + 7 = 23, ㅁ + 18 = 23, ㅁ = 5"},
            {"question": "18 + 11 = ㅁ + 20", "answer": 9, "explanation": "18 + 11 = 29, ㅁ + 20 = 29, ㅁ = 9"},
            {"question": "20 + 6 = ㅁ + 22", "answer": 4, "explanation": "20 + 6 = 26, ㅁ + 22 = 26, ㅁ = 4"}
        ]
        st.session_state.step3_problems = [
            {"question": r"56 + 24 = \Box + 37", "answer": 43, "explanation": "56 + 24 = 80, ㅁ + 37 = 80, ㅁ = 43"}
        ]