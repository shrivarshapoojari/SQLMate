# import streamlit as st
# from pathlib import Path
# from langchain.agents import  create_sql_agent
# from langchain.sql_database import SQLDatabase
# from langchain.callbacks import StreamlitCallbackHandler
# from langchain.agents.agent_types import AgentType
# from  langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from flask import Flask, request, jsonify
# from sqlalchemy import create_engine
# import sqlite3
# from langchain_groq import ChatGroq

# from flask_cors import CORS 

# app = Flask(__name__)
# CORS(app) 

# LOCALDB = "USE_LOCALDB"
# MYSQL = "USE_MYSQL"

# def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
#     if db_uri==LOCALDB:
#         dbfilepath=(Path(__file__).parent/"student.db").absolute()
#         print(dbfilepath)
#         creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
#         return SQLDatabase(create_engine("sqlite:///", creator=creator))
#     elif db_uri==MYSQL:
#         if not (mysql_host and mysql_user and mysql_password and mysql_db):
#             return jsonify({"error": "plzz provid db details"}), 400
            
#         return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))   
    

# @app.route('/ask_sql', methods=['POST'])
# def ask_sql():
#     data = request.json
#     user_query = data['query']
#     db_uri = data.get('db_uri')
#     api_key = data.get('api_key')
#     print(db_uri)
#     if not db_uri or not api_key:
#         return jsonify({"error": "Database URI and API key are required"}), 400

#     # Initialize the ChatGroq LLM
#     llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

 
    
#     db=configure_db(db_uri)
#     # Initialize toolkit and agent
#     toolkit = SQLDatabaseToolkit(db=db, llm=llm)
#     agent = create_sql_agent(
#         llm=llm,
#         toolkit=toolkit,
#         verbose=True,
#         agent_type="ZERO_SHOT_REACT_DESCRIPTION"
#     )

#     # Process the query
#     response = agent.run(user_query)
#     return jsonify({"response": response})

# if __name__ == '__main__':
#     app.run(debug=True)




import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
      dbfilepath=(Path(__file__).parent/"student.db").absolute()
      print(dbfilepath)
      creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
      return SQLDatabase(create_engine("sqlite:///", creator=creator))

@app.route('/ask_sql', methods=['POST'])
def ask_sql():
    data = request.json
    user_query = data['query']
    db_uri = data.get('db_uri')
    api_key = data.get('api_key')
    
    if not db_uri or not api_key:
        return jsonify({"error": "Database URI and API key are required"}), 400

    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

    db = configure_db(db_uri)
    if db is None:
        return jsonify({"error": "Invalid database configuration"}), 400
    
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

    response = agent.run(user_query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
