from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from prompts import PROMPT_QUESTIONS, REFINE_PROMPT_QUESTIONS
from PyPDF2 import PdfReader

#Function to load data from pdf
def load_data(uploaded_file):
    #Load data  from pdf
    pdf_reader=PdfReader(uploaded_file)
    #Combine text from Document to strings
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()
    
    return text

#Function to split text into chunks
def split_text(text,chunk_size, chunk_overlap):
    #initialize text splitter
    text_splitter=TokenTextSplitter(model_name="gpt-3.5-turbo-16k",text=text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    #split_text into chunks
    text_chunks=text_splitter.split_text(text)

    #convert chunks to document
    documents=[Document(page_content=t) for t in text_chunks]

    return documents

#Function to initialize large language model
def initialize_llm(openai_api_key, model, temperature):
    #initialize large language model
    llm=ChatOpenAI(openai_api_key=openai_api_key, model=model, temperature=temperature)

    return llm
#function to generate questions
def generate_questions(llm, chain_type, documents):
    #initialize question chain
    question_chain=load_summarize_chain(llm=llm, chain_type=chain_type, qustion_prompt=PROMPT_QUESTIONS, refine_prompt=REFINE_PROMPT_QUESTIONS)

    #generate questions
    questions=question_chain.run(documents)
    return questions

#Function to create Retrieval QA chain

def create_retrieval_qa_chain(openai_api_key, documents, llm):
    #set embeddings
    embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key)

    #Create vector database
    vector_database=Chroma.from_documents(documents=documents, embeddings=embeddings)

    #Create Retrieval QA chain
    retrieval_qa_chain=RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_database.as_retriever())

    return retrieval_qa_chain
