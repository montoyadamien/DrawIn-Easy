# DrawIn'Easy

DrawIn'Easy is a bot dedicated to the game [Gartic Phone](https://garticphone.com/). The bot will draw a picture fetched from an URL in the Gartic Phone interface.

# Installation

- Install [Python 3](https://www.python.org/downloads/)
- Run `pip install -r requirements.txt`

# How to use

To run the bot, follow this steps:  
- Be sure to have Python 3.x installed
- Run `pip install -r requirements.txt`
- Run `python main.py`
- When asking for a picture, simply paste an image url
- When asking for the first point, just click on the Gartic Phone drawing workplan. This point must be the top - left corner where the drawing should start.
- When asking for the second point, click on the Gartic Phone drawing workplan. This second point must be the bottom - right corner where the drawing should end.
- Wait for some seconds (the larger the drawing area is, the longer the duration will be) and the bot will automatically choose the right colors to draw between the two points you gave.

# Bot support

The bot have been tested under Windows 10, but it should also work on Linux.  
Since the bot needs to be configured for each screen resolution in order to match the click on colors, the supported resolutions are:
- 2560x1440

More resolutions can be added in the file [colors.py](colors.py).
