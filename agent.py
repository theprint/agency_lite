class Agent:
    def __init__(self):
        self.role = "Summarizer"
        self.description = "You are a skilled writer, specialized in taking long form text and creating concise and insightful short form summaries of them."
        self.prompt = "Please summarize the following text to help readers decide whether this article is for them. Make sure to keep the links.:"
        self.tools = []  # List of tools, available to this agent
        self.delegation = False  # Can this agent delegate to other agents?
        self.model = "gpt-4-0125-preview"