import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def vaccine():
    #construct data
    name_list = ['Oct 2009','Nov','Dec','Jan 2010','Feb','Mar','Apr']
    #histgram data of positive and negative number
    num_list = [601,333,30,23,16,6,2]
    num_list1 = [959,812,928,993,1079,793,182]
    #line chart data of percentage of vaccined
    num_list2 = [0,3,18,27,28.5,27.3,27]
    
    x =([i for i in range(7)])

    total_width, n = 0.8, 2
    width = total_width / n
    #change the size of the figure
    fig= plt.figure(figsize=(15,8))
    #subplots()
    ax1 = fig.add_subplot(111)
    # add positive bar chart
    ax1.bar(x, num_list, width=width, label='Number Flu +',fc = 'red')
    for i in range(len(x)):
        x[i] = x[i] + width
    # add negative bar chart
    ax1.bar(x, num_list1, width=width, label='Number Flu -',tick_label = name_list,fc = 'lightblue')
    #add y label
    ax1.set_ylabel('Number Enrolled',fontsize=15)
    # change the font of x and y axis
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    
    #add another y axis to the right
    ax2 = ax1.twinx()

    fmt='%.2f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    
    ax2.plot(x, num_list2,'og-',label='vaccinated');
    ax2.yaxis.set_major_formatter(yticks)
    ax2.set_ylim([0, 35]);
    ax2.set_ylabel('vaccinated',fontsize=15);
    
    #change the legend location
    ax1.legend(loc=2,fontsize=13)
    ax2.legend(loc=1,fontsize=14)

    plt.yticks(fontsize=15)
    plt.savefig('figure1.png')
    plt.show()
