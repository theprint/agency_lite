from agent import Agent
from openai import OpenAI
import tools
from api_key import API_KEY

MAX_CHUNK_SIZE = 600

# Using OpenAI, such as gpt-4
# client = OpenAI(api_key=API_KEY)  # The API key is loaded from api_key.py which you have to create manually.

# Using Local LLM. Example here is from LM Studio.
# Note that using this as-is will overwrite specified models at the Agent level.
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

agents = []  # List to hold the agent objects in your chain

# Example Agent to search the web, clean up the results and send them back.
searchcleaner = Agent()
searchcleaner.role = "text cleaner"
searchcleaner.model = "gpt-4-1106-preview"
searchcleaner.description = "You receive messy and unorganized text from search results and will attempt to clean them up. This includes removing all HTML, XML and similar tagging, but also text that is not directly related to the main content. The result should be a coherent article of text, based on available paragraphs and sections from the source material provided."
searchcleaner.prompts = ["Please clean up the following text and return the cleaned, clearly separated results without commentary or additional notes, but ALWAYS include the link to each search result at the end of each summary:"]
agents.append(searchcleaner)

# Example Agent to summarize text. This Agent has two tasks, first to summarize and organize the results from the text cleaner Agent, and then to summarize these summaries to use as an intro.
summarizer = Agent()
summarizer.role = "summarizer"
summarizer.model = "gpt-3.5-turbo-0125"
summarizer.description = "You are an expert in taking long-form text and extracting and creating a summary of its key points, suggestions or ideas."
summarizer.prompts = ["Please summarize the following search results to help readers decide whether these articles is for them. Return a list of individual summaries and ALWAYS include the relevant link for each one:",
                      "Add an intro paragraph to the list of story summaries, drawing on underlying themes and sentiments in the overall list. The description should be concise and tailored to an audience that is familiar with the topic. Attach your response to the top of the list provided, without changing the list itself. You MUST include the associated link for each story and return the combined text."]
agents.append(summarizer)


if __name__ == '__main__':
    topic = input("What would you like news about? ")
    prompt_topic = topic  # Original prompt is saved for later reference.
    sump = ""
    last_response = ""

    for agent in agents:

        # Specific code to run, for each agent.
        if agent.role == "text cleaner":
            print("Searching the web ...")
            cleaned_text = ""
            searchresults = tools.simple_web_search(topic,limit=6)
            print(f"Search found {len(searchresults)} results.")
            rnum = 1
            for r in searchresults:
                c = f"{tools.scrape(r)}"
                if (len(c) > MAX_CHUNK_SIZE):
                    print(f"Response was {len(c)} characters long. Shortening to {MAX_CHUNK_SIZE}.")
                    c = tools.getResponse(f"Shorten the following text while maintaining all main points and arguments, so that the output is shorter than {MAX_CHUNK_SIZE} characters. The final output MUST include the source link to the story being summarized. TEXT TO SHORTEN: {c}", agent, client)

                p = f"TEXT {rnum}:\n\t{c}\n"
                sump += p
            topic += sump
        if agent.role == "summarizer":
            print("Starting summarization.")
            topic = last_response

        # Basic description of the Agent
        agentrole = f"You are a helpful and friendly {agent.role}."

        # Loops to cycle through each task/prompt for an Agent
        for p in agent.prompts:
            prompt = f"{p}\n\n{topic}"
            last_response = tools.getResponse(prompt, agent, client)
            print("Step complete.")
    print(last_response)  # Final output

    # Save the final output to a txt file.

    outfile = tools.save_file(f"**TOPIC: {prompt_topic}**\n\n{last_response}")
    print(f"Done. Final output saved to {outfile}")