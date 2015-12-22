import ply.lex as lex
import ply.yacc as yacc
import re
err=''
syn_error=False
class Preprocessor:

	class __Lexer:
		
		tokens =['id', ]
		literals = ['=', '+', '-', '/', '*',  '%', '(', ')', '^']
		t_id=r'[a-zA-Z_][a-zA-Z0-9_]*'
		t_ignore=' \t'
		
		def t_newline(self, t):
		    r'\n+'
		    t.lexer.lineno += t.value.count("\n")
		    
		def t_error(self, t):
		    global err,syn_error
		    syn_error=True
		    err=''
		    err=err+"Warning: ignored faulty token at line {}".format(t.lineno)
		    print("Warning: ignored faulty token at line {}".format(t.lineno))
		    t.lexer.skip(1)

		def __init__(self, **kwargs):
			
			self.lexer=lex.lex(module=self, **kwargs)

		def test(self, string):
			self.lexer.input(string)
			for i in lexer: print(i.type, i.value)

	
	precedence = ( ('left', '+', '-'), ('left', '/', '*', '%'), ('right', '^'), ('right', 'umin'))
	ins=[]
	ctr=1

	def p_assignment(self, p):
		'''statement : id '=' expression'''
		Preprocessor.ins.append(p[1]+" = "+p[3])

	def p_expression(self, p):
		'''expression : expression '+' term 
					| expression '-' term 
					| term '''

		if len(p)>2: 
			temp="_temp"+str(Preprocessor.ctr)
			Preprocessor.ins.append(temp+" = 0")
			Preprocessor.ins.append(temp+" = "+p[1]+" "+p[2]+" "+p[3])
			p[0]=temp
			Preprocessor.ctr+=1


		else: p[0]=p[1]

	def p_term(self, p):
		'''term : term '*' exponentiation
				| term '/' exponentiation
				| term '%' exponentiation
				| exponentiation '''

		if len(p)>2: 	
			temp="_temp"+str(Preprocessor.ctr)
			Preprocessor.ins.append(temp+" = 0")
			Preprocessor.ins.append(temp+" = "+p[1]+" "+p[2]+" "+p[3])
			p[0]=temp
			Preprocessor.ctr+=1

		else: p[0]=p[1]

	def p_exponentiation(self, p):
		''' exponentiation : factor '^' exponentiation 
						   | factor '''
		if len(p)>2: 	
			temp="_temp"+str(Preprocessor.ctr)
			Preprocessor.ins.append(temp+" = 0")
			Preprocessor.ins.append(temp+" = "+p[1]+" "+p[2]+" "+p[3])
			p[0]=temp
			Preprocessor.ctr+=1		

		else: p[0] = p[1]	 

	def p_factor(self, p):
		''' factor : '(' expression ')'
				   | '-' expression %prec umin
				   | id '''

		if p[1]=='(':
			p[0]=p[2]

		elif p[1]=='-':
			temp="_temp"+str(Preprocessor.ctr)
			Preprocessor.ins.append(temp+" = 0")
			Preprocessor.ins.append("zero = 0")
			Preprocessor.ins.append(temp+" = zero "+p[1]+" "+p[2])
			p[0]=temp
			Preprocessor.ctr+=1		

		else: p[0]=p[1]

	def p_error(self, p):
		global err,syn_error
		syn_error=True
		err=''
		try:
			err=err+"Error at line no" +str(p.lineno)
			print("Error at line no", p.lineno)
		except: 
			err=err+"Error during preprocessing."
			print("Error during preprocessing.")

		

	def __init__(self):
		self.tokens=Preprocessor.__Lexer.tokens
		self.parser=yacc.yacc(module=self)

	def parse(self, string):
		lexer=Preprocessor.__Lexer()
		self.parser.parse(string, lexer=lexer.lexer)
		self.parser.restart()
		temp=Preprocessor.ins
		Preprocessor.ins=[]
		return temp

def preprocessor(string):
	global err,syn_error
	mult_macro_code="""one = 1
zero = 0
_t_scl = 0
{0} = zero
for ( _t_scl = {2} ; _t_scl >= one ; _t_scl = _t_scl - one )
[
	{0} = {0} + {1}
]
"""

	div_macro_code="""one = 1
zero = 0
_t_dvsr = 0
_t_qnt = 0	
_t_dvnd = 0
_t_dvsr = {2}
_t_qnt = zero

if ( _t_dvsr != zero )
[
	for ( _t_dvnd = {1} ; _t_dvnd >= _t_dvsr  ; _t_dvnd = _t_dvnd - _t_dvsr)
	[
		_t_qnt = _t_qnt + one
	]

	{0} = _t_qnt
]
else
[
	end
]"""

	mod_macro_code="""one = 1
zero = 0
_t_dvsr = 0
_t_qnt = 0	
_t_dvnd = 0
_t_dvsr = {2}
_t_qnt = zero
for ( _t_dvnd = {1} ; _t_dvnd >= _t_dvsr  ; _t_dvnd = _t_dvnd - _t_dvsr)
[
	_t_qnt = _t_qnt + one
]

{0} = _t_dvnd"""

# r = x ^ y

	exp_macro_code="""one = 1
zero = 0
_t_scl = 0
_t_sbscl = 0
_dst = 0
_t_dst = 0
_dst = one
if( {1} != zero )
[
	for ( _t_scl = {2} ; _t_scl >= one ; _t_scl = _t_scl - one )
	[
		_t_dst = _dst
		for ( _t_sbscl = {1} - one ; _t_sbscl >= one ; _t_sbscl = _t_sbscl - one )
		[
			_dst = _dst + _t_dst
		]
	]
]
else
[
	_dst = zero 
]
{0} = _dst"""

	s=re.sub(pattern=r'(/\*.*?\*/)|(#.*?\n)', repl='', string=string, flags=re.M | re.S)

	parser=Preprocessor()

	ins=[]
	for i in s.split("\n"):

		if re.search("[/*%^-]", i)!=None:
			if re.search("for\s\(", i)!=None:
				syn_error=True
				err=''
				err=err+"Error - cannot parse such operations in the loop header."
				print("Error - cannot parse such operations in the loop header.")
				
				break
			else:
				syn_error=False
				ins = ins + parser.parse(i)

		else: 
				ins = ins + [i]


	s=ins[:]
	ins=[]
	
	for i in s:
		if i=='': continue
		if re.search("\*", i)!=None:
			dst, src1, src2=re.split("[=*]", i)
			t=mult_macro_code.format(dst.strip(), src1.strip(), src2.strip())
			t=re.sub(r"\[", "{", t, re.M)
			t=re.sub(r"\]", "}", t, re.M)
			ins=ins + t.split("\n")

		elif re.search(r"/", i)!=None:
			dst, src1, src2=re.split("[=/]", i)
			t=div_macro_code.format(dst.strip(), src1.strip(), src2.strip())
			t=re.sub(r"\[", "{", t, re.M)
			t=re.sub(r"\]", "}", t, re.M)
			ins=ins + t.split("\n")

		elif re.search(r"%", i)!=None:
			dst, src1, src2=re.split("[=%]", i)
			t=mod_macro_code.format(dst.strip(), src1.strip(), src2.strip())
			t=re.sub(r"\[", "{", t, re.M)
			t=re.sub(r"\]", "}", t, re.M)
			ins=ins + t.split("\n")

		elif re.search(r"\^", i)!=None:
			dst, src1, src2=re.split("[=^]", i)
			t=exp_macro_code.format(dst.strip(), src1.strip(), src2.strip())
			t=re.sub(r"\[", "{", t, re.M)
			t=re.sub(r"\]", "}", t, re.M)
			ins=ins + t.split("\n")

		else:
			ins = ins + [i] 

	parser=None

	if 'end' not in ins[-1]: ins=ins+['end']

	return "\n".join(ins)


if __name__=="__main__":

	print(preprocessor("""x = 2
y = 3
z = 4
result = 0				
one = 1
i = 0
bounds = 10

for ( ; i <= bounds ; i = i + one )
{
	result =  - ( x + - z )
}
end""")) 				# test input


