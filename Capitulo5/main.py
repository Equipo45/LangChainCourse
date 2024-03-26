from langchain_community.chat_models  import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from streamlit_chat import message

INITIAL_STATE = "Continue the conversation"

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
model_name = st.sidebar.radio("Elegir modelo:", ("gemma", "llama2", "mixtral"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Coste total de la conversación: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Limpiar conversación", key="clear")
llm = ChatOllama(model=model_name,
            temperature=0.0,
             )

if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": INITIAL_STATE}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    
def list_to_dicts(dict_list):
    cadena_resultado = ""
    for dictionary in dict_list:
        cadena_resultado += f"Role: {dictionary['role']}, MSG: {dictionary['content']}\n"
        
    return cadena_resultado

def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    chain = llm | StrOutputParser()
    response = chain.invoke(list_to_dicts(st.session_state['messages']))
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response

prompt = st.chat_input("Dime algo majo!")
response_container = st.container()

if prompt:
    output = generate_response(prompt)
    st.session_state['past'].append(prompt)
    st.session_state['generated'].append(output)
    st.session_state['model_name'].append(model_name)
    
if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")