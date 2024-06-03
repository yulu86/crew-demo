from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
# from crewai_tools import SerperDevTool
import os

os.environ["OPENAI_API_KEY"] = "NA"

# search_tool = SerperDevTool()

design_model = Ollama(model = "llama3:70b-instruct")
woker_model = Ollama(model = "codestral:22b")

game_designer = Agent(
  role='游戏设计师',
  goal='详细描述游戏{topic}的规则，提供给开发者用于开发',
  verbose=True,
  memory=True,
  backstory=(
    "你是资深的游戏设计师。"
    "你热爱并熟悉所有经典游戏，对游戏规则熟悉了然于胸。"
  ),
  # tools=[search_tool],
  allow_delegation=True,
  llm=design_model
)

worker = Agent(
  role='游戏开发者',
  goal='用html开发游戏{topic}',
  verbose=True,
  memory=True,
  backstory=(
    "你是一名资深的游戏开发者。"
    "你擅长用游戏设计师设计的游戏规则来构建游戏。"
    "你精通用html、javascript、css开发游戏。"
  ),
  # tools=[search_tool],
  allow_delegation=False,
  llm=woker_model
)

game_design_task = Task(
  description=(
    "描述游戏{topic}的开发需求。"
    "需求中需要包含游戏界面的详细描述，界面精美，能满足游戏玩家。"
    "需求中需要详细描述游戏规则，包括并不限于游戏玩家数量、游戏启动、得分、游戏结束、游戏失败的规则。"
  ),
  expected_output='用Markdown格式输出游戏的需求和规则',
  agent=game_designer,
  # tools=[search_tool],
)

worker_task = Task(
  description=(
    "用html、javascript、css、图片和必要的三方件构建游戏{topic}。"
    "游戏需要满足设计师提供的需求和规则。"
    "请输出游戏的详细代码。"
  ),
  expected_output='仅输出游戏的详细代码，不需要输出代码注释和其他解释说明内容',
  agent=worker,
  # tools=[search_tool],
  async_execution=False,
  output_file='output/game.html'
)

crew = Crew(
  agents=[game_designer, worker],
  tasks=[game_design_task, worker_task],
  process=Process.sequential,
#   memory=True,
#   cache=True,
  max_rpm=5,
  share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': '贪吃蛇'})
print(result)