from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Use local LlamaServer endpoint
llm = ChatOpenAI(
    openai_api_base="http://127.0.0.1:8080/v1",
    openai_api_key="not-needed",  # Dummy key; llama-server ignores this
    model="gemma-3-27b-it",  # Can be anything; llama-server doesn't validate this
    temperature=0.7,
)

# Optional: Define a prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer the following question clearly:\n\n{question}"
)

# Format prompt
formatted_prompt = prompt.format(question="What are the benefits of using AI in healthcare?")

# Call model
response = llm.invoke(formatted_prompt)

print(response.content)
