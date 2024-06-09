from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from crewai_tools import SeleniumScrapingTool
from urllib.parse import quote
from custom_tools.tavily_ai_tool import TavilyAiTool
import os

os.environ["OPENAI_API_KEY"] = "NA"

tavily_ai_tool = TavilyAiTool()
ollama_model = Ollama(model = "wangshenzhi/llama3-70b-chinese-chat-ollama-q4:latest")

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='高级研究员',
  goal='探索以下领域的突破性技术: {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "在好奇心的驱使下，你走在创新的前沿，渴望探索和分享可能改变世界的知识"
  ),
  tools=[tavily_ai_tool],
  allow_delegation=False,
  llm=ollama_model
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='作家',
  goal='讲述引人注目的故事: {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "您善于将复杂的话题简单化，您的叙述引人入胜、寓教于乐，以通俗易懂的方式揭示了新的发现"
  ),
  tools=[tavily_ai_tool],
  allow_delegation=False,
  llm=ollama_model
)

# Research task
research_task = Task(
  description=(
    "确定{topic}的下一个大趋势。重点确定利弊和整体叙述。您的最终报告应清晰阐述要点。"
  ),
  expected_output='一份长达 10 段的综合性报告，介绍了{topic}的最新研究成果，并给出参考资料的具体出处',
  tools=[tavily_ai_tool],
  agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "就{topic}撰写一篇有见地的文章。重点关注最新趋势及其对行业的影响。文章应通俗易懂、引人入胜、积极向上。"
  ),
  expected_output='关于 {topic} 进展的 5 段文章，每段有一个小标题，格式为 markdown，并给出参考资料的具体出处。',
  tools=[tavily_ai_tool],
  agent=writer,
  async_execution=False,
  output_file='output/new-blog-post.md'  # Example of output customization
)

# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
#   memory=True,
#   cache=True,
  max_rpm=100,
  share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'AICG的发展趋势如何'})
print(result)