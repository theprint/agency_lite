# agency_lite
Lightweight tool set for setting up a sequential AI Agent workflow.

**How it works**
1. User provides a prompt to kick off the chain.
2. One-by-one, in the order they are listed, each Agent will be activated.
3. The active Agent will have a list of prompts, and will go through them in the order they are listed. Once done, the next Agent in the list will take their turn.
4. A final output is generated.


**Limitations**
Because this is a lightweight tool, its powers are limited compared to similar tools, such as CrewAI. The tools.py file holds a few methods that can be invoked, such as searching the web and cleaning up the results. This is mainly to show, that it is possible to extend the tool however you want.


**Terminology**
* Agent: LLM instance with specific instructions for its role and priorities. The role description is included in the Agent's instructions.
* Prompt: Each Agent can have any number of tasks to do. Each task is called a prompt, because you need a prompt for each one.
* Model: Refers to the LLM model used for any given Agent. Each Agent can have their own LLM model, but will default to the model indicated in the agent.py template, if none is specified for that Agent.

In the example files, OpenAI models are used, but you can just as easily use local LLM models. Note that "agency_lite" does not require Langchain.