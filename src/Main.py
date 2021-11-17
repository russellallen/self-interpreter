from interpreting.Interpreter import *
from parsing.Parser import *

def main():
	isParser = False
	parser = Parser()
	interpreter = Interpreter()

	mode = input('Select mode (i)nterpret or (p)arse: ')
	if mode == "p":
		isParser = True

	while True:
		try:
			s = input('>>> ')
		except EOFError:
			break
		
		try:
			if isParser:
				print(parser.parse(s))
			else:
				print(interpreter.interpret(parser.parse(s)))
		except SelfParsingError as selfParsingError:
			print(selfParsingError)
		except SelfException as selfException:
			print(selfException)
main()