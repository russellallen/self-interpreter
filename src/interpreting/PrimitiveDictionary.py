from interpreting.objects.SelfException import *
from Messages import *

def handleIntAdd(receiver, parameter_argument_list):
	from interpreting.objects.SelfInteger import SelfInteger
	argument = parameter_argument_list[0].get_value(receiver)
	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format("_IntAdd:", receiver, argument))

	return SelfInteger(receiver.get_value() + argument.get_value())

primitive_dict = {
	'_IntAdd:' : handleIntAdd
}