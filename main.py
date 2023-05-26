from langchain.llms import OpenAI
from langchain.chains import LLMChain, TransformChain, SimpleSequentialChain
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.agents import AgentType
from langchain.agents import load_tools
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.tools.zapier.tool import ZapierNLARunAction
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = OpenAI(temperature=0)
zapier = ZapierNLAWrapper()
# toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
# tools = load_tools(["serpapi", "llm-math"], llm=llm)
# agent = initialize_agent(toolkit.get_tools() + tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# template = """You are an AI assisstant who schedules, accepts, rejects meetings on google calendar.
# Get details of my google calendar account from zapier.
# Use google search engine wherever you deem necessary.
# {user}
# """

# prompt_template = PromptTemplate.from_template(template=template)

# agent.run(prompt_template.format(user="Schedule a meeting for me tomorrow for 30mins between 2pm-5pm IST with shaan@biconomy.io"))

## step 0
actions = ZapierNLAWrapper().list()

# ## step 1. find events in calendar

GOOGLE_CALENDAR_INSTRUCTIONS = "Get the list of events scheduled on google calendar for this week for charan@biconomy.io"

def nla_gcalendar(inputs):
    action = next((a for a in actions if a["description"].startswith("Google Calendar: Find Event")), None)
    return {"calendar_data": ZapierNLARunAction(action_id=action["id"], zapier_description=action["description"], params_schema=action["params"]).run(inputs["instructions"])}
calendar_chain = TransformChain(input_variables=["instructions"], output_variables=["calendar_data"], transform=nla_gcalendar)

# ## step 2. generate draft reply

# template = """You are an assisstant who schedules, accepts, rejects meetings on google calendar. Identify status of scheduled meeting and write it (name, meeting link, status) in plain text (not JSON).

# Incoming calendar event:
# {calendar_data}

# Event Status:"""

# prompt_template = PromptTemplate(input_variables=["calendar_data"], template=template)
# status_chain = LLMChain(llm=OpenAI(temperature=.7), prompt=prompt_template)

# ## step 3. send draft reply via a slack direct message

# SLACK_HANDLE = "@Charan"

# def nla_slack(inputs):
#     action = next((a for a in actions if a["description"].startswith("Slack: Send Direct Message")), None)
#     instructions = f'Send this to {SLACK_HANDLE} in Slack: {inputs["draft_reply"]}'
#     return {"slack_data": ZapierNLARunAction(action_id=action["id"], zapier_description=action["description"], params_schema=action["params"]).run(instructions)}
# slack_chain = TransformChain(input_variables=["draft_reply"], output_variables=["slack_data"], transform=nla_slack)

overall_chain = SimpleSequentialChain(chains=[calendar_chain], verbose=True)
overall_chain.run(GOOGLE_CALENDAR_INSTRUCTIONS)