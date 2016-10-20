## RedditReplaceBot
A generic Reddit bot that scrapes comments and replies to them, substituting specific words in the text.
You can define word substitutions for the bot to identify and replace. (See **Setup** section below)

It'll cycle through the subreddits indefenitely and log its own comments to a local text file to avoid repeating comments after restart.


**Setup:**

Customize your bot: ('CONSTANTS' section in [bot.py](/bot.py)) 
- Enter your Username, Password and a custom reply message.
- Add or remove subreddits of interest.
- Add word substitution pairs in 'keywords_original' and 'keywords_substitute' lists respectively.

**Usage:**
- `python bot.py`

**Requirements:**
- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [PRAW](https://github.com/praw-dev/praw) (`pip install praw`)