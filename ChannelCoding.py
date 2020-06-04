from Huffman import *
import random
from noise import *


def channelCoding(cipherText):
    convolutionalCoding = dict()
    convolutionalCoding["00"] = dict()
    convolutionalCoding["01"] = dict()
    convolutionalCoding["10"] = dict()
    convolutionalCoding["11"] = dict()
    convolutionalCoding["00"]["0"] = ("00", "00")  # in state 00 if 0 is data ->  go to state 00 and parity is 00
    convolutionalCoding["00"]["1"] = ("10", "11")  # in state 00 if 1 is data ->  go to state 10 and parity is 11
    convolutionalCoding["10"]["0"] = ("01", "11")  # in state 10 if 0 is data ->  go to state 01 and parity is 11
    convolutionalCoding["10"]["1"] = ("11", "00")  # in state 10 if 1 is data ->  go to state 11 and parity is 00
    convolutionalCoding["11"]["0"] = ("01", "01")  # in state 11 if 0 is data ->  go to state 01 and parity is 01
    convolutionalCoding["11"]["1"] = ("11", "10")  # in state 11 if 1 is data ->  go to state 11 and parity is 10
    convolutionalCoding["01"]["0"] = ("00", "10")  # in state 01 if 0 is data ->  go to state 00 and parity is 10
    convolutionalCoding["01"]["1"] = ("10", "01")  # in state 01 if 1 is data ->  go to state 10 and parity is 01
    currentState = "00"
    codeWord = list()
    for i in range(len(cipherText) - 1, -1, -1):
        nextState, code = convolutionalCoding[currentState][cipherText[i]]
        currentState = nextState
        codeWord.insert(0, code)
    return "".join(codeWord)


def channelDecoding(codeWord):
    Trellis = dict()
    Trellis["00"] = (["0", "00", "00"], ["0", "10", "01"])  # [incoming bit, parity , prev state]
    Trellis["01"] = (["0", "11", "10"], ["0", "01", "11"])
    Trellis["10"] = (["1", "11", "00"], ["1", "01", "01"])
    Trellis["11"] = (["1", "00", "10"], ["1", "10", "11"])
    states = ["00", "01", "10", "11"]

    splitedCodeWord = list()
    for i in range(0, len(codeWord)):  # split codeword in 2 for example 010011 into ['01', '00', '11']
        if i % 2 == 0:
            splitedCodeWord.append(codeWord[i] + codeWord[i + 1])

    pathMetric = [dict() for i in range(0, len(splitedCodeWord) + 1)]
    # pathMetric[timeSlot][state] = value

    pathMetric[0]["00"] = 0  # initial path metric of state 00 in time 0 is 0 and others is infinite
    pathMetric[0]["01"] = 2 ** 32
    pathMetric[0]["10"] = 2 ** 32
    pathMetric[0]["11"] = 2 ** 32

    for i in range(0, len(splitedCodeWord)):
        for state in states:
            firstState, secondState = Trellis[state]
            pair_bit = len(splitedCodeWord) - i - 1
            firstPathCost = pathMetric[i][firstState[2]] + hammingDistance(splitedCodeWord[pair_bit], firstState[1])
            secondPathCost = pathMetric[i][secondState[2]] + hammingDistance(splitedCodeWord[pair_bit], secondState[1])
            bestPath = min(firstPathCost, secondPathCost)
            pathMetric[i + 1][state] = bestPath
    print(pathMetric)
    path = list()
    currentState = findMinimumState(pathMetric[len(pathMetric) - 1])

    for i in range(len(splitedCodeWord) - 1, -1, -1):
        firstState, secondState = Trellis[currentState]
        firstPathCost = pathMetric[i][firstState[2]] + hammingDistance(splitedCodeWord[i], firstState[1])
        secondPathCost = pathMetric[i][secondState[2]] + hammingDistance(splitedCodeWord[i], secondState[1])
        if firstPathCost == secondPathCost:
            if random.randint(0, 1) == 0:
                currentState = firstState[2]
                path.append(firstState[0])
            else:
                currentState = secondState[2]
                path.append(secondState[0])
        elif firstPathCost > secondPathCost:
            currentState = secondState[2]
            path.append(secondState[0])
        else:
            currentState = firstState[2]
            path.append(firstState[0])
    return "".join(path)


def hammingDistance(code1, code2):
    if len(code1) != len(code2):
        print("Codes should be equal in size")
        return

    hammingDist = 0
    for i in range(0, len(code1)):
        hammingDist += abs(int(code1[i]) - int(code2[i]))
    return hammingDist


def findMinDistance(firstPathCost, secondPathCost):
    if firstPathCost == secondPathCost:
        return secondPathCost
    if firstPathCost > secondPathCost:
        return secondPathCost
    else:
        return firstPathCost


def findMinimumState(timeSlot):  # timeSlot is a dictionary that key is state and value is path metric
    minimum = 2 ** 32 + 1
    minimumState = "00"
    for state in timeSlot:
        if timeSlot[state] < minimum:
            minimum = timeSlot[state]
            minimumState = state
    return minimumState


def testChannelCoding():
    numBit = 3
    for num in range(2 ** numBit):
        binary = bin(num)[2:].zfill(numBit)
        print(binary + "  convert To: " + channelCoding(binary))
    print("\n")


if __name__ == '__main__':
    Nodes = generateNodes()
    HuffmanCode = generateHuffman(Nodes)
    decoder = HuffmanDecoder(HuffmanCode)

    plainText = "alirezazarenejad"
    cipherText = sourceCoding(HuffmanCode, plainText)
    print("encode huffman code is: " + cipherText)

    codeWord = channelCoding(cipherText)
    print("channelCoding: " + codeWord)

    decodedWord = channelDecoding(codeWord)
    print("decoded word:" + decodedWord)

    decodedData = destinationDecoding(decoder, decodedWord)
    print("decodedData : ", decodedData)

    print("\n\nwith noise:")
    noisyCodeWord = noise(codeWord)
    print("noisy codeword: " + noisyCodeWord)
    decodedWordNoisy = channelDecoding(noisyCodeWord)
    print("decoded word:" + decodedWordNoisy)
    decodedDataNoisy = destinationDecoding(decoder, decodedWordNoisy)
    print("decodedData : ", decodedDataNoisy)
