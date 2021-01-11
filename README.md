# SB-Discord-Bot-v0.1 (WIP)
A discord bot made to complement the Minecraft: Bedrock Edition server, NetherGames. Made for my guild SweatyBoi.

Note 1: there is a noticable lack of 'bot' currently; that part is still a work-in-progress. It's more efficient for me to get all of the back-end code in place before working on the bot side of things. 

Note 2: the code is quite messy in a lot of places, and I very rarely comment on my code. Still getting better at programming, so please do excuse it.

# Features:
- exceptions.py:
  - Handles logging errors and database changes, as well as caching recent player stats.
- stats.py:
  - Pulls player stats from NG servers, and also calculates stats that aren't tracked by NG, such as win rate.
- logic.py:
  - Tracks guild members and their stats in a database. Each registered guild will have their own table within that database.
    - Admins of Discord servers will be able to add and remove members from the guild table.
    - There is a function to update a member's stats; This is currently unused, but eventually the bot will update each member's stats automatically every day.
    - The bot will also post the MVP (player who gained the most wins in a day) at the same time.
    - Eventually, the bot would be able to post various different leaderboards within the guild, such as KDR, win rate etc.
      - *NOTE*: Eventually, I hope to make member-tracking automatic, but currently, NG has disabled the API feature that lets me do this. Eventually, they'll probably update it,         but until then admins of servers will have to update it manually.
- tournaments.py:
  - Will eventually enable admins to start tournaments to compete, tracking various different player statistics.
