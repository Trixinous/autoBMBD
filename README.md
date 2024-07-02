# autoBMBD
< Non-invasive Python script to make Counter-Strike more chaotic.>


I've tried my best to explain everything in config.ini, but all the links and handy stuff will be provided here.
BM is chosen randomly between "." and ",", put a say bind on those to let the BM side of the script work.

The bomb drop has an alias to go in "steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg". I'll assume you can find your steamapps folder.

The alias is as follows:

alias "+bomb" "slot3; slot5"

alias "-bomb" "drop;"

bind "h" +bomb

You can enable and disable Bad Mouthing with ctrl + alt + n. You can enable and disable Bomb Dropping with ctrl + alt + b.

Python 3 is required to run the script. You will need to install dependencies for the script to function.

Run the line below in CMD/Powershell to install all requirements:



pip install pillow numpy opencv-python pynput keyboard colorama winsound



My explanation of the coordinates and bounding boxes needed to get things working:

https://ibb.co/wzL7FCv


This was my first real experience programming with python after abandoning vb.net, 
hence the chaotic nature and borderline insanity of the script.
Modify the script as you see fit. Try and make sense of it. I dare you.

                                                           AUTOBMBD                                                             
                                             IT MEANS AUTO BAD MANNERS & BOMB DROPS                                             
                       ORIGINAL CODE BY COLOSSALTROLLER. MODIFIED MASSIVELY BY TRIXINOUS. PROVIDED AS IS.                       
							VERSION NUMBER 45                           							 

										╱|、
					  meow   			       (˚ˎ 。7  
										|、˜〵          
										じしˍ,)ノ
