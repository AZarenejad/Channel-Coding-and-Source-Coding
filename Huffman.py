class HuffNode:
    def __init__(self, value, alphabet):
        self.value = value
        self.alphabet = alphabet
        self.left = None
        self.right = None


def generateNodes():
    alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                 "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    fileStream = open("freq.txt", "r")
    frequencies = fileStream.read().split(",")

    Nodes = list()

    for i in range(0, len(alphabets)):
        Nodes.append(HuffNode(float(frequencies[i]), alphabets[i]))

    return Nodes


def generateHuffman(Nodes):
    if len(Nodes) == 0:
        return None
    if len(Nodes) == 1:
        return {Nodes[0].alphabet: 0}

    while len(Nodes) != 1:
        left = Nodes[extractMin(Nodes)]
        Nodes.remove(left)
        right = Nodes[extractMin(Nodes)]
        Nodes.remove(right)
        parent = HuffNode(left.value + right.value, left.alphabet + right.alphabet)
        parent.left = left
        parent.right = right
        Nodes.append(parent)

    root = Nodes[0]
    HuffmanCode = dict()
    code = ""
    inOrderIterator(root, HuffmanCode, code)
    return HuffmanCode


def extractMin(Nodes):
    minIndex = 0
    minValue = Nodes[0].value
    for i in range(0, len(Nodes)):
        if Nodes[i].value < minValue:
            minValue = Nodes[i].value
            minIndex = i
    return minIndex


def inOrderIterator(root, dictionary, code):
    if root.left is None and root.right is None:
        dictionary[root.alphabet] = code
        return
    inOrderIterator(root.left, dictionary, code + "0")
    inOrderIterator(root.right, dictionary, code + "1")


def sourceCoding(codeBook, plainText):
    plainText = list(plainText)

    for i in range(0, len(plainText)):
        plainText[i] = codeBook[plainText[i]]

    return "".join(plainText)


def HuffmanDecoder(HuffmanCode):
    root = HuffNode(-1, None)
    rootPrime = root

    for codeWord in HuffmanCode:
        code = HuffmanCode[codeWord]

        for binary in code:
            if binary == "0":
                if root.left is None:
                    newNode = HuffNode(-1, None)
                    root.left = newNode
                root = root.left
            if binary == "1":
                if root.right is None:
                    newNode = HuffNode(-1, None)
                    root.right = newNode
                root = root.right
        root.alphabet = codeWord
        root = rootPrime

    return root


def destinationDecoding(decoder, cipherText):
    root = decoder
    decodedData = list()
    for binary in cipherText:
        if binary == "0":
            root = root.left
        if binary == "1":
            root = root.right

        if root.left is None and root.right is None:
            decodedData.append(root.alphabet)
            root = decoder

    return "".join(decodedData)


if __name__ == '__main__':
    input_text = input("Enter your word with small alphabet:\n")
    codeBook = generateHuffman(generateNodes())
    print(codeBook, len(codeBook))
    encodeText = sourceCoding(codeBook, input_text)
    print("HuffmanCode: " + encodeText)
    decoder = HuffmanDecoder(codeBook)
    decodeText = destinationDecoding(decoder, encodeText)
    print("initial input text was:" + decodeText)
