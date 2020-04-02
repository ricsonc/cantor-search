In [this blog post](http://math.andrej.com/2007/09/28/seemingly-impossible-functional-programs/), Martin Escardo describes how, for any function f mapping infinite binary sequences to {0,1}, it's possible to find x such that f(x) = 1, or to determine that \forall x, f(x) = 0 -- and this in finite time.

The blog post is fairly technical and even as someone who has a passing familiarity with haskell, it took me a few passes to decipher. I've implemented everything up to the "modulus function" -- about the half of the post, in python. This makes it obvious that haskell's laziness semantics are actually doing a lot of the heavy lifting in the blog post.

I recommend running the code with [pypy](https://www.pypy.org/) because otherwise it is painfully slow.
