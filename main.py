from agent import Agent
from team import team
import config
from openai import OpenAI
import tools
from api_key import API_KEY

# Using OpenAI, such as gpt-4
# client = OpenAI(api_key=API_KEY)  # The API key is loaded from api_key.py which you have to create manually.

# Using Local LLM (Example here is from LM Studio)
# Note that using this as-is will overwrite specified models at the Agent level.
# To use multiple local LLM models, you need to define a client for each one.
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

if __name__ == '__main__':
    # Initial prompt from the user.
    topic = input("What would you like news about? ")

    # Variables needed to process request
    prompt_topic = topic  # Original prompt is saved for later reference.
    last_response = ""

    
    for agent in team.agents:
        print(f"Activating the {agent.role} agent ...")
        # Custom actions / Put custom code in team.py
        topic = team.agentAction(agent, client, topic, last_response)

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