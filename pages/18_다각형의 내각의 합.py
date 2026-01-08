
import streamlit as st

st.set_page_config(page_title="다각형 내각의 합 학습 앱", page_icon="📐")
st.title("다각형 내각의 합 단계별 학습")

# 1단계: 삼각형 내각의 합 퀴즈
if 'triangle_quiz_step' not in st.session_state:
    st.session_state['triangle_quiz_step'] = 'quiz'
if 'triangle_answer' not in st.session_state:
    st.session_state['triangle_answer'] = None
if 'triangle_hint' not in st.session_state:
    st.session_state['triangle_hint'] = ''

def triangle_quiz():
    st.subheader("1단계: 삼각형의 내각의 합 퀴즈")
    st.write("초등학교 때 배운 삼각형의 내각의 합을 맞춰보세요!")
    answer = st.number_input("삼각형의 내각의 합은 몇 도일까요?", min_value=0, max_value=1000, step=1, key="triangle_input")
    if st.button("정답 제출"):
        if answer < 180:
            st.session_state['triangle_hint'] = "정답보다 작아요! (업)"
        elif answer > 180:
            st.session_state['triangle_hint'] = "정답보다 커요! (다운)"
        else:
            st.session_state['triangle_hint'] = "정답입니다! 다음 단계로 이동합니다."
            st.session_state['triangle_quiz_step'] = 'done'
            st.session_state['triangle_answer'] = answer
    if st.session_state['triangle_hint']:
        st.info(st.session_state['triangle_hint'])

if st.session_state['triangle_quiz_step'] == 'quiz':
    triangle_quiz()
elif st.session_state['triangle_quiz_step'] == 'done':
    st.success("삼각형의 내각의 합을 정확히 맞췄어요! 다음 단계로 이동합니다.")

    # 2단계: 다각형 꼭짓점 개수 입력 및 그림 그리기
    st.subheader("2단계: 다각형 꼭짓점 개수 입력 및 다각형 그리기")
    if 'polygon_vertex' not in st.session_state:
        st.session_state['polygon_vertex'] = None
    if 'polygon_vertex_hint' not in st.session_state:
        st.session_state['polygon_vertex_hint'] = ''

    # number_input의 key를 별도로 지정하고, session_state에 vertex 저장
    vertex = st.number_input("다각형의 꼭짓점 개수를 입력하세요 (4~6)", min_value=3, max_value=12, step=1, key="polygon_vertex_number")
    if vertex == 3:
        st.warning("삼각형은 대각선이 없습니다! 4 이상의 꼭짓점 개수를 입력해 주세요.")
    elif vertex > 6:
        st.warning("꼭짓점이 너무 많으면 어려워져요! 6 이하의 수를 입력해 주세요.")
    if st.button("다각형 그리기"):
        if vertex == 3:
            st.session_state['polygon_vertex_hint'] = "삼각형에는 대각선이 없어요! 4 이상의 꼭짓점 개수를 입력해 주세요."
            st.session_state['polygon_vertex'] = None
        elif vertex > 6:
            st.session_state['polygon_vertex_hint'] = "6 이하의 수를 입력해 주세요."
            st.session_state['polygon_vertex'] = None
        else:
            st.session_state['polygon_vertex'] = int(vertex)
            st.session_state['polygon_vertex_hint'] = ''

    if st.session_state['polygon_vertex_hint']:
        st.info(st.session_state['polygon_vertex_hint'])

    if st.session_state['polygon_vertex']:
        import matplotlib.pyplot as plt
        import numpy as np
        fig, ax = plt.subplots(figsize=(2,2))
        n = st.session_state['polygon_vertex']
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        points = np.array([[np.cos(a), np.sin(a)] for a in angles])
        polygon = np.vstack([points, points[0]])
        ax.plot(polygon[:,0], polygon[:,1], 'o-', color='blue')
        # 한 꼭짓점(0번)에서 대각선 그리기 (변은 제외)
        diagonal_count = 0
        for i in range(1, n):
            # 변(0-1, 0-n-1)은 제외, 0에서 2~n-1까지 대각선만 그림
            if i != 1 and i != n-1:
                ax.plot([points[0,0], points[i,0]], [points[0,1], points[i,1]], '--', color='orange')
                diagonal_count += 1
        ax.set_aspect('equal')
        ax.axis('off')
        st.pyplot(fig)
        st.info(f"한 꼭짓점에서 {diagonal_count}개의 대각선을 그릴 수 있어요! (변은 제외한 대각선만 계산)")
        st.info(f"이렇게 하면 {n-2}개의 삼각형으로 분할할 수 있어요!")
        # 다음 단계: 분할된 삼각형 개수 퀴즈로 이동 예정

        # 추가: 다양한 모습(정다각형/비정다각형)을 2초 간격으로 번갈아 보여주기
        if st.button("다양한 모습 보기"):
            import time
            import numpy as np
            import matplotlib.pyplot as plt
            from random import random

            frames = 4  # 총 보여줄 프레임 수 (번갈아 보여줌)
            anim_container = st.empty()
            for i in range(frames):
                fig2, ax2 = plt.subplots(figsize=(2,2))
                if i % 2 == 0:
                    # 정다각형
                    pts = points
                else:
                    # 비정다각형: 반경과 각도를 약간씩 무작위로 흔들어 비정형으로 만듦
                    ang_perturb = (np.random.rand(n) - 0.5) * (np.pi / 12)
                    radii = 1 + (np.random.rand(n) - 0.5) * 0.2
                    angles2 = angles + ang_perturb
                    pts = np.array([[radii[j] * np.cos(angles2[j]), radii[j] * np.sin(angles2[j])] for j in range(n)])
                poly = np.vstack([pts, pts[0]])
                ax2.plot(poly[:,0], poly[:,1], 'o-', color='blue')
                # 한 꼭짓점(0번)에서 대각선 그리기 (변은 제외)
                for j in range(1, n):
                    if j != 1 and j != n-1:
                        ax2.plot([pts[0,0], pts[j,0]], [pts[0,1], pts[j,1]], '--', color='orange')
                ax2.set_aspect('equal')
                ax2.axis('off')
                anim_container.pyplot(fig2)
                time.sleep(3)
            # 애니메이션 종료 후 마지막 이미지는 유지

        # 3단계: 삼각형 분할 개수 퀴즈
        if 'triangle_split_quiz_step' not in st.session_state:
            st.session_state['triangle_split_quiz_step'] = 'quiz'
        if 'triangle_split_hint' not in st.session_state:
            st.session_state['triangle_split_hint'] = ''
        if 'triangle_split_answer' not in st.session_state:
            st.session_state['triangle_split_answer'] = None

        def split_quiz():
            st.subheader("3단계: 삼각형 분할 개수 퀴즈")
            st.write(f"{n}각형을 한 꼭짓점에서 대각선으로 삼각형으로 쪼갤 때, 몇 개의 삼각형으로 분할될까요?")
            user_answer = st.number_input("삼각형 분할 개수는?", min_value=1, max_value=20, step=1, key="split_input")
            if st.button("분할 개수 정답 제출"):
                correct = n - 2
                if user_answer < correct:
                    st.session_state['triangle_split_hint'] = "정답보다 작아요! (업)"
                elif user_answer > correct:
                    st.session_state['triangle_split_hint'] = "정답보다 커요! (다운)"
                else:
                    st.session_state['triangle_split_hint'] = "정답입니다! 다음 단계로 이동합니다."
                    st.session_state['triangle_split_quiz_step'] = 'done'
                    st.session_state['triangle_split_answer'] = user_answer
            if st.session_state['triangle_split_hint']:
                st.info(st.session_state['triangle_split_hint'])

        if 'repeat_count' not in st.session_state:
            st.session_state['repeat_count'] = 1

        if st.session_state['triangle_split_quiz_step'] == 'quiz':
            split_quiz()
        elif st.session_state['triangle_split_quiz_step'] == 'done':
            if st.session_state['repeat_count'] < 3:
                st.success("정답! 반복 학습을 위해 위의 2단계에서 꼭짓점의 개수를 바꾸어 입력해보세요.")
                st.session_state['repeat_count'] += 1
                # 반복을 위해 상태 초기화
                st.session_state['polygon_vertex'] = None
                st.session_state['polygon_vertex_hint'] = ''
                st.session_state['triangle_split_quiz_step'] = 'quiz'
                st.session_state['triangle_split_hint'] = ''
                st.session_state['triangle_split_answer'] = None
            else:
                st.success("3번 반복 학습 완료! 이제 다각형 내각의 합 공식 정리 단계로 넘어갑니다.")

                # 4단계: 다각형 내각의 합 공식 테이블 및 완성 팝업
                st.subheader("4단계: 다각형 내각의 합 공식 정리")
                st.write("아래 표의 빈 칸을 모두 채워보세요! (n각형의 내각의 합 공식: (n-2)×180°)")

                polygons = [3, 4, 5, 6, 7]
                answers = {}
                all_correct = True
                for n in polygons:
                    col1, col2 = st.columns([1,2])
                    col1.write(f"{n}각형")
                    user_input = col2.number_input(f"{n}각형의 내각의 합 (°)", min_value=0, max_value=2000, step=1, key=f"angle_sum_{n}")
                    correct = (n-2)*180
                    answers[n] = user_input
                    if user_input != correct:
                        all_correct = False

                if st.button("정답 확인", key="table_check"):
                    if all_correct:
                        st.success("모든 빈 칸을 정확히 채웠어요! 다각형 내각의 합 완성!! 🎉")
                        st.balloons()
                    else:
                        st.warning("아직 틀린 칸이 있어요. 다시 확인해보세요!")