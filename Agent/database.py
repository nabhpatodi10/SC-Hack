from dotenv import load_dotenv
load_dotenv()

import os
from langchain_mongodb import MongoDBChatMessageHistory
from langchain.schema.messages import AIMessage, HumanMessage, BaseMessage

class Database:

    def __init__(self, session_id: str):
        self.__chat_history = MongoDBChatMessageHistory(connection_string=os.getenv("MONGODB_URI"), database_name="LangChain", collection_name="chats", session_id=session_id)
        
    def add_human_message(self, message: str | HumanMessage) -> None:
        try:
            self.__chat_history.add_user_message(message)
        except Exception as error:
            raise error
        
    def add_ai_message(self, message: str | AIMessage) -> None:
        try:
            self.__chat_history.add_ai_message(message)
        except Exception as error:
            raise error
        
    def add_message(self, message: BaseMessage) -> None:
        try:
            self.__chat_history.add_message(message)
        except Exception as error:
            raise error
        
    def get_messages(self) -> list:
        try:
            return self.__chat_history.messages
        except Exception as error:
            raise error
        
    def clear_chat(self) -> None:
        try:
            self.__chat_history.clear()
        except Exception as error:
            raise error
        
    def close_connection(self) -> None:
        del self.__chat_history