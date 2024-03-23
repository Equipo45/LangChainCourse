from openai import OpenAI
import streamlit as st
from streamlit_chat import message
import key

INITIAL_STATE = "Eres un asistente de voz vacilón"

client = OpenAI(api_key=key.GET_OPEN_API_KEY())

st.set_page_config(page_title="IRR Tutorial", page_icon="🖥")
st.write("<h1 style='text-align: center;'>Habla con el chat vacilón</h1>", unsafe_allow_html=True)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": INITIAL_STATE}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

st.sidebar.title("Aqui se muestran los st.sidebar")
model_name = st.sidebar.radio("Elegir modelo:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Coste total de la conversación: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Limpiar conversación", key="clear")

if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": INITIAL_STATE}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Coste total de la conversación: ${st.session_state['total_cost']:.5f}")


def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(model=model,
    messages=st.session_state['messages'])
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

prompt = st.chat_input("Dime algo majo!")
response_container = st.container()

if prompt:
    output, total_tokens, prompt_tokens, completion_tokens = generate_response(prompt)
    st.session_state['past'].append(prompt)
    st.session_state['generated'].append(output)
    st.session_state['model_name'].append(model_name)
    st.session_state['total_tokens'].append(total_tokens)

    if model_name == "GPT-3.5":
        cost = total_tokens * 0.002 / 1000
    else:
        cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

    st.session_state['cost'].append(cost)
    st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")