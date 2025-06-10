import pickle
import pandas as pd

def reidx(tri):
    tri_reidx = []
    ent_reidx = dict()
    entidx = 0
    rel_reidx = dict()
    relidx = 0
    for h, r, t in tri:
        if h not in ent_reidx.keys():
            ent_reidx[h] = entidx
            entidx += 1
        if t not in ent_reidx.keys():
            ent_reidx[t] = entidx
            entidx += 1
        if r not in rel_reidx.keys():
            rel_reidx[r] = relidx
            relidx += 1
        tri_reidx.append([ent_reidx[h], rel_reidx[r], ent_reidx[t]])
    return tri_reidx, dict(rel_reidx), dict(ent_reidx)


def reidx_withr(tri, rel_reidx):
    tri_reidx = []
    ent_reidx = dict()
    entidx = 0
    for h, r, t in tri:
        if h not in ent_reidx.keys():
            ent_reidx[h] = entidx
            entidx += 1
        if t not in ent_reidx.keys():
            ent_reidx[t] = entidx
            entidx += 1
        tri_reidx.append([ent_reidx[h], rel_reidx[r], ent_reidx[t]])
    return tri_reidx, dict(ent_reidx)


def reidx_withr_ande(tri, rel_reidx, ent_reidx):
    tri_reidx = []
    for h, r, t in tri:
        tri_reidx.append([ent_reidx[h], rel_reidx[r], ent_reidx[t]])
    return tri_reidx


def data2pkl(data_name):

    train_tri = []
    file = open('data/{}/train.txt'.format(data_name), "r", encoding='utf-8')
    train_tri.extend([l.strip().split('\t') for l in file.readlines()])
    file.close()

    valid_tri = []
    file = open('data/{}/valid.txt'.format(data_name), "r", encoding='utf-8')
    valid_tri.extend([l.strip().split('\t') for l in file.readlines()])
    file.close()

    test_tri = []
    file = open('data/{}/test.txt'.format(data_name), "r", encoding='utf-8')
    test_tri.extend([l.strip().split('\t') for l in file.readlines()])
    file.close()

    sum_tri = train_tri + valid_tri + test_tri

    train_tri, fix_rel_reidx, ent_reidx = reidx(sum_tri)
    valid_tri = reidx_withr_ande(valid_tri, fix_rel_reidx, ent_reidx)
    test_tri = reidx_withr_ande(test_tri, fix_rel_reidx, ent_reidx)

    # file = open('data/{}_ind/train.txt'.format(data_name), "r", encoding='utf-8')
    # ind_train_tri = ([l.strip().split('\t') for l in file.readlines()])
    # file.close()

    # file = open('data/{}_ind/valid.txt'.format(data_name), "r", encoding='utf-8')
    # ind_valid_tri = ([l.strip().split('\t') for l in file.readlines()])
    # file.close()

    # file = open('data/{}_ind/test.txt'.format(data_name), "r", encoding='utf-8')
    # ind_test_tri = ([l.strip().split('\t') for l in file.readlines()])
    # file.close()

    # sum_ind_trt = ind_test_tri + ind_train_tri + ind_valid_tri

    # test_train_tri, ent_reidx_ind = reidx_withr(sum_ind_trt, fix_rel_reidx)
    # test_valid_tri = reidx_withr_ande(ind_valid_tri, fix_rel_reidx, ent_reidx_ind)
    # test_test_tri = reidx_withr_ande(ind_test_tri, fix_rel_reidx, ent_reidx_ind)

    save_data = {'train_graph': {'train': train_tri, 'valid': valid_tri, 'test': test_tri}}
                #  'ind_test_graph': {'train': test_train_tri, 'valid': test_valid_tri, 'test': test_test_tri}}#delete ind_subgraph

    pickle.dump(save_data, open(f'data/{data_name}.pkl', 'wb'))