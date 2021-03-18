import re
import os

#Initialize trie node class
class TrieNode:
    def __init__(self, char: str):
        self.char = char                                        #Text property
        self.children = dict()                                  #Children nodes property
        self.path = {}
        self.words_in_path = 0
        self.counter = 0                                        #Counts node passing
        self.isWord = False                                     #Flag for word finish
        self.word_cnt = 0                                       #Word reference counter
        self.probability = lambda num, tot: num/tot*100         #lambda function for probability value

    def getChars(self):                                         #Method for getting node's text
        return self.char

    def getCounter(self):                                       #Method for getting node's counter
        return self.counter

    def getPath(self):
        return self.path

#Initialize prefixed tree class 
class PrefixTree:
    def __init__(self):
        self.root = TrieNode("/")                               #Root node constructor 
        self.for_sort = []
        self.word_dict = dict()

    def insert(self, word, path): 
        current = self.root                                     #Start function from root node
        for i, char in enumerate(word.lower()):                 #Check each letter of given word
            if char not in current.children:
                prefix = word[0:i+1]                            #Word from first letter to current 
                new_node = TrieNode(prefix)                     #Create new TrieNode for each new letter
                current.children[char] = new_node

            #current.counter += 1                               #increase times passed
            current = current.children[char]
        if(current.isWord and path not in current.path):
            current.words_in_path = 1
            current.path.update({path : current.words_in_path})
            current.word_cnt += 1
            return
        elif(current.isWord and path in current.path):
            current.words_in_path += 1
            current.path.update({path : current.words_in_path})
            current.word_cnt += 1
            return

        current.isWord = True                                   #End of word, true flag to distinct valid word
        #current.path = path
        current.words_in_path += 1                              #Words in path ++
        current.path = {path : current.words_in_path}
        
        current.word_cnt += 1                                   #Word reference counter ++

    #Display function 
    def display(self):
        current = self.root 
        word_dict = self.word_dict
        
        self._display(current)

        for key, value in word_dict.items(): 
            word_dict.setdefault(key, []).append(current.probability(value[0], len(word_dict.keys())))

        for key, value in sorted(word_dict.items()): 
            print(key + " -> ", end=""),
            print(str(value[0]) +" times ", end=""),
            print("probability: %.2f" % value[1] + "%")
        # print("Total words found: " + str(len(self.word_dict.keys())))               
        
    #helper function for display (recursive nodes pass)
    def _display(self, current):
        if(current.isWord):
            self.word_dict.update({current.getChars().lower() : [current.word_cnt]})
            #print(current.path.items())
            for char in current.children:
                self._display(current.children[char])

        else:
            for char in current.children:
                self._display(current.children[char])


    def findWord(self, word):
        current = self.root
        for char in word:
            if char not in current.children:                
                return None
            current = current.children[char]
        if current.isWord: return current


def searchTxts():
    ########################################################################
    #            Change the path after '+' to your project path            #
    ########################################################################
    #path = os.path.expanduser('~') + '/Downloads/'
    path = './test/'

    _txt_files = []
    _txt_path = []

    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            _txt_files = (re.findall(".*.txt$", name))
            for t in _txt_files: 
                _txt_path.append(os.path.join(root, name))
                print(t + " -> " + os.path.join(root, name))            #print path of existing txt files.
    return _txt_path

def CommonString():
        txt_paths = []
        words_list = []                                                 #Initialize word list
        delimiters = [r'\s', ', ', ',', '[.]']                          #Choose specific delimiters
        root = PrefixTree()

        try:
            print("Searching project path for txt files...\n")
            txt_paths = searchTxts()
        except:
            print("Operation failed")
        
        for path in txt_paths:
            f = open(path, encoding='windows-1252')                                              #Open sample file

            for line in f.readlines():
                words = re.split('|'.join(delimiters), line)            #Split words per line using re python library

                for word in words:
                    if(word != ''): 
                        words_list.append(word)                         #Append splitted words to list
                        root.insert(word, path)

        root.display()
        #print(words_list)
        print("Total number of words: " + str(len(words_list)))
        f.close()
        return root

def SearchMachine():    
    root = CommonString()
    # string_list = []
    # path_list = []
    found_nodes = []
    string = [word for word in input("Insert string for search: ").split()]
    print(string)
    for word in string:
        fw = root.findWord(word)
        if(fw != None):
            found_nodes.append(fw)
        else:
            print(word + " is not exist in files.")

    for node in found_nodes:
        sorted_dict = {key : val for key, val in sorted(node.path.items(), key = lambda ele: ele[1], reverse = True)}
        #max_path_val = max(node.path, key=node.path.get)
        for keys, values in sorted_dict.items():
            print(node.getChars()+" found "+str(values)+" times in "+keys)
        

def default():
    print("Not valid option. Exiting..")

def optionSwitch():
    print("1. Find the most common used Strings")
    print("2. Mini searching machine")
    option = int(input("Choose Option(1,2): "))

    dict = {
        1 : CommonString,
        2 : SearchMachine
    }

    dict.get(option, default)()

if __name__ == "__main__":
    print("#################################")
    print("          Program Start          ")
    print("#################################")

    optionSwitch()

    
