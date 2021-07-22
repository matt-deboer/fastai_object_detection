# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_core.ipynb (unless otherwise specified).

__all__ = ['BinaryMasksBlock', 'show_binmask', 'TensorBinMasks', 'TensorBinMasks2TensorMask', 'ObjDetLearner',
           'InstSegLearner']

# Cell

from fastai.vision.all import *

# Cell

def BinaryMasksBlock():
    "A `TransformBlock` for binary masks"
    return TransformBlock(type_tfms=lambda x: tuple(apply(PILMask.create,x)), batch_tfms=IntToFloatTensor)

# Cell

@delegates(plt.Axes.imshow, keep=True, but=['shape', 'imlim'])
def show_binmask(im, ax=None, figsize=None, title=None, ctx=None, **kwargs):
    "Function to show binary masks with matplotlib"
    if hasattrs(im, ('data','cpu','permute')):
        im = im.data.cpu()
    if not isinstance(im,np.ndarray): im=array(im)
    ax = ifnone(ax,ctx)
    if figsize is None: figsize = (_fig_bounds(im.shape[0]), _fig_bounds(im.shape[1]))
    if ax is None: _,ax = plt.subplots(figsize=figsize)
    for m in im:
        c = (np.random.random(3) * 0.6 + 0.4)
        #draw_mask(ax, m, c)
        color_mask = np.ones((*m.shape, 3)) * c
        ax.imshow(np.dstack((color_mask, m * 0.5)))
        ax.contour(m, colors=[color_mask[0, 0, :]], alpha=0.4)
    if title is not None: ax.set_title(title)
    ax.axis('off')
    return ax

def _fig_bounds(x):
    r = x//32
    return min(5, max(1,r))

# Cell

class TensorBinMasks(TensorImageBase):
    "Tensor class for binary mask representation"
    def show(self, ctx=None, **kwargs):
        return show_binmask(self,ctx=ctx, **{**self._show_args, **kwargs})

# Cell

class TensorBinMasks2TensorMask(Transform):
    "Class to transform binary masks to fastai's `TensorMask` class to make fastai's transforms available"
    def encodes(self, x:TensorBinMasks):
        return TensorMask(x)
    def decodes(self, x:TensorMask):
        return TensorBinMasks(x)

# Cell

class ObjDetLearner(Learner): pass

# Cell

class InstSegLearner(Learner): pass