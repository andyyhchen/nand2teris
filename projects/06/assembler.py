'''
Authour: andyisman
'''
'''

Parser(line, isFirstPass) return {'type': (A, C, Label, null), 'value': }
Assembler(file, isFirstPass)
SymbolTable(symobl, load)return (bin value)
Code(symbol) ruturn (bin vlaue)


'''

'''
(label)
@value
dest = comp; jump


'''

def init():

	#initialize symbol table
	global sdict
	for i in range(16):
		sdict['R'+str(i)] = i
	sdict['SP'], sdict['LCL'], sdict['ARG'], sdict['THIS'], sdict['THAT'] = 0, 1, 2, 3, 4
	sdict['SCREEN'], sdict['KBD'] = 16384, 24576

def Parser(line, isFirstPass):

	#clear space and comment 
	line = line.replace(' ', '')
	line = line.strip()

	if(not line):
		return {'type': "null", 'value': -1}
	comStart = line.find('//')
	if(comStart == 0):
		return {'type': "null", 'value': -1}
	if(comStart > 0):
		line = line[:comStart]
	if(line[0]=='('):
		return {'type': 'Label', 'value': line[line.find("(")+1: line.find(")")]}
	
	#only look for lable and empty line in ths first pase
	#no need to look for A or C instruction 
	if(isFirstPass==1):
		return {'type': 'Ins', 'value': -1}

	if(line[0]=='@'):
		if(line[1:].isdigit()):
			return {'type':'A', 'value': bin(int(line[1:]))[2:].zfill(16)}
		else:
			#print(line)
			return {'type':'A', 'value': SymbolTable(line[1:], load=-1)}

	else:
		cStart = line.find('=')
		jStart = line.find(';')
		if(cStart == -1): 
			dest = 'null'
			comp = line[cStart+1: jStart]
			jump = line[jStart+1:]

		elif (jStart == -1):
			dest = line[:cStart]
			comp = line[cStart+1:]
			jump = 'null'
		else:
			dest = line[:cStart]
			comp = line[cStart+1: jStart]
			jump = line[jStart+1:]

		return {'type': 'C', 'value':'111'+Code(comp, type='c')+Code(dest, type='d')+Code(jump, type='j')}

def Code(symbol, type):
	inst=''
	if(type=='c'):
		a='0'
		if('M' in symbol): 
			a='1'
			symbol = symbol.replace('M', 'A')

		cdict = {'0': '101010', '1': '111111', '-1':'111010', 'D': '001100',
				 'A': '110000', '!D': '001101', '!A':'110001', '-D': '001111',
				 '-A': '110011', 'D+1': '011111', 'A+1': '110111', 'D-1':'001110',
				 'A-1':'110010', 'D+A': '000010', 'D-A':'010011', 'A-D': '000111',
				 'D&A':'000000', 'D|A': '010101'}
		return a+cdict[symbol]
	if(type=='d'):
		ddict = {'null': '000', 'M': '001', 'D': '010', 'MD': '011',
				 'A': '100', 'AM': '101', 'AD':'110', 'AMD': '111'}
		return ddict[symbol]

	if(type=='j'):
		jdict = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
				 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP':'111'}
		return jdict[symbol]

def SymbolTable(symbol, load):
	global mCounter, sdict
	#print (sdict)
	if(symbol in sdict.keys()):
		return bin(int(sdict[symbol]))[2:].zfill(16)
	elif(load >= 0):
		sdict[symbol] = load
		return bin(int(sdict[symbol]))[2:].zfill(16)
	else: 
		sdict[symbol] = mCounter;
		mCounter += 1
		return bin(int(sdict[symbol]))[2:].zfill(16)

def Assembler(fileName, isFirstPass=1):
	#First pass => only handle (...)
	try: 
		lines = open(fileName, 'r')
	except:
		print("Failed to open the asm file")
		return

	if(isFirstPass==1):
		linCounter = 0
		for line in lines:
			#print(line)
			parse = Parser(line, isFirstPass)
			if(parse['type'] == 'null'):
				continue
			if(parse['type'] == 'Label'):
				SymbolTable(parse['value'], load=linCounter)
				#print(parse)
				#print(linCounter)
				continue
			linCounter+=1

	if(isFirstPass==0):

		try: 
			output = open(fileName[:-3]+'hack', 'w')
		except:
			print('Failed to open a hack file')
			return

		linCounter = 0

		for line in lines:
			parse = Parser(line, isFirstPass)
			if(parse['type'] == 'null'):
				continue
			if(parse['type'] == 'Label'):
				continue
			linCounter+=1
			output.write(parse['value']+'\n')
		
		output.close()
	
	lines.close()



if __name__ == "__main__":
	
	fileNames = ["./add/Add.asm", "./max/Max.asm", "./pong/Pong.asm", "./rect/Rect.asm"]
	#fileNames = ["./max/Max.asm"]
	for fileName in fileNames:
		sdict = dict()
		mCounter = 16
		init()

		#print(fileName)
		Assembler(fileName, isFirstPass=1)
		Assembler(fileName, isFirstPass=0)





