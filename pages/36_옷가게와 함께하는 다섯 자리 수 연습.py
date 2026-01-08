import streamlit as st
import random
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="옷가게와 함께하는 다섯 자리 수 연습", layout="centered")

# ---------- Helper functions ----------
NUM_TO_KOR = {0:'',1:'일',2:'이',3:'삼',4:'사',5:'오',6:'육',7:'칠',8:'팔',9:'구'}

def number_to_korean(n:int)->str:
    """Convert 10000-99999 to Korean like '삼만 팔천 오백원'"""
    if not (10000 <= n <= 99999):
        raise ValueError("범위를 벗어난 수")
    d = [int(x) for x in f"{n:05d}"]  # [만,천,백,십,일]
    parts = []
    if d[0]: parts.append(f"{NUM_TO_KOR[d[0]]}만")
    if d[1]: parts.append(f"{NUM_TO_KOR[d[1]]}천")
    if d[2]: parts.append(f"{NUM_TO_KOR[d[2]]}백")
    if d[3]: parts.append(f"{NUM_TO_KOR[d[3]]}십")
    if d[4]: parts.append(f"{NUM_TO_KOR[d[4]]}원")
    # Join with spaces for readability
    return ' '.join(parts).replace('일만','만')  # 1만 -> '만' is fine

KOR_DIGIT = {'영':0,'영':0,'공':0,'일':1,'이':2,'삼':3,'사':4,'오':5,'육':6,'칠':7,'팔':8,'구':9}

def parse_korean_digits(s:str)->dict:
    """Try to extract digit for each 자리 from a simple Korean input.
    Returns dict with keys ['man','cheon','baek','sip','il'] values 0-9 or None if not found.
    This is a heuristic parser to provide helpful feedback for common student inputs.
    Treats bare unit mentions like '만' as 1 (equivalent to '일만').
    """
    s = s.replace('원','')
    s = s.replace(' ','')
    res = {'man':None,'cheon':None,'baek':None,'sip':None,'il':None}
    # look for patterns like '삼만', '팔천', etc. If unit appears without a leading digit, treat it as 1 (일)
    for k,unit in [('man','만'),('cheon','천'),('baek','백'),('sip','십')]:
        m = re.search(r'([일이삼사오육칠팔구])'+unit, s)
        if m:
            res[k] = KOR_DIGIT.get(m.group(1), None)
        else:
            # if unit present without explicit digit, interpret as 1
            if re.search(unit, s):
                res[k] = 1
    # ones place: last remaining Korean digit at end (explicit digit only)
    m = re.search(r'([일이삼사오육칠팔구])$', s)
    if m:
        res['il'] = KOR_DIGIT.get(m.group(1), None)
    return res


def normalize_korean(s:str)->str:
    s = s.strip()
    s = s.replace('원','')
    # remove spaces to normalize inputs like '일 만' -> '일만'
    s_nospace = s.replace(' ','')
    # treat '일만' == '만', '일천' == '천', '일백' == '백'
    s_nospace = re.sub(r'일만', '만', s_nospace)
    s_nospace = re.sub(r'일천', '천', s_nospace)
    s_nospace = re.sub(r'일백', '백', s_nospace)
    # now add a single space after each unit for canonical spacing
    s = re.sub(r'만', '만 ', s_nospace)
    s = re.sub(r'천', '천 ', s)
    s = re.sub(r'백', '백 ', s)
    s = re.sub(r'십', '십 ', s)
    s = s.strip()
    return s


def digits_of(n:int)->dict:
    s = f"{n:05d}"
    return {'man':int(s[0]), 'cheon':int(s[1]), 'baek':int(s[2]), 'sip':int(s[3]), 'il':int(s[4])}


# ---------- Simple CSS & Emoji map for friendlier UI ----------
st.markdown("""
<style>
/* 라이트 모드 (기본) */
.app-header {font-size:28px; color: #3b3b3b; font-weight:700}
.welcome {background: linear-gradient(135deg, #FFFBF0, #FFF7F8); padding:20px; border-radius:12px}
.item-card {display:flex; align-items:center; gap:12px; padding:8px 10px; border-radius:8px; background:#fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05)}
.price-badge {background:#FFDFD6; padding:6px 8px; border-radius:8px; font-weight:700; color:#2d2d2d}
.connect-line {margin:6px 0; padding:8px; border-left:4px solid #FF9AA2; background:#fff5f6; border-radius:6px; color:#2d2d2d}
.badge-num {background:#E3F7FF; padding:6px 8px; border-radius:6px; color:#2d2d2d}
.selecting {outline: 3px solid #FFD966; border-radius:6px}
pre {background:#F7F7F7; padding:12px; border-radius:8px; font-family:monospace; white-space:pre-wrap; color:#2d2d2d}

/* 다크 모드 */
@media (prefers-color-scheme: dark) {
  .app-header {color: #e8e8e8}
  .welcome {background: linear-gradient(135deg, #2d2d2d, #3a3a3a); color: #e8e8e8}
  .item-card {background:#2d2d2d; box-shadow: 0 2px 5px rgba(255,255,255,0.08); color: #e8e8e8}
  .price-badge {background:#5a3a3a; color:#ffd6cc}
  .connect-line {border-left:4px solid #ff6b7a; background:#3a2828; color: #e8e8e8}
  .badge-num {background:#2a4a5a; color:#b3e5ff}
  .selecting {outline: 3px solid #d4a933}
  pre {background:#2d2d2d; color:#e8e8e8; border: 1px solid #4a4a4a}
}
</style>
""", unsafe_allow_html=True)

CLOTH_EMOJI = {
    '티셔츠':'👕', '원피스':'👗', '청바지':'👖', '코트':'🧥', '스웨터':'🧶', '자켓':'🧥', '치마':'👗', '셔츠':'👔', '운동화':'👟', '모자':'🧢'
}

# ---------- Sample data (옷가게) ----------
SAMPLE_PRICES = [38500, 47000, 12900, 56000, 24100, 99000, 15000, 30800, 72000, 41300]
CLOTHES = ['티셔츠','원피스','청바지','코트','스웨터','자켓','치마','셔츠','운동화','모자']
ITEMS = list(zip(CLOTHES, SAMPLE_PRICES))

# ---------- Session initialization ----------
if 'stats' not in st.session_state:
    st.session_state['stats'] = {'correct':0, 'wrong':0, 'mistake_types':{}}
if 'hint_used' not in st.session_state:
    st.session_state['hint_used'] = 0

# Fallback rerun helper: use Streamlit's public API if available, otherwise raise the internal RerunException
# so that the script is re-executed in environments where `st.experimental_rerun` is not present.

def safe_rerun():
    try:
        return st.experimental_rerun()
    except AttributeError:
        # Streamlit internals: construct minimal RerunData and raise RerunException
        from streamlit.runtime.scriptrunner import RerunException, RerunData
        rd = RerunData(query_string='', widget_states=None, page_script_hash='', page_name='', fragment_id=None, fragment_id_queue=[], is_fragment_scoped_rerun=False, is_auto_rerun=False, cached_message_hashes=set(), context_info=None)
        raise RerunException(rd)

# ---------- Defaults (고정 설정) ----------
# Removed sidebar settings per request; use sensible defaults
show_place_colors = True
hint_limit = 2
num_questions = 8
# 활동 1의 보기 수을 5로 고정 (품목과 가격은 무작위로 바뀝니다)
num_choices_activity1 = 5

def colored_digit_text(n:int):
    """Return a simple representation of digits with colored badges (text-based)."""
    d = digits_of(n)
    if show_place_colors:
        return f"만:{d['man']}  천:{d['cheon']}  백:{d['baek']}  십:{d['sip']}  일:{d['il']}"
    else:
        return f"{n}"


# ---------- App header ----------
st.markdown("<div class='app-header'>👗 옷가게와 함께하는 다섯 자리 수 연습</div>", unsafe_allow_html=True)
st.write('옷가게에서 가격표를 보고, 숫자와 한글 표현을 바꿔 보는 즐거운 활동이에요!')

# ---------- Start page / Tabs for activities ----------
if 'started' not in st.session_state:
    st.session_state['started'] = False

if not st.session_state['started']:
    st.markdown("""
    <div class='welcome'>
      <h2>안녕하세요! 👋</h2>
      <p>옷가게에 오신 걸 환영해요! 함께 가격표를 읽고, 숫자와 한글을 바꿔보는 재미있는 연습을 해봐요.</p>
      <div style='display:flex; gap:16px; align-items:center; margin-top:12px'>
        <div style='font-size:48px'>👗</div>
        <div>
          <div class='item-card'>
            <div style='font-size:18px'>치마</div>
            <div class='price-badge'>41,300원</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button('시작하기', help='활동을 시작하려면 눌러요'):
        st.session_state['started'] = True
        safe_rerun()
    st.stop()

# Activities tabs
try:
    st.markdown('### 활동 흐름')
    tabs = st.tabs(['활동 1', '활동 2', '활동 3'])

    # ---------- Activity 1: Matching (click-to-connect with stable session state) ----------
    with tabs[0]:
        st.header('활동 1: 숫자 ↔ 한글을 선으로 연결해요 ✏️')
        st.write('왼쪽 숫자 카드에서 하나를 클릭한 다음, 오른쪽 한글 카드에서 같은 짝을 클릭해 연결하세요.')

        # fixed 5-choice activity; items and prices are randomized each problem
        num_choices = num_choices_activity1
        # initialize a stable problem set for activity 1
        if ('activity1_items' not in st.session_state) or (len(st.session_state.get('activity1_items', [])) != num_choices):
            sel = random.sample(ITEMS, num_choices)
            st.session_state['activity1_items'] = sel
            st.session_state['activity1_left'] = [price for name,price in sel]
            right = sel.copy(); random.shuffle(right)
            st.session_state['activity1_right'] = [number_to_korean(price) for name,price in right]
            st.session_state['activity1_kor_to_price'] = {number_to_korean(price): price for name,price in sel}
            st.session_state['activity1_item_names'] = [name for name,_ in sel]
            st.session_state['activity1_selected_num'] = None
            st.session_state['activity1_selected_kor'] = None
            st.session_state['activity1_matches'] = {}
            # ensure activity is active (in case we auto-advanced earlier and then reshuffle)
            if 'current_activity' not in st.session_state:
                st.session_state['current_activity'] = 1

        left_col, right_col = st.columns(2)

        with left_col:
            st.subheader('숫자 카드')
            for n in st.session_state['activity1_left']:
                # find item name for emoji
                name = next((nm for nm,pr in st.session_state['activity1_items'] if pr==n), None)
                emoji = CLOTH_EMOJI.get(name, '🧾')
                matched = n in st.session_state['activity1_matches']
                key = f"a1_num_{n}"
                label = f"{emoji}  {n:,}원"
                if matched:
                    st.markdown(f"<div class='item-card'>{label} <span style='margin-left:8px;color:#59A6FF'>&#10003; 연결됨</span></div>", unsafe_allow_html=True)
                else:
                    if st.session_state.get('activity1_selected_num') == n:
                        st.markdown(f"<div class='item-card selecting'>{label} <span style='margin-left:8px;color:#FFD966'>선택됨</span></div>", unsafe_allow_html=True)
                    else:
                        if st.button(label, key=key):
                            st.session_state['activity1_selected_num'] = n

        with right_col:
            st.subheader('한글 카드')
            for k in st.session_state['activity1_right']:
                price_for_k = st.session_state['activity1_kor_to_price'][k]
                name = next((nm for nm,pr in st.session_state['activity1_items'] if pr==price_for_k), None)
                emoji = CLOTH_EMOJI.get(name, '🧾')
                matched = price_for_k in st.session_state['activity1_matches']
                key = f"a1_kor_{price_for_k}"
                label = f"{emoji}  {k}"
                if matched:
                    st.markdown(f"<div class='item-card'>{label} <span style='margin-left:8px;color:#59A6FF'>&#10003; 연결됨</span></div>", unsafe_allow_html=True)
                else:
                    if st.session_state.get('activity1_selected_kor') == k:
                        st.markdown(f"<div class='item-card selecting'>{label} <span style='margin-left:8px;color:#FFD966'>선택됨</span></div>", unsafe_allow_html=True)
                    else:
                        if st.button(label, key=key):
                            st.session_state['activity1_selected_kor'] = k

        # show current selection and connect action
        sel_col1, sel_col2, sel_col3 = st.columns([1,1,1])
        with sel_col1:
            st.write('선택한 숫자:')
            if st.session_state.get('activity1_selected_num'):
                st.markdown(f"<div class='badge-num'>{st.session_state['activity1_selected_num']:,}원</div>", unsafe_allow_html=True)
            else:
                st.write('-')
        with sel_col2:
            st.write('선택한 한글:')
            if st.session_state.get('activity1_selected_kor'):
                st.write(st.session_state['activity1_selected_kor'])
            else:
                st.write('-')
        with sel_col3:
            if st.button('연결하기'):
                if not st.session_state.get('activity1_selected_num') or not st.session_state.get('activity1_selected_kor'):
                    st.warning('숫자와 한글을 차례로 선택해 주세요.')
                else:
                    n = st.session_state['activity1_selected_num']
                    kor = st.session_state['activity1_selected_kor']
                    correct_kor = number_to_korean(n)
                    if normalize_korean(kor) == normalize_korean(correct_kor):
                        st.success(f'정답이에요! {n:,}원 = {correct_kor} ✅')
                        st.session_state['activity1_matches'][n] = kor
                        st.session_state['stats']['correct'] += 1
                    else:
                        st.error(f'아쉽네요. {n:,}원은 {correct_kor}이에요. 다시 선택해 볼까요?')
                        st.session_state['stats']['wrong'] += 1
                        st.session_state['stats']['mistake_types'].setdefault('matching_wrong',0)
                        st.session_state['stats']['mistake_types']['matching_wrong'] += 1
                    # clear temporary selection
                    st.session_state['activity1_selected_num'] = None
                    st.session_state['activity1_selected_kor'] = None
                    # if all matched, advance automatically to activity 2
                    if len(st.session_state.get('activity1_matches', {})) >= num_choices:
                        st.session_state['current_activity'] = 2
                        # set a one-time activation hook so the client scrolls/jumps to activity 2
                        st.session_state['activate_hook'] = 2
                        st.success('활동1을 모두 완료했어요! 다음 활동으로 넘어갑니다 → 활동 2')
                        safe_rerun()

        st.markdown('---')
        st.subheader('현재 연결 상태')
        if st.session_state['activity1_matches']:
            for n, k in st.session_state['activity1_matches'].items():
                st.markdown(f"<div class='connect-line'> {n:,}원 &nbsp;&nbsp; → &nbsp;&nbsp; {k} </div>", unsafe_allow_html=True)
            if st.button('연결 해제(모두)'):
                st.session_state['activity1_matches'] = {}
        else:
            st.info('아직 연결된 짝이 없어요. 숫자와 한글을 선택해 연결해 보세요!')

        if st.button('문제 다시 섞기'):
            # regenerate a new fixed problem set
            sel = random.sample(ITEMS, num_choices)
            st.session_state['activity1_items'] = sel
            st.session_state['activity1_left'] = [price for name,price in sel]
            right = sel.copy(); random.shuffle(right)
            st.session_state['activity1_right'] = [number_to_korean(price) for name,price in right]
            st.session_state['activity1_kor_to_price'] = {number_to_korean(price): price for name,price in sel}
            st.session_state['activity1_item_names'] = [name for name,_ in sel]
            st.session_state['activity1_selected_num'] = None
            st.session_state['activity1_selected_kor'] = None
            st.session_state['activity1_matches'] = {}
            safe_rerun()
    with tabs[1]:
        # anchor for client-side navigation
        st.markdown("<div id='activity-2'></div>", unsafe_allow_html=True)
        st.header('활동 2: 영수증을 보고 숫자를 한글로 읽어요 🧾')
        st.write('영수증에 여러 물건과 가격이 있어요. 숫자를 보고 한글로 써보세요')
        # if activation hook present, jump to this section and clear the hook
        if st.session_state.get('activate_hook') == 2:
            components.html("<script>document.getElementById('activity-2').scrollIntoView({'behavior':'auto'});</script>", height=0)
            del st.session_state['activate_hook']

        # initialize a receipt (fixed for the session until '새 문제' is pressed)
        if 'activity2_receipt_items' not in st.session_state:
            # keep sampling until the total is exactly 5 digits (10000-99999)
            for _ in range(100):
                n_items = random.randint(3,5)
                sel = random.sample(ITEMS, n_items)
                total = sum(price for _, price in sel)
                if 10000 <= total <= 99999:
                    break
            else:
                # fallback: pick three items that will produce a 5-digit total
                candidates = [it for it in ITEMS if 10000 <= it[1] <= 99999]
                sel = random.sample(candidates, 3)
                total = sum(price for _, price in sel)
            st.session_state['activity2_receipt_items'] = sel
            st.session_state['activity2_receipt_total'] = total
            # choose a target: either 합계(총합) or 한 품목
            if random.random() < 0.25:
                st.session_state['activity2_target'] = 'total'
                st.session_state['activity2_q_price'] = total
                st.session_state['activity2_target_label'] = '합계'
            else:
                idx = random.randrange(len(sel))
                st.session_state['activity2_target'] = 'item'
                st.session_state['activity2_target_idx'] = idx
                st.session_state['activity2_q_price'] = sel[idx][1]
                st.session_state['activity2_target_label'] = sel[idx][0]
            st.session_state['activity2_ans'] = ''
            st.session_state['activity2_hint_used'] = 0
            st.session_state['activity2_submitted'] = False

        # clear-flag handling to avoid widget lifecycle issues
        if st.session_state.get('activity2_clear'):
            st.session_state['activity2_ans'] = ''
            st.session_state['activity2_submitted'] = False
            del st.session_state['activity2_clear']

        # ensure flags exist so the very first problem doesn't show place-values by default
        if 'activity2_submitted' not in st.session_state:
            st.session_state['activity2_submitted'] = False
        if 'activity2_hint_used' not in st.session_state:
            st.session_state['activity2_hint_used'] = 0

        items = st.session_state['activity2_receipt_items']
        total = st.session_state['activity2_receipt_total']
        price = st.session_state['activity2_q_price']
        target_label = st.session_state['activity2_target_label']

        # render a simple receipt using monospace for alignment
        receipt_lines = []
        for i, (name, p) in enumerate(items):
            receipt_lines.append(f"    {name:<12}{p:>10,}원")
            # add an extra blank line between items for readability
            if i != len(items) - 1:
                receipt_lines.append("")
        receipt_lines.append(f"    {'-'*20}")
        receipt_lines.append(f"    {'합계':<12}{total:>10,}원")
        receipt_text = "\n".join(receipt_lines)
        # render inside a fenced code block so it appears in a gray boxed area
        st.markdown(f"```text\n{receipt_text}\n```")

        st.subheader(f"문제: {target_label}의 금액을 한글로 입력하세요")
        ans = st.text_input('한글로 입력해 보세요', placeholder='예: 삼만 팔천 오백원', key='activity2_ans')

        place_labels = {'man':'만','cheon':'천','baek':'백','sip':'십','il':'일'}

        cols = st.columns([1,1,1])
        with cols[0]:
            if st.button('제출', key='activity2_submit'):
                if not ans.strip():
                    st.warning('답을 입력해 주세요.')
                else:
                    correct = number_to_korean(price)
                    norm_ans = normalize_korean(ans)
                    norm_correct = normalize_korean(correct)
                    if norm_ans == norm_correct:
                        # mark the result and increment stats (do not auto-advance)
                        st.session_state['activity2_result'] = 'correct'
                        st.session_state['stats']['correct'] += 1
                    else:
                        st.session_state['activity2_result'] = 'wrong'
                        st.session_state['stats']['wrong'] += 1
                        parsed = parse_korean_digits(ans)
                        true_digits = digits_of(price)
                        hints = []
                        for k in ['man','cheon','baek','sip','il']:
                            if parsed[k] is not None and parsed[k] != true_digits[k]:
                                hints.append(f"{place_labels[k]} 자리: 입력 {parsed[k]} vs 정답 {true_digits[k]}")
                        if hints:
                            st.info('오답 힌트: ' + '; '.join(hints))
                            st.session_state['stats']['mistake_types'].setdefault('place_confusion',0)
                            st.session_state['stats']['mistake_types']['place_confusion'] += 1
                        else:
                            st.info(f"힌트: 만/천/백/십/일 자리를 다시 확인해 보세요. 예: {correct}")
                            st.session_state['stats']['mistake_types'].setdefault('other_input',0)
                            st.session_state['stats']['mistake_types']['other_input'] += 1
                    # show place-value info after a submission attempt
                    st.session_state['activity2_submitted'] = True
        with cols[1]:
            if st.button('힌트', key='activity2_hint'):
                if st.session_state.get('activity2_hint_used', 0) >= hint_limit:
                    st.warning('힌트 사용 횟수를 모두 사용했어요.')
                else:
                    st.session_state['activity2_hint_used'] = st.session_state.get('activity2_hint_used', 0) + 1
                    d = digits_of(price)
                    st.info(f"힌트: 만 자리={d['man']}, 천 자리={d['cheon']}")
        with cols[2]:
            if st.button('새 문제', key='activity2_new'):
                # regenerate a new receipt question and ensure total is 5-digit
                for _ in range(100):
                    n_items = random.randint(3,5)
                    sel = random.sample(ITEMS, n_items)
                    total = sum(price for _, price in sel)
                    if 10000 <= total <= 99999:
                        break
                else:
                    candidates = [it for it in ITEMS if 10000 <= it[1] <= 99999]
                    sel = random.sample(candidates, 3)
                    total = sum(price for _, price in sel)
                st.session_state['activity2_receipt_items'] = sel
                st.session_state['activity2_receipt_total'] = total
                if random.random() < 0.25:
                    st.session_state['activity2_target'] = 'total'
                    st.session_state['activity2_q_price'] = total
                    st.session_state['activity2_target_label'] = '합계'
                else:
                    idx = random.randrange(len(sel))
                    st.session_state['activity2_target'] = 'item'
                    st.session_state['activity2_target_idx'] = idx
                    st.session_state['activity2_q_price'] = sel[idx][1]
                    st.session_state['activity2_target_label'] = sel[idx][0]
                st.session_state['activity2_clear'] = True
                st.session_state['activity2_hint_used'] = 0
                st.session_state['activity2_submitted'] = False
                if 'activity2_result' in st.session_state:
                    del st.session_state['activity2_result']
                safe_rerun()

        st.markdown('---')
        if st.session_state.get('activity2_submitted') or st.session_state.get('activity2_hint_used', 0) > 0:
            st.write('자릿값 보기:')
            st.write(colored_digit_text(price))

        # show persistent submission result (so the user sees feedback even after the run)
        if st.session_state.get('activity2_result') == 'correct':
            st.success(f"정답이에요! {price:,}원 = {number_to_korean(price)} ✅")
        elif st.session_state.get('activity2_result') == 'wrong':
            st.error('아쉽네요, 다시 생각해 볼까요?')
            # Show the correct answer explicitly when the user is wrong
            st.info(f"정답: {number_to_korean(price)} — {price:,}원")



    with tabs[2]:
        # anchor for client-side navigation
        st.markdown("<div id='activity-3'></div>", unsafe_allow_html=True)
        st.header('활동 3: 한글을 보고 알맞은 숫자를 골라요 ✅')
        st.write('한글 표기를 보고 알맞은 숫자(네 가지 중 하나)를 골라한 후, 반드시 "제출" 버튼을 눌러 확인하세요.')
        # if activation hook present, jump to this section and clear the hook
        if st.session_state.get('activate_hook') == 3:
            components.html("<script>document.getElementById('activity-3').scrollIntoView({'behavior':'auto'});</script>", height=0)
            del st.session_state['activate_hook']

        def setup_activity3():
            q_item, q_price = random.choice(ITEMS)
            st.session_state['activity3_q_item'] = q_item
            st.session_state['activity3_q_price'] = q_price
            true_digits = digits_of(q_price)
            choices = set([q_price])
            swapped = int(f"{true_digits['cheon']}{true_digits['man']}{true_digits['baek']}{true_digits['sip']}{true_digits['il']}")
            removed_man = int(f"0{true_digits['cheon']}{true_digits['baek']}{true_digits['sip']}{true_digits['il']}")
            changed = int(f"{true_digits['man']}{true_digits['cheon']}{(true_digits['baek']+1)%10}{true_digits['sip']}{true_digits['il']}")
            choices.update([swapped, removed_man, changed])
            choice_list = list(choices)
            random.shuffle(choice_list)
            st.session_state['activity3_choice_values'] = choice_list
            st.session_state['activity3_submitted'] = False

        if 'activity3_q_price' not in st.session_state:
            setup_activity3()

        # If a clear flag was set by the previous run, set up a fresh question before widgets are created
        if st.session_state.get('activity3_clear'):
            setup_activity3()
            del st.session_state['activity3_clear']

        q_item = st.session_state['activity3_q_item']
        q_price = st.session_state['activity3_q_price']
        q_kor = number_to_korean(q_price)
        emoji = CLOTH_EMOJI.get(q_item, '🧾')
        # make the emoji/visual larger per request
        st.markdown(f"<div class='item-card'><div style='font-size:64px'>{emoji}</div><div style='margin-left:8px'><div style='font-weight:700'>{q_item}</div><div style='margin-top:6px'>{q_kor}</div></div></div>", unsafe_allow_html=True)
        st.write('다음 한글 가격에 맞는 숫자를 골라주세요!')

        options = [f"{c:,}원" for c in st.session_state['activity3_choice_values']]
        option = st.radio('숫자를 고르세요', options, key='activity3_choice')

        if st.button('제출(객관식)'):
            if not st.session_state.get('activity3_choice'):
                st.warning('보기를 먼저 선택해 주세요.')
            else:
                sel = int(st.session_state['activity3_choice'].replace(',','').replace('원',''))
                if sel == q_price:
                    st.success('정답이에요! 잘했어요 ✅')
                    st.session_state['stats']['correct'] += 1
                else:
                    st.error(f'틀렸어요. 정답은 {q_price:,}원 이에요.')
                    st.session_state['stats']['wrong'] += 1
                    # detect type
                    true_digits = digits_of(q_price)
                    swapped = int(f"{true_digits['cheon']}{true_digits['man']}{true_digits['baek']}{true_digits['sip']}{true_digits['il']}")
                    removed_man = int(f"0{true_digits['cheon']}{true_digits['baek']}{true_digits['sip']}{true_digits['il']}")
                    if sel == swapped:
                        st.info('오답 분석: 만 자리와 천 자리를 바꿔 선택했어요—자릿값 위치를 확인해 보세요!')
                        st.session_state['stats']['mistake_types'].setdefault('swap_man_cheo',0)
                        st.session_state['stats']['mistake_types']['swap_man_cheo'] += 1
                    elif sel == removed_man:
                        st.info('오답 분석: 만 자리 숫자가 빠져 있어요—다섯 자리인지 확인해 보세요!')
                        st.session_state['stats']['mistake_types'].setdefault('missing_man',0)
                        st.session_state['stats']['mistake_types']['missing_man'] += 1
                    else:
                        st.session_state['stats']['mistake_types'].setdefault('other_mc_wrong',0)
                        st.session_state['stats']['mistake_types']['other_mc_wrong'] += 1
                st.session_state['activity3_submitted'] = True

        # allow moving to next only after submission
        if st.session_state.get('activity3_submitted'):
            if st.button('다음 문제'):
                # set a clear flag so the new question is initialized safely on the next run
                st.session_state['activity3_clear'] = True
                safe_rerun()


except Exception as e:
    st.error('앱 실행 중 오류가 발생했습니다. 아래 내용을 확인해주세요.')
    st.exception(e)
    import traceback
    st.text(traceback.format_exc())