#from bootstrapvz.base import Task
#from bootstrapvz.common import phases
#import os
#
#class ConvertStreamOptimized(Task):
#    @classmethod
#    def run(cls, info):
#        convert_command_path = info.manifest.provider['vmdk_convert']
#        if not convert_command_path:
#            msg = 'Specify vmdk-convert command.'
#            raise TaskError(msg)
#        log.call([os.path.abspath(convert_command_path), ]
#        pass
#
