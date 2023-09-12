# Snake PyGame
This is a Snake Game created using Pygame library as a solution for an assignment in ELEE 2045. The game is fully customizable and includes features such as sound effects, custom images, and animations. This game utilizes an M5 stick as the controller, which has a working button feature.

<b> Video Demonstration: https://youtu.be/TQ5n2FtrQIo </b>

## Accomplishments/Failures

I am very proud of my game for this lab. It was fun to create the Snake Game & customize how I wanted it to be played. My favorite part was choosing the eat sound, food image, and making the snake sparkle. 

One almost failure in this lab was that I could not initially figure out how to communicate a button press on the M5 Stick to python. I was trying to send both the accel values & a value indicating button press in one buffer sent from arduino, but was struggling with parsing the buffer once recieved. I was just going to turn in my lab without the button press feature and make up for lost points with the bonuses. When we were given an extra day to finish the lab, I figured out I could create two seperate characteristics for BLE (one for the accel values & one for the button). When I did this, parsing all of the variables became much simpler since it was broken down. Now I have working button feature!

## Reflections

The first difference I notice between the solutions' part2 & mine is the use of classes. I have never seen the use of "@dataclass" before, but looking it up I see that it is a class that strictly stores data values. I wish I had known about this prior to doing the lab, becuase it definetly would save a lot of hassle from declaring "global" variables at the beginning of each function. This got to be kind of annoying as continued to write multiple functions that mutated the values of multiple different varibales. 

Another difference I notice it with the structure of the connecting device loop & pygame loop. I decided to write my pygame "while running:" loop within my "async with BleakClient(address) as client:" loop. I figured this would ensure that the game would only run when a proper M5 stick connected. Obviously, this does not account for other M5 sticks to play simultaneously, but with Snake Game this isn't really necessary. 
The solutions also does most of it's updating & value re-assignment within functions, where I had a lot more inside the running loop. I'm not sure if this makes a huge difference, maybe it makes editing the code easier since you know where to go to edit specific things (i.e. you're not just combing through the big loop trying to find where you put values every time). 
