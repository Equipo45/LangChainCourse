import argparse

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings

from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

MODEL = "llama2"

def main():
    parser = argparse.ArgumentParser(description="Filtrar el argumentod de URL.")
    parser.add_argument(
        "--url",
        type=str,
        default="http://as.com",
        required=True,
        help="La URL para buscar.",
    )

    args = parser.parse_args()
    url = args.url
    print(f"usando la URL: {url}")

    loader = WebBaseLoader(url)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    all_splits = text_splitter.split_documents(data)
    print(f"Dividido en {len(all_splits)} partes")

    vectorstore = Chroma.from_documents(
        documents=all_splits, embedding=GPT4AllEmbeddings()
    )

    question = "Make me a summary of the most important headlines in {url}?"
    docs = vectorstore.similarity_search(question)

    print(f"Documentos {len(data)} cargados")
    print(f"Recuperado {len(docs)} documents")

    from langchain import hub
    #https://smith.langchain.com/hub/rlm
    QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")

    llm = Ollama(
        model=MODEL,
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    print(f"Modelo {llm.model} cargado")

    from langchain.chains import RetrievalQA

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    question = f"Show me the most important headlines of {url}"
    qa_chain.invoke({"query": question})


if __name__ == "__main__":
    main()
