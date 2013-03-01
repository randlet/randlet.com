title: Debuggex - A visual regex debugging tool
date: 2013-03-01
tags: [regex, tools, python, javascript]
blurb: Debuggex is an excellent online tool for debugging regexes.

Yesterday for a project at work I needed to develop some regexes to parse a
bunch of strings like:

    Dmax <= 30Gy(35.1Gy)
    Dmin >= 100.4cGy (99Gy)
    D90% > 20.1 Gy
    V2Gy > 80.0% (75%)
    V10Gy < 100cc
    
and so on. I was having a bit of trouble getting the regex to match up all
the different cases (as everyone knows, 
[regexs can be a bit tricky to get right](http://www.codinghorror.com/blog/2008/06/regular-expressions-now-you-have-two-problems.html) 
:). I remembered 
[reading something on Hacker News](http://news.ycombinator.com/item?id=5265567) 
a couple of days ago about a [visual regex debugger](http://www.debuggex.com) so I decided to give it a shot.

<br/>

This tool rocks.

<br/>

It displays a visual flow of how the current regex is matching, shows you
which part of your test string is currently matching and a really cool
feature is that it will generate random matches to the current regex. If
you're interested in an example, 
[here's my first pass](http://www.debuggex.com/?re=%5Bd%7CD%5D%5Cs%2A%28max%7Cmin%7Cmean%7C%28%5B0-9%5D%2B%28%5C.%5B0-9%5D%2A%29%3F%29%25%29%5Cs%2A%28%3C%7C%3C%3D%7C%3D%7C%3E%3D%7C%3E%29%5Cs%2A%28%28%5B0-9%5D%2B%28%5C.%5B0-9%5D%2A%29%3F%29%28Gy%7CcGy%29%29%28%5Cs%2A%28%5C%28%28%28%5B0-9%5D%2B%28%5C.%5B0-9%5D%2A%29%3F%29%28cGy%7CGy%29%29%5C%29%29%7C%24%29&str=D90%25+%3E%3D+1234.5Gy%2850.6Gy%29) 
at parsing the "D" strings above.  The actual Python re that I used looks slightly different:
    
    "d\s*(?P<type>max|min|mean|(?P<volume>[0-9]+(\.[0-9]*)?)%)\s*(?P<comparison><|<=|=|>=|>)\s*((?P<hard_limit>[0-9]+(\.[0-9]*)?)(?P<limit_unit>gy|cgy))(\s*(\(((?P<soft_limit>[0-9]+(\.[0-9]*)?)(?P=limit_unit))\))|$)"        
    
because I used named groups and lowercased the string before matching but Debuggex made it a snap to get to this point. 

<br/>

Check out [Debuggex](http://www.debuggex.com) next time you are working on a tricky regex.
 