import numpy as np
import matplotlib.pyplot as plt

def pie_charts(sizes,title):
    #adjust the size of figure
    plt.figure(figsize=(6,9)) 
    #define label
    labels = ['0-17 years','18-64 years','65+ years']
    
    colors = ['yellow','lightskyblue','yellowgreen']
    #The larger the value is, the larger the gap is
    explode = (0.02,0.02,0.005) 
    patches,text1,text2 = plt.pie(sizes,
                          explode=explode,
                          labels=labels,
                          colors=colors,
                          labeldistance = 1.2,
                          autopct = '%3.2f%%', 
                          shadow = False, 
                          startangle =90, 
                          pctdistance = 0.6) 
    for t in text1:
        t.set_size(17)
    for t in text2:
        t.set_size(17)

    #x,y is consistent so ensure it's a circle
    plt.axis('equal')
    #plt.legend()
    plt.title(title,fontsize=25)
    plt.show()
    
death_proportion = [1282,9565,1621]
title1 = 'Deaths Proportion'
hosp_proportion  = [86813,160229,27263]
title2 = 'Hospitalizations Proportion'
cases_proportion = [19501004,35392931,5943813]
title3 = 'Cases Proportion'
pie_charts(death_proportion,title1)
pie_charts(hosp_proportion,title2)
pie_charts(cases_proportion,title3)