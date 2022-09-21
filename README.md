# waikinbot-twitch
Waikinbot is a twitch statistics chat bot that actively tracks and records player game statistics for the game World of Tanks (WOT). The chatbot itself was built in python and based on the twitchio package, an asynchronous python API wrapper for twitch. 

Want to try it out? Go to [my twitch channel](https://www.twitch.tv/waikin_) and type in !hello / !commands in chat!

Player “random battle” data (random battle is a term used in WOT to describe the primary game mode in which most players play), is collected through the WOT API using python’s request library. This data is then used by the twitch bot to send live game statistics in twitch’s chat UI.

The twitch bot source code is hosted on the cloud based platform Heroku and deployed through GitHub. All player statistics are stored and managed in a PostgreSQL database hosted by Amazon AWS and connected though heroku data.

![alt text](https://cdn.discordapp.com/attachments/732549918702436455/1015110737875697784/waikinBot_architecture_1.png)
