import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import random

# --- 페이지 설정 ---
st.set_page_config(page_title="함수 그래프 연습", page_icon="📈")

# --- 앱 제목 및 설명 ---
st.title("정비례와 반비례 그래프 연습기 📈")
st.write("제시된 함수가 지나는 점들을 캔버스에 마우스로 **클릭**하여 점으로 표시해 보세요.")
st.write("정답과 일치하는 점은 **초록색**으로, 그래프의 모양은 **검은색 선**으로 표시됩니다.")
st.markdown("---")

# --- 좌표평면 객체 생성 함수 (4사분면 버전) ---
def create_grid_objects(size=700, grid_range=30, padding=40):
    half_range = grid_range // 2
    origin_x, origin_y = size / 2, size / 2
    graph_size = size - 2 * padding
    cell_size = graph_size / grid_range
    objects = []

    # 격자선
    for i in range(grid_range + 1):
        x = padding + i * cell_size
        objects.append({"type": "line", "x1": x, "y1": padding, "x2": x, "y2": size - padding, "stroke": "#cccccc", "strokeWidth": 1})
        y = padding + i * cell_size
        objects.append({"type": "line", "x1": padding, "y1": y, "x2": size - padding, "y2": y, "stroke": "#cccccc", "strokeWidth": 1})
    
    # 축 (X, Y)
    objects.append({"type": "line", "x1": padding, "y1": origin_y, "x2": size - padding, "y2": origin_y, "stroke": "black", "strokeWidth": 2})
    objects.append({"type": "line", "x1": origin_x, "y1": padding, "x2": origin_x, "y2": size - padding, "stroke": "black", "strokeWidth": 2})

    # 좌표 숫자 (5단위로 표시)
    for i in range(-half_range, half_range + 1, 5):
        if i == 0: continue
        # X축 숫자
        x_pos = origin_x + i * cell_size
        objects.append({"type": "text", "left": x_pos, "top": origin_y + 15, "text": str(i), "fill": "black", "fontSize": 15, "originX": "center", "originY": "center"})
        # Y축 숫자
        y_pos = origin_y - i * cell_size
        objects.append({"type": "text", "left": origin_x - 20, "top": y_pos, "text": str(i), "fill": "black", "fontSize": 15, "originX": "center", "originY": "center"})
    objects.append({"type": "text", "left": origin_x - 15, "top": origin_y + 15, "text": "0", "fill": "black", "fontSize": 15, "originX": "center", "originY": "center"})
    
    return objects

# --- 문제 생성 및 관리 ---
if 'problem' not in st.session_state:
    st.session_state.problem = {}
def generate_new_problem():
    func_type = random.choice(['direct', 'inverse'])
    if func_type == 'direct':
        a_options = [1, 2, 3, 4, 5, 6, 7]
        a = random.choice(a_options)
        st.session_state.problem = {'type': 'direct', 'a': a, 'latex': f"y = {a}x"}
    else:
        a_options = [60, 72, 80, 90, 96, 100, 120]
        a = random.choice(a_options)
        st.session_state.problem = {'type': 'inverse', 'a': a, 'latex': f"y = \\frac{{{a}}}{{x}}"}
if not st.session_state.problem:
    generate_new_problem()

# --- session_state 변수 초기화 ---
if 'show_solution' not in st.session_state:
    st.session_state.show_solution = False
if 'user_drawing' not in st.session_state:
    st.session_state.user_drawing = None

# --- 화면 UI 구성 ---
st.header("1. 함수 확인하기")
st.latex(st.session_state.problem['latex'])

# --- 캔버스 설정 ---
CANVAS_SIZE = 700
GRID_RANGE = 30
PADDING = 40
CELL_SIZE = (CANVAS_SIZE - 2 * PADDING) / GRID_RANGE
HALF_GRID = GRID_RANGE // 2
CANVAS_CENTER_X, CANVAS_CENTER_Y = CANVAS_SIZE / 2, CANVAS_SIZE / 2
grid_objects = create_grid_objects(CANVAS_SIZE, GRID_RANGE, PADDING)

# --- 화면 분기 (문제 풀이 / 정답 확인) ---
if not st.session_state.show_solution:
    st.header("2. 그래프 위의 점 찍기")
    canvas_result = st_canvas(
        stroke_width=0, fill_color="blue", background_color="#FFFFFF",
        height=CANVAS_SIZE, width=CANVAS_SIZE,
        initial_drawing={"version": "5.1.0", "objects": grid_objects},
        drawing_mode="point", point_display_radius=8, key="canvas",
    )
    if st.button("정답 확인하기"):
        st.session_state.user_drawing = canvas_result.json_data
        st.session_state.show_solution = True
        st.rerun()
else:
    st.header("3. 정답 확인")
    prob = st.session_state.problem
    
    # 1. 정답 좌표 계산
    correct_coords_set = set()
    for x in range(-HALF_GRID, HALF_GRID + 1):
        if x == 0: continue
        if prob['type'] == 'direct':
            y = prob['a'] * x
            if -HALF_GRID <= y <= HALF_GRID:
                correct_coords_set.add((x, int(y)))
        elif prob['type'] == 'inverse':
            if prob['a'] % x == 0:
                y = prob['a'] / x
                if -HALF_GRID <= y <= HALF_GRID:
                    correct_coords_set.add((x, int(y)))

    # 2. 사용자 점을 수학 좌표로 변환
    user_coords_set = set()
    if st.session_state.user_drawing and st.session_state.user_drawing["objects"]:
        user_points_raw = st.session_state.user_drawing["objects"][len(grid_objects):]
        for point in user_points_raw:
            user_x = round((point['left'] - CANVAS_CENTER_X) / CELL_SIZE)
            user_y = round((CANVAS_CENTER_Y - point['top']) / CELL_SIZE)
            user_coords_set.add((user_x, user_y))
            
    # 3. 좌표 비교
    matched_coords = user_coords_set.intersection(correct_coords_set)
    missed_correct_coords = correct_coords_set - user_coords_set
    wrong_user_coords = user_coords_set - correct_coords_set

    # 4. 점 객체 생성
    final_points = []
    to_canvas_coords = lambda x, y: (CANVAS_CENTER_X + x * CELL_SIZE, CANVAS_CENTER_Y - y * CELL_SIZE)
    
    for x, y in matched_coords:
        cx, cy = to_canvas_coords(x, y)
        final_points.append({"type": "circle", "left": cx, "top": cy, "radius": 8, "fill": "#28a745", "originX": "center", "originY": "center"})
    for x, y in missed_correct_coords:
        cx, cy = to_canvas_coords(x, y)
        final_points.append({"type": "circle", "left": cx, "top": cy, "radius": 7, "fill": "#dc3545", "originX": "center", "originY": "center"})
    for x, y in wrong_user_coords:
        cx, cy = to_canvas_coords(x, y)
        final_points.append({"type": "circle", "left": cx, "top": cy, "radius": 7, "fill": "#007bff", "originX": "center", "originY": "center"})

    # 5. 선 객체 생성
    graph_lines = []
    
    def draw_lines_for_sorted_coords(coords):
        if len(coords) > 1:
            for i in range(len(coords) - 1):
                p1, p2 = coords[i], coords[i+1]
                p1_cx, p1_cy = to_canvas_coords(p1[0], p1[1])
                p2_cx, p2_cy = to_canvas_coords(p2[0], p2[1])
                graph_lines.append({"type": "line", "x1": p1_cx, "y1": p1_cy, "x2": p2_cx, "y2": p2_cy, "stroke": "black", "strokeWidth": 2})

    if prob['type'] == 'direct':
        draw_lines_for_sorted_coords(sorted(list(correct_coords_set)))
    elif prob['type'] == 'inverse':
        pos_coords = sorted([p for p in correct_coords_set if p[0] > 0])
        neg_coords = sorted([p for p in correct_coords_set if p[0] < 0])
        draw_lines_for_sorted_coords(pos_coords)
        draw_lines_for_sorted_coords(neg_coords)

    # 6. 최종 결과물 그리기
    solution_drawing = {"version": "5.1.0", "objects": grid_objects + graph_lines + final_points}
    st.write("결과: ✅**초록색**-정답, ❌**파란색**-오답, ⭕**빨간색**-놓친 정답")
    st_canvas(
        height=CANVAS_SIZE, width=CANVAS_SIZE,
        drawing_mode="transform",
        initial_drawing=solution_drawing,
        key="solution_canvas",
    )
    if st.button("새로운 문제 풀기"):
        generate_new_problem()
        st.session_state.show_solution = False
        st.session_state.user_drawing = None
        st.rerun()