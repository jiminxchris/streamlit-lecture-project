# app.py
# ------------------------------------------------------------
# Streamlit: AI 논리 배틀 아레나 (flash-latest, 1000토큰, Step3·4 제거 + 다시 시도 버튼)
# ------------------------------------------------------------
import streamlit as st
import streamlit.components.v1 as components
import re
import json
import requests
from typing import Optional

# ---------------- Page Config ----------------
st.set_page_config(page_title="AI 논리 배틀 아레나", page_icon="🧠")

# ---------------- 세션 초기화 ----------------
def init_session_state():
    if "student_claim" not in st.session_state:
        st.session_state.student_claim = ""
    if "ai_response" not in st.session_state:
        st.session_state.ai_response = ""
    if "student_followup_answer" not in st.session_state:
        st.session_state.student_followup_answer = ""
    if "final_evaluation" not in st.session_state:
        st.session_state.final_evaluation = ""
    if "ai_response_json" not in st.session_state:
        st.session_state.ai_response_json = {}
    # 사용자가 직접 입력한 API 키(세션 단위 저장)
    if "user_gpt_key" not in st.session_state:
        st.session_state.user_gpt_key = ""


def _extract_followup_question(ai_text: str) -> str:
    """AI의 응답에서 '학생이 던질 수 있는 되묻는 질문'을 추출합니다. 발견되지 않으면 기본 질문을 반환합니다."""
    if not ai_text:
        return "이 반박에 대해 어떻게 더 질문하시겠습니까?"

    # 우선: 명시적 태그 <FOLLOWUP_QUESTION>...</FOLLOWUP_QUESTION> 검색 (멀티라인 캡처)
    tag_match = re.search(r"<FOLLOWUP_QUESTION>([\s\S]+?)</FOLLOWUP_QUESTION>", ai_text, re.IGNORECASE)
    if tag_match:
        q = tag_match.group(1).strip()
        # 질문형으로 끝나지 않으면 물음표 추가
        if not q.endswith("?"):
            q = q.rstrip('.') + "?"
        return q

    # 라벨을 검색 (기존 로직)
    m = re.search(r"학생[\s\S]{0,10}되묻는 질문[:：]?\s*(.+)$", ai_text, re.MULTILINE)
    if m:
        candidate = m.group(1).strip()
        first_line = candidate.splitlines()[0].strip()
        return first_line

    parts = ai_text.splitlines()
    for i, line in enumerate(parts):
        if "되묻" in line or "되묻는" in line or "질문" in line:
            for j in range(i+1, min(i+6, len(parts))):
                maybe = parts[j].strip()
                if maybe:
                    return maybe

    # 물음표가 포함된 마지막 문장
    sentences = re.split(r"(?<=[.?!])\s+", ai_text)
    for s in reversed(sentences):
        if s.strip().endswith("?"):
            return s.strip()

    return "이 반박에 대해 어떻게 더 질문하시겠습니까?"


def call_gemini_evaluate(claim: str, ai_response: str, student_answer: str) -> Optional[str]:
    """학생의 답변에 대해 AI가 최종 평가와 조언을 제공하도록 Gemini에 요청합니다."""
    # 우선 사용자가 입력한 세션 키를 사용하고, 없으면 Streamlit secrets의 키를 사용합니다.
    # 우선 사용자가 입력한 세션 키를 사용하고, 없으면 Streamlit secrets의 OPENAI_API_KEY, 그다음 GOOGLE_API_KEY로 폴백
    api_key = (
        st.session_state.get("user_gpt_key")
        or st.secrets.get("OPENAI_API_KEY")
        or st.secrets.get("GOOGLE_API_KEY")
    )
    if not api_key:
        st.error("API 키를 찾을 수 없습니다. 페이지 상단에서 API 키를 입력하거나 Streamlit secrets에 설정하세요.")
        return None

    # OpenAI Chat Completions 호출 helper
    def _call_openai_chat(system: str, user: str, model: str = "gpt-3.5-turbo", max_tokens: int = 1024, temperature: float = 0.6) -> Optional[str]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            # 표준 응답 구조에서 첫 번째 선택지의 메시지 텍스트 반환
            choices = data.get("choices") or []
            if choices:
                msg = choices[0].get("message", {}).get("content")
                return msg
            return None
        except Exception as e:
            st.error(f"OpenAI 호출 실패: {e}")
            return None

    prompt = f"""
당신은 고등학교 수학 수업의 논리 토론 파트너입니다.
학생의 원래 주장: "{claim}"
AI의 반박(요약):
{ai_response}

학생의 답변(학생이 AI의 반박에 대해 대답한 내용):
{student_answer}

위의 학생 답변을 평가하고, 다음을 포함한 최종 평가와 구체적인 지도(조언)를 제시하세요:
1) 학생 답변의 강점과 약점 (간단히)
2) 논리적 오류나 오해가 있다면 지적
3) 다음 토론에서 학생이 더 발전시킬 수 있는 구체적인 연습이나 질문 추천

출력은 명확한 문단으로 제공하세요.
"""

    # 요약 요청을 함께 포함시켜 OpenAI에 전달
    user_prompt = prompt + "\n요청: 아래 출력은 간결하게 (6문장 이내 또는 약 180단어 이내) 요약해 주세요.\n"
    return _call_openai_chat(system="You are a helpful assistant for evaluating student answers.", user=user_prompt, model="gpt-3.5-turbo", max_tokens=1024, temperature=0.6)


# ---------------- Gemini 호출 함수 ----------------
def call_gemini(claim: str) -> Optional[str]:
    """Gemini AI 호출 (flash-latest, 1000토큰 고정)"""
    # 우선 사용자가 입력한 세션 키를 사용하고, 없으면 Streamlit secrets의 키를 사용합니다.
    api_key = (
        st.session_state.get("user_gpt_key")
        or st.secrets.get("OPENAI_API_KEY")
        or st.secrets.get("GOOGLE_API_KEY")
    )
    if not api_key:
        st.error("API 키를 찾을 수 없습니다. 페이지 상단에서 API 키를 입력하거나 Streamlit secrets에 설정하세요.")
        return None
    # OpenAI Chat Completions 호출 helper (재사용)
    def _call_openai_chat(system: str, user: str, model: str = "gpt-3.5-turbo", max_tokens: int = 1500, temperature: float = 0.7) -> Optional[str]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            choices = data.get("choices") or []
            if choices:
                return choices[0].get("message", {}).get("content")
            return None
        except Exception as e:
            st.error(f"OpenAI 호출 실패: {e}")
            return None

    # JSON 형식으로 정확히 출력하도록 모델에 강하게 지시합니다.
    prompt = f"""
당신은 고등학교 수학 수업의 논리 토론 파트너입니다.
학생의 주장: "{claim}"

이 주장에 대해 위의 요구사항에 따라 논리적으로 반박한 뒤, 아래의 JSON 객체 하나만을 출력하세요.
JSON 키는 정확히 다음과 같아야 합니다:
{{
    "error_type": "(오류 유형)",
    "definition_explanation": "(정의에 근거한 설명)",
    "counterexamples": ["(반례1)", "(반례2)"],
    "one_line_conclusion": "(한줄 결론)",
    "followup_question": "(학생이 던질 수 있는 되묻는 질문, 반드시 물음표로 끝날 것)"
}}

중요: 출력은 반드시 위의 JSON 객체만 단독으로 반환하고, 추가 설명이나 텍스트는 첨가하지 마세요. followup_question 값은 반드시 물음표(?)로 끝나야 합니다.

추가 요구사항: `error_type` 필드는 한국어로 간단히 작성하고, 필요하면 괄호 안에 영어 원문을 덧붙여 주세요. 예: "단일 원인 오류 (Single Cause Fallacy)".
"""

    # OpenAI로 호출
    text = _call_openai_chat(system="You are a helpful assistant that produces a single JSON object answer.", user=prompt, model="gpt-3.5-turbo", max_tokens=1500, temperature=0.7)
    if not text:
        st.warning("AI 응답이 비어 있거나 차단되었습니다.")
        return None

    # 응답에서 JSON 객체 추출 시도
    try:
        jstart = text.find("{")
        jend = text.rfind("}")
        if jstart != -1 and jend != -1 and jend > jstart:
            json_text = text[jstart:jend+1]
            parsed = json.loads(json_text)
            # followup_question이 물음표로 끝나는지 보장
            fq = parsed.get("followup_question")
            if fq and not fq.strip().endswith("?"):
                parsed["followup_question"] = fq.strip().rstrip('.') + "?"
            # 저장
            st.session_state.ai_response_json = parsed
            # 사람이 볼 수 있도록 원본 텍스트도 반환
            return text
    except Exception:
        # 파싱 실패 시 원본 텍스트 반환
        st.session_state.ai_response_json = {}
        return text

    st.warning("AI 응답이 비어 있거나 차단되었습니다.")
    return None


def _format_error_type(raw: str) -> str:
    """가능하면 한국어(영어 병기) 형태로 포맷합니다. 이미 한국어면 그대로 반환."""
    if not raw:
        return ""
    # 이미 한글을 포함하면 그대로 반환
    if re.search(r"[\u3131-\u318E\uAC00-\uD7A3]", raw):
        return raw
    # 간단한 매핑
    mapping = {
        "Ignoring Multiple Causality": "다중 원인 무시",
        "Multiple Sufficient Conditions": "다중 충분 원인",
        "Single Cause Fallacy": "단일 원인 오류",
        "Ignoring Multiple Causes": "다중 원인 무시",
        "Hasty Generalization": "성급한 일반화",
    }
    # 영어 키에 대해 매핑을 찾음
    for eng, kor in mapping.items():
        if eng.lower() in raw.lower():
            # 원문도 병기
            return f"{kor} ({eng})"
    # 기본: 영어 원문을 괄호로 제공
    return raw

# ---------------- 메인 앱 ----------------
init_session_state()
st.header("AI 논리 배틀 아레나 🧠⚔️")

try:
    st.caption("OpenAI Chat API 사용: 모델 gpt-3.5-turbo (HTTP 호출)")
except Exception:
    pass

# --- 사용자 입력형 API 키 ---
with st.expander("🔐 API Key 설정 (직접 입력)", expanded=False):
    st.markdown("여기에 본인의 ChatGPT API Key를 입력하세요. 입력한 키는 이 세션에만 저장됩니다.")
    # 세션 상태 키와 동일한 key를 사용하면 자동으로 st.session_state에 반영됩니다.
    st.text_input(
        "Google API Key (Gemini용)",
        value=st.session_state.user_gpt_key,
        placeholder="예: ya29.... 또는 sk-...",
        type="password",
        key="user_gpt_key",
    )
    st.caption("※ 키를 빈칸으로 두거나 올바른 키를 사용하지 않으면 호출이 차단됩니다.")

# Step 1
st.subheader("Step 1: AI에게 도전장 내밀기")
# 모둠 이름 입력창 제거(요청에 따라)
st.session_state.student_claim = st.text_area(
    "오류가 포함된 명제 입력",
    value=st.session_state.student_claim,
    placeholder="예: AI가 사람보다 더 빠르게 학습하고 문제를 푸는 시대가 왔으니, 인간의 창의력은 이미 인공지능에게 완전히 뒤처졌다.",
    height=120,
)

# Step 2
st.subheader("Step 2: AI의 반박 확인하기")
col1, col2 = st.columns(2)

with col1:
    if st.button("🤖 AI, 내 주장을 반박해봐!"):
        if not st.session_state.student_claim.strip():
            st.warning("먼저 명제를 입력하세요.")
        else:
            with st.spinner("AI가 반박을 준비하는 중입니다..."):
                ai_out = call_gemini(st.session_state.student_claim)
                if ai_out:
                    st.session_state.ai_response = ai_out
    # 버튼 바로 아래에 간단한 새로고침 안내(아이콘 + 굵은 빨간색)
    st.markdown('<span style="color: red; font-weight: 700;">🔁&nbsp;새로고침:&nbsp;&nbsp;Ctrl+R</span>', unsafe_allow_html=True)

with col2:
    # 오른쪽 칸의 안내문은 제거(위치 이동)
    st.write("")


# 반박 출력
if st.session_state.ai_response:
    st.markdown("### 🤖 AI의 반박 결과")
    # JSON으로 파싱된 구조화 응답이 있으면 구조화하여 표시
    if st.session_state.get("ai_response_json"):
        parsed = st.session_state.ai_response_json
        err_raw = parsed.get('error_type','')
        st.markdown(f"**오류 유형:** {_format_error_type(err_raw)}")
        st.markdown("**정의에 근거한 설명:**")
        st.write(parsed.get('definition_explanation',''))
        st.markdown("**반례:**")
        for ce in parsed.get('counterexamples', []) or []:
            st.write(f"- {ce}")
        st.markdown("**한줄 결론:**")
        st.write(parsed.get('one_line_conclusion',''))

        followup_q = parsed.get('followup_question', '')
        if followup_q and not followup_q.strip().endswith('?'):
            followup_q = followup_q.strip().rstrip('.') + '?'

        st.markdown("**AI가 제시한 질문 (학생이 응답해 보세요):**")
        st.info(followup_q or "이 반박에 대해 어떻게 질문하시겠습니까?")
    else:
        # 파싱된 JSON이 없으면 기존 동작(원문 표시 및 추출기 사용)
        st.markdown(st.session_state.ai_response)
        followup_q = _extract_followup_question(st.session_state.ai_response)
        st.markdown("**AI가 제시한 질문 (학생이 응답해 보세요):**")
        st.info(followup_q)

    # 학생이 그 질문에 답할 수 있는 입력창
    st.session_state.student_followup_answer = st.text_area(
        "학생의 답변",
        value=st.session_state.student_followup_answer,
        placeholder="여기에 학생이 AI 질문에 답한 내용을 입력하세요.",
        height=120,
    )

    if st.button("📘 AI의 최종 평가 및 조언 받기"):
        if not st.session_state.student_followup_answer.strip():
            st.warning("먼저 학생의 답변을 입력하세요.")
        else:
            with st.spinner("AI가 최종 평가와 조언을 작성하는 중입니다..."):
                eval_out = call_gemini_evaluate(
                    st.session_state.student_claim,
                    st.session_state.ai_response,
                    st.session_state.student_followup_answer,
                )
                if eval_out:
                    st.session_state.final_evaluation = eval_out

    if st.session_state.final_evaluation:
        st.markdown("### 📝 AI의 최종 평가 및 조언")
        st.markdown(st.session_state.final_evaluation)