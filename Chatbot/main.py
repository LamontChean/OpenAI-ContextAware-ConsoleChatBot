from openai import OpenAI
from dotenv import load_dotenv
import os
import json
    
load_dotenv()

def chatbot_response(client, chat_history, prompt):
    chat_history.append({"role":"user", "content":prompt})
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=chat_history
    )
    chat_history.append({"role":"assistant", "content":completion.choices[0].message.content})
    return completion.choices[0].message.content

# Load chat history if exists
def load_chat_history(file_path=os.getenv("HISTORY_PATH")):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return [{"role": "system", "content": "You're my assistant."}]

# Save chat history
def save_chat_history(history, file_path=os.getenv("HISTORY_PATH")):
    with open(file_path, "w") as f:
        json.dump(history, f, indent=2)

def start_up() -> tuple:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chat_history = load_chat_history()
    return client, chat_history

def main():
    # Then modify your main loop:
    client, chat_history = start_up()

    print("Hello! Tell me something ('quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            save_chat_history(chat_history)
            break
        answer = chatbot_response(client, chat_history, user_input)
        print("Bot: ", answer)


if __name__ == "__main__":
    main()