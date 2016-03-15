from bootstrapvz.common import task_groups
import tasks.packages
from bootstrapvz.common.tasks import image
from bootstrapvz.common.tasks import loopback
from bootstrapvz.common.tasks import initd
from bootstrapvz.common.tasks import ssh


def validate_manifest(data, validator, error):
	import os.path
	schema_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'manifest-schema.yml'))
	validator(data, schema_path)


def resolve_tasks(taskset, manifest):
	taskset.update(task_groups.get_standard_groups(manifest))

	taskset.update([tasks.packages.DefaultPackages,
					loopback.AddRequiredCommands,
					loopback.Create,
					initd.InstallInitScripts,
					ssh.AddOpenSSHPackage,
					ssh.ShredHostkeys,
					ssh.AddSSHKeyGeneration,
					image.MoveImage,
					])

	tools_type = manifest.provider.get('vmware_tools', "")
	if not tools_type:
		msg = 'Specify VMware Tools or open-vm-tools.'
		raise TaskError(msg)
	if tools_type == "open-vm-tools":
		taskset.update([tools.OpenVmTools])
	if tools_type == "vmware-tools":
		taskset.update([tools.VMwareTools])

	#taskset.update([vmdk.ConvertStreamOptimized])


def resolve_rollback_tasks(taskset, manifest, completed, counter_task):
	taskset.update(task_groups.get_standard_rollback_tasks(completed))
