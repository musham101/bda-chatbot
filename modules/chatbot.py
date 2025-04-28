from langchain_ollama import OllamaLLM


llm = OllamaLLM(model="llama3")


class Chatbot:
    def format_docs(docs):
        return "\n\n\n".join(
                f"{doc.page_content}"
                for doc in docs
        )
    
    def simple_response(user_query):
        return llm.invoke(user_query)
    
    def rag_response(retriever, user_query):
        prompt_template = """given some data, i want you to answer the user query.
documents:
{context}

user query:
{question}

make sure to refer to the files path you used at the end of your response.
"""

        relevant_docs = retriever.invoke(user_query)


        relevant_docs = Chatbot.format_docs(relevant_docs)

        # print(relevant_docs)

        return llm.invoke(prompt_template.format(context=relevant_docs, question=user_query)), relevant_docs
    