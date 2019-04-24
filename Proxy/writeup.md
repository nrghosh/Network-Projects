
My program uses web_proxy.py and web_client.py which connect a client and proxy through a TCP connection. 
The program uses the proxy to issue a HTTP GET request using a url provided by the client, and opening a TCP connection to 
a host (isolated from the url). After forwarding the request, the proxy receives an HTTP response back, and sends it back along 
to the client, through the TCP connection set up at the beginning. The client’s purpose is the allow the input of a URL (it’s 
hardcoded for testing purposes), allow for monitoring of the process, and receive and display the HTTP response, along with the 
status code (i.e. 200 OK, 304 Not Modified, etc...). The proxy file also creates a cache (implemented in python with a
dictionary), where it stores previous http requests with the format cache[url] = [response, date], in order for us to implement 
conditional GET requests (appending an ‘if-modified-since’ line to the GET requests). This allows us to view whether the URL 
object has, or has not changed since the last time (if applicable) we ran the code and requested the same thing. 

The program works for www.wesleyan.edu/mathcs/index.html, www.mit.edu, www.sfsu.edu, http://abilityone.gov/, cattheory.com, 
www.sina.com.cn/, www.spiegel.de/, http://time.com/, http://www.un.org/, http://www.unitetheunion.org/, and 
http://www.sueddeutsche.de/. The program doesn’t work for Google or Yahoo because they redirect to https://-type addresses, and 
could also not work for other potential sites becaues of my program’s reliance on utf-8 formatting and encoding.  
