# Web Client and Web Proxy
Implementing caching and conditional HTTP GET requests with a web client and proxy.

# Directions
- Open two terminals in a directory with web_client.py and web_proxy.py
- First, run web_proxy.py: ```$ python3 web_proxy.py``` in one terminal
- Next, run web_client.py: ```$ python3 web_client.py``` in the other terminal 
- The client will prompt you for a url. Type the url and hit enter. 
- You should be able to monitor the status in the proxy and client window, and see the results
- Run the client code again, with the same url, to observe the 304 Not Modified response, and to see that you get a response from the cache, instead. 
- NOTE: If the code is not able to extract a date, it will not cache the request, and you’ll get an updated (200 OK) response each subsequent time...
