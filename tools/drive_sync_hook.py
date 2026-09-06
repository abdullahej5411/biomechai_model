from mmaction.registry import HOOKS
from mmengine.hooks import Hook

@HOOKS.register_module()
class DriveCheckpointSyncHook(Hook):
    def __init__(self, *args, **kwargs):
        super().__init__()
