import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="개념 정리",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 사이드바
st.sidebar.title("메뉴")
page = st.sidebar.radio(
    "페이지를 선택하세요",
    ["개념 정리", "땅따먹기 놀이하기"],
    index=0
)

if page == "개념 정리":
    # 메인페이지 내용: 개념 정리
    st.title("📚 자연수의 혼합계산 개념 정리")

    st.markdown("""
### 자연수의 혼합계산이란?
자연수의 혼합계산은 덧셈(+), 뺄셈(-), 곱셈(×), 나눗셈(÷)이 섞인 식을 계산하는 것을 말해요. 
중요한 점은 **계산 순서**를 지켜야 해요!

#### 계산 순서 (중요!)
1. **괄호**가 있으면 괄호부터 계산해요.
2. **곱셈과 나눗셈**을 먼저 해요 (왼쪽부터).
3. **덧셈과 뺄셈**을 나중에 해요 (왼쪽부터).

예를 들어: 2 + 3 × 4 = ?
- 곱셈 먼저: 3 × 4 = 12
- 그 다음 덧셈: 2 + 12 = 14

다른 예: 10 - 2 × 3 + 4 = ?
- 곱셈 먼저: 2 × 3 = 6
- 뺄셈과 덧셈: 10 - 6 + 4 = 8
""")

    st.markdown("---")

    st.subheader("예시 문제")
    st.markdown("""
**문제 1:** 5 + 2 × 3 - 1  
**풀이:**  
- 곱셈 먼저: 2 × 3 = 6  
- 덧셈과 뺄셈: 5 + 6 - 1 = 10  

**문제 2:** 8 ÷ 2 + 3 × 2  
**풀이:**  
- 나눗셈과 곱셈 먼저: 8 ÷ 2 = 4, 3 × 2 = 6  
- 덧셈: 4 + 6 = 10  
""")

    st.markdown("---")

    st.subheader("문제 풀어보기")
    st.markdown("아래 문제를 풀어보세요!")

    # 문제 생성 (랜덤)
    def generate_simple_problem():
        nums = [random.randint(1, 10) for _ in range(4)]
        ops = [random.choice(['+', '-', '*']) for _ in range(3)]
        expression = f"{nums[0]} {ops[0]} {nums[1]} {ops[1]} {nums[2]} {ops[2]} {nums[3]}"
        try:
            result = eval(expression)
            if isinstance(result, int) and result > 0:
                return expression, result
        except:
            pass
        return generate_simple_problem()

    problem, correct_answer = generate_simple_problem()

    st.write(f"문제: {problem.replace('/', '÷').replace('*', '×')} = ?")
    user_answer = st.number_input("정답을 입력하세요 (숫자만):", value=None, step=1)

    if st.button("제출"):
        if user_answer is not None:
            if user_answer == correct_answer:
                st.success("정답입니다! 🎉")
                st.markdown(f"**풀이:** {problem.replace('/', '÷').replace('*', '×')} = {correct_answer}")
            else:
                st.error("오답입니다. 😅")
                st.markdown(f"**풀이:** {problem.replace('/', '÷').replace('*', '×')} = {correct_answer} (정답: {correct_answer})")
        else:
            st.warning("정답을 입력해주세요.")

elif page == "땅따먹기 놀이하기":
    # 게임 페이지 내용
    st.title("🎮 땅따먹기 놀이하기")

    # 세션 상태 초기화
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
        st.session_state.player_name = ""
        st.session_state.board = [['empty' for _ in range(5)] for _ in range(5)]
        st.session_state.turn = 'player'
        st.session_state.turn_count = 0
        st.session_state.max_turns = 20
        st.session_state.player_score = 0
        st.session_state.computer_score = 0
        st.session_state.current_problem = None
        st.session_state.feedback = ""
        st.session_state.show_next_button = False
        st.session_state.player_lands = set()  # 플레이어 차지한 땅
        st.session_state.computer_lands = set()  # 컴퓨터 차지한 땅
        st.session_state.problem_id = 0  # 문제 ID

    # 이름 입력
    if not st.session_state.game_started:
        st.subheader("이름을 입력하세요")
        player_name = st.text_input("당신의 이름은 무엇인가요?", key="name_input")
        if st.button("게임 시작"):
            if player_name.strip():
                st.session_state.player_name = player_name.strip()
                st.session_state.game_started = True
                st.info("잠시만 기다리세요...")
                st.rerun()
            else:
                st.warning("이름을 입력해주세요.")

    # 게임 방법 설명
    if st.session_state.game_started and st.session_state.turn_count == 0 and st.session_state.turn == 'player':
        st.subheader("게임 방법")
        st.markdown(f"""
        안녕하세요, {st.session_state.player_name}님!  
        땅따먹기 놀이를 시작합니다.  

        - 정사각형 땅 칸이 5x5로 총 25개 있습니다.  
        - 당신과 컴퓨터가 번갈아 땅을 선택하고, 자연수의 혼합계산 문제를 풀어요.  
        - 이후에는 자신이 차지한 땅의 주변 빈 땅만 선택할 수 있습니다. (컴퓨터가 차지한 땅은 피합니다.)  
        - 정답이면 땅을 차지하고, 오답이면 턴을 넘겨요.  
        - 총 20턴 진행되며, 더 많은 땅을 가진 쪽이 승리합니다.  
        - 당신이 먼저 시작합니다!  

        준비되셨나요? 아래 보드에서 땅을 선택하세요.
        """)

    # 문제 생성 함수
    def generate_problem():
        operations = ['+', '-', '*', '/']
        types = [
            ['+', '-', '*'],  # 덧셈, 뺄셈, 곱셈
            ['+', '-', '/'],  # 덧셈, 뺄셈, 나눗셈
            ['+', '-', '*', '/']  # 모두
        ]
        op_type = random.choice(types)
        nums = [random.randint(1, 10) for _ in range(4)]
        ops = [random.choice(op_type) for _ in range(3)]
        expression = f"{nums[0]} {ops[0]} {nums[1]} {ops[1]} {nums[2]} {ops[2]} {nums[3]}"
        try:
            result = eval(expression)
            if isinstance(result, int) and result > 0:
                return expression, result
        except:
            pass
        return generate_problem()  # 재귀적으로 다시 생성

    # 인접 칸 찾기
    def get_adjacent(i, j):
        adjacent = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < 5 and 0 <= nj < 5:
                    adjacent.append((ni, nj))
        return adjacent

    # 선택 가능한 칸 찾기
    def get_selectable_cells(player):
        if player == 'player':
            lands = st.session_state.player_lands
            forbidden = st.session_state.computer_lands
        else:
            lands = st.session_state.computer_lands
            forbidden = st.session_state.player_lands

        if not lands:
            # 자신이 땅이 없는 경우: 모든 빈 칸 선택 (컴퓨터가 차지한 땅 제외)
            return [(i, j) for i in range(5) for j in range(5) if st.session_state.board[i][j] == 'empty' and (i, j) not in forbidden]
        else:
            selectable = set()
            for land in lands:
                for adj in get_adjacent(*land):
                    if st.session_state.board[adj[0]][adj[1]] == 'empty' and adj not in forbidden:
                        selectable.add(adj)
            return list(selectable)

    # 보드 렌더링
    def render_board():
        cols = st.columns(5)
        selectable = get_selectable_cells(st.session_state.turn)
        for i in range(5):
            for j in range(5):
                color = '#CC9933'  # 기본 색
                if st.session_state.board[i][j] == 'player':
                    color = '#66CCFF'
                elif st.session_state.board[i][j] == 'computer':
                    color = '#FF66CC'
                key = f"cell_{i}_{j}"
                disabled = (i, j) not in selectable or st.session_state.show_next_button
                with cols[j]:
                    # 박스와 버튼을 옆에 배치
                    box_col, btn_col = st.columns([1, 1])
                    with box_col:
                        st.markdown(f"<div style='background-color: {color}; width: 50px; height: 50px; border: 1px solid black; display: inline-block;'></div>", unsafe_allow_html=True)
                    with btn_col:
                        if st.button("선택", key=key, disabled=disabled):
                            if st.session_state.turn == 'player' and st.session_state.turn_count < st.session_state.max_turns:
                                st.session_state.current_problem = generate_problem()
                                st.session_state.selected_cell = (i, j)
                                st.session_state.problem_id += 1
                                st.rerun()

    # 게임 진행
    if st.session_state.game_started:
        st.subheader(f"턴: {st.session_state.turn_count + 1} / {st.session_state.max_turns}")
        st.write(f"{st.session_state.player_name}의 땅: {st.session_state.player_score} | 컴퓨터의 땅: {st.session_state.computer_score}")

        render_board()

        # 플레이어 턴: 문제 풀기
        if st.session_state.current_problem and st.session_state.turn == 'player':
            expr, ans = st.session_state.current_problem
            st.subheader("문제를 풀어보세요!")
            st.write(f"문제: {expr.replace('/', '÷').replace('*', '×')} = ?")
            user_ans = st.number_input("정답을 입력하세요:", key=f"user_ans_{st.session_state.problem_id}", step=1)
            if st.button("제출"):
                if user_ans == ans:
                    st.session_state.feedback = f"정답입니다! 잘 풀었어요! 🎉"
                    i, j = st.session_state.selected_cell
                    st.session_state.board[i][j] = 'player'
                    st.session_state.player_lands.add((i, j))
                    st.session_state.player_score += 1
                else:
                    st.session_state.feedback = f"오답입니다. 정답은 {ans}입니다. 풀이: {expr.replace('/', '÷').replace('*', '×')} = {ans}"
                st.session_state.show_next_button = True
                st.rerun()

        # 피드백 표시
        if st.session_state.feedback:
            if "정답입니다" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)

        # 다음 턴 버튼
        if st.session_state.show_next_button:
            if st.button("다음 턴으로 넘기기"):
                st.session_state.turn_count += 1
                if st.session_state.turn == 'player':
                    st.session_state.turn = 'computer'
                    # 컴퓨터 턴 바로 실행
                    selectable = get_selectable_cells('computer')
                    if selectable:
                        selected = random.choice(selectable)
                        i, j = selected
                        expr, ans = generate_problem()
                        st.session_state.current_problem = (expr, ans)
                        st.session_state.selected_cell = selected
                        # 컴퓨터 정답률 70%
                        correct = random.random() < 0.7
                        comp_ans = ans if correct else random.randint(ans-5, ans+5)
                        st.write(f"컴퓨터가 {i*5+j+1}번 칸을 선택했습니다.")
                        st.write(f"문제: {expr.replace('/', '÷').replace('*', '×')} = ?")
                        st.write(f"컴퓨터의 답: {comp_ans}")
                        if correct:
                            st.session_state.feedback = f"컴퓨터가 정답을 맞췄습니다! {expr.replace('/', '÷').replace('*', '×')} = {ans}\n당신의 차례입니다, 땅을 선택하세요"
                            st.session_state.board[i][j] = 'computer'
                            st.session_state.computer_lands.add((i, j))
                            st.session_state.computer_score += 1
                        else:
                            st.session_state.feedback = f"컴퓨터가 오답을 했습니다. 정답은 {ans}입니다.\n당신의 차례입니다, 땅을 선택하세요"
                        st.session_state.show_next_button = False
                        st.session_state.turn = 'player'
                        st.session_state.turn_count += 1
                        st.session_state.current_problem = None  # 컴퓨터 턴 후 문제 리셋
                        st.info("이제 당신의 차례입니다!")
                        st.rerun()
                else:
                    st.session_state.turn = 'player'
                    st.info("이제 당신의 차례입니다!")
                st.session_state.current_problem = None
                st.session_state.feedback = ""
                st.session_state.show_next_button = False
                st.rerun()

        # 게임 종료
        if st.session_state.turn_count >= st.session_state.max_turns:
            st.subheader("게임 종료!")
            if st.session_state.player_score > st.session_state.computer_score:
                st.success(f"{st.session_state.player_name}님이 승리했습니다! 🏆")
            elif st.session_state.player_score < st.session_state.computer_score:
                st.error("컴퓨터가 승리했습니다. 😢")
            else:
                st.info("무승부입니다!")
            if st.button("다시 시작"):
                st.session_state.game_started = False
                st.rerun()