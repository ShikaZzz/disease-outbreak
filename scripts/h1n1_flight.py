import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def flight():
    #construct data
    name_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    #line chart data
    num_list2 = [532339,488410,557422,537793,546832,557594,580134,568301,1021704,0,509540,529269]
    num_list1 = [0,0,0,102,5330,19436,10406,4887,6713,20948,28033,4633]

    x =([1,2,3,4,5,6,7,8,9,10,11,12])
    
    #change the size of the figure
    fig= plt.figure(figsize=(15,9))
    #subplots()
    ax1 = fig.add_subplot(111)
    ax1.bar(x,num_list1,label='Num of Infected',color='r')
    ax1.set_ylabel('Number of Infected',fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    # add second y-ticks
    ax2 = ax1.twinx()

    ax2.plot(x, num_list2,'ob-',label='Total Flights');
    ax2.set_ylabel('Num of Flights',fontsize=15);
    
    #change the legend location
    ax1.legend(loc=0,fontsize=15)
    ax2.legend(loc=9,fontsize=15)
    
    plt.yticks(fontsize=15)
    plt.xticks(x,name_list,fontsize = 15)
    plt.savefig('flights.png')
    plt.show()
