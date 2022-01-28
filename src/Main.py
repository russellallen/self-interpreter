from os import system
from interpreting.Interpreter import *
from interpreting.printingutils.SelfObjectPrinter import SelfObjectPrinter
from parsing.Parser import *
from sys import platform
if platform == "linux":
	import readline

def main():
	isParser = False
	parser = Parser()
	interpreter = Interpreter()
	printer = SelfObjectPrinter()
	system("")

	mode = input('Select mode (i)nterpret or (p)arse: ')
	if mode == "p":
		isParser = True
	else:
		interpreter.initializeBootstrap()

	while True:
		try:
			s = input('>>> ')
		except EOFError:
			break

		if s.strip() == "":
			continue

		try:
			if isParser:
				print(parser.parse(s))
			else:
				print(printer.get_object_string(interpreter.interpret(parser.parse(s))))
		except SelfParsingError as selfParsingError:
			print(selfParsingError)
		except SelfException as selfException:
			print(selfException)

main()