
class CantorInterface:
    '''
    The Cantor space is the set of all infinite binary strings {0,1}^\infty.
    We can talk about each element of cantor space as a mapping from the natural numbers to {0,1}.
    Thus any object implementing __getitem__ : N -> {0,1} is a cantor.
    '''
    def __getitem__(self, i): raise NotImplemented

class PrependCantor(CantorInterface):
    def __init__(self, first, rest):
        self.first = first; self.rest = rest
        
    def __getitem__(self, i):
        return self.first if i == 0 else self.rest[i-1]

class DeferredCantor(CantorInterface): 
    def __init__(self, thunk):
        self.thunk = thunk; self.cantor = None
        
    def __getitem__(self, i):
        self.cantor = self.cantor if self.cantor else self.thunk()
        return self.cantor[i]            
    
def find(pred):
    '''
    given pred : Cantor -> {0,1}
    find x such that pred(x) = True if such x exists
    otherwise return x \in Cantor
    '''
    def prefix_with(fn, first):
        return lambda x: fn(PrependCantor(first, x))
    
    def go():
        pred_0 = prefix_with(pred, 0)
        if forsome(pred_0):
            return PrependCantor(0, find(pred_0))
        else:
            return PrependCantor(1, find(prefix_with(pred, 1)))
    return DeferredCantor(go)

def forsome(pred): 
    return pred(find(pred))

def equal(pred_a, pred_b):
    return not forsome(lambda x: pred_a(x) != pred_b(x))

## this function not necessary for understanding `find`.
def modulus(pred):
    '''
    the modulus of a function f: {0,1}^\infty -> {0,1} is the least k such that
    for any input sequence x, f(x) only depends on the first k elements in the sequence.
    '''
    def forsome_pair(pair_pred): # \exists x, y s.t pair_pred(x,y) = 1 ?
        return forsome(lambda x: forsome(lambda y: pair_pred(x, y)))

    for n in range(1000): #1000 ~= infinity
        def counterexample_n(x, y): #is x, y a counterexample to modulus(f) = n?
            return all((x[i] == y[i] for i in range(n))) and pred(x) != pred(y)

        if not forsome_pair(counterexample_n):
            return n

def f(x): return x[5*x[3] + 3*x[5] + 3]

def g(x): return x[x[3] + 8*x[5]]

def h(x):
    if   x[3] == 0 and x[5] == 0: return x[3]
    elif x[3] == 0 and x[5] == 1: return x[6]
    elif x[3] == 1 and x[5] == 0: return x[8]
    elif x[3] == 1 and x[5] == 1: return x[11]

if __name__ == '__main__':
    print 'are f and g equal?', equal(f, g)
    print 'are f and h equal?', equal(f, h)
    print 'are g and g equal?', equal(g, g)

    print '' 
    counterexample = find(lambda x: f(x) != g(x))
    print 'a counterexample to f(x) = g(x) is'
    print ''.join((str(counterexample[i]) for i in range(15))) + '...'
    print 'f(x) = %d, g(x) = %d' % (f(counterexample), g(counterexample))

    #these might take a few minutes to run
    print ''
    print 'the modulus of g is', modulus(g)
    print 'the modulus of f is', modulus(f)
