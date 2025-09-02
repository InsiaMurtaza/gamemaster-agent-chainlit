import os
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI
from function_tools import run_narrator, run_monster, run_item, generate_event


gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta"
model = "gemini-2.0-flash"
client = AsyncOpenAI(api_key=gemini_api_key,base_url= base_url)

itemagent = Agent(name="ItemAgent",
                  instructions="You are the **ItemAgent**, responsible for managing the player's inventory and rewards. "
        "Upon receiving control, your task is to **distribute loot or add items to the inventory** "
        "by using the *run_item* tool. You will inform the player what they have received "
        "and their current inventory. After fulfilling your task, the current turn or round concludes.",
                  model=OpenAIChatCompletionsModel(model= model,openai_client=client),
                  tools=[run_item]
                  )
monsteragent = Agent(name="MonsterAgent", 
                     instructions="You are the **MonsterAgent**, in charge of combat encounters. "
        "When you receive control, your immediate task is to **initiate a combat sequence**, "
        "by using the *run_monster* tool, to determine the outcome of the battle. "
        "Once the combat result is determined, regardless of win or loss, "
        "you **must hand off control to the ItemAgent** to manage any rewards or consequences.",
                     model=OpenAIChatCompletionsModel(model= model, openai_client=client),
                     tools=[run_monster],
                     handoffs=[itemagent])

narratoragent = Agent(name="NarratorAgent", 
                      instructions="You are the **NarratorAgent**, the storyteller of this adventure."
        "Your first task is to **generate an initial event** by using tool *generate_event* for the player and then tell the next action to the user by using the *run_narrator* tool. "
        "Then you **have to hand off control to the MonsterAgent** to handle any potential encounters.",
                      model=OpenAIChatCompletionsModel(model= model,openai_client=client),
                      tools=[generate_event,run_narrator],
                      handoffs=[monsteragent])