# python3

# usage:

# import knitout
# knitout.init(carrier set)
# knitout.tuck('+','f0','1')
# knitout.rack(1)
# ...
# knitout.write(filename)
# mostly similar to js except 'in' is a python keyword

import re
# array of carrier names, front-to-back
carriers = list()
# array of operations, strings
operations = list()
# array of headers, strings
headers = list()
validHeaders = ['Machine', 'Position', 'Yarn', 'Gauge']
############### helpers ######################################################


reg = re.compile("([a-zA-Z]+)([0-9]+)")
def shiftCarrierSet(args):
    global carriers
    if len(args) == 0:
        raise AssertionError("No carriers specified")

    for c in args:
        if not str(c) in carriers:
            raise ValueError("Carrier not specified in initial set", c)
    cs = ' '.join(str(c) for c in args)
    return cs

def shiftBedNeedle(args):
    if len(args) == 0:
        raise AssertionError("No needles specified")
    bn = args.pop(0)
    if  not (type(bn) == str or type(bn) == list or type(bn) == tuple):
        raise AssertionError("Invalid BedNeedle type")
    bed = None
    needle = None
    if type(bn) == str:
        m = reg.match(bn)
        if (m.group(1) == 'f' or m.group(1) == 'b' or m.group(1) == 'fs' or m.group(1) == 'bs'):
            bed = m.group(1)
        else:
            raise ValueError("Invalid bed type. Must be 'f' 'b' 'fs' 'bs'.")
        if m.group(2).isdigit() :
            needle = m.group(2)
        else:
            raise ValueError("Invalid needle. Must be numeric.", m.group(2))
    else:
        if len(bn) != 2:
            raise ValueError("Bed and Needle need to be supplied.")
        if (bn[0] == 'f' or bn[0] == 'b' or bn[0] == 'fs' or bn[0] == 'bs'):
            bed = bn[0]
        else:
            raise ValueError("Invalid bed type. Must be 'f' 'b' 'fs' 'bs'.")
        if type(bn[1]) == int or bn[1].isdigit():
            needle = int(bn[1])
        else:
            raise ValueError("2.Invalid needle. Must be numeric.")

    return bed + str(needle)

def shiftDirection(args):
    if len(args) == 0:
        raise AssertionError("No direction specified")
    direction = args.pop(0)
    if direction != '+' and dir != '-':
        raise ValueError("Invalid direction")
    return direction

##############################################################################

def init(cs):
    global carriers
    carriers = cs.split()

def addHeader(name, value):
    global headers
    if not name in validHeaders:
        raise ValueError("Unknown header, must be " + ' '.join(validHeaders) + "; " + name)
    headers.append(';;' + name + ': ' + value)

def addRawOperation(op):
    global operations
    operations.append(op)

def ingripper(*args):
    global operations
    global carriers
    argl = list(args)
    operations.append('in ' +  shiftCarrierSet(argl))


def inhook(*args):
    global operations
    global carriers
    argl = list(args)
    operations.append('inhook ' + shiftCarrierSet(argl))



def outgripper(*args):
    global operations
    global carriers
    argl = list(args)
    operations.append('out ' + shiftCarrierSet(argl))


def outhook(*args):
    global operations
    global carriers
    argl = list(args)
    operations.append('outhook ' + shiftCarrierSet(argl))



def releasehook(*args):
    global operations
    global carriers
    argl = list(args)
    operations.append('releasehook ' + shiftCarrierSet(argl))


def rack(r):
    global operations
    if not (type(r) == int or type(r) == float or (type(r) == str and r.isdigit())):
        raise ValueError("Rack is not an integer or fraction")
    #TODO only certain values make sense
    operations.append('rack ' + str(r))


def knit(*args):
    global operations
    argl = list(args)
    direction = shiftDirection(argl)
    bn = shiftBedNeedle(argl)
    cs = shiftCarrierSet(argl)
    operations.append('knit ' + direction + ' ' + bn + ' ' + cs)

def tuck(*args):
    global operations
    argl = list(args)
    direction = shiftDirection(argl)
    bn = shiftBedNeedle(argl)
    cs = shiftCarrierSet(argl)
    operations.append('tuck ' + direction + ' ' + bn + ' ' + cs)


def xfer(*args):
    global operations
    argl = list(args)
    bn_from = shiftBedNeedle(argl)
    bn_to = shiftBedNeedle(argl)
    operations.append('xfer ' + bn_from + ' ' + bn_to)


def split(*args):
    global operations
    argl = list(args)
    direction  = shiftDirection(argl)
    bn_from = shiftBedNeedle(argl)
    bn_to = shiftBedNeedle(argl)
    cs = shiftCarrierSet(argl)
    operations.append('shift '+ direction + ' '  + bn_from + ' ' + bn_to + ' ' + cs)


def miss(*args):
    global operations
    argl = list(args)
    direction = shiftDirection(argl)
    bn = shiftBedNeedle(argl)
    cs = shiftCarrierSet(argl)
    operations.append('miss ' + direction + ' ' + bn + ' ' + cs)

def drop(*args):
    global operations
    argl = list(args)
    bn = shiftBedNeedle(argl)
    operations.append('drop ' + bn)

def amiss(*args):
    global operations
    argl = list(args)
    bn = shiftBedNeedle(argl)
    operations.append('amiss ' + bn)

def pause():
    global operations
    operations.append('pause')

def comment(commentString):
    global operations
    if type(commentString) != str:
        raise ValueError('comment has to be string')
    operations.append(';' + commentString)


#Extensions

def stitchNumber(val):
    global operations
    operations.append('x-stitch-number ' + str(val))

def fabricPresser(mode):
    global operations
    if not (mode == 'auto' or mode == 'on' or mode == 'off'):
        raise ValueError("Mode must be one of 'auto','on','off' : "+ str(mode))
    operations.append('x-fabric-presser ' + mode)

def write(filename):
    global headers
    global operations
    version = ';!knitout-2\n'
    content = version + '\n'.join(headers) + '\n' +  '\n'.join(operations)
    try:
        with open(filename, "w") as out:
            print(content, file=out)
    except IOError as error:
        print('Could not write to file ' + filename)

def example():
    #TODO simple stockinette hello world example
    global operations
    #init carrier set
    init('1 2 3 4 5')
    addHeader('Position', 'Right')
    ingripper(1,2)
    knit('+','f0','1','2')
    rack(-1)
    xfer('f0', ('b',1))
    rack(0)
    knit('+',['b',0],'1',2)
    knit('+',('f',0),'1','2')
    outgripper(1,2)
    print(operations)
    write('example.k')


