from .search_tool import SearchTool

# General web scraper — no trusted-domain filter, includes older articles (days=10)
scrap_tool = SearchTool(
    name="Web Scraper Tool",
    description="Scrapes general web content for a given claim or URL",
    trusted_only=False,
)
