from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = None


def get_llm():
    global llm

    if llm is None:
        llm = ChatOllama(
            model="phi3",
            temperature=0.9,
            top_p=0.9,              # nucleus sampling
            top_k=40,               # limits token choices
            num_predict=256,        # max tokens to generate (keep low for speed)
            num_ctx=2048,           # context window (lower = faster)
            repeat_penalty=1.1
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