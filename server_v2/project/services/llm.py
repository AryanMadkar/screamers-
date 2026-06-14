import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = None

def get_llm():
    global llm

    if llm is None:
        # Get config from env/dotenv
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_MODEL", "llama3-8b-8192")

        # Strip optional wrapping quotes from .env value
        if api_key:
            api_key = api_key.strip('"\'')

        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is not configured! Please open your '.env' file and "
                "set your real Groq API key in the GROQ_API_KEY field."
            )

        llm = ChatGroq(
            model=model,
            temperature=0.9,
            api_key=api_key
        )

    return llm


def generate_response(user_message):
    llm = get_llm()

    messages = [
        SystemMessage(
            content="""
You are Priya, a professional real estate consultant.

Rules:
- Keep replies short.
- Be polite.
- Never hallucinate.
- Ask one follow-up question.
- Never invent property details.
- If unsure say "Let me check our listings."
"""
        ),
        HumanMessage(content=user_message)
    ]

    response = llm.invoke(messages)
    return response.content