import argparse
import os
import pickle
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_file_in_cache(file_name):
    file_path = os.path.join('record', file_name)
    with open(file_path, 'rb') as f:
        obj = pickle.load(f)
    return obj

def plot(args):
    asbe = np.array(load_file_in_cache('sbe'+'_'+args.network+'_a'+str(args.attack)+'_lam'+str(args.lam)+'.pkl'))
    ace = np.array(load_file_in_cache('ce'+'_'+args.network+'_a'+str(args.attack)+'_lam'+str(args.lam)+'.pkl'))
    
    plt.style.use('seaborn')
    plt.rc('axes', labelsize=20)
    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=15)
    plt.rc('legend', fontsize=19)
    # linestyles = ('-','--','-','--')
    linestyles = ('-','--','-.','-','--','-.')
    
    lam = f'{float(f"{args.lam:.1g}"):g}'
    legend_tuple = (
        'TD'+'('+lam+')-mean',
        'TD'+'('+lam+')-trim', 
        'TD'+'('+lam+')-mean-attack',
        'TD'+'('+lam+')-trim-attack',
        'TD'+'('+lam+')-local'
    )
    # MSBE
    fig = plt.figure(figsize=(5.9,5.3))
    plt.ylabel('MSBE')
    plt.xlabel('Step')
    for i in range(np.shape(asbe)[-1]):
        y = asbe[:,:,i]
        y_mean = np.mean(y, 0)
        x = np.arange(len(y_mean))
        plt.plot(x, y_mean, linestyles[i], linewidth=2.25)
    plt.subplots_adjust(left=0.15, right=0.98, top = 0.95, bottom=0.12)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
    plt.legend(legend_tuple)
    fig.savefig('sbe'+'_'+args.network+'_a'+str(args.attack)+'_lam'+str(args.lam)+'.pdf', dpi=fig.dpi)
    
    # MCE
    fig = plt.figure(figsize=(5.9,5.3))
    plt.ylabel('MCE')
    try:
        if args.lnk:
            plt.ylabel(r'MCE$\times k/\ln(k)$')
    except:
        pass
    plt.xlabel('Step')
    for i in range(np.shape(ace)[-1]):
        y = ace[:,:,i] 
        y_mean = np.mean(y, 0)
        if args.lnk:
            for j in np.arange(1,len(y_mean)):
                y_mean[j] = y_mean[j]*(j+1)/np.log(j+1)
        x = np.arange(len(y_mean))
        plt.plot(x, y_mean, linestyles[i], linewidth=2.25)
    plt.subplots_adjust(left=0.15, right=0.98, top=0.95, bottom=0.12)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
    plt.legend(legend_tuple)
    fig.savefig('ce'+'_'+args.network+'_a'+str(args.attack)+'_lam'+str(args.lam)+'.pdf', dpi=fig.dpi)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plotter for robust TD')
    
    parser.add_argument('--network', type=str, default='complete',
    help='name of the network (h1b1, h3b1, b3b2, renyi, complete)')
    parser.add_argument('--attack', type=int, default=2,
    help='Type of attack')
    parser.add_argument('--lam', type=float, default=0.,
    help='Lambda')
    parser.add_argument('--lnk', action='store_true',
    help='whether to divide aggregate ce by ln(epoch) or epoch')
    args = parser.parse_args()
    
    plot(args)