import ply.lex as lex
import ply.yacc as yacc
import re
import preprocessor

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class Stack:
	def __init__(self):
		self.stack=[]
		self.top=-1

	def __str__(self):
		return str(self.stack)

	def push(self, value):
		self.top+=1
		self.stack.append(value)

	def pop(self):
		if self.top!=-1:
			temp=self.stack[-1]
			self.stack=self.stack[:len(self.stack)-1]
			self.top-=1
			return temp

	def length(self):
		return (self.top+1)

# ----------------------------------------------------------------
# ----------------------------------------------------------------

class MU0Parser:

	class __Lexer:

		tokens =('id','num', 'do', 'while', 'break', 'continue', 'if', 'else', 'end', 'cond', 'for')

		literals = ['=', '+', '-', '(', ')', '{', '}', ';', ',']

		# Tokens

		def t_if(self, t):
			r'\bif\b'
			return t

		def t_else(self, t):
			r'\belse\b'
			return t

		def t_end(self, t):
			r'\bend\b|\bEND\b'
			return t 

		def t_do(self, t):
			r'\bdo\b'
			return t

		def t_while(self, t):
			r'\bwhile\b'
			return t

		def t_for(self, t):
		    r'\bfor\b'
		    return t

		def t_break(self, t):
			r'\bbreak\b'
			return t

		def t_continue(self, t):
			r'\bcontinue\b'
			return t

		def t_num(self, t):
		    r'\d+'
		    t.value = int(t.value)
		    return t

		t_id=r'[a-zA-Z_][a-zA-Z0-9_]*'

		t_cond=r'<=|<|>=|>|==|!='

		#t_ignore_comments=r'\#.*'

		#t_ignore_multiline_comments=r'(/\*(.|\n)*?\*/)|(//.*)'

		t_ignore=' \t'

		def t_newline(self, t):
		    r'\n+'
		    t.lexer.lineno += t.value.count("\n")
		    
		def t_error(self, t):
		    print("Warning: ignored faulty token at line {}".format(t.lineno))
		    t.lexer.skip(1)

		def __init__(self, **kwargs):
			self.lexer=lex.lex(module=self, **kwargs)

		def test(self, string):
			self.lexer.input(string)
			for i in lexer: print(i.type, i.value)

	# ----------------------------------------------------------------

	# Parsing rules
	precedence = (
	    ('left', '+', '-'),
	    )

	# data list
	data=set()
	ins=[]
	names=[]
	update=0

	line_no=0

	s=Stack()
	brstack=Stack()
	contstack=Stack()
	forstack=Stack()

	# ----------------------------------------------------------------

	def p_master(self, p):
		'''statements : loop statements
					  | condition statements 
					  | statement statements 
					  | '''

	# ----------------------------------------------------------------

	def p_for_loop(self, p):
		''' loop : for '(' initial ';' forcondition ';' updstart update ')' nextpart '''

		try:
			temp=MU0Parser.forstack.pop()
			MU0Parser.ins=MU0Parser.ins+temp
			MU0Parser.line_no+=len(temp)
			temp=MU0Parser.s.pop()
		except:
			self.p_error(self, p)

		MU0Parser.ins.append("jmp "+str(temp - 3))
		MU0Parser.line_no+=1

		while MU0Parser.contstack.top!=-1:
			target=MU0Parser.contstack.pop()
			jump_dist=MU0Parser.line_no-target+1
			#print(MU0Parser.ins[len(MU0Parser.ins)-jump_dist])
			MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(temp-3), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])

		while MU0Parser.brstack.top!=-1:
			target=MU0Parser.brstack.pop()
			jump_dist=MU0Parser.line_no-target+1
			MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(MU0Parser.line_no+1), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])

		jump_dist=MU0Parser.line_no-temp+1
		MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(MU0Parser.line_no+1), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])


	def p_for_initial(self, p):
		''' initial : istatement moreinit '''

	def p_for_more_initial(self, p):
		''' moreinit : ',' istatement  moreinit 
				 | '''

	def p_for_no_initial(self, p):
		''' initial : '''

	def p_istatement_assign(self, p):
	    '''istatement : id '=' iexpression 
	                '''

	    if p[1] not in MU0Parser.names: 
	    	self.syntax_error(p, p[1])
		    	
	    MU0Parser.ins.append('sto ' + p[1])
	    MU0Parser.line_no+=1

	def p_iexpression_binop(self, p):
	    '''iexpression : iexpression '+' id
	                  | iexpression '-' id'''

	    if p[3] not in MU0Parser.names: 
	    	self.syntax_error(p, p[3])

	    if p[2] == '+':
	    	MU0Parser.ins.append('add ' + p[3])
	    elif p[2] == '-': 
	    	MU0Parser.ins.append('sub ' + p[3])

	    MU0Parser.line_no+=1

	def p_iexpression_name(self, p):
	    '''iexpression : id'''

	    if p[1] not in MU0Parser.names: 
	    	self.syntax_error(p, p[1])

	    MU0Parser.ins.append("lda " + p[1])
	    MU0Parser.line_no+=1

	def p_for_condition(self, p):
		'''forcondition : id cond id'''

		if p[1] not in MU0Parser.names: self.syntax_error(p, p[1])
		if p[3] not in MU0Parser.names: self.syntax_error(p, p[3])

		if p[2]=='>=' or p[2]=='==':
			MU0Parser.ins.append("lda " + p[1])
			MU0Parser.ins.append("sub " + p[3])
			MU0Parser.ins.append("jge {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")

		elif p[2]=='>' or p[2]=='<' or p[2]=='!=':
			MU0Parser.ins.append("lda " + p[1])
			MU0Parser.ins.append("sub " + p[3])
			MU0Parser.ins.append("jne {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")

		elif p[2]=='<=':
			MU0Parser.ins.append("lda " + p[3])
			MU0Parser.ins.append("sub " + p[1])
			MU0Parser.ins.append("jge {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")

		MU0Parser.line_no+=4
		MU0Parser.s.push(MU0Parser.line_no)

	def p_update_start(self, p):
		''' updstart : '''
		MU0Parser.forstack.push([])

	def p_for_update(self, p):
		''' update : ustatement moreupd '''

	def p_for_more_update(self, p):
		''' moreupd : ',' ustatement  moreupd 
				 | '''

	def p_for_no_update(self, p):
		''' update : '''

	def p_ustatement_assign(self, p):
	    '''ustatement : id '=' uexpression '''

	    if p[1] not in MU0Parser.names: 
	    	self.syntax_error(p, p[1])
		    	
	    MU0Parser.forstack.stack[MU0Parser.forstack.top].append('sto ' + p[1])

	def p_uexpression_binop(self, p):
	    '''uexpression : uexpression '+' id
	                  | uexpression '-' id'''

	    if p[3] not in MU0Parser.names: 
	    	self.syntax_error(p, p[3])

	    if p[2] == '+':
	    	MU0Parser.forstack.stack[MU0Parser.forstack.top].append('add ' + p[3])

	    elif p[2] == '-': 
	    	MU0Parser.forstack.stack[MU0Parser.forstack.top].append('sub ' + p[3])

	def p_uexpression_name(self, p):
	    '''uexpression : id'''

	    if p[1] not in MU0Parser.names: 
	    	self.syntax_error(p, p[1])

	    MU0Parser.forstack.stack[MU0Parser.forstack.top].append("lda " + p[1])
	 
	def p_for_body(self, p):
		''' nextpart : '{' statements '}' '''

	# ----------------------------------------------------------------

	def p_while_loop(self, p):
		''' loop : while '(' whilecondition ')' '{' statements '}' '''
		

		temp=MU0Parser.s.pop()
		MU0Parser.ins.append("jmp "+str(temp - 3))
		MU0Parser.line_no+=1

		while MU0Parser.contstack.top!=-1:
			target=MU0Parser.contstack.pop()
			jump_dist=MU0Parser.line_no-target+1
			#print(MU0Parser.ins[len(MU0Parser.ins)-jump_dist])
			MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(temp-3), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])

		while MU0Parser.brstack.top!=-1:
			target=MU0Parser.brstack.pop()
			jump_dist=MU0Parser.line_no-target+1
			MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(MU0Parser.line_no+1), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])


		jump_dist=MU0Parser.line_no-temp+1
		MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(MU0Parser.line_no+1), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])


	def p_while_condition(self, p):	 	# only >=, <= and != are supported properly
		'''whilecondition : id cond id'''

		if p[1] not in MU0Parser.names: self.syntax_error(p, p[1])
		if p[3] not in MU0Parser.names: self.syntax_error(p, p[3])

		if p[2]=='>=' or p[2]=='==':
			MU0Parser.ins.append("lda " + p[1])
			MU0Parser.ins.append("sub " + p[3])
			MU0Parser.ins.append("jge {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")

		elif p[2]=='>' or p[2]=='<' or p[2]=='!=':
			MU0Parser.ins.append("lda " + p[1])
			MU0Parser.ins.append("sub " + p[3])
			MU0Parser.ins.append("jne {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")

		elif p[2]=='<=':
			MU0Parser.ins.append("lda " + p[3])
			MU0Parser.ins.append("sub " + p[1])
			MU0Parser.ins.append("jge {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")
		MU0Parser.line_no+=4
		MU0Parser.s.push(MU0Parser.line_no)

	# ----------------------------------------------------------------

	def p_do_while_loop(self, p):
		''' loop : header statements '}' while '(' dowhilecondition ')' '''

	def p_do_while_loop_cont(self, p):
		''' header :  do '{' '''
		#MU0Parser.ins.append("DO")
		MU0Parser.s.push(MU0Parser.line_no)

	def p_do_while_condition(self, p): 	 # only >=, <= and != are supported properly
		'''dowhilecondition : id cond id'''

		temp=MU0Parser.s.pop()
		if p[1] not in MU0Parser.names: self.syntax_error(p, p[1])
		if p[3] not in MU0Parser.names: self.syntax_error(p, p[3])

		if p[2]=='>=' or p[2]=='==':
			MU0Parser.ins.append("lda " + p[1])
			MU0Parser.ins.append("sub " + p[3])
			MU0Parser.ins.append("jge {}".format(temp+1))
		elif p[2]=='>' or p[2]=='<' or p[2]=='!=':
			MU0Parser.ins.append("lda " + p[1])
			MU0Parser.ins.append("sub " + p[3])
			MU0Parser.ins.append("jne {}".format(temp+1))

		elif p[2]=='<=':
			MU0Parser.ins.append("lda " + p[3])
			MU0Parser.ins.append("sub " + p[1])
			MU0Parser.ins.append("jge {}".format(temp+1))
		
		#MU0Parser.ins.append("END DO")

		MU0Parser.line_no+=3

		while MU0Parser.contstack.top!=-1:
			target=MU0Parser.contstack.pop()
			jump_dist=MU0Parser.line_no-target+1
			#print(MU0Parser.ins[len(MU0Parser.ins)-jump_dist])
			MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(temp+1), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])

		while MU0Parser.brstack.top!=-1:
			target=MU0Parser.brstack.pop()
			jump_dist=MU0Parser.line_no-target+1
			#print(MU0Parser.ins[len(MU0Parser.ins)-jump_dist])
			MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(MU0Parser.line_no+1), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])

	# ----------------------------------------------------------------

	def p_if_only(self, p):
		''' condition : ifpart '''

		temp=MU0Parser.s.pop()
		jump_dist=MU0Parser.line_no-temp+1
		MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(MU0Parser.line_no+1), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])

	def p_if_else(self, p):
		''' condition : ifpart else '{' statements '}' '''

		temp=MU0Parser.s.pop()
		jump_dist=MU0Parser.line_no-temp+1
		MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(MU0Parser.line_no+1), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])

	def p_ifpart(self, p):
		''' ifpart : if '(' ifcondition ')' '{' statements '}' '''

		temp=MU0Parser.s.pop()
		jump_dist=MU0Parser.line_no-temp+1
		MU0Parser.ins[len(MU0Parser.ins)-jump_dist]=re.sub(r'-1', str(MU0Parser.line_no+2), MU0Parser.ins[len(MU0Parser.ins)-jump_dist])
		MU0Parser.ins.append("jmp -1")
		MU0Parser.line_no+=1
		MU0Parser.s.push(MU0Parser.line_no)
		
	def p_ifcondition(self, p): 		# only >=, <= and != are supported properly
		'''ifcondition : id cond id'''
		if p[1] not in MU0Parser.names: self.syntax_error(p, p[1])
		if p[3] not in MU0Parser.names: self.syntax_error(p, p[3])

		if p[2]=='>=' or p[2]=='==':
			MU0Parser.ins.append("lda " + p[1])
			MU0Parser.ins.append("sub " + p[3])
			MU0Parser.ins.append("jge {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")

		elif p[2]=='>' or p[2]=='<' or p[2]=='!=':
			MU0Parser.ins.append("lda " + p[1])
			MU0Parser.ins.append("sub " + p[3])
			MU0Parser.ins.append("jne {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")

		elif p[2]=='<=':
			MU0Parser.ins.append("lda " + p[3])
			MU0Parser.ins.append("sub " + p[1])
			MU0Parser.ins.append("jge {}".format(MU0Parser.line_no+5))
			MU0Parser.ins.append("jmp -1")
		MU0Parser.line_no+=4

		MU0Parser.s.push(MU0Parser.line_no)

	# ----------------------------------------------------------------

	def p_statement_break(self, p):
		''' statement : break '''
	
		MU0Parser.ins.append("jmp -1")
		MU0Parser.line_no+=1
		MU0Parser.brstack.push(MU0Parser.line_no)

	def p_statement_continue(self, p):
		''' statement : continue '''

		MU0Parser.ins.append("jmp -1")
		MU0Parser.line_no+=1
		MU0Parser.contstack.push(MU0Parser.line_no)

	# ----------------------------------------------------------------

	def p_statement_assign(self, p):
	    '''statement : id '=' expression 
	                | id '=' num '''

	    if type(p[3])==type(0):

	    	MU0Parser.data.add(p[1]+' '+str(p[3]))
	    	MU0Parser.names.append(p[1])
	    else: 
	    	if p[1] not in MU0Parser.names: 
	    		self.syntax_error(p, p[1])
		    	
	    	MU0Parser.ins.append('sto ' + p[1])
	    	MU0Parser.line_no+=1

	def p_expression_binop(self, p):
	    '''expression : expression '+' id
	                  | expression '-' id'''

	    if p[3] not in MU0Parser.names: 
	    	self.syntax_error(p, p[3])

	    if p[2] == '+':
	    	MU0Parser.ins.append('add ' + p[3])

	    elif p[2] == '-': 
	    	MU0Parser.ins.append('sub ' + p[3])
	    MU0Parser.line_no+=1 

	def p_expression_name(self, p):
	    '''expression : id'''
	    if p[1] not in MU0Parser.names: 
	    	self.syntax_error(p, p[1])

	    MU0Parser.ins.append("lda " + p[1])
	    MU0Parser.line_no+=1 

	# ----------------------------------------------------------------

	def p_statement_end(self, p):
	    '''statement : end'''

	    MU0Parser.ins.append("stp")
	    MU0Parser.line_no+=1 

	# ----------------------------------------------------------------

	def p_error(self, p):
		global syn_error,err
		syn_error=True
		err=""
		try:
			print("Syntax error detected at line {} - faulty token '{}'.".format(p.lineno, p.value))
			err=err+"Syntax error detected at line {} - faulty token '{}'.".format(p.lineno, p.value)
			syn_error=True
		except:
			err=err+"Syntax error detected."
			print("Syntax error detected.")

		#exit()

	def syntax_error(self, p, name):
		global syn_error,err
		err=""
		try:
			syn_error=True
			if name!=None: 
				print("Syntax error detected - '{}' used but not declared.".format(name))
				err=err+"Syntax error detected - '{}' used but not declared.".format(name)
			else: 
				err=err+"Syntax error detected."
				print("Syntax error detected.")
		except: 
			syn_error=True
			err="Syntax error detected."
			print("Syntax error detected.")

		#exit()

	# ----------------------------------------------------------------

	def __init__(self):
		self.tokens=MU0Parser.__Lexer.tokens
		self.parser=yacc.yacc(module=self)

	def restart(self):
		MU0Parser.data=set()
		MU0Parser.ins=[]
		MU0Parser.names=[]
		MU0Parser.update=0

		MU0Parser.line_no=0

		MU0Parser.s=Stack()
		MU0Parser.brstack=Stack()
		MU0Parser.contstack=Stack()
		MU0Parser.forstack=Stack()

		self.parser.restart()

	def parse(self, string):
		global err,syn_error
		string2 = preprocessor.preprocessor(string)
		if (string != string2):
			print("Program code after preprocessing: ", string2)
			string=string2
		from preprocessor import err as err
		from preprocessor import syn_error as syn_error
		#print(string)
		lexer=MU0Parser.__Lexer()
		self.parser.parse(string, lexer=lexer.lexer)
		#print(syn_error,err)
		if MU0Parser.s.length()==0 and MU0Parser.brstack.length()==0 and MU0Parser.contstack.length()==0 and MU0Parser.forstack.length()==0 and syn_error==False:
			err=''
			err=err+"No syntax errors detected."
			print("No syntax errors detected.")

		else:
			if MU0Parser.s.length()==0:
				print("Syntax error detected - continue/break used outside loop")
			else: 
				print("Syntax error detected.")

		ins=MU0Parser.ins
		data=MU0Parser.data
		self.restart()

		return ins + list(data)

# ----------------------------------------------------------------
# ----------------------------------------------------------------

cmd1="""a = 121  # program to check whether a is a palindrome or not
d = 0
zero = 0
temp = 0
temp = a
ten = 10
n = 0

while ( temp != zero )
{
	d = temp % ten
	temp  = temp / ten
	n = ( ten * n ) + d
}

result = 0			# result = 1 means a is a palindrome, result = 0 means a is not a palindrome
if ( n != a )
{
	result = zero
}

else 
{
	result = one
}

end
"""

cmd2="""
a = 371		# armstrong number program
d = 0
zero = 0
temp = 0
temp = a
zero = 0
ten = 10
sum = 0
while ( temp != zero )
{
	d = temp % ten
	temp = temp / ten
	sum = sum + ( d * d * d )
}

result = 0
if ( sum != a )
{

}
else 
{
	result = one
}
"""


#print(cmd6)

#exit()

def main(s):
	f=open('test.txt','w')
	parser =  MU0Parser()
	for i in parser.parse(s):
		f.write(i+"\n")
		print(i)
	f.close()







