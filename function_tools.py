import random
import chainlit as cl
from agents import function_tool

@function_tool
async def run_narrator()->str:
    options = ["explore","hunt","escape"]
    await cl.Message(content=f"You may {options}").send()
    only_option = random.choice(options)
    await cl.Message(content=f"You got to {only_option}").send()
    
@function_tool
async def generate_event()->str:
    events = [
        "You encounter a group of goblins!",
        "You find a hidden treasure chest.",
        "A mysterious fog rolls in...",
        "You discover an ancient scroll.",
        "A trap is triggered beneath your feet!"
    ]
    await cl.Message(content=events).send()
    event = random.choice(events)    
    await cl.Message(content= event).send()
    

@function_tool
async def run_monster()->str:
    player_roll= random.randint(1,6)
    monster_roll = random.randint(1,6)
    if player_roll > monster_roll:
        await cl.Message(content= f"Combat begins! You roll {player_roll}, monster rolls {monster_roll}. You win!").send()
    else:
        await cl.Message(content= f"Combat begins! You roll {player_roll}, monster rolls {monster_roll}. You lose!").send()
    
@function_tool
async def run_item()->str:
    inventory = []
    # print(f"DEBUG: Type of inventory in run_item: {type(inventory)}") 
    loot = random.choice(["Healing Potion", "Silver Sword", "Magic Scroll"])
    inventory.append(loot)
    await cl.Message(content=f"You received: {loot}. Inventory now: {inventory}").send()
    

