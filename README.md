YuukiBot v1.3.1
===

About YuukiBot
---

YuukiBot is a Telegram Bot made by Yuukari. Originally made to test out the Telegram API, it began to become a testing ground for API and integration as a toy chatbot for chatrooms.

Commands
---
[See Here](https://github.com/awuwu/yuukibot/wiki/Commands)


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
 * 1.2.1 -- Add points values to /wins
 * 1.2.2 -- Add top command
 * 1.3.0 -- Introduced standardized point measurements in multiples of 50. Included a DB rounding script to nearest 50.
 * 1.3.1 -- Added /shrug
 * 1.4.0 -- Introduced Infamy, /reset, and Remodeled the User and Points databases. In addition, this update allows Administrators to issue official points using /win and /points that are tracked on the /top list.

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

