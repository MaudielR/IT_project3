0. Please write down the full names and netids of all your team members.
-Maudiel Romero mar641
-Alex Miller arm297

1. Briefly discuss how you implemented the LS functionality of
   tracking which TS responded to the query and timing out if neither
   TS responded.
   - We separated the allocation of which ts it sends to based on hashing the ip name and sending it to ts1 if the hash was even, and sent it to ts2 if the hash was odd. This was how Abraham the TA explained in lecture. We also tracked the timing of TS responses by setting a timeout of 5 seconds, if nothing was returned in 5 seconds we would send back an error message to LS and then, if there was an error in LS sent it to the other TS server. Again we set a timeout of 5 seconds so if the second request timedout then we would catch THAT timeout and write that there was an error from both in the resolved.txt. We did this to send to ts1 first then to ts2 and vice versa so that you could send it to the second ts server no matter which server you sent to first.  
   
2. Are there known issues or functions that aren't working currently in your
   attached code (note I give half credit for any reasonably sized explained bug)?
  If so, explain.
  using the hashlib.sha224() function does not fully ensure that ts1 and ts2 will get an equal load of work. For example if the query has a stack of addresses, witch will go through the digest and finding the modulo value, are all even, they will all be sent to ts1. But in most of our test cases it seemed to split them
  
3. What problems did you face developing code for this project?
    timeout functions broke the connection of ts to ls so we had to figure out how to catch these errors and not just send the error back to LS but to continue the TS server. We also had some errors in connecting to cloudflare because we were using the wrong port number but fixed that eventually
    
4. What did you learn by working on this project?
    We learned about timeouts and how to best use try excepts. We also grew in our knowledge of hashlib, and overall are more confident in our socket programming, as this probably took us the least time but was the hardest technically.
