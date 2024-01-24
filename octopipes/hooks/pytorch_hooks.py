import gc

import torch


def free_memory(wf_iter):
    del wf_iter
    torch.cuda.empty_cache()
    gc.collect()

