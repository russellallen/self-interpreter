from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.IntegerNode import *
from parsing.nodes.UnaryMessageNode import *
from interpreting.Interpreter import *


def test_simply_unary_method_call():
	# (|x = (| | 1)|) x
	interpreter = Interpreter()

	parser_result = UnaryMessageNode(RegularObjectNode([DataSlotNode("x","=",RegularObjectNode([], IntegerNode(1)))]), "x")
	expected_result = SelfInteger(1)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_method_code_is_not_run_until_called():
	# (|x = (| | () bogus)|)
	interpreter = Interpreter()

	parser_result = RegularObjectNode([DataSlotNode("x","=",RegularObjectNode([], UnaryMessageNode(RegularObjectNode(), "bogus")))])
	slot_list = {}
	self_object_inner = SelfObject({}, UnaryMessageNode(RegularObjectNode(), "bogus"))
	slot_list["x"] = SelfSlot("x", self_object_inner, isImmutable=True)
	expected_result = SelfObject(slot_list)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_method_code_with_bad_unary_message():
	# (|x = (| | () bogus)|) x
	interpreter = Interpreter()

	parser_result_object = RegularObjectNode([DataSlotNode("x","=",RegularObjectNode([], UnaryMessageNode(RegularObjectNode(), "bogus")))])
	parser_result = UnaryMessageNode(parser_result_object, "x")
	expected_result = SelfException("Lookup error")

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)