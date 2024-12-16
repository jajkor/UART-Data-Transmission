class PriorityQueue:
    def __init__(self):
        self.queue = []

    def append(self, val):
        if not self.queue:
            self.queue.append(val)
            return

        l = 0
        r = len(self.queue)

        while l < r:
            mid = (l+r) // 2
            if self.queue[mid].frequency < val.frequency:
                l = mid + 1
            else:
                r=mid
        
        self.queue.insert(l, val)

    def extend(self, vals):
        for val in vals:
            self.append(val)

    def pop(self):
        return self.queue.pop(0)
    
    def getSize(self):
        return len(self.queue)
        

class Node:
    def __init__(self, left=None, right=None, value=None, frequency=None):
        self.left = left
        self.right = right
        self.value = value
        self.frequency = frequency

def merge_nodes(node1, node2):
    node3 = Node(frequency=node1.frequency + node2.frequency, left=node1, right=node2)
    return node3

def build_tree(text):
    frequencies = {}

    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1

    nodes = [Node(value=val, frequency=freq) for val,freq in frequencies.items()]

    queue = PriorityQueue()
    queue.extend(nodes)
    
    while queue.getSize() > 1:
        queue.append(merge_nodes(queue.pop(), queue.pop()))
    
    return queue.pop()

def generate_codes(node, prefix="", codes={}):
    if not (node.left and node.right):
        codes[node.value] = prefix
    
    if node.left:
        generate_codes(node.left, prefix + "0", codes)

    if node.right:
        generate_codes(node.right, prefix + "1", codes)

    return codes

def compact(binary):
    bits=10
    compacted_text = ''
    added_bits = bits - len(binary)%bits
    binary = (added_bits * '0') + binary
    
    # Compacting bits into one char
    for i in range(len(binary)//bits):
        compacted_text += chr(int(binary[i*bits:(i+1)*bits],2))
    compacted_text = str(added_bits) + compacted_text
    
    return compacted_text

def decompact(text):
    bits = 10
    added_bits = text[0]
    text = text[1:]
    decompacted_text = ''
    for char in text:
        temp = bin(ord(char))[2:]
        temp = temp.zfill(bits)
        decompacted_text += temp
        
        
    if added_bits:
        decompacted_text = decompacted_text[int(added_bits):]
    
    return decompacted_text

delimeter = '|'

def encode(text):
    global delimeter
    if not text:
        return ''
    global delimeter
    tree = build_tree(text)
    codes = generate_codes(tree)
    encoded_text = ''.join(codes[char] for char in text)
    compacted_text = compact(encoded_text)
    for code in codes:
        codes[code] = compact(codes[code])
    return compacted_text + delimeter + ''.join(f'{val}:{code};' for val,code in codes.items())

def decode(text):
    global delimeter
    encoded_text, codes = text.split(delimeter)
    encoded_text = decompact(encoded_text)
    
    codes_map = {}

    for code in codes.split(';'):
        if code:
            codes_map[decompact(code.split(':')[1])] = code.split(':')[0]

    buffer = ''
    decoded_text = ''
    
    for char in encoded_text:
        buffer += char

        if buffer in codes_map:
            decoded_text += codes_map[buffer]
            buffer = ''
    
    return decoded_text
