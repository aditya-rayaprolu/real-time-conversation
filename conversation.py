from gpt_stream import stream_gpt_reply

conversation_history = []

async def handle_user_utterance(user_text):
    # 1) Add user to history
    conversation_history.append({"role": "user", "content": user_text})

    # 2) Get GPT's streaming reply
    ai_reply = await stream_gpt_reply(conversation_history)

    # 3) Append GPT reply to history
    conversation_history.append({"role": "assistant", "content": ai_reply})

    # 4) (Optional) Limit conversation to last N turns
    if len(conversation_history) > 10:
        conversation_history.pop(0)
        conversation_history.pop(0)