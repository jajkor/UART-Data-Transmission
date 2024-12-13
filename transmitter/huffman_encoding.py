class PriorityQueue:
    def __init__(self):
        self.queue = []

    def append(self, val):
        if self.queue == []:
            self.queue.append(val)
            return

        l = 0
        r = len(self.queue)

        while l < r:
            mid = int((l+r) / 2)
            if self.queue[mid].frequency < val.frequency:
                l = mid + 1
            elif self.queue[mid].frequency > val.frequency:
                r = mid - 1
            else:
                self.queue.insert(mid, val)
                return
        
        self.queue.insert(l, val)

    def extend(self, vals):
        for val in vals:
            self.append(val)

    def pop(self):
        return self.queue.pop()
    
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

delimeter = '|'

def encode(text):
    if not text:
        return ''
    global delimeter
    tree = build_tree(text)
    codes = generate_codes(tree)
    encoded_text = ''.join(codes[char] for char in text)

    delimeter = '|'

    return encoded_text + delimeter + ''.join(f'{val}:{code};' for val,code in codes.items())

def decode(text):
    global delimeter
    encoded_text, codes = text.split(delimeter)

    codes_map = {}

    for code in codes.split(';'):
        if code:
            codes_map[code.split(':')[1]] = code.split(':')[0]

    buffer = ''
    decoded_text = ''
    
    for char in encoded_text:
        buffer += char

        if buffer in codes_map:
            decoded_text += codes_map[buffer]
            buffer = ''

    return decoded_text
