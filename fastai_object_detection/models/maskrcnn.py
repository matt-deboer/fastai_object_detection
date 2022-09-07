# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/04b_models.maskrcnn.ipynb (unless otherwise specified).

__all__ = ['get_maskrcnn_model', 'maskrcnn_resnet18', 'maskrcnn_resnet34', 'maskrcnn_resnet50', 'maskrcnn_resnet101',
           'maskrcnn_resnet152']

# Cell

from torchvision.models.detection.backbone_utils import resnet_fpn_backbone
from torch.hub import load_state_dict_from_url
from torchvision.models.detection.anchor_utils import AnchorGenerator
from torchvision.models.detection import MaskRCNN
from torchvision.ops.misc import FrozenBatchNorm2d
from functools import partial
from fastai.vision.all import delegates
import importlib
# Cell
#hide


_model_urls = {
    'maskrcnn_resnet50_fpn_coco':
        'https://download.pytorch.org/models/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth',
}

# Cell

@delegates(MaskRCNN)
def get_maskrcnn_model(arch_str, num_classes, pretrained=False, pretrained_backbone=True,
                 trainable_layers=5, **kwargs):

    #if pretrained: pretrained_backbone = False
    backbone_weights = None
    if pretrained_backbone:
        import importlib
        resnet_sz = arch_str.replace('resnet', '')
        weights_module = importlib.import_module(f"torchvision.models.resnet.ResNet{resnet_sz}_Weights", fromlist=[''])
        backbone_weights=weights_module.DEFAULT
    backbone = resnet_fpn_backbone(arch_str, weights=backbone_weights, trainable_layers=trainable_layers)
    model = MaskRCNN(backbone,
                     num_classes,
                     image_mean = [0.0, 0.0, 0.0], # already normalized by fastai
                     image_std = [1.0, 1.0, 1.0],
                     **kwargs)

    if pretrained:
        try:

            pretrained_dict = load_state_dict_from_url(_model_urls['maskrcnn_'+arch_str+'_fpn_coco'],
                                                       progress=True)
            model_dict = model.state_dict()

            pretrained_dict = {k: v for k, v in pretrained_dict.items() if
                       (k in model_dict) and (model_dict[k].shape == pretrained_dict[k].shape)}

            model_dict.update(pretrained_dict)
            model.load_state_dict(model_dict)

            for module in model.modules():
                if isinstance(module, FrozenBatchNorm2d):
                    module.eps = 0.0

        except Exception as e:
            #print(e)
            print("No pretrained coco model found for maskrcnn_"+arch_str)
            print("This does not affect the backbone.")

    return model

# Cell
#hide

maskrcnn_resnet18 = partial(get_maskrcnn_model, arch_str="resnet18")
maskrcnn_resnet34 = partial(get_maskrcnn_model, arch_str="resnet34")
maskrcnn_resnet50 = partial(get_maskrcnn_model, arch_str="resnet50")
maskrcnn_resnet101 = partial(get_maskrcnn_model, arch_str="resnet101")
maskrcnn_resnet152 = partial(get_maskrcnn_model, arch_str="resnet152")