import sys
import os
import random


def readFastA(filename):
    name = []
    genome = []
    with open(filename, 'r') as fh:
        i = 0
        while True:
            nav = fh.readline().rstrip()
            gen = fh.readline().rstrip()
            if len(nav) == 0:
                break
            # x = {nav:i}
            # print(x)
            name.append(nav)
            genome.append(gen)
            i += 1
            '''
            for line in f:
                if line[0] != '>':
                    genome += line.rstrip()
                    len1 += line.__len__()
            length.append(len1)
            '''
    return genome,name

def readFastQ(filename):
    sequences = []
    qualities = []
    with open(filename) as fh:
        while True:
            fh.readline()
            seq = fh.readline().rstrip()
            fh.readline()
            qual = fh.readline().rstrip()
            if len(seq) == 0:
                break
            sequences.append(seq)
            qualities.append(qual)
    return sequences, qualities

def create_cigar(len):
    cigar = ['='] * len
    return cigar


def naiveFind(S, T, N, Q):
    i = 0
    j = 0
    while i < len(S) and j < len(T):
            if S[i] == T[j]:
                i += 1
                j += 1
            else:
                i = i - j + 1
                j = 0
            if j >= len(T):
                print(T," 0 ", N,i - len(T) + 1, " 0 ",end="")
                print(f' {len(T)}M', " * 0 0 ", T, Q)
                j = 0
            # return i - len(T) + 1
    return -1

def calNext(T):
    i = 0
    next = [-1]
    j = -1
    while(i<len(T) - 1):
        if(j == -1 or T[i] == T[j]):
            i += 1
            j += 1
            next.append(j)
        else:
            j = next[j]
    return next


def KMP(S, T, N, Q):
    next = calNext(T)
    i = 0
    j = 0
    while(i<len(S) and j<len(T)):
        if(j == -1 or S[i] == T[j]):
            i += 1
            j += 1
        else:
            j = next[j]
        if (j >= len(T)):
            print(T," 0 ", N,i - len(T) + 1, " 0 ",end="")
            print(f' {len(T)}M', " * 0 0 ", T, Q)
            j = 0
    return -1
    '''
    if(j >= len(T)):
        return i - len(T) + 1 # run till the last
    else:
        return -1
    '''

def bmh(S,T, N, Q):
    n = len(S)
    m = len(T)
    cigar = create_cigar(m)
    if m > n:
        return -1
    skip = []
    for k in range(200):
        skip.append(m)
    # print(skip[ord("H")])
    for k in range(m - 1):# does not count the last letter in T array, so if the last letter didn't show before it, it just get the length
        # print(k)
        # print("a", m - k - 1)
        skip[ord(T[k])] = m - k - 1
    # print(skip[ord("A")],skip[ord("B")],skip[ord("C")],skip[ord("D")])
    k = m - 1
    # print(skip[ord("H")])
    j = m - 1
    i = k
    tmp = 0
    while(k < n):
        if tmp == 1:
            i += 1
        else:
            i = k
        j = m - 1
        # i = k
        tmp = 0
        while j >= 0 and S[i] == T[j]:
            j -= 1
            i -= 1
            # print("a:",j)
        if j == -1:
            """
            print(seqs[j], " 0 ", name[i], " ", end="")
            print(bmh(genome[i], seqs[j], name[i], quals[j]), end="")
            print(" 0 ", end="")
            print(" * 0 0 ", end="")
            print(seqs[j], " ", end="")
            print(quals[j])
            """
            print(T," 0 ", N," ",i+2 , " 0 ",end="")
            print(f'{m}M', " * 0 0 ", T, Q)
            tmp = 1
        k += skip[ord(S[k])]
    return -1

def simulate_cigar(n, d):
    cigar = ['='] * n
    for _ in range(d):
        mutation = random.randrange(3)
        position = random.randrange(n)
        if mutation == 0:
            cigar[position] = 'X'
        elif mutation == 1:
            cigar[position] = 'D'
        else:
            cigar[position] = 'I'
    return ''.join(cigar)


if __name__ == '__main__':

    genome, name = readFastA('test.fa')
    seqs, quals = readFastQ('test1.fq')

    # print(name)
    # print(genome)
    # print("seqs: ",seqs)
    # print("quals: ",quals)
    len1 = len(genome)
    len2 = len(seqs)
    # print(len1,len2)
    # print(name[1])
    # print(seqs[1])
    i = 0; j = 0
    # print(name[0],name[1])
    '''
        STR = "ATCGCTCGTTGCA"
        print('Naive: ', naiveFind(STR, "CTCG"))
        print('Naive: ', naiveFind(STR, "CCC"))

        print("KMP: ", KMP(STR, "GCA"))

        print('BMH: ',bmh(STR,"CTCG"))
        print(bmh("HHHHTOOTH","TOOTH"))
    '''
    while j < len2:
        while i < len1:
            # The three below can find all matching parts in the sequences
            if sys.argv[1] == 'kmp':
                KMP(genome[i],seqs[j], name[i], quals[j])
            elif sys.argv[1] == 'bmh':
                bmh(genome[i], seqs[j], name[i], quals[j])
                # print("a")
            elif sys.argv[1] == 'naive':
                naiveFind(genome[i], seqs[j], name[i], quals[j])

            '''
            # print('Naive: ', naiveFind(genome[i],seqs[j]))
            # print('KMP: ', KMP(genome[i],seqs[j]))
            # print(seqs[j]," 0 ", name[i]," ", end="" )
            # print(bmh(genome[i],seqs[j], name[i], quals[j]),end="")
            # print(" 0 ", end="")
            # print(" * 0 0 ",end="")
            # print(seqs[j]," ", end="")
            # print(quals[j])

            # print('BMH: ', bmh(genome[i],seqs[j]))
            # print('CIGAR: ',simulate_cigar(len(genome[i]),len(seqs[j])))
            '''
            i += 1
        j += 1
        i = 0

    # print('KMP: ', KMP(" ", "abc"))

