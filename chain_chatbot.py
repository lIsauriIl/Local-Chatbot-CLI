from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
import ollama

def run_chatbot(model_name: str, prompted: bool = False):
    """
    Runs a chatbot session with the specified model.

    Args:
        model_name (str): The name of the model to use.
        prompted (bool): Whether to prompt the user for chatbot guidelines.

    """
    model = ChatOllama(model=model_name)
    session_ids = {}

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        """
        Retrieves the chat history for a given session ID. Creates a new history if not found.

        Args:
            session_id (str): The session ID.

        Returns:
            BaseChatMessageHistory: The chat history for the session.
        """
        if session_id not in session_ids:
            session_ids[session_id] = ChatMessageHistory()
        return session_ids[session_id]

    def list_session_ids():
        """Prints all current session IDs."""
        print('Session IDs:')
        for key in session_ids.keys():
            print(key)

    def create_prompt(system_prompt: str) -> ChatPromptTemplate:
        """
        Creates a prompt template with a system message and a placeholder for user messages.

        Args:
            system_prompt (str): The system message to include in the prompt.

        Returns:
            ChatPromptTemplate: The constructed prompt template.
        """
        return ChatPromptTemplate.from_messages([
            ('system', system_prompt + ' And if someone asks you how to exit, tell them to type "select session" in lowercase.'),
            MessagesPlaceholder(variable_name='messages')
        ])

    if not prompted:
        runnable = RunnableWithMessageHistory(model, get_session_history)

    while True:
        list_session_ids()
        session_id_input = input("Enter session id, or enter 'exit chatbot': ").strip()
        if session_id_input == 'exit chatbot':
            break

        if prompted:
            sys_prompt = input('Tell the chatbot what kind of chatbot it is, or "select session" to back: ').strip()
            if sys_prompt == "select session":
                break

            prompt = create_prompt(sys_prompt)
            chain = prompt | model
            runnable = RunnableWithMessageHistory(chain, get_session_history)

        while True:
            config = {'configurable': {'session_id': session_id_input}}
            human_query = input('Enter query or "select session" to go to menu: ').strip()
            if human_query == 'select session':
                break

            response = runnable.invoke({'messages': [human_query]}, config=config)
            print(response.content)

def pull_model(model_name: str):
    """
    Pulls a model using the ollama library.

    Args:
        model_name (str): The name of the model to pull.
    """
    ollama.pull(model_name)

def list_models() -> list:
    """
    Lists all installed models using the ollama library.

    Returns:
        list: A list of installed model names.
    """
    return [model['name'] for model in ollama.list()['models']]

def ensure_model_installed(model_name: str):
    """
    Ensures that a model is installed. Prompts the user to pull the model if it is not installed.

    Args:
        model_name (str): The name of the model to check and install.
    """
    while True:
        pull_confirm = input('Model is not installed. Do you want to download it? (Y/n): ').strip()
        if pull_confirm.lower() == 'y':
            pull_model(model_name)
            break
        elif pull_confirm.lower() == 'n':
            break

def main():
    """
    The main function that runs the chatbot application.
    """
    while True:
        model_list = list_models()
        model_input = input("Choose model, or type 'list models' to see list of installed models, or 'exit' to exit: ").strip()
        if model_input == 'exit':
            break
        elif model_input == 'list models':
            print(model_list)
        else:
            prompted = input('Do you want to set guidelines for your chatbot? (Y/n): ').strip().lower() == 'y'
            try:
                run_chatbot(model_name=model_input, prompted=prompted)
            except Exception:
                ensure_model_installed(model_input)

main()