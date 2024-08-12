# Swipetify
Swipetify is a Mediapipe-to-Spotify hand tracking controller for Windows, written in Python. With it, you can control Spotify with a simple hand set of hand movements! (I'll upload a showcase video later :D)

# ⚠ Disclaimer ⚠
This program is *NOT* particularly user friendly, nor is it *really* ready for a public release. It functions, but definitely needs a good bit of work. **More of a proof of concept than anything else.** (It might stay that way, I just wanted to show off what I had, though it *is* still under active development by yours truly).
One thing I can't seem to get rid of at the moment are the deprecation warnings, if anyone has any fixes I'd love to see that resolved so as to stop clogging up the console. It's likely weighing down the whole script.

# How to Use
After launching Spotify, run the *swipetify.py* file to activate the Swipetify script (do this while Spotify is open & not playing music to ensure a good connection). Sometimes the script can be a little finicky (I believe due to issues with Spotify) but once you can get one command through you're good to go and *shouldn't* experience any other issues.
![Swipetify gesture: Index & middle fingers raised, ring & pinkie fingers closed](https://raw.githubusercontent.com/MasonNotJason/Swipetify/main/SwipetifyGesture.png)
To control, make the Swipetify gesture (see SwipetifyGesture.png . Swiping from left to right skips; right to left unskips; high to low (un)pauses. Dissolving the gesture by making a fist or bringing it off camera will trigger the command. 

# How it Works
The application hooks into Spotify with **pywinauto**, which allows keybinds to be sent to the Spotify application even when it's unfocused (though doing this does focus Spotify if it was minimized).

**OpenCV** reads camera data and feeds it to **Mediapipe** for hand tracking. (It is also used to display the testing window, which shows the webcam overlayed with **Mediapipe's** hand landmarks.

**Mediapipe** detects finger positions [(more about that here)](https://mediapipe.readthedocs.io/en/latest/solutions/hands.html), from which 2d coordinates are obtained for tracking key segments which are used for very simple calculations, determining whether or not the Swipetify gesture is being made. My script uses the start & end positions of the gesture as a simple way to determine what the intended action is.


# Customizing
In **v1-1**, most of the easily-accessed settings are in lines 8-12 of the *swipetify.py* script, with comments explaining how they work. 


