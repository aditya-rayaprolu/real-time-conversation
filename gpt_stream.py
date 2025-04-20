import openai
from config import OPENAI_API_KEY, GPT_MODEL

openai.api_key = OPENAI_API_KEY

async def stream_gpt_reply(conversation_history):
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=conversation_history,
        stream=True
    )
    partial_reply = ""
    print("[Assistant Partial]: ", end="", flush=True)
    for chunk in response:
        if 'choices' in chunk and len(chunk['choices']) > 0:
            delta = chunk['choices'][0]['delta']
            if 'content' in delta:
                token = delta['content']
                partial_reply += token
                print(token, end="", flush=True)
    print("\n")
    return partial_reply