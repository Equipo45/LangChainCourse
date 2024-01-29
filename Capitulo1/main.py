from langchain.prompts import ChatPromptTemplate
from langchain_openai  import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader

import key
#Recuerda poner tu key
KEY = key.OPEN_AI_KEY()

loader = PyPDFLoader("datos/DIEEEINV07_2020JUAESC_MENA (1).pdf")
pages = loader.load_and_split()


vectorstore = FAISS.from_documents(
    pages, embedding=OpenAIEmbeddings(openai_api_key=KEY)
)

retriever = vectorstore.as_retriever()

template = """Responde a mi pregunta en base al siguientes contexto:
{contexto}

Pregunta: {pregunta}"""

prompt = ChatPromptTemplate.from_template(template=template)

# Inicializa el modelo LLM (puedes elegir el modelo específico que desees usar)
llm = ChatOpenAI(model_name="gpt-4",openai_api_key=KEY)

# Output parser
parser = StrOutputParser()
# Crea una cadena de procesamiento con un solo componente (el modelo LLM)
chain = {"contexto": retriever, "pregunta": RunnablePassthrough()} | prompt | llm | parser 

# Imprime la respuesta del modelo
print(chain.invoke("Resumeme el contenido del texto"))
