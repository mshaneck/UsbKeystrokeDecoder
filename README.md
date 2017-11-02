I recently encountered a challenge that had a pcap file with USB traffic inside. I don't want to post any spoilers, so I won't mention which challenge it was or all the details of how I solved it. I did however, want to post the tool that I created in order to solve it. It seemed like a good CTF challenge, and so I wanted to keep the tool for future use.

This tool was created specifically for the challenge in question, so using it for anything else will probably require modifying it quite a bit. Feel free to grab the code and modify it however you want.

The first step was to use tshark to cut out the data. Tshark is definitely a tool I need to spend more time learning for more advanced scripted pcap manipulation.


