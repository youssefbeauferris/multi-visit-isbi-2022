#!/usr/bin/env python
# coding: utf-8

# # Compute and Compare the Three Quantitative Assessment Metrics Using Bar Graphs

# In[55]:


import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import wilcoxon


# In[20]:



# ## Load the previously calculated metrics with dimensions = (3,7,3) -- ([ssim,psnr,vif], [nvolumes], [5,10,15x])

# In[2]:


previous_metrics = []
for R in ['5x', '5x', '5x']: #all previous metrics are the same so no need to recalculate for each acceleration factor
    with open(f'../data/metrics/metrics_previous_{R}.pkl','rb') as fp:
        metrics_previous = pickle.load(fp)
    previous_metrics.append(metrics_previous)

enhanced_metrics = []
for R in ['5x','10x','15x']:
    with open(f'../data/metrics/metrics_enhanced_{R}.pkl','rb') as fp:
        metrics_enhanced = pickle.load(fp)
    enhanced_metrics.append(metrics_enhanced)

non_enhanced_metrics = []
for R in ['5x','10x','15x']:
    with open(f'../data/metrics/metrics_non_enhanced_{R}.pkl','rb') as fp:
        metrics_non_enhanced = pickle.load(fp)
    non_enhanced_metrics.append(metrics_non_enhanced)


# ## Calculate the mean for each metrics and acceleration factors for all samples excluding first & last 20 slices

# crop each volume by the first and last 20 slices where little anatomical structures are present

# In[3]:


cropped_enhanced_metrics = []
cropped_non_enhanced_metrics = []
cropped_previous_metrics = []
for R in range(3):
    cropped_enhanced_metrics.append([])
    cropped_non_enhanced_metrics.append([])
    cropped_previous_metrics.append([])
    for n in range(7):
        cropped_enhanced_metrics[R].append([])
        cropped_non_enhanced_metrics[R].append([])
        cropped_previous_metrics[R].append([])
        for m in range(3):
            cropped_previous_metrics[R][n].append(previous_metrics[0][n][m][20:-20])
            cropped_enhanced_metrics[R][n].append(enhanced_metrics[R][n][m][20:-20])
            cropped_non_enhanced_metrics[R][n].append(non_enhanced_metrics[R][n][m][20:-20])


# In[4]:


# calculate the non-enhanced & enhanced metrics with croppign
cropped_non_enhanced = []
cropped_enhanced = []
for i in range(3):
    cropped_non_enhanced.append(np.mean(np.concatenate(cropped_non_enhanced_metrics[i],axis=1),axis=1))
    cropped_enhanced.append(np.mean(np.concatenate(cropped_enhanced_metrics[i],axis=1),axis=1))


# In[5]:


# calculate the non-enhanced & enhanced metrics without cropping
non_enhanced = []
enhanced = []
for i in range(3):
    non_enhanced.append(np.mean(np.concatenate(non_enhanced_metrics[i],axis=1),axis=1))
    enhanced.append(np.mean(np.concatenate(enhanced_metrics[i],axis=1),axis=1))


# In[6]:


#metrics for previous scan at R=5x
previous = np.mean(np.concatenate(cropped_previous_metrics[0],axis=1),axis=1)


# ## Calculate the standard deviation for the error bars

# In[13]:


# calculate the std for the non-enhanced & enhanced metrics with croppign
cropped_non_enhanced_std = []
cropped_enhanced_std = []
for i in range(3):
    cropped_non_enhanced_std.append(np.std(np.concatenate(cropped_non_enhanced_metrics[i],axis=1),axis=1))
    cropped_enhanced_std.append(np.std(np.concatenate(cropped_enhanced_metrics[i],axis=1),axis=1))


# In[14]:


#metrics for previous scan at R=5x
previous_std = np.std(np.concatenate(cropped_previous_metrics[0],axis=1),axis=1)

# ## use wilcoxon t-test to compare the means of the enhnaced vs. non-enhanced metrics

# In[102]:


x = np.concatenate(cropped_enhanced_metrics[0], axis=1)
y = np.concatenate(cropped_non_enhanced_metrics[0], axis=1)

print(wilcoxon(x[0],y[0]))
print(wilcoxon(x[1],y[1]))
print(wilcoxon(x[2],y[2]))


# In[ ]:





# ## Plot the bar graphs for each quality assessment metric

# In[48]:


colors = sns.color_palette("cubehelix",3,as_cmap=False)


# In[100]:


metrics = ['SSIM','pSNR','VIF']
height = [[1.05,0.05], [50,2.5], [1.05,0.05]]

for ii in range(3):
    data1 = np.array(cropped_non_enhanced)[:,ii]#[non_enhanced_5x[0],non_enhanced_10x[0],non_enhanced_15x[0]]
    data2 = np.array(cropped_enhanced)[:,ii]#[enhanced_5x[0],enhanced_10x[0],enhanced_15x[0]]
    data3 = [previous[ii]]#[previous[0]]
    width = 0.3
    yerr1 = np.array(cropped_non_enhanced_std)[:,ii]
    yerr2 = np.array(cropped_enhanced_std)[:,ii]
    yerr3 = [previous_std[ii]]
    fig = plt.figure()
    plt.bar(np.arange(0.85,len(data1) + 0.85),data1,yerr=yerr1, width=width,label='single-visit',color=colors[0], error_kw=dict(ecolor='black', lw=2, capsize=0, capthick=2))
    plt.bar(np.arange(0.85,len(data2)+0.85)+ width,data2,yerr=yerr2, width=width,label='multi-visit',color=colors[1], error_kw=dict(ecolor='black', lw=2, capsize=0, capthick=2))
    plt.bar(np.arange(len(data3)),data3,yerr=yerr3, width=width,label='previous',color=colors[2], error_kw=dict(ecolor='black', lw=2, capsize=0, capthick=2))
    for R in [0.85, 1.85, 2.85]:
        #statistical annotation
        x1, x2 = R, R+.3   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
        y, h, col = height[ii][0], height[ii][1], 'k'
        plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c='black')
        plt.text((x1+x2)*.5, y+h, "***", ha='center', va='bottom', color='black')

    plt.xticks([0,1,2,3], ['$PS_{reg}$','$R=5x$','$R=10x$','$R=15x$'])
    plt.ylabel(f'{metrics[ii]}',weight='bold')
    plt.legend(loc=4)
    plt.show()
    plt.tight_layout()
    fig.savefig(f'../figures/{metrics[ii]}.png',dpi=300)


# In[ ]:
