# %%[markdown]
# ## Reproduce langchaing notebooks

# %%
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

# %%
db = SQLDatabase.from_uri("sqlite:///./example_data/Chinook.db")
llm = OpenAI(temperature=0)

# %%
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

# %%
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
db_chain.run("How many employees are there in the Employee table who live in Calgary City?")

# %%[markdown]
# ## Return intermediate steps

# %%
db_chain = SQLDatabaseChain(llm=llm, database=db, prompt=PROMPT, verbose=True, return_intermediate_steps=True)

# %%
# result = db_chain("How many employees do not live in Calgary City?")
# result = db_chain("What is the name and title of the oldest employee")
# result = db_chain("What is the name of the customer with most number of invoices and state the total count of invoices")

result = db_chain("remove details of customers living in USA")

# %%

