from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.agents import AgentType
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = OpenAI(model_name="text-davinci-003", temperature=1)
zapier = ZapierNLAWrapper()
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
tools = toolkit.get_tools()
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

template = """
    You are helpful assistant that schedules, modifies, creates and views google calendar meetings.

    Your goal is to help the user manage the busy scheduling meetings in a way that optimizes user's time.

    Try to be precise about the information you share with user in the final step.

    This is the user input: {user_input}
"""

prompt_template = PromptTemplate.from_template(template)

# Prompt 1 
# output = agent.run(prompt_template.format(user_input="Schedulie a 30 minute meeting including me and Shaan(shaan.sundar@biconomy.io) tomorrow at 12pm IST with title 'DYOR' on my google calendar. Share meeting details(title,meeting link, time) with me here"))
# print(output)

# Prompt 2
output = agent.run(prompt_template.format(user_input="update my slack status to 'Working Remotely'"))
print(output)

# Prompt 3
# output = agent.run(prompt_template.format(user_input="Block my calendar for 3 hours from now with status 'busy'."))
# print(output)
