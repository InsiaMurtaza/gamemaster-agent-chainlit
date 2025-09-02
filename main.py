import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
import chainlit as cl
from typing import cast
from agents.run import RunConfig
from game_agents import narratoragent


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta"
model = "gemini-2.0-flash"

@cl.on_chat_start
async def chat_start():

    client = AsyncOpenAI(api_key=gemini_api_key,base_url= base_url)
    config = RunConfig(model=OpenAIChatCompletionsModel(model=model,openai_client=client),
                       model_provider= model,
                       tracing_disabled= True)
    
    cl.user_session.set("config",config)
    cl.user_session.set("chathistory",[])
    cl.user_session.set("agent",narratoragent)

    await cl.Message("👋Welcome to the Game Master Agent! Let's play and have some fun😊 Type start to begin the adventure.").send()
    # await cl.Message("Type *start* to begin the adventure.").send()
    
@cl.on_message
async def main(message:cl.Message):
    msg = cl.Message(content="")
    await msg.send()
     
    agent:Agent = cast(Agent,cl.user_session.get("agent"))
    config = cast(RunConfig,cl.user_session.get("config"))
    history= cl.user_session.get("chathistory") or []
    history.append({"role":"user","content":message.content})
    
    try:
        if message.content.lower() == "start":
            print("\nCALLING AGENT WITH CONTEXT\n",history,"\n")
            result = await Runner.run(starting_agent=agent, input= "The game begins!", run_config= config)
            await cl.Message(content=str(result.final_output)).send()
            # history= cl.user_session.set("chathistory",result.to_input_list())
            # history = result.to_input_list()
            print(f"User:{message.content}")
            print(f"Game Agent: {msg.content}")
            
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await  msg.update()
        print(msg.content)




    
    
    

