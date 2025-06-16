from gpt_functions import get_current_time, tools
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키 가져오기

client = OpenAI(api_key=api_key)  # 오픈AI 클라이언트의 인스턴스 생성

def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",  # 응답 생성에 사용할 모델 지정
        messages=messages,  # 대화 기록을 입력으로 전달
        tools=tools,  # 사용 가능한 도구 목록 전달
    )
    return response  # 생성된 응답 내용 반환

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"system","content":"너는 사용자를 도와주는 상담사야."},
    ]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
if user_input := st.chat_input():
    st.session_state.messages.append({"role":"user","content":user_input})
    st.chat_messages("user").write(user_input)
    
    ai_respose=gpt_ai_response(st.session_state.messages, tools=tools)
    print(ai_response)
    ai_message=ai_message.tool_calls
    if tools_call in tool_calls:
        tool_name = tool_call.function.name
        tool_call_id=tool_call.id
        arguments=json.loads(tool_call.function.arguments) #문자열을 딕셔너리로 변경
        
        if tool_name == "get_current_time":
            st.session_state.messages.append({
                "role":"function",
                "tool_call_id":tool_call_id,
                "name":tool_name,
                "content":get_current_time(timezone=arguments['timezone']),
            })
    st.session_state.messages.append({"role":"system", "content": "이제 주어진 결과를바탕으로 답현할 차례입니다."})
    ai_response=get_ai_response(st.session_state.messages)
    ai_message=ai_response.choices[0].message

st.session_state.messages.append({
    "role":"assistant",
    "content":ai_message.content
})

print("AI\t: " + ai_message.content)  # AI 응답 출력
st.chat_message("assistant").write(ai_message.content)
    
    