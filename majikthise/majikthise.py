import re

# https://wbec-ridderkerk.nl/html/UCIProtocol.html

def main():
    print("We're in\n")

    f = open('/Users/kalebburnham/Workspaces/Majikthise-Python/majikthise/log.txt', 'a+')
    f.write("We're in!\n")
    f.close()

    while True:
        instruction = "" 
        
        try:
            instruction = input()
        except:
            print("EOF")

        if instruction:
            # This is just creating a ton of new lines. Only write if instruction exists.
            f = open('/Users/kalebburnham/Workspaces/Majikthise-Python/majikthise/log.txt', 'a')
            f.write(instruction + '\n')
            f.close()

        if instruction == 'uci':
            writeId()
        elif re.search('debug (on|off)', instruction):
            pass
        elif instruction == 'isready':
            writeReadyOk()
        elif instruction == 'register':
            writeRegisterResponse()
        elif re.search('setoption name .*', instruction):
            pass
        elif instruction == 'register':
            pass
        elif instruction == 'ucinewgame':
            pass
        elif re.search('position .*', instruction):
            if re.search('position startpos moves *', instruction):
                pass
            elif re.search('position fen moves'):
                pass
            else:
                print("Uknown command")
        elif instruction == 'go':
            pass
        elif instruction == 'stop':
            pass
        elif instruction == 'ponderhit':
            pass
        elif instruction == 'quit':
            pass
        else:
            pass

def writeId():
    print('id name majikthise')
    print('id author Kaleb Burnham')

def writeUciok():
    print('uciok')

def writeReadyOk():
    print('readyok')

def writeRegisterResponse():
    print('later')

def writeBestMove():
    pass

def writeInfo():
    pass

def writeOption():
    pass

if __name__ == "__main__":
    main()