0. Please write down the full names and netids of all your team members.
-Maudiel Romero mar641
-Alex Miller arm297
1. Briefly discuss how you implemented the LS functionality of
   tracking which TS responded to the query and timing out if neither
   TS responded.
   -We
2. Are there known issues or functions that aren't working currently in your
   attached code (note I give half credit for any reasonably sized explained bug)?
  If so, explain.
  using the hashlib.sha224() function does not fully ensure that ts1 and ts2 will get an equal load of work.
  For example if the query has a stack of addresses, witch will go through the digest and finding the modulo value, are
  all even, they will all be sent to ts1.
3. What problems did you face developing code for this project?
    timeout functions broke the connection of ts to ls.
    we are not sure if we set up the
4. What did you learn by working on this project?
    We learned multiple timeout
