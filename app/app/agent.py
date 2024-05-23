import logging
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.documents.base import Document

class Agent():
    def __init__(self, model_name='llama3', url_ollama = 'http://host.docker.internal:11434'):
        self.model_name = model_name
        self.url_ollama = url_ollama

    def summary_chain(self, docs: list[Document]):
        prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> 
            You are an assistant for helping summarizing documents. 
            Use the following pieces of retrieved documents to generate a summary. 
            
            Use four sentences maximum and keep the answer concise. no preamble or explanation<|eot_id|><|start_header_id|>user<|end_header_id|>

            Context: {context} 
            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["question", "document"],
        )

        llm = ChatOllama(model=self.model_name, temperature=0, base_url=self.url_ollama)


        # Post-processing
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)


        # Chain
        rag_chain = prompt | llm | StrOutputParser()

        return rag_chain.invoke({"context": docs})
