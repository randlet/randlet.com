title: Formatting floats to a specific number of significant digits in Python
date: 2013-08-25
tags: [python, javascript]
blurb: A Python function for formatting floats to a specific number of significant digits. This is a port of Javascripts Number.toPrecision method.
thumbnail: digits.jpg
attribution: http://www.flickr.com/photos/mulmatsherm/2221220246/

Often when you are writing scientific code you want to display numbers with a
specific number of significant digits.  This is easily achievable using
[Python's exponential format
specifier](http://docs.python.org/2/library/string.html#format-specification-mini-language):
`%e` or `%E`. For example if you want to display the number 1.23 to 4
significant digits you can do `"%.3E" % (1.23)` and Python will correctly print
`1.230E+00`.  However, sometimes you would rather have more "friendly"
formatting for small numbers (e.g. 40.54 instead of 4.054E+01) and fall back to
exponential notation when numbers are much greater than 1 or much smaller than
1.  The "general" format specifiers `%g` and `%G` come very close to the
correct behavior.  The general format specifier is [described in the
docs](http://docs.python.org/2/library/string.html#format-specification-mini-language)
as follows:

> General format. For a given precision p >= 1, this rounds the number to p
> significant digits and then formats the result in either fixed-point format
> or in scientific notation, depending on its magnitude.
>
> The precise rules are as follows: suppose that the result formatted with
> presentation type 'e' and precision p-1 would have exponent exp. Then if -4
> <= exp < p, the number is formatted with presentation type 'f' and
> precision p-1-exp. Otherwise, the number is formatted with presentation
> type 'e' and precision p-1. In both cases __insignificant trailing zeros are
> removed from the significand, and the decimal point is also removed if
> there are no remaining digits following it__.

Note the bit I've emphasised in the last paragraph.  Even though the docs say
that only "insignficant trailing zeros's" are trimmed this is a little bit
misleading. For example, if you tried `"%.4G" % (1.230)` you might expect
Python to print "1.230" i.e. you would expect 4 significant figures to be
included. What actually happens is that Python trims that trailing zero even
though it is a significant digit in this case. So when you try `"%.4G" %
(1.230)` what you get is "1.23" with only 3 significant figures.

I was playing around with some Javascript and noticed the
[Number.toPrecision](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toPrecision)
method does precisely what we are looking for.  If you enter `(1.230).toPrecision(4)` in your
Javascript console, Javascript will correctly print "1.230", likewise if you try
`(123000000).toPrecision(4)` you will correctly get `"1.230e+8"`.

I wanted to duplicate this behaviour in Python so I dug around in the
[WebKit source code for the toPrecision method](https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp)
and ported it to Python as seen below:

    :::python

    def to_precision(x,p):
        """
        returns a string representation of x formatted with a precision of p

        Based on the webkit javascript implementation taken from here:
        https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
        """


        x = float(x)

        if x == 0.:
            return "0." + "0"*(p-1)

        out = []

        if x < 0:
            out.append("-")
            x = -x

        e = int(math.log10(x))
        tens = math.pow(10, e - p + 1)
        n = math.floor(x/tens)

        if n < math.pow(10, p - 1):
            e = e -1
            tens = math.pow(10, e - p+1)
            n = math.floor(x / tens)

        if abs((n + 1.) * tens - x) <= abs(n * tens -x):
            n = n + 1

        if n >= math.pow(10,p):
            n = n / 10.
            e = e + 1


        m = "%.*g" % (p, n)

        if e < -2 or e >= p:
            out.append(m[0])
            if p > 1:
                out.append(".")
                out.extend(m[1:p])
            out.append('e')
            if e > 0:
                out.append("+")
            out.append(str(e))
        elif e == (p -1):
            out.append(m)
        elif e >= 0:
            out.append(m[:e+1])
            if e+1 < len(m):
                out.append(".")
                out.extend(m[e+1:])
        else:
            out.append("0.")
            out.extend(["0"]*-(e+1))
            out.append(m)

        return "".join(out)

Now you can have nicely formatted numbers with the correct number of
significant digits always preserved!

    :::python

    >>> to_precision(1.23,4)
    '1.230'
    >>> to_precision(123000000,4)
    '1.230e+8'
    >>> to_precision(0.00000123,7)
    '1.230000e-6'
    >>>

The code is [on GitHub](https://github.com/randlet/to-precision) and hopefully
someone else finds this function useful.

Update: [BebeSparkelSparkel](https://github.com/BebeSparkelSparkel/) has added more functionality
to my original implementation.  His version can be found here: https://github.com/BebeSparkelSparkel/to-precision

