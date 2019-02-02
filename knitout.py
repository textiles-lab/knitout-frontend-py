# python3

# usage:

# import knitout
# knitout.init(carrier set)
# knitout.tuck('+','f0','1')
# knitout.rack(1)
# ...
# knitout.write(filename)
# mostly similar to js except 'in' is a python keyword


# array of carrier names, front-to-back
carriers = list()
# array of operations, strings
operations = list()
# array of headers, strings
headers = list()

############### helpers ######################################################

#TODO parsing bed needles, verify types

def shiftCarrierSet(args):
    if len(args) == 0:
        raise AssertionError("No carriers specified")
    #TODO handle variations
    cs = ' '.join(str(c) for c in args)
    return cs

def shiftBedNeedle(args):
    if len(args) == 0:
        raise AssertionError("No needles specified")
    #TODO handle variations, parse bed and needle, verify validity
    bn = args.pop(0)
    return bn

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
    headers.append(';;' + name + ': ' + value)

def addRawOperation(op):
    global operations
    operations.append(op)

def ingripper(*args):
    global operations
    global carriers
    if len(carriers) == 0:
        raise AssertionError("No carriers set.")
    operations.append('in ' + ''.join(str(c) for c in args))


def inhook(*args):
    global operations
    global carriers
    if len(carriers) == 0:
        raise AssertionError("No carriers set.")
    operations.append('inhook ' + ''.join(str(c) for c in args))



def outgripper(*args):
    global operations
    global carriers
    if len(carriers) == 0:
        raise AssertionError("No carriers set.")
    operations.append('out ' + ''.join(str(c) for c in args))


def outhook(*args):
    global operations
    global carriers
    if len(carriers) == 0:
        raise AssertionError("No carriers set.")
    operations.append('outhook ' + ''.join(str(c) for c in args))



def releasehook(*args):
    global operations
    global carriers
    if len(carriers) == 0:
        raise AssertionError("No carriers set.")
    operations.append('releasehook ' + ''.join(str(c) for c in args))


def rack(r):
    global operations
    #TODO check numeric r
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

#TODO xfer, split, miss, amiss, drop, pause, extensions:stitch number, fabric presser, headers

def write(filename):
    global headers
    global operations
    version = ';knitout-2\n'
    content = version + '\n'.join(headers) + '\n'.join(operations)
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
    rack(1.)
    knit('+','f0','1','2')
    print(operations)
    write('example.k')


