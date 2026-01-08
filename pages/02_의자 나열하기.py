import itertools

import streamlit as st

st.header("의자 나열하기")

# 의자 개수 입력
num_chairs = st.number_input("의자 개수 설정", min_value=1, max_value=20, value=5, step=1)

st.write("자리 주인의 이름을 입력하세요 ()로 자리를 고정할 수 있습니다.")
names = []
for i in range(int(num_chairs)):
	name = st.text_input(f"{i+1}번 의자 주인 이름", key=f"chair_name_{i}")
	names.append(name)

# 의자와 이름 나열
# 의자와 이름 나열
chair_emoji = "🪑"
html = "<div style='display:flex;gap:2em;align-items:flex-end;'>"
for name in names:
	html += f"<div style='text-align:center;'><div style='font-size:1.2em;'>{name if name else '&nbsp;'}</div>"
	html += f"<div style='font-size:3em;'>{chair_emoji}</div></div>"
html += "</div>"
st.markdown(html, unsafe_allow_html=True)

# 모든 경우의 수 버튼 및 결과 표시
if st.button("모든 경우의 수 보기"):
	# 입력된 이름 중 빈칸 제외
	filtered_names = [n for n in names if n.strip()]
	if len(filtered_names) == int(num_chairs):
		# 괄호로 감싼 이름은 고정, 나머지만 순열
		fixed = []  # (index, name)
		unfixed = []
		for idx, n in enumerate(names):
			n_strip = n.strip()
			if n_strip.startswith("(") and n_strip.endswith(")"):
				fixed.append((idx, n_strip[1:-1]))
			else:
				unfixed.append(n_strip)
		# unfixed 자리만 순열
		perms = list(itertools.permutations(unfixed))
		result_set = set()
		for p in perms:
			result = [None]*int(num_chairs)
			unfixed_idx = 0
			for i in range(int(num_chairs)):
				fixed_name = next((name for idx2, name in fixed if idx2 == i), None)
				if fixed_name:
					result[i] = fixed_name
				else:
					result[i] = p[unfixed_idx]
					unfixed_idx += 1
			result_set.add(tuple(result))
		st.write(f"총 경우의 수: {len(result_set)}")
		# 첫 글자 기준 그룹화
		sorted_results = sorted(result_set, key=lambda x: x[0])
		grouped = []
		current_group = []
		prev_initial = None
		for r in sorted_results:
			initial = r[0][0] if r[0] else ""
			if prev_initial is None or initial == prev_initial:
				current_group.append(r)
			else:
				grouped.append(current_group)
				current_group = [r]
			prev_initial = initial
		if current_group:
			grouped.append(current_group)

		# HTML로 가로-세로 배열
		html = "<div style='display:flex;gap:2em;'>"
		for group in grouped:
			html += "<div>"
			for r in group:
				html += f"<div>{', '.join(r)}</div>"
			html += "</div>"
		html += "</div>"
		st.markdown(html, unsafe_allow_html=True)
	else:
		st.warning("모든 의자에 이름을 입력해야 경우의 수를 볼 수 있습니다.")