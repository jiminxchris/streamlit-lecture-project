import time
import streamlit as st
import pandas as pd
import altair as alt
import textwrap

st.set_page_config(page_title="거리-속력 시뮬레이터 (비교)", layout="wide")

st.title("누가 더 빠를까?")
st.write("여러 캐릭터가 각각 다른 거리/시간으로 달릴 때 속력을 한눈에 비교할 수 있습니다.")

with st.sidebar:
    st.header("설정")
    num_runners = st.slider("러너 수", 1, 3, 2)
    track_meters = st.number_input("트랙 길이 (m)", min_value=1.0, step=1.0, value=100.0)
    visual_speed_scale = st.selectbox("속도 막대 스케일 (m/s)", [1, 2, 5, 10], index=2)
    st.markdown("---")

    runners = []
    for i in range(num_runners):
        with st.expander(f"러너 {i+1} 설정", expanded=(i == 0)):
            # 기본값을 빈칸으로 두어 자유롭게 이름을 입력하도록 함
            name = st.text_input(f"이름 {i+1}", value="", placeholder="이름을 입력하세요", key=f"name_{i}")
            # 캐릭터 타입을 제한하여 사람/자전거/자동차 중 선택 가능
            char_type = st.selectbox(f"캐릭터 타입 {i+1}", options=["사람", "자전거", "자동차"], index=0, key=f"type_{i}")
            # 타입에 따라 적절한 이모지를 자동 선택
            emoji_map = {"사람": "🏃", "자전거": "🚴", "자동차": "🚗"}
            emoji = emoji_map.get(char_type, "🏃")
            distance = st.number_input(f"거리 {i+1} (미터)", min_value=0.0, step=0.5, value=100.0, key=f"dist_{i}")
            time_sec = st.number_input(f"시간 {i+1} (초)", min_value=0.1, step=0.5, value=10.0, key=f"time_{i}")
            runners.append({"name": name, "emoji": emoji, "distance": float(distance), "time": float(time_sec)})

    start = st.button("시뮬레이션 시작")

st.markdown("---")

TRACK_CSS = """
<style>
.track { position: relative; background: linear-gradient(#f7f7f7, #efefef); border-radius: 8px; height: 90px; margin: 6px 0; width:100%; }
.track-inner { position: absolute; left: 2%; right: 2%; top: 50%; transform: translateY(-50%); height: 12px; background: #d6d6d6; border-radius: 6px; }
.runner { position: absolute; font-size: 36px; transform: translateX(-50%) translateY(0); will-change: transform; }
.label { font-size: 14px; margin-bottom: 4px; }

@keyframes run-bounce {
    0% { transform: translateX(-50%) translateY(0); }
    50% { transform: translateX(-50%) translateY(-8px); }
    100% { transform: translateX(-50%) translateY(0); }
}
</style>
"""


def render_single_track_html(runners_info, track_meters, elapsed):
        # runners_info: list of dicts {name, emoji, speed, frac, top_offset}
        # Build tick marks (every 50m)
        ticks_html = ""
        if track_meters > 0:
                num_ticks = int(track_meters // 50)
                # include final mark if track_meters is exact multiple
                for t in range(0, num_ticks + 1):
                        m = t * 50
                        left = (m / track_meters) * 92 + 4
                        ticks_html += f"<div style='position:absolute; left:{left}%; top:18px; height:10px; width:2px; background:#444;'></div>"
                        ticks_html += f"<div style='position:absolute; left:{left}%; top:28px; font-size:11px; transform:translateX(-50%); color:#333'>{m}m</div>"

        runners_html = ""
        for info in runners_info:
                left = max(0, min(info.get('frac', 0) * 92 + 4, 96))
                top = info.get('top', 0)

                # vertical bounce animation duration depends on speed
                speed = info.get('speed', 0.0)
                if speed and speed > 0:
                    bounce_dur = max(0.25, min(1.5, 1.5 / (speed + 0.1)))
                    bounce_state = 'running'
                else:
                    bounce_dur = 1.5
                    bounce_state = 'paused'

                # movement animation (browser-side keyframes) — name and duration provided in info
                move_name = info.get('move_name')
                move_dur = info.get('move_dur')
                move_part = ''
                if move_name and move_dur and move_dur > 0:
                    move_part = f"{move_name} {move_dur}s linear forwards, "

                anim_style = f"animation: {move_part} run-bounce {bounce_dur}s linear infinite; animation-play-state: {bounce_state};"
                runners_html += f"<div class='runner' style='left:{left}%; top:{top}px; {anim_style}'>" + f"{info['emoji']}</div>"

        html = f"""
        <div class='label'><strong>트랙 ({track_meters} m)</strong></div>
        <div class='track' style='height:80px;'>
            <div class='track-inner' style='top:50%;'></div>
            {ticks_html}
            {runners_html}
        </div>
        <div style='font-size:12px;color:#666'>경과: {elapsed:.1f}s</div>
        """
        # Remove common leading indentation so Streamlit doesn't render the HTML as a code block
        return textwrap.dedent(html).strip()


if num_runners == 0:
    st.warning("러너를 1명 이상 선택하세요.")
else:
    # Compute per-runner stats (speed from distance/time, then compute time to finish the configured track)
    for r in runners:
        if r["time"] <= 0 or r["distance"] <= 0:
            r["speed"] = 0.0
        else:
            r["speed"] = r["distance"] / r["time"]
        # time to run the displayed track (in seconds)
        if r["speed"] > 0:
            r["time_to_finish"] = track_meters / r["speed"]
        else:
            r["time_to_finish"] = float('inf')

    # Top: 러너별 속력을 가로로 나열
    st.subheader("러너별 속력")
    top_cols = st.columns(len(runners))
    for idx, r in enumerate(runners):
        with top_cols[idx]:
            display_name = r.get('name') or f"참가자 {idx+1}"
            st.markdown(f"**{display_name}** {r['emoji']}")
            st.write(f"속력: {r['speed']:.2f} m/s  —  입력: 거리 {r['distance']} m ÷ 시간 {r['time']} s")
            if r.get('time_to_finish', float('inf')) != float('inf'):
                st.write(f"트랙 {track_meters} m를 달리는 데 걸리는 시간: 약 {r['time_to_finish']:.1f} s")
            else:
                st.write("트랙을 달릴 수 없습니다 (속력 0)")
            prog = min(r['speed'] / float(visual_speed_scale), 1.0) if visual_speed_scale > 0 else 0.0
            st.progress(prog)

    # Inject track CSS once
    st.markdown(TRACK_CSS, unsafe_allow_html=True)

    # 트랙: 러너별 속력 바로 밑에 전체 너비로 표시
    with st.container():
        st.subheader("트랙 (모든 러너가 한 트랙에서 함께 달립니다)")
        track_placeholder = st.empty()

    # 트랙 아래: 시간에 따른 거리 비교 그래프 (러너 1,2)
    with st.container():
        st.subheader("시간-거리 비교")
        st.caption("같은 그래프 안에서 두 러너의 거리 변화를 비교합니다.")
        graph_placeholder = st.empty()

    # 초기(비시작) 상태에서의 정적 그래프: 각 러너의 시간-거리 곡선을 미리 보여줌
    # 그래프에는 최대 두 러너를 표시
    try:
        names_preview = [r.get('name') or f"참가자 {idx+1}" for idx, r in enumerate(runners[:2])]
        # 우선 사용자가 입력한 각 러너의 time_to_finish 값 중 유한한 값과 입력된 시간 값 중 최대 사용
        ttf_list = [r.get('time_to_finish') for r in runners if r.get('time_to_finish') != float('inf')]
        fallback_max_time = max([r.get('time', 0.0) for r in runners]) if runners else 10.0
        if ttf_list:
            preview_max = min(max(ttf_list), 60)
        else:
            preview_max = min(fallback_max_time, 60)
        if preview_max <= 0:
            preview_max = 10.0
        step = max(preview_max / 40.0, 0.1)
        times_preview = [round(i * step, 3) for i in range(int(preview_max / step) + 1)]
        data_preview = {}
        for idx, r in enumerate(runners[:2]):
            col_name = names_preview[idx]
            speed = r.get('speed', 0.0)
            data_preview[col_name] = [min(speed * t, track_meters) for t in times_preview]
        if data_preview:
            df_preview = pd.DataFrame(data_preview, index=times_preview)
            df_preview = df_preview.reset_index().rename(columns={"index": "time"})
            df_melt = df_preview.melt(id_vars=["time"], var_name="runner", value_name="distance")
            chart_preview = (
                alt.Chart(df_melt)
                .mark_line()
                .encode(x=alt.X("time:Q", title="시간 (s)"), y=alt.Y("distance:Q", title="거리 (m)"), color="runner:N")
                .properties(height=300)
            )
            graph_placeholder.altair_chart(chart_preview, use_container_width=True)
    except Exception:
        # 안전 장치: 그래프 생성 실패하면 그냥 넘어감
        pass

    if start:
        # On start: generate browser-side movement keyframes so the animation is smooth
        finite_times = [r["time_to_finish"] for r in runners if r["time_to_finish"] != float('inf')]
        if not finite_times:
            st.warning("모든 러너의 속력이 0입니다. 올바른 거리/시간을 입력하세요.")
        else:
            max_time = min(max(finite_times), 60)
            # assign vertical offsets so runners don't overlap (in px)
            top_positions = [18, 46, 74]

            # build movement keyframes CSS
            movement_css = "\n<style>\n"
            # We'll create per-runner keyframes named move-0, move-1, ...
            runners_info = []
            for idx, r in enumerate(runners):
                start_left = 4
                speed = r.get("speed", 0.0)
                # Target the track end: runners stop when they reach the track length, not their input distance
                runner_target_m = float(track_meters) if track_meters > 0 else 0.0

                if speed and speed > 0 and runner_target_m > 0 and track_meters > 0:
                    frac = max(0.0, min(1.0, runner_target_m / track_meters))
                    end_left = frac * 92 + 4
                    # duration to reach the configured target distance at current speed
                    duration_to_target = runner_target_m / speed
                    move_name = f"move-{idx}"
                    move_dur = min(duration_to_target, 60)
                    movement_css += f"@keyframes {move_name} {{ from {{ left: {start_left}%; }} to {{ left: {end_left}%; }} }}\n"
                else:
                    frac = 0.0
                    end_left = start_left
                    move_name = None
                    move_dur = None

                runners_info.append({
                    "name": r.get("name", ""),
                    "emoji": r.get("emoji", "🏃"),
                    "speed": speed,
                    "frac": frac,
                    "top": top_positions[idx] if idx < len(top_positions) else 32,
                    "move_name": move_name,
                    "move_dur": move_dur,
                    "time_to_finish": r.get("time_to_finish", float('inf')),
                })

            movement_css += "</style>\n"

            # Render CSS + initial HTML. Browser will handle movement animation smoothly.
            track_html = render_single_track_html(runners_info, track_meters, 0)
            track_placeholder.markdown(TRACK_CSS + movement_css + track_html, unsafe_allow_html=True)

            # Build graph data: time grid from 0..max_time, distances capped at track_meters.
            times = []
            steps = 200
            for i in range(steps + 1):
                times.append(round(i * (max_time / steps), 3))

            data = {}
            names = [r.get('name') or f"참가자 {idx+1}" for idx, r in enumerate(runners[:3])]
            for idx, r in enumerate(runners[:3]):
                col_name = names[idx]
                speed = r.get('speed', 0.0)
                ttf = r.get('time_to_finish', float('inf'))
                series = []
                for t in times:
                    if ttf == float('inf') or speed <= 0:
                        # no movement — show NaN so line does not draw
                        series.append(float('nan'))
                    else:
                        if t <= ttf:
                            series.append(min(speed * t, track_meters))
                        else:
                            # after reaching target, break the line by using NaN
                            series.append(float('nan'))
                data[col_name] = series

            df = pd.DataFrame(data, index=times)
            df = df.reset_index().rename(columns={"index": "time"})
            df_melt = df.melt(id_vars=["time"], var_name="runner", value_name="distance")
            chart = (
                alt.Chart(df_melt)
                .mark_line()
                .encode(x=alt.X("time:Q", title="시간 (s)"), y=alt.Y("distance:Q", title="거리 (m)"), color="runner:N")
                .properties(height=360)
            )
            # Do not call .interactive() — leave interactions disabled (no zoom/pan)
            graph_placeholder.altair_chart(chart, use_container_width=True)
            st.success("시뮬레이션 시작 — 트랙 위 러너들이 브라우저에서 부드럽게 이동합니다.")

st.markdown("---")
st.write("팁: 동일한 거리를 주고 시간을 다르게 하면 속력의 차이를, 동일한 시간을 주고 거리를 다르게 하면 거리와 속력의 관계를 비교해보세요.")