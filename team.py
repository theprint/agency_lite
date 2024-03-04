from agent import Agent
import tools, config

class Team:
    def __init__(self) -> None:
        self.agents = []  # List to hold the agent objects in your chain
        self.sump = ""

    # This is called in the loop in main.py:
    def agentAction(self, agent, client, topic, last_response):
        # Customize this block to fit your agents:
        # # # # # # # # # # # # # # # # # # # # # # #

        if agent.role == "text cleaner":
            print("Searching the web ...")
            cleaned_text = ""
            searchresults = tools.simple_web_search(topic)
            print(f"Search found {len(searchresults)} of {config.MAX_SEARCH_RESULTS} results.")
            rnum = 1
            for r in searchresults:
                c = f"{tools.scrape(r)}"
                if (len(c) > config.MAX_CHUNK_SIZE):
                    c = tools.shorten(c, agent, client)

                p = f"TEXT {rnum}:\n\t{c}\n"
                self.sump += p
            topic += self.sump
        if agent.role == "summarizer":
            print("Starting summarization.")
            topic = last_response
        return topic

        # # # # # # # # # # # # # # # # # # # # # # #
        # End of custom code block

team = Team()

# # # # # # # # # # # # # # #
# Define your team below:   #
# # # # # # # # # # # # # # #

# Example Agent to search the web, clean up the results and send them back.
searchcleaner = Agent()
searchcleaner.role = "text cleaner"
searchcleaner.model = "gpt-4-1106-preview"
searchcleaner.description = "You receive messy and unorganized text from search results and will attempt to clean them up. This includes removing all HTML, XML and similar tagging, but also text that is not directly related to the main content. The result should be a coherent article of text, based on available paragraphs and sections from the source material provided."
searchcleaner.prompts = ["Please clean up the following text and return the cleaned, clearly separated results without commentary or additional notes, but ALWAYS include the link to each search result at the end of each summary:"]
team.agents.append(searchcleaner)

# Example Agent to summarize text. This Agent has two tasks, first to summarize and organize the results from the text cleaner Agent, and then to summarize these summaries to use as an intro.
summarizer = Agent()
summarizer.role = "summarizer"
summarizer.model = "gpt-3.5-turbo-0125"
summarizer.description = "You are an expert in taking long-form text and extracting and creating a summary of its key points, suggestions or ideas."
summarizer.prompts = ["Please summarize the following search results to help readers decide whether these articles is for them. Return a list of individual summaries and ALWAYS include the relevant link for each one:",
                    "Add an intro paragraph to the list of story summaries, drawing on underlying themes and sentiments in the overall list. The description should be concise and tailored to an audience that is familiar with the topic. Attach your response to the top of the list provided, without changing the list itself. The final reply MUST include the associated link for each source story on the list!"]
team.agents.append(summarizer)