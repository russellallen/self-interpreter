from interpreting.objects.traits.SelfSmallInt import SelfSmallInt
from Messages import Messages
from interpreting.objects.SelfObject import SelfObject
import warnings

class SelfReal(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.value = value
		if (type(value) is not float):
			warnings.warn(Messages.NUMBER_NOT_VERIFIED.value.format('float', self.value))
			self.value = float(value)

	def __str__(self):
		return f"SelfReal: (value='{self.value}')"

	def __hash__(self):
		return hash(self.value)

	def get_value(self):
		return self.value

	def as_dict(self, visited):
		dict = super().as_dict(visited)
		dict['annotation'] = self.value
		dict['alt_string'] = True
		return dict