# %%[markdown]
# ## Reproduce langchaing notebooks

# %%
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from sqlalchemy import create_engine


# %%
# engine = create_engine("sqlite:///./example_data/Chinook.db", connect_args={'mode': 'ro'}, uri=True)
# # perform a read-only query using the engine
# with engine.connect() as connection:
#     result = connection.execute('SELECT * FROM Employee')
#     for row in result:
#         print(row)

# %%
# db = SQLDatabase(engine)
db = SQLDatabase.from_uri("sqlite:///./example_data/Chinook.db")
# db = SQLDatabase.from_uri(
#     "sqlite:///./example_data/Chinook.db?"
#     "check_same_thread=true&timeout=10&mode=ro&nolock=1&uri=true"
#)
# llm = OpenAI(model_name="gpt-3.5-turbo" ,temperature=0)
llm = ChatOpenAI(model_name="gpt-3.5-turbo" ,temperature=0)
# llm = ChatOpenAI(model_name="gpt-4" ,temperature=0)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
db_chain.run("How many employees are there?")

# %%[markdown]
# ## Customized Prompts

# %%
from langchain.prompts.prompt import PromptTemplate

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

If someone asks for the table foobar, they really mean the employee table.

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)

# %%
db_chain = SQLDatabaseChain(llm=llm, database=db, prompt=PROMPT, verbose=True)

# %%
db_chain.run("How many employees live in Calgary City?")

# %%[markdown]
# ## Return intermediate steps

# %%
db_chain = SQLDatabaseChain(llm=llm, database=db, prompt=PROMPT, verbose=True, return_intermediate_steps=True)

# %%
result = db_chain("How many employees do not live in Calgary City?")

# %%
result = db_chain("What is the name and title of the oldest employee")

# %%
result = db_chain("What is the name of the customer with most number of invoices and state the total count of invoices")

# %%
result = db_chain("remove details of customers living in USA")

# %%[markdown]
# ## SCRATCH

# %%
# perform a read-only query using the engine
with engine.connect() as connection:
    result = connection.execute('SELECT * FROM my_table')
    for row in result:
        print(row)
