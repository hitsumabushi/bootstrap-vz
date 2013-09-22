from manifest import Manifest
from tasks import packages
from common.tasks import volume as volume_tasks
from common.tasks import loopback
from common.tasks import partitioning
from common.tasks import filesystem
from common.tasks import bootstrap
from tasks import boot
from common.tasks import boot as common_boot
from common.tasks import security
from common.tasks import network
from common.tasks import initd
from common.tasks import cleanup
from common.tasks import workspace


def initialize():
	pass


def tasks(tasklist, manifest):
	from common.task_sets import base_set
	from common.task_sets import volume_set
	from common.task_sets import mounting_set
	from common.task_sets import apt_set
	from common.task_sets import locale_set
	tasklist.add(*base_set)
	tasklist.add(*volume_set)
	tasklist.add(*mounting_set)
	tasklist.add(*apt_set)
	tasklist.add(*locale_set)

	if manifest.volume['partitions']['type'] != 'none':
		from common.task_sets import partitioning_set
		tasklist.add(*partitioning_set)

	tasklist.add(packages.HostPackages,
	             packages.ImagePackages,

	             loopback.Create,
	             filesystem.Format,

	             bootstrap.Bootstrap,
	             boot.ConfigureGrub,
	             filesystem.FStab,
	             common_boot.BlackListModules,
	             common_boot.DisableGetTTYs,
	             security.EnableShadowConfig,
	             network.RemoveDNSInfo,
	             network.ConfigureNetworkIF,
	             network.RemoveHostname,
	             initd.ResolveInitScripts,
	             initd.InstallInitScripts,
	             cleanup.ClearMOTD,
	             cleanup.CleanTMP,

	             loopback.MoveImage,
	             workspace.DeleteWorkspace)

	if manifest.bootstrapper.get('tarball', False):
		tasklist.add(bootstrap.MakeTarball)

	from common.task_sets import fs_specific_set
	for partition in manifest.volume['partitions']:
		if 'filesystem' in partition:
			fs_tasks = fs_specific_set.get(partition['filesystem'], [])
			tasklist.add(fs_tasks)

	if 'boot' in manifest.volume['partitions']:
		from common.task_sets import boot_partition_set
		tasklist.add(*boot_partition_set)


def rollback_tasks(tasklist, tasks_completed, manifest):
	completed = [type(task) for task in tasks_completed]

	def counter_task(task, counter):
		if task in completed and counter not in completed:
			tasklist.add(counter)

	counter_task(loopback.Create, volume_tasks.Delete)
	counter_task(filesystem.CreateMountDir, filesystem.DeleteMountDir)
	counter_task(partitioning.MapPartitions, partitioning.UnmapPartitions)
	counter_task(filesystem.MountRoot, filesystem.UnmountRoot)
	counter_task(filesystem.MountBoot, filesystem.UnmountBoot)
	counter_task(filesystem.MountSpecials, filesystem.UnmountSpecials)
	counter_task(volume_tasks.Attach, volume_tasks.Detach)
	counter_task(workspace.CreateWorkspace, workspace.DeleteWorkspace)
