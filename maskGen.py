# -*- coding: utf-8 -*-
'''
Hashcat mask generator made by Daniel_YC
Quick and dirty but it should work

Use for fun an profit
'''


filename = '_output'
words = []
chars = ''
pos = ''
maxc = 0
hloc = ''
hmode = ''

def all_casings(input_string):
    if not input_string:
        yield ""
    else:
        first = input_string[:1]
        if first.lower() == first.upper():
            for sub_casing in all_casings(input_string[1:]):
                yield first + sub_casing
        else:
            for sub_casing in all_casings(input_string[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing


def AskWords():
    global words
    global filename
    w = input('Enter words separated by spaces (not case sensitive, only alphabetical characters): ')
    com = input('Do you want to combine the words as well? [Y]es / [N]o: ')
    wo = w.split()
    if com.upper() == 'Y' or com.upper() == 'YES':
        wo.append(''.join(wo))
    for word in wo:
        for x in list(all_casings(word)):
            words.append(x)
    filename = '_' + wo[0]


def AskChar():
    global chars
    print('Character possibilities:\n')
    print('?l = abcdefghijklmnopqrstuvwxyz')
    print('?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    print('?d = 0123456789')
    print('?h = 0123456789abcdef')
    print('?H = 0123456789ABCDEF')
    print('?s = «space»!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~')
    print('?a = ?l?u?d?s')
    print('?b = 0x00 - 0xff')
    print('custom\n')
    inp = input('Enter a charset or enter a custom charset: ')
    if inp in '?l ?u ?d ?h ?H ?s ?a ?a':
        chars = inp
    else:
        chars = '-1 ' + inp


def AskPos():
    global pos
    print('Position possibilities:\n')
    print('1. before word(s)')
    print('2. after word(s)')
    print('3. before and after words\n')
    inp = input('Enter the number of the option: ')
    if inp == '1':
        pos = 'B'
    elif inp == '2':
        pos = 'A'
    elif inp == '3':
        pos = 'BA'
    else:
        print('[*] Invalid input')
        AskPos()


def AskMax():
    global maxc
    inp = input('Enter max number of brute force characters: ')
    if not inp.isdigit():
        print('[*] Not a number')
        AskMax()
    maxc = int(inp)


def AskHash():
    global hloc, hmode
    hloc = input('Enter location of hashlist: ')
    inp = input('Enter hashmode: ')
    if inp.isdigit():
        hmode = inp


def gen():
    mask = []
    commands = []
    if '-1' not in chars:
        if pos == 'B':
            for word in words:
                for x in range(maxc):
                    mask.append(((x + 1) * chars) + word)
        elif pos == 'A':
            for word in words:
                for x in range(maxc):
                    mask.append(word + ((x + 1) * chars))
        elif pos == 'BA':
            for word in words:
                for x in range(maxc):
                    mask.append(word + ((x + 1) * chars))
            for word in words:
                for x in range(maxc):
                    mask.append(((x + 1) * chars) + word)
            for x in range(1, maxc):
                aft = maxc - x
                for y in range(aft + 1):
                    for word in words:
                        mask.append((x * chars) + word + (y * chars))
    else:
        if pos == 'B':
            for word in words:
                for x in range(maxc):
                    mask.append(chars[3:] + ',' + ((x + 1) * '?1') + word)
        elif pos == 'A':
            for word in words:
                for x in range(maxc):
                    mask.append(chars[3:] + ',' + word + ((x + 1) * '?1'))
        elif pos == 'BA':
            for word in words:
                for x in range(maxc):
                    mask.append(chars[3:] + ',' + ((x + 1) * '?1') + word)
            for word in words:
                for x in range(maxc):
                    mask.append(chars[3:] + ',' + word + ((x + 1) * '?1'))
            for x in range(1, maxc):
                aft = maxc - x
                for y in range(aft + 1):
                    for word in words:
                        mask.append(chars[3:] + ',' + (x * '?1') + word + (y * '?1'))

    for c in mask:
        commands.append(c + '\n')

    f = open(filename + '.hcmask', 'w')
    for cm in commands:
        f.write(cm)
    f.close()

    open(filename + '.cmd', 'w').write('hashcat64.exe -m %s %s --session gen -a 3 %s -w 3 -O --gpu-temp-disable\n' %(str(hmode), hloc, filename + '.hcmask'))
    print('\n[*] Done!')


def main():
    AskWords()
    AskChar()
    AskMax()
    AskPos()
    AskHash()
    gen()


if __name__ == '__main__':
    main()
