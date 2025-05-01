from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from typing import List, Dict
import os

class LLMService:
    def __init__(self):
        llm_server_url = os.getenv("LLM_SERVER_URL", "http://host.docker.internal:8080")
        self.llm = ChatOpenAI(
            openai_api_base=f"{llm_server_url}/v1",
            openai_api_key="not-needed",
            model="google_gemma-3-27b-it",
            temperature=0.7,
            max_tokens=100,
            timeout=60  # Increased timeout for local processing
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["messages"],
            template="""{messages}"""
        )

    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        formatted_messages = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            formatted_messages.append(f"{role}: {content}")
        return "\n".join(formatted_messages)

    async def create_chat_completion(self, request_data: Dict) -> str:
        try:
            formatted_messages = self.format_messages(request_data["messages"])
            formatted_prompt = self.prompt_template.format(messages=formatted_messages)
            
            response = self.llm.invoke(formatted_prompt)
            return response.content
        except Exception as e:
            print(f"Error in create_chat_completion: {str(e)}")
            raise 