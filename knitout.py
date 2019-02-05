# python3
# see example() for usage

import re
validHeaders = ['Carriers', 'Machine', 'Position', 'Yarn', 'Gauge']
############### helpers ######################################################


reg = re.compile("([a-zA-Z]+)([\+\-]?[0-9]+)")
def shiftCarrierSet(args, carriers):
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
        if not m and (bn == 'f' or bn == 'b' or bn == 'fs' or bn == 'bs'):
            bed = bn
            if not len(args):
                raise ValueError("Needle not specified")
            if  isinstance(args[0],int) or args[0].isdgit():
                needle = int(args.pop(0))

        else:
            if (m.group(1) == 'f' or m.group(1) == 'b' or m.group(1) == 'fs' or m.group(1) == 'bs'):
                bed = m.group(1)
            else:
                raise ValueError("Invalid bed type. Must be 'f' 'b' 'fs' 'bs'.")
            if m.group(2):
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
    if direction != '+' and direction != '-':
        raise ValueError("Invalid direction: " + direction)
    return direction

##############################################################################


class Writer:

    def __init__(self, cs):
        # array of carrier names, front-to-back
        self.carriers = list()
        # array of operations, strings
        self.operations = list()
        # array of headers, strings
        self.headers = list()

        self.carriers = cs.split()
        self.addHeader('Carriers', cs);
    def addHeader(self, name, value):
        if not name in validHeaders:
            raise ValueError("Unknown header, must be " + ' '.join(validHeaders) + "; " + name)
        self.headers.append(';;' + name + ': ' + value)

    def addRawOperation(self, op):
        self.operations.append(op)

    def ingripper(self, *args):
        argl = list(args)
        self.perations.append('in ' +  shiftCarrierSet(argl, self.carriers))


    def inhook(self, *args):
        argl = list(args)
        self.operations.append('inhook ' + shiftCarrierSet(argl, self.carriers))



    def outgripper(self, *args):
        argl = list(args)
        self.operations.append('out ' + shiftCarrierSet(argl, self.carriers))


    def outhook(self, *args):
        argl = list(args)
        self.operations.append('outhook ' + shiftCarrierSet(argl, self.carriers))



    def releasehook(self, *args):
        argl = list(args)
        self.operations.append('releasehook ' + shiftCarrierSet(argl, self.carriers))


    def rack(self, r):
        if not (type(r) == int or type(r) == float or (type(r) == str and r.isdigit())):
            raise ValueError("Rack is not an integer or fraction")
        #TODO only certain values make sense
        self.operations.append('rack ' + str(r))


    def knit(self, *args):
        argl = list(args)
        direction = shiftDirection(argl)
        bn = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)
        self.operations.append('knit ' + direction + ' ' + bn + ' ' + cs)

    def tuck(self, *args):
        argl = list(args)
        direction = shiftDirection(argl)
        bn = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)
        self.operations.append('tuck ' + direction + ' ' + bn + ' ' + cs)


    def xfer(self, *args):
        argl = list(args)
        bn_from = shiftBedNeedle(argl)
        bn_to = shiftBedNeedle(argl)
        self.operations.append('xfer ' + bn_from + ' ' + bn_to)


    def split(self, *args):
        argl = list(args)
        direction  = shiftDirection(argl)
        bn_from = shiftBedNeedle(argl)
        bn_to = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)
        self.operations.append('shift '+ direction + ' '  + bn_from + ' ' + bn_to + ' ' + cs)


    def miss(self, *args):
        argl = list(args)
        direction = shiftDirection(argl)
        bn = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)
        self.operations.append('miss ' + direction + ' ' + bn + ' ' + cs)

    def drop(self, *args):
        argl = list(args)
        bn = shiftBedNeedle(argl)
        self.operations.append('drop ' + bn)

    def amiss(self, *args):
        argl = list(args)
        bn = shiftBedNeedle(argl)
        self.operations.append('amiss ' + bn)

    def pause(self):
        self.operations.append('pause')

    def comment(self, commentString):
        if type(commentString) != str:
            raise ValueError('comment has to be string')
        self.operations.append(';' + commentString)


    #Extensions

    def stitchNumber(self, val):
        self.operations.append('x-stitch-number ' + str(val))

    def fabricPresser(self, mode):
        if not (mode == 'auto' or mode == 'on' or mode == 'off'):
            raise ValueError("Mode must be one of 'auto','on','off' : "+ str(mode))
        self.operations.append('x-fabric-presser ' + mode)

    def clear(self):
        #clear buffers
        self.headers = list()
        self.operations = list()

    def write(self, filename):
        version = ';!knitout-2\n'
        content = version + '\n'.join(self.headers) + '\n' +  '\n'.join(self.operations)
        try:
            with open(filename, "w") as out:
                print(content, file=out)
            print('wrote file ' + filename)
        except IOError as error:
            print('Could not write to file ' + filename)

def example():
    stockinette_rectangle()
    garter_rectangle()
    rib_rectangle()

def stockinette_rectangle(width=10, height=20):
    writer = Writer('1 2 3 4')
    writer.addHeader('Machine', 'swg')
    carrier = '1'
    writer.inhook(carrier)
    for i in range(width-1, 0, -2):
        writer.tuck('-', ('f',i), carrier)
    writer.releasehook(carrier)
    for i in range(0, width, 2):
        writer.tuck('+', ('f', i), carrier)
    for j in range(0, height):
        if j%2 == 0:
            for i in range(width, 0,-1):
                writer.knit('-', ('f', i-1), carrier)
        else:
            for i in range(0, width):
                writer.knit('+', ('f', i), carrier)

    writer.outhook(carrier)
    for i in range(0, width):
        writer.drop(('f', i))

    writer.write('stockinette-'+str(width)+'x'+str(height)+'.k')

def garter_rectangle(width=10, height=20):
    writer = Writer('1 2 3 4')
    writer.addHeader('Machine', 'swg')
    carrier = '1'
    writer.inhook(carrier)
    for i in range(width-1, 0, -2):
        writer.tuck('-', ('f',i), carrier)
    writer.releasehook(carrier)
    for i in range(0, width, 2):
        writer.tuck('+', ('f', i), carrier)
    for j in range(0, height):
        if j%2 == 0:
            for i in range(width, 0,-1):
                writer.knit('-', ('f', i-1), carrier)
        else:
            for i in range(0, width):
                writer.xfer(('f',i), ('b',i))
            for i in range(0, width):
                writer.knit('+', ('b', i), carrier)
            for i in range(0, width):
                writer.xfer(('b',i), ('f',i))

    writer.outhook(carrier)
    for i in range(0, width):
        writer.drop(('f', i))

    writer.write('garter-'+str(width)+'x'+str(height)+'.k')

def rib_rectangle(width=10, height=20):
    writer = Writer('1 2 3 4')
    writer.addHeader('Machine', 'swg')
    carrier = '1'
    writer.inhook(carrier)
    for i in range(width-1, 0, -2):
        bed = 'f'
        if i%2:
            bed = 'b'
        writer.tuck('-', (bed,i), carrier)
    writer.releasehook(carrier)
    for i in range(0, width, 2):
        bed = 'f'
        if i%2:
            bed = 'b'

        writer.tuck('+', (bed, i), carrier)
    for j in range(0, height):
        if j%2 == 0:
            for i in range(width, 0,-1):
                bed = 'f'
                if (i-1)%2:
                    bed = 'b'
                writer.knit('-', (bed, i-1), carrier)
        else:
            for i in range(0, width):
                bed = 'f'
                if i%2:
                    bed = 'b'
                writer.knit('+', (bed, i), carrier)

    writer.outhook(carrier)
    for i in range(0, width):
        writer.drop(('f', i))
        writer.drop(('b', i))

    writer.write('rib-'+str(width)+'x'+str(height)+'.k')


