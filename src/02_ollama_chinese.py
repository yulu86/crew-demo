from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
import os

os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model = "wangshenzhi/llama3-70b-chinese-chat-ollama-q4:latest",
    base_url = "http://localhost:11434/v1")

general_agent = Agent(role = "数学专家",
                      goal = """为提出数学问题的学生提供解决方案，并给出答案。""",
                      backstory = """你是一位优秀的数学教授，喜欢用大家都能理解的方式解决数学问题""",
                      allow_delegation = False,
                      verbose = True,
                      llm = llm)
task = Task (description="""树上有7只鸟，用枪打死4只，树上还剩下几只""",
             agent = general_agent,
             expected_output="数字")

crew = Crew(
            agents=[general_agent],
            tasks=[task],
            verbose=2
        )

result = crew.kickoff()

print(result)