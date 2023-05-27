from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.agents import AgentType
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv, find_dotenv

class CalendarModel:
  def __init__(self):
    load_dotenv(find_dotenv())
    self.llm = OpenAI(model_name="text-davinci-003", temperature=0.7)
    self.zapier = ZapierNLAWrapper()
    self.toolkit = ZapierToolkit.from_zapier_nla_wrapper(self.zapier)
    self.tools = self.toolkit.get_tools()
    self.agent = initialize_agent(self.tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    self.template = """
        If user question is not related to google calendar or slack status simply reply 'Sorry! I dont know'. Be strict about this rule.

        Consider the following line as user question:
        {user_input}
    """
    self.prompt_template = PromptTemplate.from_template(self.template)

  def run(self, user_input):
    output = self.agent.run(self.prompt_template.format(user_input=user_input))
    return output

