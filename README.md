python-rcon
===========

Python wrapper for MCRcon (http://github.com/barneygale/MCRcon)

#### Getting set up ####
1. Install python-rcon

  ```
  git clone http://github.com/xavbabe/python-rcon
  cd python-rcon
  sudo python setup.py install
  ```
2. Install MCRcon (needed for python-rcon)

  ```
  cd ../
  git clone http://github.com/barneygale/MCRcon
  cd MCRcon
  wget https://raw.githubusercontent.com/xavbabe/python-rcon/master/setup-MCRcon.py
  sudo python setup-MCRcon.py
  ```
3. Test python-rcon

  ```python
  from rcon import rcon
  
  server = rcon("localhost","username","password") # connect to server
  
  print(server.list()) # print currently logged in users
  ```

Functions
---------
***Note: all results apart from status() are returned in JSON format***
* server.users() - get currently logged in users
* server.status() - get current server status - True = up, False = down
* server.stop() - stop the server
* server.list() - same as users()
* server.close() - close the rcon connection
* server.cmd("your command") - run the given command on the server
* server.reload() - reload the server
* server.version() - return the server's version
* server.say("Hello World!") - broadcast Hello World!
* server.save(mode="mode") - turn saving on ("on"), turn saving off ("off") or save everything ("all") - default
* server.time("time") - change server time
* server.day() - change server time to day
* server.night() - change server time to night
* server.weather("thunder") change server weather to "thunder"
* server.clear() - change server weather to sunny
* server.op("user") - op "user"
* server.deop("user") - deop "user"
* server.stats() - return loads of server stats
