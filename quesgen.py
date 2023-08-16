import streamlit as st
from llm_functions import load_data, split_text, initialize_llm, generate_questions, create_retrieval_qa_chain 
#initialize of session states
#since streamlit always reruns the script when a widget changes, we need to initialize the session states
if 'questions' not in st.session_state:
    st.session_state['questions']='empty'
    st.session_state['separated_questions_list']='empty'
    st.session_state['questions_to_answers']='empty'
    st.session_state['submitted']='empty'
with st.container():
    st.markdown("""# Smart Study Buddy""")

#get user's openai api key
openai_api_key=st.text_input(label="openAI API Key", placeholder="Ex sk-ztsh9h9jsoka...", key="openai_api_key_input", help="How to get an OpenAI API key: https://platform.openai.com/account/api-keys/")

with st.container():
    st.markdown("""Make sure you've entered your openAI API key.
                Don't have an API Key yet?
                Read [this]:(https://medium.com/@joristechtalk/how-to-get-an-openai-api-key-for-chatgpt-fd2cf6a436c5) article on how to get an API key.) 
""")

#let user upload a file
uploaded_file=st.file_uploader("Upload your study material", type=['pdf'])

if uploaded_file is not None:
    #check whether user entered an api key
    if not openai_api_key:
        st.error("Please enter your openai key 🤖 ")
    else:
        #load data from pdf
        text_from_pdf=load_data(uploaded_file)

        #split text for question generation
        documents_for_question_gen=split_text(text_from_pdf, chunk_size=10000, chunk_overlap=200)

        #split text fo question answering
        documents_for_question_answering= split_text(text_from_pdf, chunk_size=500, chunk_overlap=200)

        #initialize large language model
        llm_question_gen=initialize_llm(openai_api_key=openai_api_key, model="gpt-3.5-turbo-16k", temperature=0.4)

        #initialize large language model for question answering
        llm_question_answering=initialize_llm(openai_api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.1)

        #create question if they have not been generated
        if st.session_state['questions'] == 'empty':
            with st.spinner("Generating questions...."):
                #Assign the generated questions to the state.This way, the questions are only generated once
                st.session_state['questions']=generate_questions(llm=llm_question_gen, chain_type="refine", documents=documents_for_question_gen)
        
        if st.session_state['questions']!='empty':
            #show questions on screen. you couls use st.code for easy copy-pasting
            st.info(st.session_state['questions'])

            #Split questions in list
            st.session_state(['questions'])

            with st.form(key='my_form'):
                #create a list of questions that have to be aswerered
                st.session_state['questions_to_answers']= st.multiselect(label="select question to answer", options=st.session_state['questions_list'])
                submitted=st.form_submit_button('Generate answeres')
                if submitted:
                    st.session_state['submitted']=True

            if st.session_state['submitted']:
                #initialize the retrieval qa chain
                with st.spinner("Generating answers...."):
                    generate_answer_chain=create_retrieval_qa_chain(openai_api_key=openai_api_key,documents=documents_for_question_answering, llm=llm_question_answering)

                    #for each question geneate an answer
                    for question in st.session_state['questions_to_answers']:
                        #generate answer
                        answer=generate_answer_chain.run(question)

                        #show answer on screen
                        st.write(f"Question: {question}")
                        st.info({f"Answer : {answer}"})

            