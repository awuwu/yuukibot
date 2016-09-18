YuukiBot v1.2.0
===

About YuukiBot
---

YuukiBot is a Telegram Bot made by Yuukari. Originally made to test out the Telegram API, it began to become a testing ground for API and integration as a toy chatbot for chatrooms.

Commands
---

Command | Description |
--- | :---
`/awuwu`   | Makes YuukiBot Awuwu. Random Number of 'wu's are appended to the end.
`/uwah`    | Makes YuukiBot Embarassed.
`/win`     | Displays a GIF from the win/ directory.
`/points`  | Displays a GIF from the points/ directory.
`/quote`   | Picks a random quote from the quote.txt file.
`/fortune` | Takes input and processes mystical, mythical RNG to return a vaugely in-character answer somehow.
`/spiral`  | Displays a GIF from the spiral/ directory.
`/moo`     | Makes YuukiBot Moo.
`/bray`    | Makes YuukiBot Bray.
`/me`      | Returns input after /me in bold, similar to how /me worked in IRC.
`/tweet`   | Sends a Tweet to the userpage which is defined in the twitter section of the config file. For more on Twitter API, visit http://api.twitter.com/ for details. Can only be run by the user identified in `telegram_handle`. 
`/about`   | Returns an about message on YuukiBot |

Note: commands will work even in a chatroom with multiple bots.

Versioning
---

Versioning is based on Major, Minor, Bugfix design. 1.1.1 is the current version.

 * 0.1.0 -- Initial Release
 * 0.2.0 -- Original Coding
 * 0.3.0 -- Added Additional Commands
 * 0.4.0 -- Fixed up formatting and parsing
 * 1.0.0 -- Recoded Bot to Adhere to telegram-python-bot's ext class rather than the main class.
 * 1.1.0 -- Added More Commands, Restructred code to work off of a config file.
 * 1.1.1 -- Added about command, added some quotes.
 * 1.1.2 -- Moo command, Begin concepts for new command structure
 * 1.1.3 -- Change lengths, random face picker
 * 1.2.0 -- Add updates and channel registry.

Contributing
---

Users are encouraged to contribute artifacts such as gifs, quote additions, fortune additions, and so on. All pull requests will be given a review before merging.

Please, please, please do not commit directly to master. Please use a branch.

Requirements
---

 * Python 2.7.x
 * python-twitter
 * python-telegram-bot
 * Virtualenv (Reccomended)
 * pip (Reccomended)
 * screen (Reccomended, Linux ONLY)

Installing
---

These instructions are assuming you are running on Debian 8 or a recent distribution of Ubuntu (Code tested on Debian 8). I highly reccomend a virtualenv with pip.

* `git clone https://github.com/awuwu/yuukibot.git`
* `virtualenv yuukibot/env`
* `cd yuukibot`
* `source env/bin/activate`
* `pip install -f requirements.txt`
* (if errors occur, fix those first. Usually C compilations. Warnings you can ignore, YuukiBot uses very little of it.)
* Copy config.example.cfg to config.cfg
* Edit config.cfg variables to your leisure.

Executing
---

(For most people)

* Run `python yuuki.py`

(If you're using screen)

* `screen -S yuukibot`
* `python yuuki.py`

Adding Content
---

Because of the nature that YuukiBot pulls information, you can add content like gifs, quotes, fortune entries, etc while the bot is operational, meaning you don't have to restart.

License
---

*Source code* is released under the MIT Permissive License.

Copyrighted Material
---

Material used in this code, such as gifs or other artifacts, are copyrighted to their orignial owners and are not affected by the code license. If you find copyrighted material in artifacts that belongs to you, please contact me at hey (at) yuu (dot) im. We will sort it out.

