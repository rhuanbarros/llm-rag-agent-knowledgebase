import logging
from injector import inject
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.documents.base import Document

from typing import List

from procurador.models import MessageModel
from procurador.services.vectorstore import VectorStoreService
from procurador.services.llm import LlmService

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from typing_extensions import TypedDict
from typing import List
from langchain_core.documents import Document

from langgraph.graph import END, StateGraph

class AgentReflectiveRetrieval():
    @inject
    def __init__(self, llmService: LlmService, vectorStoreService: VectorStoreService):
        self.llmService = llmService
        self.vectorStoreService = vectorStoreService

    def main_chain(self, chatHistory: List[MessageModel], model ):
        
        self.model = model        

        class GraphState(TypedDict):
            """
            Represents the state of our graph.

            Attributes:
                question: question
                generation: LLM generation
                web_search: whether to add search
                documents: list of documents
            """

            question: str
            generation: str
            documents: List[str]

       

        workflow = StateGraph(GraphState)
        workflow.add_node("retrieve", self.retrieve_documents)  # retrieve
        # workflow.add_node("grade_documents", grade_documents)  # grade documents
        workflow.add_node("generate", self.generate)  # generatae

        # Build graph
        workflow.set_entry_point('retrieve')

        workflow.add_edge("retrieve", "generate")
        # workflow.add_edge("retrieve", "grade_documents")
        # workflow.add_conditional_edges(
        #     "grade_documents",
        #     decide_to_generate,
        #     {
        #         "websearch": "websearch",
        #         "generate": "generate",
        #     },
        # )
        # workflow.add_edge("websearch", "generate")
        workflow.add_conditional_edges(
            "generate",
            self.grade_generation_v_documents_and_question,
            {
                "not supported": "generate",
                "useful": END,
                # "not useful": "websearch",
            },
        )

        chain = workflow.compile()
        
        return chain.invoke( { 'question': chatHistory[-1].Content })

        
    
    def rag_chain(self, model):
        '''
            RAG - Retrieval augmented generation chain
        '''

        # Prompt
        prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> 
            You are an assistant helping the user absorve and understand a great amount of information. 
            The user provide a Query that could be a real question or just keywords used in the document retriver.
            Also is provided a Context that are the documents retrived using the Query.
            If the Query is a question, you should generate a answer to the question using the provided context. 
                If you don't know the answer, just say that you don't know and generate a summary as stated below.
            If the Query are keywords, you should generate a summary of the documents and point how these documents are relevant to the query.
            
            Your answer should be 5 lines maximum and keep the answer concise.
            Use bullet list to help understanding.
            Answer ONLY in Brazilian Portuguese.

            Example of answer:
            '* Documentos 1 e 2 discutem a memória curta e longa em relação à LLM.
            * O documento 3 apresenta uma discussão mais geral sobre a memória humana e sua aplicação na inteligência artificial.'

            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Query: {question} 
            Context: {context} 
            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["question", "document"],
        )

        llm = self.llmService.get_provider(model)

        # Post-processing
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)


        # Chain
        rag_chain = prompt | llm | StrOutputParser()

        return rag_chain

    def retrieval_grader_chain(self, model):
        '''
        Grade one document if it is relavant to a user query
        '''
        
        llm = self.llmService.get_provider(model, format='json')
        
        prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing relevance 
            of a retrieved document to a user question. If the document contains keywords related to the user question, 
            grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
            Provide the binary score as a JSON with a single key 'score' and no premable or explanation.
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Here is the retrieved document: \n\n {document} \n\n
            Here is the user question: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """,
            input_variables=["question", "document"],
        )

        retrieval_grader = prompt | llm | JsonOutputParser()
        
        return retrieval_grader

    def hallucionation_checker_chain(self, model):
        '''
            Check if the generated answer have halucination. Verify if it is based in the documents.
        '''

        # Prompt
        prompt = PromptTemplate(
            template=""" <|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether 
            an answer is grounded in / supported by a set of facts. Give a binary 'yes' or 'no' score to indicate 
            whether the answer is grounded in / supported by a set of facts. Provide the binary score as a JSON with a 
            single key 'score' and no preamble or explanation. <|eot_id|><|start_header_id|>user<|end_header_id|>
            Here are the facts:
            \n ------- \n
            {documents} 
            \n ------- \n
            Here is the answer: {generation}  <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "documents"],
        )

        llm = self.llmService.get_provider(model, format='json')

        hallucination_grader = prompt | llm | JsonOutputParser()

        return hallucination_grader
    
    def answer_useful_chain(self, model):
        '''
            Verify if the generate answer is useful to answer the question.
        '''

        # Prompt
        prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether an 
            answer is useful to resolve a question. Give a binary score 'yes' or 'no' to indicate whether the answer is 
            useful to resolve a question. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            <|eot_id|><|start_header_id|>user<|end_header_id|> Here is the answer:
            \n ------- \n
            {generation} 
            \n ------- \n
            Here is the question: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "question"],
        )
        
        llm = self.llmService.get_provider(model, format='json')

        answer_grader = prompt | llm | JsonOutputParser()

        return answer_grader
    
    def retrieve_documents(self, state):
        print("---RETRIEVE---")
        index_name = 'index_1'
        
        question = state["question"]
        retriever = self.vectorStoreService.get_retriever(index_name)

        # Retrieval
        documents = retriever.invoke(question)
        return {"documents": documents, "question": question}
    
    def generate(self, state):
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]

        # RAG generation
        rag_chain = self.rag_chain(self.model)
        generation = rag_chain.invoke({"context": documents, "question": question})
        return {"documents": documents, "question": question, "generation": generation}
    
    def grade_documents(self, state):
        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        retrieval_grader = self.retrieval_grader_chain()

        # Score each doc
        filtered_docs = []
        web_search = "No"
        for d in documents:                
            score = retrieval_grader.invoke(
                {"question": question, "document": d.page_content}
            )
            grade = score["score"]
            # Document relevant
            if grade.lower() == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            # Document not relevant
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                # We do not include the document in filtered_docs
                # We set a flag to indicate that we want to run web search
                web_search = "Yes"
                continue
        return {"documents": filtered_docs, "question": question, "web_search": web_search}

    def grade_generation_v_documents_and_question(self, state):
        print("---CHECK HALLUCINATIONS---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]

        hallucination_grader = self.hallucionation_checker_chain(self.model)
        # answer_grader = self.answer_useful_chain(self.model)

        score = hallucination_grader.invoke(
            {"documents": documents, "generation": generation}
        )
        try:
            grade = score["score"]
        except:
            print("EXCEPTIION!!!")
            print("score")
            print(score)
            return

        # Check hallucination
        if grade == "yes":
            print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
            return "useful"
            # Check question-answering
            # print("---GRADE GENERATION vs QUESTION---")
            # score = answer_grader.invoke({"question": question, "generation": generation})
            # grade = score["score"]
            # if grade == "yes":
            #     print("---DECISION: GENERATION ADDRESSES QUESTION---")
            #     return "useful"
            # else:
            #     print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            #     return "not useful"


        else:
            print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
            return "not supported"
    