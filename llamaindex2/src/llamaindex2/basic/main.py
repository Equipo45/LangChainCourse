import os
from config import config, setup_console_logger
import nest_asyncio

nest_asyncio.apply()
config()

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI

from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core import Settings, StorageContext, load_index_from_storage

logger = setup_console_logger()
Settings.llm = OpenAI(temperature=0.2, model="gpt-3.5-turbo")
PERSIST_DIR = "./storage"

# Desacargar los datos de aqui
# https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10q/uber_10q_march_2022.pdf
# https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10q/uber_10q_june_2022.pdf
# https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10q/uber_10q_sept_2022.pdf

# DATOS
march_2022 = SimpleDirectoryReader(
    input_files=["./data/10q/uber_10q_march_2022.pdf"]
).load_data()

june_2022 = SimpleDirectoryReader(
    input_files=["./data/10q/uber_10q_june_2022.pdf"]
).load_data()

sept_2022 = SimpleDirectoryReader(
    input_files=["./data/10q/uber_10q_sept_2022.pdf"]
).load_data()

# BASE DE DATOS DE VECTORES [3342,423423,423423]

def _index_data(data_name, data):
    if not os.path.exists(PERSIST_DIR+"_"+data_name):
        index = VectorStoreIndex.from_documents(data)
        index.storage_context.persist(persist_dir=PERSIST_DIR+"_"+data_name)
        logger.info(f"{data_name} has been indexed.")
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR+"_"+data_name)
        index = load_index_from_storage(storage_context)
    logger.info(f"{data_name} index has been logged.")
    return index

march_index = _index_data("march", march_2022)
june_index = _index_data("june", june_2022)
sept_index = _index_data("sept", sept_2022)


# MOTORES PARA HACER QUERIES
march_engine = march_index.as_query_engine(similarity_top_k=3)
june_engine = june_index.as_query_engine(similarity_top_k=3)
sept_engine = sept_index.as_query_engine(similarity_top_k=3)

# HERAMMIENTA MONTADA PARA PODER BUSCAR
query_engine_tools = [
    QueryEngineTool(
        query_engine=sept_engine,
        metadata=ToolMetadata(
            name="sept_22",
            description=(
                "Provides information about Uber quarterly financials ending"
                " September 2022"
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=june_engine,
        metadata=ToolMetadata(
            name="june_22",
            description=(
                "Provides information about Uber quarterly financials ending"
                " June 2022"
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=march_engine,
        metadata=ToolMetadata(
            name="march_22",
            description=(
                "Provides information about Uber quarterly financials ending"
                " March 2022"
            ),
        ),
    ),
]

# MOTOR MONTADO CON LAS HERRAMIENTAS
s_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools
)

# RESPUESTAS
response = s_engine.query(
    "Analyze Uber revenue in the last two quarters"
)
print(response)
