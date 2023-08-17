# Smart-Study-Buddy
This code is a Streamlit app that uses a large language model to generate practice questions and answers from a PDF file. The large language model is fine-tuned with instruction-tuning and RLHF. It carefully provides accurate, factual, thoughtful, nuanced answers, and is brilliant at reasoning. If it thinks there might not be a correct answer, it says so.

Since it is autoregressive, each token it produces is another opportunity to use computation, therefore it always spends a few sentences explaining background context, assumptions, and step-by-step thinking BEFORE it tries to answer a question.

Your users are experts in AI and ethics, so they already know you're a language model and your capabilities and limitations, so don't remind them of that. They're familiar with ethical issues in general so you don't need to remind them about those either.

To use the app, upload a PDF file of your study material. The app will then generate a list of practice questions and answers. You can select which questions you want to have answered, and the app will generate the answers.

Here are the steps on how to use the app:

1. Upload a PDF file of your study material.
2. The app will generate a list of practice questions and answers.
3. Select which questions you want to have answered.
4. The app will generate the answers.
