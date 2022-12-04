import sys
import os
import hashlib
import pickle


import tkinter as tk


class Main:
    bufferSize = 1024*16
    def __init__(self, target, mode, resFile):
        self.targetFolder = target
        self.mode = mode
        self.resFile = resFile
        if(self.resFile=="D"):
            self.resFile="data.dat"
        self.currentStructure = dict()
    def runThrough(self):
        #navigating through folders
        for folders in os.walk(self.targetFolder):
            #iterating through files in current folder
            for file in folders[2]:
                self.hashFile(os.path.join(folders[0], file))
        self.endProgram()
    def hashFile(self, file):
        with open(os.path.join(file), 'rb') as source:
            hash = hashlib.blake2b()
            block = source.read(self.bufferSize)
            while block:
                hash.update(block)
                block = source.read(self.bufferSize)
            hash.digest()
            res = hash.hexdigest()
            self.currentStructure[file] = res
            print(f"HASH file {file}, hash: {res}")
    def endProgram(self):
        if(self.mode=='S'):
            with open(self.resFile, 'wb') as f:
                pickle.dump(self.currentStructure, f)
        if(self.mode == 'C'):
            with open(self.resFile, 'rb') as f:
                self.prevDict = pickle.load(f)
            resultText=''
            for el in self.currentStructure:
                if(not self.prevDict.get(el)):
                    resultText+=f"File {el} added\n"
                elif(self.prevDict.get(el)!=self.currentStructure.get(el)):
                    resultText+=f"File {el} changed\n"
            for el in self.prevDict:
                if(not self.currentStructure.get(el)):
                    resultText+=f"File {el} removed\n"
            if(resultText!=''):                
                self.alert(resultText)
    def alert(self, text):
        root = tk.Tk()
        w = tk.Label(root, text=text)
        w.pack()
        
        button = tk.Button(root, text='OK', width=25, command=root.destroy)
        button.pack()
        def updateStructure():
            with open(self.resFile, 'wb') as f:
                pickle.dump(self.currentStructure, f)
                root.destroy()

        button = tk.Button(root, text='APPLY CHANGES', width=25, command=updateStructure)
        button.pack()
        
        
        root.mainloop()
        
if __name__ == '__main__':
    if(len(sys.argv)!=4 or sys.argv[2] not in ['S', 'C']):
        print("Incorrect args")
        print("Run like:python3 main.py <root folder> <program mode 'S'-scan(first run) 'C'-compare> <data file path, 'D'-default(data.dat)>")
        print("Example:python3 main.py myData S D")
        print("Example:python3 main.py myEncryptedData C data.txt")
        sys.exit()
    main = Main(sys.argv[1], sys.argv[2], sys.argv[3])
    main.runThrough()