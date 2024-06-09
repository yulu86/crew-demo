from typing import Type, Any
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool
from tavily import TavilyClient
import os

tavily_api_key = os.getenv('Tavily_api_key', '')

class TavilyAiToolSchema(BaseModel):
	"""Input for SerperDevTool."""
	search_query: str = Field(..., description="Mandatory search query you want to use to search the internet")

class TavilyAiTool(BaseTool):
	name: str = "Search the internet by travily ai"
	description: str = "A tool that can be used to search the internet with a search_query."
	args_schema: Type[BaseModel] = TavilyAiToolSchema
	n_results: int = 10

	def _run(
		self,
		**kwargs: Any,
	) -> Any:
		search_query = kwargs.get('search_query')
		if search_query is None:
			search_query = kwargs.get('query')

		tavily = TavilyClient(api_key=tavily_api_key)
		search_reponse = tavily.search(query=str(search_query), search_depth="advanced")
	
		context = []
		results = search_reponse["results"]
		if results:
			for obj in results:
			    context.append('\n'.join([
			        f"Title: {obj['title']}",
					f"Link: {obj['url']}",
					f"Snippet: {obj['content']}",
					"---"
			    ]))
			content = '\n'.join(context)
			return f"\nSearch results: {content}\n"
		else:
			return f"\nSearch results: \n"