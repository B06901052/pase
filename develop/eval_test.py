from pase.models.frontend import wf_builder
pase = wf_builder('../cfg/frontend/PASE+.cfg').eval().cuda()
pase.load_pretrained('../model/FE_e199.ckpt', load_last=True, verbose=True)

# Now we can forward waveforms as Torch tensors
import torch
x = torch.randn(1, 1, 100000, device='cuda') # example with random noise to check shape
# y size will be (1, 256, 625), which are 625 frames of 256 dims each
y = pase(x)
print(x[:,:,:100])
print(y.shape)
print(y[:,:10,:10])
