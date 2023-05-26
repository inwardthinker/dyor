from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Basic model
# # initialize model
# llm = OpenAI(temperature=0.9)

# # initialize prompt
# prompt = PromptTemplate(
#     input_variables=["product"],
#     template="What is a good name for a company that makes {product}?",
# )

# # initialize llm chain
# chain = LLMChain(llm=llm, prompt=prompt)

# # run chain
# text = chain.run(product="colorful socks")
# print(text)

# Basic Agent
# llm = OpenAI(temperature=0.9)
# tools = load_tools(["serpapi", "llm-math"], llm=llm)
# agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# agent.run("Whats the topmost exciting news today in AI?")

# Basic Chat Model
chat = ChatOpenAI(temperature=0)

# chat([HumanMessage(content="Translate this sentence from English to French. I love programming.")])
# messages = [
#     SystemMessage(content="You are a helpful assistant that translates English to French."),
#     HumanMessage(content="I love programming.")
# ]
# print(chat(messages=messages))
# batch_messages = [
#     [
#         SystemMessage(content="You are a helpful assistant that translates English to French."),
#         HumanMessage(content="I love programming.")
#     ],
#     [
#         SystemMessage(content="You are a helpful assistant that translates English to French."),
#         HumanMessage(content="I love artificial intelligence.")
#     ],
# ]
# result = chat.generate(batch_messages)
# print(result)

template = "You are helpful assistant that translates {input_language} to {output_language}"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
# result = chat(chat_prompt.format_prompt(input_language="English", output_language="French", text="I love programming").to_messages())
# print(result)
chain = LLMChain(llm=chat, prompt=chat_prompt)
chain.run()

