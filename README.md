# snapspam2

This is a new version of my old repository, [snapspam](https://github.com/mehadh/snapspam). The concept is the same, it spams reports on Snapchat's website in order to hopefully get a user banned. 

Snapchat changed the endpoint and format of the posted data, so I took that as an opportunity to rewrite the code entirely. The old repository was built in Node.js, but I find that Python's much more lightweight multithreading option is far superior for a simple task like this. As a result, it is possible to run a far greater amount of threads in the new version of snapspam. 

Additionally, I've added proxy support, which will hopefully increase the hitrate of these reports. Emails are no longer completed sequentially, but rather an email is selected at random from the whole list. Instead of finishing when the list of emails has all sent a report, the program will only exit when captcha balance becomes too low. 

Rather than using only one reason, it is now possible to input a list of reasons with any desired length. The program will pick randomly from the list of reasons. Similarly, the program also support multiple targets in case you are hoping to attack multiple users at once. Simply place each username on a new line, and the program will select randomly which user to report. 

With limited testing, I've found that before you run into processor limitations, ImageTyperz will hit you with the "LIMITS EXCEEDS" error. I'm hoping to either transition to another captcha service that does not ratelimit, or figure out how to get the ratelimit increased, but as for now it is recommended that you lower your thread count if you face this error. 

You will need the following files in the directory of the file:
emails.txt - This should have email addresses to send reports from. I use real ones, but you can use fake ones.
reasons.txt - The old version of the tool worked fine with just one reason, but I'm sure this will run better with more reasons. 
proxies.txt - This program can run proxyless, just remove the proxy part of the request, but I'd suggest using some premium residential proxies. 
targets.txt - A list of your targets.
token.txt - ImageTyperz access token. 

Todo:

More graceful error handling

Report bad or expired captchas to ImageTyperz
