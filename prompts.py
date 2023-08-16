from langchain.prompts import PromptTemplate
prompt_template_questions= """

You are an expert in creating practice question based on study material.
Your goal is to prepare a student for thier an exam. You do this by questions about the text below : 

------------
{text}
------------

Create question that will prepare the student for thier exam. Make sure not to lose any important information.

Questions:

"""
PROMPT_QUESTIONS=PromptTemplate(template=prompt_template_questions, input_variables=["text"])

refine_template_questions=("""
You are an expert in creating practice questions based on study material.
Your goal is to help a student prepare for an exam.
We have recieved some practice questions to a certain extent: {existing_answer}.
We have the option to refine the existing questions or add new ones.
(only_if_necessary) with soome more context below:
                           
------------
{text}
------------

Given the new context, refine the original questions in English.
If the context is not helpful, please provide the original questions.

Questions:
                            
""")

REFINE_PROMPT_QUESTIONS=PromptTemplate(
    input_variables=["existing_answer", "text"],
    template=refine_template_questions
    )