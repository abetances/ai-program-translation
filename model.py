# Implementation from https://github.com/dmlc/dgl/blob/master/examples/pytorch/tree_lstm/tree_lstm.py
import sys
import os
import torch as th
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#in_dim =
#h_dim =
# num_layers = 1

# tree LSTM cell for binary trees
class BinaryTreeLSTMCell(nn.Module):
    def __init__(self, in_dim, h_dim):
        super().__init__()
        self.iou_x = nn.Linear(in_dim, h_dim * 3)         # i, o, u matrices for x (cell state)
        self.iou_hl = nn.Linear(h_dim, h_dim * 3)         # i, o, u matrices for left h (hidden state)
        self.iou_hr = nn.Linear(h_dim, h_dim * 3)         # i, o, u matrices for right h (hidden state)
        self.f_x = nn.Linear(in_dim, h_dim)               # forget for x

        # forget for hidden state
        self.f_h = nn.ModuleList([[nn.Linear(h_dim, h_dim), nn.Linear(h_dim, h_dim)],
                                [nn.Linear(h_dim, h_dim), nn.Linear(h_dim, h_dim)]])

# takes in input, cell states, and hidden states
    def forward(self, x, hl, hr, cl, cr):
        # i, o, u, gates
        self.iou = self.iou_x(x) + self.iou_hl(hl) + self.iou_hr(hr)
        i, o, u = th.split(iou, iou.size(1) // 3, dim=1)      # split

        # apply activation functions
        i = F.sigmoid(i)                         
        o = F.sigmoid(o)
        u = F.tanh(u)

        # forget for left and right
        fl = F.sigmoid(self.f_x(x) + self.f_h[0][0](hr) + self.f_h[0][1](hl))
        fr = F.sigmoid(self.f_x(x) + self.f_h[1][0](hr) + self.f_h[1][1](hl))

        # calculate hidden state and cell state
        c = i * u + fl * cl + fr * cr
        h = o * F.tanh(c)

        return h, c

# encoder
class Encoder(nn.Module):
    def __init__(self, in_dim, h_dim):
        super().__init__()
        self.initial_h = 0
        self.initial_c = 0
        self.tree_cell = BinaryTreeLSTMCell(in_dim, h_dim)
        self.embed = nn.Embedding(in_dim, )

# Attention class

# decoder class
class Decoder:
    pass

# tree-to-tree class
"""
class TreeToTree(nn.Module)
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        # hey holden
#gentoo is an inferior race, i use arch btw
"""