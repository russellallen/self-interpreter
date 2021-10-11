from parsing.Parser import *
from parsing.nodes.IntegerNode import *

def test_basic_binary_message_parsing():
	parser = Parser()

	binary_message = CodeNode([BinaryMessageNode(IntegerNode(1), "+", IntegerNode(1))])
	parsed_object = parser.parse("1 + 1")
	assert str(binary_message) == str(parsed_object)

def test_binary_message_parsing_with_objects():
	parser = Parser()

	reg_object = RegularObjectNode([ BinarySlotNode("+", RegularObjectNode([ArgumentSlotNode("arg")], CodeNode([IntegerNode(5)]))) ])
	binary_message = CodeNode([BinaryMessageNode(reg_object, "+", IntegerNode(1))])
	parsed_object = parser.parse("(| + = (|:arg| 5)|) + 1")
	assert str(binary_message) == str(parsed_object)

def test_binary_message_associativity():
	parser = Parser()

	binary_message1 = BinaryMessageNode(IntegerNode(1), "+", IntegerNode(2))
	binary_message = CodeNode([BinaryMessageNode(binary_message1, "+", IntegerNode(3))])
	parsed_object = parser.parse("1 + 2 + 3")

	assert str(binary_message) == str(parsed_object)

def test_binary_message_parsing_slot_names():
	parser = Parser()

	reg_object = RegularObjectNode([ BinarySlotNode("||", RegularObjectNode([], CodeNode([IntegerNode(5)]))) ])
	binary_message = CodeNode([BinaryMessageNode(reg_object, "||", IntegerNode(1))])
	parsed_object = parser.parse("(| || = (| | 5)|) || 1")

	reg_object2 = RegularObjectNode([ BinarySlotNode("@|#|!@#$%^&*+~/?>,;\\", RegularObjectNode([], CodeNode([IntegerNode(5)]))) ])
	binary_message2 = CodeNode([BinaryMessageNode(reg_object2, "@|#|!@#$%^&*+~/?>,;\\", IntegerNode(1))])
	parsed_object2 = parser.parse("(| @|#|!@#$%^&*+~/?>,;\\ = (| | 5)|) @|#|!@#$%^&*+~/?>,;\\ 1")

	reg_object3 = RegularObjectNode([ BinarySlotNode("||@|#|!@#$%^&*+~/?>,;\\", RegularObjectNode([], CodeNode([IntegerNode(5)]))) ])
	binary_message3 = CodeNode([BinaryMessageNode(reg_object3, "||@|#|!@#$%^&*+~/?>,;\\", IntegerNode(1))])
	parsed_object3 = parser.parse("(| ||@|#|!@#$%^&*+~/?>,;\\ = (| | 5)|) ||@|#|!@#$%^&*+~/?>,;\\ 1")

	reg_object4 = RegularObjectNode([ BinarySlotNode("@#!@#$%^&*+~/?>,;\\", RegularObjectNode([], CodeNode([IntegerNode(5)]))) ])
	binary_message4 = CodeNode([BinaryMessageNode(reg_object4, "@#!@#$%^&*+~/?>,;\\", IntegerNode(1))])
	parsed_object4 = parser.parse("(| @#!@#$%^&*+~/?>,;\\ = (| | 5)|) @#!@#$%^&*+~/?>,;\\ 1")

	assert str(binary_message) == str(parsed_object)
	assert str(binary_message2) == str(parsed_object2)
	assert str(binary_message3) == str(parsed_object3)
	assert str(binary_message4) == str(parsed_object4)