# agency_lite
Lightweight tool set for setting up a sequential AI Agent workflow. You can use this with both local and hosted LLM models. When using this with a locally hosted LLM, smaller models (7B or less) may have trouble following multiple steps consistently. Experiment with chunk sizes as well, if context length is a concern with the model you are using.

**Files**
* *agent.py* - the agent object is defined here.
* *api_key.py* - add this if you want to use OpenAI (see below).
* *config.py* - for setting the text chunk size and number of search results.
* *main.py* - where it all comes together. Modify to suit your needs.
* *team.py* - where the team is created. Modify to suit your needs.
* *tools.py* - various utility methods

**How it works**
1. User provides a prompt to kick off the chain.
2. One-by-one, in the order they are listed, each Agent will be activated.
3. The active Agent will have a list of prompts, and will go through them in the order they are listed.
4. If set up, the results are processed further (such as summarization to avoid context limits).
5. Once done, the next Agent in the list will take their turn.
6. A final output is generated.


**Limitations**
Because this is a lightweight tool, its powers are limited compared to similar tools, such as CrewAI. The tools.py file holds a few methods that can be invoked, such as searching the web and cleaning up the results. This is mainly to show, that it is possible to extend the tool however you want.

**API Key**
If you're using OpenAI, you'll want to put your api key in file called api_key.py. The content of said file should be:

```python
API_KEY="put-whatever-your-api-key-is-here"
```

**Terminology**
* Agent: LLM instance with specific instructions for its role and priorities. The role description is included in the Agent's instructions.
* Prompt: Each Agent can have any number of tasks to do. Each task is called a prompt, because you need a prompt for each one.
* Model: Refers to the LLM model used for any given Agent. When using an API key, each Agent can have their own LLM model, but will default to the model indicated in the agent.py template, if none is specified for that Agent. When using a local LLM, whatever is specified will be used for all calls.

Note that "agency_lite" does not require Langchain. It does require a few non-standard libraries, such as openai, bs4 and requests. 