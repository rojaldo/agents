import autogen
from ..models import AgentRequest
from .common import get_humor_instruction

class AutoGenService:
    def run_agent(self, request: AgentRequest) -> str:
        humor_instruction = get_humor_instruction(request.humor_setting)
        
        config_list = [
            {
                "model": "llama3.2:3b",
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
            }
        ]
        
        llm_config = {
            "config_list": config_list,
            "temperature": 0.7,
        }

        assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config=llm_config,
            system_message=f"You are a helpful AI assistant. {humor_instruction}"
        )

        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
        )

        chat_res = user_proxy.initiate_chat(
            assistant,
            message=request.message,
            summary_method="last_msg"
        )
        
        response_text = "No response"
        if hasattr(chat_res, 'summary'):
            response_text = chat_res.summary
        elif hasattr(chat_res, 'chat_history'):
             if chat_res.chat_history:
                 response_text = chat_res.chat_history[-1]['content']
                 
        return response_text
