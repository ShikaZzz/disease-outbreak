import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


class H1N1Visualizer():
    '''
    : 
    '''
    def __init__(self):
        pass
    
    def map_plot(self,fname="states data.csv",column='Value'):
        '''
        : 
        '''
        assert isinstance(fname,str)
        assert os.path.exists(fname) 
        
        self.fname = fname
        self.column=column
        self.get_data()
        self.get_fig_handle()
        self.get_basemap()
        self.get_plot_params()
        self.draw_state_boundaries()
        self.get_colors()
        self.get_patches()
        self.plot_bounding_boxes()
        self.set_color_bar()
        plt.savefig('H1N1 distribution.png')
        plt.show()
        
    def get_fig_handle(self,):
        '''
        :
        '''
        self.fig= plt.figure(figsize=(14,7))
        self.ax = self.fig.add_subplot(111)
        #%% ---- Add the title name ----
        if self.column=='Value':
            self.ax.set_title('United States H1N1 Distribution',fontsize=25)
        elif self.column=='Population':
            self.ax.set_title('United States Population Distribution',fontsize=25)
        else:
            pass
        
        self.ax.tick_params(axis='y',labelsize=15)
#         self.ax.set_yticks(fontsize=15)
        
    def set_color_bar(self,):
        '''
        : add color bar axes
        '''
        self.ax_c = self.fig.add_axes([0.82, 0.11, 0.03, 0.8])
        self.cb = ColorbarBase(self.ax_c,cmap=self.cmap,norm=self.norm,orientation='vertical')
        
    def get_plot_params(self,):
        self.AREA_1 = 0.005  # exclude small Hawaiian islands that are smaller than AREA_1
        self.AREA_2 = self.AREA_1 * 30.0  # exclude Alaskan islands that are smaller than AREA_2
        self.AK_SCALE = 0.19  # scale down Alaska to show as a map inset
        self.HI_OFFSET_X = -1900000  # X coordinate offset amount to move Hawaii "beneath" Texas
        self.HI_OFFSET_Y = 250000    # similar to above: Y offset for Hawaii
        self.AK_OFFSET_X = -250000   # X offset for Alaska (These four values are obtained
        self.AK_OFFSET_Y = -750000   # via manual trial and error, thus changing them is not recommended.)
        
    
    def get_basemap(self):
        # Lambert Conformal map of lower 48 states.
        self.m = Basemap(llcrnrlon=-119,llcrnrlat=20,urcrnrlon=-64,urcrnrlat=49,resolution='l',
                    projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

        # Mercator projection, for Alaska and Hawaii
        self.m_ = Basemap(llcrnrlon=-190,llcrnrlat=20,urcrnrlon=-143,urcrnrlat=46,resolution='l',
                    projection='merc',lat_ts=20)  # do not change these numbers
    
    def draw_state_boundaries(self,):
        '''
        : ---------   draw state boundaries  --------------
        :data from U.S Census Bureau
        : http://www.census.gov/geo/www/cob/st2000.html
        '''
        
        shp_info = self.m.readshapefile('st99_d00','states',drawbounds=True,
                                   linewidth=0.45,color='gray')
        shp_info_ = self.m_.readshapefile('st99_d00','states',drawbounds=False)
    
    def get_colors(self):
        '''
        
        '''
        #%% -------- choose a color for each state based on population density. -------
        self.colors={}
        self.statenames=[]
        self.cmap = plt.cm.hot_r # use 'reversed hot' colormap
        self.vmin = 0; self.vmax = 11000 # set range.
        self.norm = Normalize(vmin=self.vmin, vmax=self.vmax)
        for shapedict in self.m.states_info:
            statename = shapedict['NAME']
            # skip DC and Puerto Rico.
            if statename not in ['District of Columbia','Puerto Rico']:
                pop = self.data[statename]
                #pop = h1n1[statename]
                # calling colormap with value between 0 and 1 returns
                # rgba value.  Invert color range (hot colors are high
                # population), take sqrt root to spread out colors more.
                cmap = plt.get_cmap('Reds')
                self.colors[statename] = cmap(np.sqrt((pop-self.vmin)/(self.vmax-self.vmin)))[:3]
            self.statenames.append(statename)
        
    def get_patches(self,):
        '''
        :
        '''
        #%% ---------  cycle through state names, color each one.  --------------------
        for nshape,seg in enumerate(self.m.states):
            # skip DC and Puerto Rico.
            if self.statenames[nshape] not in ['Puerto Rico', 'District of Columbia']:
                color = rgb2hex(self.colors[self.statenames[nshape]])
                poly = Polygon(seg,facecolor=color,edgecolor=color)
                self.ax.add_patch(poly)
        
        for nshape, shapedict in enumerate(self.m_.states_info):  # plot Alaska and Hawaii as map insets
            if shapedict['NAME'] in ['Alaska', 'Hawaii']:
                seg = self.m_.states[int(shapedict['SHAPENUM'] - 1)]
                if shapedict['NAME'] == 'Hawaii' and float(shapedict['AREA']) > self.AREA_1:
                    seg = [(x + self.HI_OFFSET_X, y + self.HI_OFFSET_Y) for x, y in seg]
                    color = rgb2hex(self.colors[self.statenames[nshape]])
                elif shapedict['NAME'] == 'Alaska' and float(shapedict['AREA']) > self.AREA_2:
                    seg = [(x*self.AK_SCALE + self.AK_OFFSET_X, y*self.AK_SCALE + self.AK_OFFSET_Y)\
                           for x, y in seg]
                    color = rgb2hex(self.colors[self.statenames[nshape]])
                poly = Polygon(seg, facecolor=color, edgecolor='gray', linewidth=.45)
                self.ax.add_patch(poly)
    
    def plot_bounding_boxes(self,):
        '''
        : Plot bounding boxes for Alaska and Hawaii insets 
        '''
        light_gray = [0.8]*3  # define light gray color RGB
        x1,y1 = self.m_([-190,-183,-180,-180,-175,-171,-171],[29,29,26,26,26,22,20])
        x2,y2 = self.m_([-180,-180,-177],[26,23,20])  # these numbers are fine-tuned manually
        self.m_.plot(x1,y1,color=light_gray,linewidth=0.8)  # do not change them drastically
        self.m_.plot(x2,y2,color=light_gray,linewidth=0.8)
        
    def get_data(self,):
        '''
        :population density by state from
        :http://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density
        :h1n1 data
        '''
         
        self.data=pd.read_csv(self.fname)
        assert self.column in self.data.keys().values
        assert 'State' in self.data.keys().values
        print(self.column)
        self.data = dict(zip(self.data['State'].values,self.data[self.column].values))

    def pie_charts(self,sizes,title):
    	'''

    	'''
    	#adjust the size of figure
    	plt.figure(figsize=(6,9))
    	#define label
    	labels = ['0-17 years','18-64 years','65+ years']
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
    	plt.axis('equal')
    	plt.title(title,fontsize=25)
    	plt.show()


	# def plot_vaccines_effect(self,):

	# 	print("in Vaccines 1")
	# 	#load data
	# 	name_list = ['Oct 2009','Nov','Dec','Jan 2010','Feb','Mar','Apr']
	# 	#histgram data of positive and negative number
	# 	num_list = [601,333,30,23,16,6,2]
	# 	num_list1 = [959,812,928,993,1079,793,182]
	# 	#line chart data of percentage of vaccined
	# 	num_list2 = [0,3,18,27,28.5,27.3,27]

	# 	x =([i for i in range(7)])

	# 	total_width, n = 0.8, 2
	# 	width = total_width/n
	# 	#change the size of the figure
	# 	fig= plt.figure(figsize=(15,8))
	# 	#subplots()
	# 	ax1 = fig.add_subplot(111)
	# 	# add positive bar chart
	# 	ax1.bar(x, num_list, width=width, label='Number Flu +',fc = 'red')
	# 	for i in range(len(x)):
	# 	    x[i] = x[i] + width
	# 	# add negative bar chart
	# 	ax1.bar(x, num_list1, width=width, label='Number Flu -',tick_label = name_list,fc = 'lightblue')
	# 	#add y label
	# 	ax1.set_ylabel('Number Enrolled',fontsize=15)
	# 	# change the font of x and y axis
	# 	plt.xticks(fontsize=15)
	# 	plt.yticks(fontsize=15)
	# 	print("in Vaccines 2")
	# 	#add another y axis to the right
	# 	ax2 = ax1.twinx()

	# 	fmt='%.2f%%'
	# 	yticks = mtick.FormatStrFormatter(fmt)

	# 	ax2.plot(x, num_list2,'og-',label='vaccinated');
	# 	ax2.yaxis.set_major_formatter(yticks)
	# 	ax2.set_ylim([0, 35]);
	# 	ax2.set_ylabel('vaccinated',fontsize=15);

	# 	#change the legend location
	# 	ax1.legend(loc=2,fontsize=13)
	# 	ax2.legend(loc=1,fontsize=14)

	# 	plt.yticks(fontsize=15)
	# 	print("in Vaccines 3")
	# 	plt.savefig('./../plots/h1n1_vaccine.png')
	# 	plt.show()

	# def plot_flights_influence(self):
	#     #construct data
	#     name_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

	#     #line chart data
	#     num_list2 = [532339,488410,557422,537793,546832,557594,580134,568301,1021704,0,509540,529269]
	#     num_list1 = [0,0,0,102,5330,19436,10406,4887,6713,20948,28033,4633]

	#     x =([1,2,3,4,5,6,7,8,9,10,11,12])
	    
	#     #change the size of the figure
	#     fig= plt.figure(figsize=(15,9))
	#     #subplots()
	#     ax1 = fig.add_subplot(111)
	#     ax1.bar(x,num_list1,label='Num of Infected',color='r')
	#     ax1.set_ylabel('Number of Infected',fontsize=15)
	#     plt.xticks(fontsize=15)
	#     plt.yticks(fontsize=15)

	#     # add second y-ticks
	#     ax2 = ax1.twinx()

	#     ax2.plot(x, num_list2,'ob-',label='Total Flights');
	#     ax2.set_ylabel('Num of Flights',fontsize=15);
	    
	#     #change the legend location
	#     ax1.legend(loc=0,fontsize=15)
	#     ax2.legend(loc=9,fontsize=15)
	    
	#     plt.yticks(fontsize=15)
	#     plt.xticks(x,name_list,fontsize = 15)
	#     plt.savefig('./../plots/flights.png')
	#     plt.show()


	    
	
