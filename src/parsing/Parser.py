from parsing.nodes.IntegerNode import *
from parsing.nodes.StringNode import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.ParentSlotNode import *
from parsing.nodes.BinarySlotNode import *
from parsing.nodes.KeywordSlotNode import *
from parsing.nodes.KeywordMessageNode import *
from parsing.nodes.UnaryMessageNode import *
from parsing.nodes.BinaryMessageNode import *
from parsing.nodes.ArgumentSlotNode import *
from parsing.nodes.CodeNode import *
from parsing.ParsingUtils import *
from parsing.SelfParsingError import *
import ply.lex as lex
import ply.yacc as yacc

class Parser:
	def __init__(self):
		self.lexer = lex.lex(module = self)
		self.parser = yacc.yacc(module = self)

	# Ignored characters

	t_ignore = " \t\n"

	# Tokens

	tokens = ('INTEGER','LPAREN','RPAREN','PIPE','PERIOD','LARROW','EQUAL',
			'IDENTIFIER', 'PARENT_NAME', 'SMALL_KEYWORD', 'CAP_KEYWORD', 'OPERATOR',
			'COLON', 'STRING', 'CARET')

	t_LPAREN = r'\('
	t_RPAREN = r'\)'
	t_PIPE = r'\|'
	t_PERIOD = r'\.'
	t_LARROW = r'<-'
	t_EQUAL = r'='
	t_IDENTIFIER = r'[a-z_][a-zA-Z0-9_]*'
	t_PARENT_NAME = t_IDENTIFIER + r'\*'
	t_SMALL_KEYWORD = r'[a-z_][a-zA-Z0-9_]*:'
	t_CAP_KEYWORD = r'[A-Z][a-zA-Z0-9_]*:'
	t_COLON = r':'
	t_CARET = r'\^'
	operators = r"!@#$%&*+~\/?>,;\\"
	t_OPERATOR = r'[\|\^' + operators + r']{2,}|[' + operators + r']'
	t_STRING = r'\'([^\\\']|\\[tbnfrva0\\\'"?]|\\x[0-9a-fA-F]{2}|\\d[0-9]{3}|\\o[0-7]{3})*\''

	def t_INTEGER(self, t):
		r'-?\d+'
		t.value = int(t.value)
		return t

	def t_error(self, t):
		raise SelfParsingError(f'at token: \'{t.value[0]}\'')

	# Precedence Rules

	precedence = (
		('right', 'LOWER'),
		('right', 'HIGHER'),
		('right', 'SMALL_KEYWORD', 'CAP_KEYWORD'),
		('left', 'OPERATOR'),
		('nonassoc', 'IDENTIFIER')
	)

	# Productions		
	def p_code(self, p):
		'''code : expression PERIOD code
				| expression PERIOD
				| expression'''
		if(len(p) == 4):
			p[3].expressions.insert(0, p[1])
			p[0] = p[3]
		else:
			p[0] = CodeNode([p[1]])

	def p_code_with_return(self, p):
		'''code : CARET expression PERIOD
				| CARET expression'''
		p[0] = CodeNode([p[2]])

	def p_expression(self, p):
		'''expression : constant
					  | unary-message
					  | LPAREN expression RPAREN
					  | binary-message
					  | keyword-message'''
		if (len(p) == 2):
			p[0] = p[1]
		else:
			p[0] = p[2]

	def p_unary_message(self, p):
		'''unary-message : expression IDENTIFIER
						 | IDENTIFIER'''
		if(len(p) == 3):
			p[0] = UnaryMessageNode(p[1], p[2])
		else:
			p[0] = UnaryMessageNode(None, p[1])
			
	def p_constant_regular_object(self, p):
		'constant : regular-object'
		p[0] = p[1]

	def p_constant_integer(self, p):
		'constant : INTEGER'
		p[0] = IntegerNode(p[1])

	def p_constant_string(self, p):
		'constant : STRING'
		s = p[1][1:-1]
		s = convert_d_and_o_escapes_to_x(s)
		s = remove_backslash_from_backslash_question_mark(s)
		p[0] = StringNode(raw_string_to_normal_string(s))

	def p_binary_message(self, p):
		'''binary-message : expression OPERATOR expression
						  | OPERATOR expression'''
		if (len(p) == 4):
			p[0] = BinaryMessageNode(p[1], p[2], p[3])
		else:
			p[0] = BinaryMessageNode(None, p[1], p[2])

	def p_keyword_message(self, p):
		'''keyword-message : expression SMALL_KEYWORD expression cap-keyword-expression-list
						   | SMALL_KEYWORD expression cap-keyword-expression-list'''
		if(len(p) == 5):
			p[4][0].insert(0, p[2])
			p[4][1].insert(0, p[3])
			p[0] = KeywordMessageNode(p[1], p[4][0], p[4][1])
		else:
			p[3][0].insert(0, p[1])
			p[3][1].insert(0, p[2])
			p[0] = KeywordMessageNode(None, p[3][0], p[3][1])

	def p_cap_keyword_expression_list(self, p):
		'''cap-keyword-expression-list : CAP_KEYWORD expression cap-keyword-expression-list %prec LOWER
				       				   | %prec HIGHER'''
		if(len(p) == 4):
			keyword_list = p[3][0]
			value_list = p[3][1]
			keyword_list.insert(0, p[1])
			value_list.insert(0, p[2])
			p[0] = [keyword_list, value_list]
		else:
			p[0] = [[],[]]

	def p_regular_object_empty(self, p):
		'regular-object : LPAREN RPAREN'
		p[0] = RegularObjectNode()

	def p_regular_object_slotted(self, p):
		'''regular-object : LPAREN PIPE slot-list PIPE RPAREN
						  | LPAREN PIPE slot-list PIPE code RPAREN'''
		if(len(p) == 6):
			p[0] = RegularObjectNode(p[3])
		else:
			p[0] = RegularObjectNode(p[3], p[5])

	def p_slot_list(self, p):
		'''slot-list : slot PERIOD slot-list
					 | slot
					 | '''
		if(len(p) == 4):
			new_slot_list = p[3]
			new_slot_list.insert(0, p[1])
			p[0] = new_slot_list
		elif(len(p) == 2):
			p[0] = [p[1]]
		else:
			p[0] = []

	def p_slot(self, p):
		'''slot : data-slot
				| binary-slot
				| keyword-slot
				| argument-slot'''
		p[0] = p[1]

	def p_data_slot(self, p):
		'''data-slot : slot-name
					 | slot-name LARROW expression
					 | slot-name EQUAL expression'''
		if p[1][-1] == "*":
			if(len(p) == 4):
				p[0] = ParentSlotNode(p[1][:-1], p[2], p[3])
			else:
				p[0] = ParentSlotNode(p[1][:-1])
		else:
			if(len(p) == 4):
				p[0] = DataSlotNode(p[1], p[2], p[3])
			else:
				p[0] = DataSlotNode(p[1])

	def p_binary_slot(self, p):
		'''binary-slot : OPERATOR EQUAL regular-object
					   | OPERATOR IDENTIFIER EQUAL regular-object'''
		if(len(p) == 4):
			p[0] = BinarySlotNode(p[1], p[3])
		else:
			p[0] = BinarySlotNode(p[1], p[4], p[2])

	def p_keyword_slot(self, p):
		'''keyword-slot : SMALL_KEYWORD cap-keyword-list EQUAL regular-object
						| SMALL_KEYWORD IDENTIFIER cap-keyword-id-list EQUAL regular-object'''
		if(len(p) == 5):
			p[2].insert(0, p[1])
			p[0] = KeywordSlotNode(p[2], p[4])
		else:
			p[3][0].insert(0, p[1])
			p[3][1].insert(0, p[2])
			p[0] = KeywordSlotNode(p[3][0], p[5], p[3][1])

	def p_cap_keyword_list(self, p):
		'''cap-keyword-list : CAP_KEYWORD cap-keyword-list
							| '''
		if(len(p) == 3):
			keyword_list = p[2]
			keyword_list.insert(0, p[1])
			p[0] = keyword_list
		else:
			p[0] = []

	def p_cap_keyword_id_list(self, p):
		'''cap-keyword-id-list : CAP_KEYWORD IDENTIFIER cap-keyword-id-list
								| '''
		if(len(p) == 4):
			keyword_list = p[3][0]
			arg_list = p[3][1]
			keyword_list.insert(0, p[1])
			arg_list.insert(0, p[2])
			p[0] = [keyword_list, arg_list]
		else:
			p[0] = [[],[]]
			
	def p_argument_slot(self, p):
		'argument-slot : COLON IDENTIFIER'
		p[0] = ArgumentSlotNode(p[2])

	def p_slot_name(self, p):
		'''slot-name : IDENTIFIER
					 | PARENT_NAME
					 '''
		p[0] = p[1]

	def p_error(self, p):
		raise SelfParsingError(f'at token: \'{p.value if p else None}\'')

	def parse(self, string):
		return self.parser.parse(string)