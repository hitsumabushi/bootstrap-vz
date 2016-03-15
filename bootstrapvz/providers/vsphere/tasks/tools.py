from bootstrapvz.base import Task
from bootstrapvz.common import phases
import os


class VMwareTools(Task):
	description = 'Install VMware Tools modules'
	phase = phases.system_modification
	@classmethod
	def run(cls, info):
		raise TaskError('VMware Tools installation is not supported now.')

class OpenVmTools(Task):
	description = 'Install open-vm-tools modules'
	phase = phases.system_modification
	@classmethod
	def run(cls, info):
		info.packages.add('open-vm-tools')
