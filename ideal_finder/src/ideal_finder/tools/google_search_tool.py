from crewai_tools import SeleniumScrapingTool

tool = SeleniumScrapingTool(website_url='https://www.google.com/search?q=', css_element='div.MjjYud', wait_time=60)
