import argparse
from utils import init_dir, set_seed, get_num_rel
from meta_trainer import MetaTrainer
import os
from subgraph import gen_subgraph_datasets
from pre_process import data2pkl


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_name', default='mht')

    parser.add_argument('--name', default='fb237_v1_transe', type=str)

    parser.add_argument('--step', default='meta_train', type=str, choices=['meta_train', 'fine_tune'])
    parser.add_argument('--metatrain_state', default='./state/2_m_distmult/2_m_distmult.best', type=str)

    parser.add_argument('--state_dir', '-state_dir', default='./state', type=str)
    parser.add_argument('--log_dir', '-log_dir', default='./log', type=str)
    parser.add_argument('--tb_log_dir', '-tb_log_dir', default='./tb_log', type=str)

    # params for subgraph
    parser.add_argument('--num_train_subgraph', default=10000)#10000->1000,1
    parser.add_argument('--num_valid_subgraph', default=300)#200->2000,1
    parser.add_argument('--num_sample_for_estimate_size', default=50)#50->25
    parser.add_argument('--rw_0', default=10, type=int)
    parser.add_argument('--rw_1', default=10, type=int)
    parser.add_argument('--rw_2', default=5, type=int)
    parser.add_argument('--num_sample_cand', default=5, type=int)

    # params for meta-train
    parser.add_argument('--metatrain_num_neg', default=8)
    parser.add_argument('--metatrain_num_epoch', default=10)#5->10
    parser.add_argument('--metatrain_bs', default=4, type=int)#16->8->4
    parser.add_argument('--metatrain_lr', default=0.01, type=float)
    parser.add_argument('--metatrain_check_per_step', default=10, type=int)#10->5
    parser.add_argument('--indtest_eval_bs', default=16, type=int)#128->64

    # params for fine-tune
    parser.add_argument('--posttrain_num_neg', default=64, type=int)
    parser.add_argument('--posttrain_bs', default=512, type=int)
    parser.add_argument('--posttrain_lr', default=0.001, type=int)
    parser.add_argument('--posttrain_num_epoch', default=10, type=int)
    parser.add_argument('--posttrain_check_per_epoch', default=1, type=int)

    # params for KGE
    parser.add_argument('--kge', default='TransE', type=str, choices=['TransE', 'DistMult', 'ComplEx','RotatE', 'ConvE'])
    parser.add_argument('--gamma', default=10, type=float)
    parser.add_argument('--adv_temp', default=1, type=float)

    parser.add_argument('--gpu', default='cuda:0', type=str)
    parser.add_argument('--seed', default=1234, type=int)
    
    #params for ConvE
    parser.add_argument('--emb_dim', default=200, type=int)
    parser.add_argument('--num_ent', default=7305, type=int)
    parser.add_argument('--num_rel', default=263, type=int)#area1's params 
    parser.add_argument('--hid_size', default=9278, type=int)
    parser.add_argument('--inp_drop', default=0.2, type=float)
    parser.add_argument('--hid_drop', default=0.3, type=float)
    parser.add_argument('--fet_drop', default=0.2, type=float)
    parser.add_argument('--emb_shape',default=20, type=int)

    args = parser.parse_args()
    init_dir(args)

    args.ent_dim = args.emb_dim
    args.rel_dim = args.emb_dim
    if args.kge in ['ComplEx', 'RotatE']:
        args.ent_dim = args.emb_dim * 2
    if args.kge in ['ComplEx']:
        args.rel_dim = args.emb_dim * 2

    # specify the paths for original data and subgraph db
    args.data_path = f'./data/{args.data_name}.pkl'
    args.db_path = f'./data/{args.data_name}_subgraph'

    # load original data and make index
    if not os.path.exists(args.data_path):
        data2pkl(args.data_name)

    if not os.path.exists(args.db_path):
        gen_subgraph_datasets(args)

    args.num_rel = get_num_rel(args)

    set_seed(args.seed)

    # if args.step == 'meta_train':
    meta_trainer = MetaTrainer(args)
    meta_trainer.train()



