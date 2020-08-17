
'''

Parser(line) return {'type': (A, C, Label), 'value': }
Reader(file) return {'line': line}
SymbolTable(symobl)return (value)
Code(symbol) ruturn bin vlaue

'''

'''
(label)
@value
dest = comp; jump


'''
def Parser(line):

	#clear space and comment 
	line.replace(' ', '')
	comStart = line.find('//')
	if(comStart >= 0):
		line = line[:comStart]
	if(line[0]=='@'):
		if(line[1:].isdigit()):
			return {'type':'A', 'value': bin(int(line[1:]))[2:].zfill(16)}
		else
			return {'type':'A', 'value': bin(SymbolTable(line[1:]))[2:].zfill(16)}

	else
		cStart = line.find('=')
		jStart = line.find(';')
		if(cStart == -1): 
			dest = 'null'
			comp = line[cStart+1: jStart]
			jump = line[jStart+1:]

		else if(jStart == -1):
			dest = line[:cStart]
			comp = line[cStart+1: jStart]
			jump = 'null'
		else
			dest = line[:cStart]
			comp = line[cStart+1: jStart]
			jump = line[jStart+1:]

		return {'type': 'C', 'value':'111'+Code(comp, type='c')+Code(dest, type='d')+Code(jump, type='j')}

def Code(symbol, type):
	inst=''
	if(type=='c'):
		a='1'
		if('A' in symbol): 
			a='0'
			symbol.replace('M', 'A')

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



