# Original Written by DougDoug and DDarknut
# Current iteration written by aVeryGreenBanana

# Hello! This file contains the main logic to process Twitch chat and convert it to game commands.
# The code is written in Python 3.X
# There are 2 other files needed to run this code:
    # TwitchPlays_KeyCodes.py contains the key codes and functions to press keys in-game. You should not modify this file.
    # TwitchPlays_Connection.py is the code that actually connects to Twitch. You should not modify this file.

# The source code primarily comes from:
    # Wituz's "Twitch Plays" tutorial: http://www.wituz.com/make-your-own-twitch-plays-stream.html
    # PythonProgramming's "Python Plays GTA V" tutorial: https://pythonprogramming.net/direct-input-game-python-plays-gta-v/
    # DDarknut's message queue and updates to the Twitch networking code
    # DougDoug's website: https://www.dougdoug.com/twitchplays

# Disclaimer: 
    # This code is NOT intended to be professionally optimized or organized.
    # We created a simple version that works well for livestreaming, and I'm sharing it for educational purposes.

##########################################################

TWITCH_CHANNEL = 'averygreenbanana' # Replace this with your Twitch username. Must be all lowercase. 

##########################################################
import statistics as s
import TwitchPlays_Connection
import pyautogui
import random
import time
import pydirectinput
import keyboard
from collections import Counter
import concurrent.futures
from TwitchPlays_KeyCodes import *

##########################################################

# MESSAGE_RATE controls how fast we process incoming Twitch Chat messages. It's the number of seconds it will take to handle all messages in the queue.
# This is used because Twitch delivers messages in "batches", rather than one at a time. So we process the messages over MESSAGE_RATE duration, rather than processing the entire batch at once.
# A smaller number means we go through the message queue faster, but we will run out of messages faster and activity might "stagnate" while waiting for a new batch. 
# A higher number means we go through the queue slower, and messages are more evenly spread out, but delay from the viewers' perspective is higher.
# You can set this to 0 to disable the queue and handle all messages immediately. However, then the wait before another "batch" of messages is more noticeable.
MESSAGE_RATE = 0.5
# MAX_QUEUE_LENGTH limits the number of commands that will be processed in a given "batch" of messages. 
# e.g. if you get a batch of 50 messages, you can choose to only process the first 10 of them and ignore the others.
# This is helpful for games where too many inputs at once can actually hinder the gameplay.
# Setting to ~50 is good for total chaos, ~5-10 is good for 2D platformers
MAX_QUEUE_LENGTH = 50  
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 

#general variables
pauseTime = 0.2;
gameOn = True;

#boolean variables (true or false stuff)
isTalking = False;

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False

##########################################################

# An optional count down before starting, so you have time to load up the game
countdown = 3
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

t = TwitchPlays_Connection.Twitch();
t.twitch_connect(TWITCH_CHANNEL);

def handle_message(message):
    try:
        msg = message['message'].lower()
        username = message['username'].lower()

        # lets you view who is sending each message, set displayMessage to true if you want to see this
        displayMessage = False;
        if displayMessage == True:
            print("Got the message: [" + msg + "] from user [" + username + "]")         

        ###################################
        # Code Section 
        ###################################

        # reads in variables from above
        global pauseTime;
        global gameOn;

        #List of mods in your chat (include your name in this list and feel free to remove mine, it was initially there for testing)
        listOfMods = [TWITCH_CHANNEL, "averygreenbanana"];
        
        if msg == "+controlon" and username in listOfMods:
            print("control is on")
            gameOn = True;

        if msg == "+controloff" and username in listOfMods:
            print("control is off")
            gameOn = False;

        if gameOn == True:
            # If the chat message is "left", then hold down the A key for 2 seconds
            if msg == "left":
                ReleaseKey(D)
                HoldAndReleaseKey(A, 2)

            # If the chat message is "right", then hold down the D key for 2 seconds
            if msg == "right":
                ReleaseKey(A)
                HoldAndReleaseKey(D, 2)

            # If the chat message is "forward", then hold down the W key for 2 seconds
            if msg == "forward":
                ReleaseKey(S)
                HoldAndReleaseKey(W, 2)

            # If the chat message is "back", then hold down the S key for 2 seconds
            if msg == "back":
                ReleaseKey(W)
                HoldAndReleaseKey(S, 2)

            # If the chat message is "stop", then release all keys
            if msg == "stop":
                ReleaseKey(W)
                ReleaseKey(LEFT_SHIFT)
                ReleaseKey(A)
                ReleaseKey(S)
                ReleaseKey(D)

            # If the chat message is "climb", then hold space
            if msg == "climb":
                HoldAndReleaseKey(SPACE, 3.0)  
                
            # If the chat message is "interact", then hold E
            if msg == "interact":
                HoldAndReleaseKey(E, 2.0)  

            # If the chat message is "crouch", then tap C
            if msg == "crouch":
                HoldAndReleaseKey(C, 0.2)  

            # If the chat message is "prone", then tap Z
            if msg == "prone":
                HoldAndReleaseKey(Z, 0.2)  

            # If the chat message is "dive", then have a 1/8 chance to tap alt
            if msg == "dive":
                random_number = random.randint(1, 8)
                if random_number == 5:
                    HoldAndReleaseKey(LEFT_ALT, 0.2)  

            # If the chat message is "emote", then have a 1/8 chance to tap B
            if msg == "emote":
                random_number = random.randint(1, 8)
                if random_number == 5:
                    HoldAndReleaseKey(B, 0.2)  

            # If the chat message is "sprint", then same as forward but hold shift for 2 seconds
            if msg == "sprint":
                ReleaseKey(S)
                HoldKey(W)
                HoldAndReleaseKey(LEFT_SHIFT, 2)
                time.sleep(2)
                ReleaseKey(W)

            # If the chat message is "shoot", then hold down the left mouse button for 0.2 seconds 3 different times
            if msg == "shoot":
                pydirectinput.mouseDown(button="left")
                time.sleep(0.2)
                pydirectinput.mouseUp(button="left")
                time.sleep(0.2)

                pydirectinput.mouseDown(button="left")
                time.sleep(0.2)
                pydirectinput.mouseUp(button="left")
                time.sleep(0.2)

                pydirectinput.mouseDown(button="left")
                time.sleep(0.2)
                pydirectinput.mouseUp(button="left")
                time.sleep(0.2)          

            # If the chat message is "hold shoot", then hold down the left mouse button for 2.0 seconds
            if msg == "hold shoot":
                pydirectinput.mouseDown(button="left")
                time.sleep(2)
                pydirectinput.mouseUp(button="left")

            # If the chat message is "aim", then hold down the right mouse button for 1.5 seconds
            if msg == "aim":
                pydirectinput.mouseDown(button="right")
                time.sleep(1.5)
                pydirectinput.mouseUp(button="right")

            # If the chat message is "primary", then tap 1
            if msg == "primary":
                HoldAndReleaseKey(ONE, 0.2) 

            # If the chat message is "secondary", then tap 2
            if msg == "secondary":
                HoldAndReleaseKey(TWO, 0.2) 

            # If the chat message is "support", then tap 3
            if msg == "support":
                HoldAndReleaseKey(THREE, 0.2) 

            # If the chat message is "backpack", then tap 5
            if msg == "backpack":
                HoldAndReleaseKey(FIVE, 0.2) 

            # If the chat message is "grenade", then tap G
            if msg == "grenade":
                HoldAndReleaseKey(G, 0.2)  

            # If the chat message is "stim", then tap V
            if msg == "stim":
                HoldAndReleaseKey(V, 0.2)  

            # If the chat message is "reload", then tap R
            if msg == "reload":
                HoldAndReleaseKey(R, 0.2)  

            # If the chat message is "melee", then tap F
            if msg == "melee":
                HoldAndReleaseKey(F, 0.2)  
                                 
######################################################################## 

    except Exception as e:
        print("Encountered exception: " + str(e))

while True:

    active_tasks = [t for t in active_tasks if not t.done()]

    #Check for new messages
    new_messages = t.twitch_receive_messages();
    if new_messages:
        message_queue += new_messages; # New messages are added to the back of the queue
        message_queue = message_queue[-MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

    messages_to_handle = []
    if not message_queue:
        # No messages in the queue
        last_time = time.time()
    else:
        # Determine how many messages we should handle now
        r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            # Pop the messages we want off the front of the queue
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time();

    # If user presses Shift+Backspace, automatically end the program
    if keyboard.is_pressed('shift+backspace'):
        exit()

    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')
