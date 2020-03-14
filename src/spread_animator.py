'''
From our datasets, we categorize data into 3 categories.
:-------------------------------------------------------
:type 1: Each row of the data is of the type ("Country","Indicator","Date","Value") 
:type 2: Each row of the data is of the type ("Country","Date","Value") 
: 		 This is the special case of type 1 where all the Indicator values are same.
:type 3: Another representation for the same data as type 2 (for the ease of animation)
:        Example:
:         | Country | Date1  | Date2 | ......... | Date_n |
:         |  China  | value1 | value2| ......... | value_n|
:              .         .        .                   .
:              .         .        .                   .
:              .         .        .                   .
:         |   US    | value1 | value2| ......... | value_n|
:-------------------------------------------------------
: Functionality: Given a "type 3" data, this module can be used to generate animations. 
:				(You can use Convert2Type3 module to convert the data into "type 3") 
'''

import os
import re
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from matplotlib.pylab import gca
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as tkr  
from mpl_toolkits.axes_grid1 import make_axes_locatable
from src.get_datatype import GetDatatype

class OutbreakSpreadAnimator:
	'''
	: Given a "type 3" data, this module can be used to generate animations. 
	: (You can use Convert2Type3 module to convert the data into "type 3") 
	'''
	def __init__(self):
		'''
		: load the parameters from json file
		'''
		# load json file for parameters
		self.cur_dir = os.path.dirname(os.path.realpath(__file__))
		with open(os.path.join(self.cur_dir,"PARAMS.json")) as f:
			self.params = json.load(f)
		self.TYPE1 = self.params["DATATYPE"]["TYPE1"]
		self.TYPE2 = self.params["DATATYPE"]["TYPE2"]
		self.TYPE3 = self.params["DATATYPE"]["TYPE3"]

		self.folder_for_plots = os.path.join(self.cur_dir,"./../plots")
		if not os.path.exists(self.folder_for_plots):
			os.makedirs(self.folder_for_plots)

	def animate(self,data,fps=None,countries=None,include_side_plot=False,fname='animation.mp4'):
		'''
		: data: pandas dataframe and this should be a "type 3" data
		: countries: list of countires to be on the plot
		:			(you can choose the subset of the countries that you want to focus on in animation.) 
		: include_side_plot: If True, animation of graphs is also included
		: fname : name of the file to save the animation into. 
		'''
		if include_side_plot:
			raise NotImplementedError

		assert isinstance(data,pd.DataFrame)
		_,Type = GetDatatype().check_type(data,is_fname=False)
		assert Type==self.TYPE3
		assert isinstance(fname,str)

		self.data = data
		# load the shape file into dataFrame
		self.load_shp_file()
		# To rename the Countries in "data" DataFrame according to the naming convention used in shape file. 
		self.country_name_formating()
		# merge dataFrames
		self.merge_data_and_shp_df(countries=countries)
		# compute parameters for plotting
		self.compute_plot_params()
		# plot
		self.plot(include_side_plot=include_side_plot,fname=fname)

		

	def plot(self,fname,fps=None,include_side_plot=False):
		'''
		:param fname:
		'''
		if include_side_plot:
			# ----------tdb----------
			raise NotImplementedError

		NUM_FRAMES = len(self.unique_dates)

		fig = plt.figure(figsize=(14,7))
		if not include_side_plot:
			ax=fig.add_subplot(111,facecolor='lightblue')
		else:
			ax=fig.add_subplot(121,facecolor='lightblue')
			ax2=fig.add_subplot(122)
			datemin = np.datetime64(self.unique_dates[0])
			datemax = np.datetime64(self.unique_dates[-1]) 
			ax2.set_xlim(datemin, datemax)
			ax2.set_ylim(self.vmin,self.vmax)
			fig.autofmt_xdate()

		fig.subplots_adjust(left=0.01, bottom=0.2, right=0.99, top=0.98, wspace=None, hspace=None)
		ax.set_xticks([])
		ax.set_yticks([])
		date_text = ax.text(0.05,0.1,'Year: {}',transform = ax.transAxes,fontsize=22);

		divider = make_axes_locatable(ax)
		cax = divider.append_axes("bottom", size="5%", pad=0.1)
		cax.xaxis.set_ticks_position("top")
		cmap = plt.cm.plasma#spring#viridis
		cmap.set_under('w')
		ax.tick_params(axis='both', which='major', labelsize=14)
		ax.tick_params(axis='both', which='minor', labelsize=8)

		def animate_func(i):
			date = self.unique_dates[i]
			ax1 = self.data_shp_df.plot(ax=ax,column=date,\
		    	vmin=self.vmin, vmax=self.vmax,cmap=cmap,legend=True,cax=cax,
		    	legend_kwds={'orientation': "horizontal"}) 
			date_text.set_text("{}-{}-{}".format(date.year,date.month,date.day))
			cbar_axes = ax1.figure.axes[-1]
			cbar_axes.tick_params(labelsize=14) 
			cbar_axes.xaxis.label.set_size(18)
			# =============================================================
			# ==================== tbd ====================
			# if include_side_plot:
			# 	temp0 = list(self.data_shp_df.columns.values)
			# 	temp = list(set(temp0)-set(['geometry']))
			# 	temp2 = self.data_shp_df[temp].set_index("Country").T
			# 	temp1 = temp2.columns.values.tolist

			# 	print("..........",temp2.keys())
			# 	# print()
			# 	# self.data_shp_df.set_index("Country").T.plot(ax=ax2)
			# 	temp2.iloc[:i+1].plot(ax=ax2)
		# NUM_FRAMES
		ani = matplotlib.animation.FuncAnimation(fig, animate_func, frames=NUM_FRAMES, 
		                                         repeat=True,interval=500)
		

		fps = int(NUM_FRAMES/12) if fps is None else fps

		ani.save(os.path.join(self.folder_for_plots,fname), fps=fps, extra_args=['-vcodec', 'libx264'])	 


	def load_shp_file(self):
		'''
		: load the shape file into dataFrame
		'''
		self.shp_fname = self.params["Country_Shape_File"]
		self.shp_fname = os.path.join(self.cur_dir,self.shp_fname)
		self.shp_df = gpd.read_file(self.shp_fname)
		self.shp_df.rename(columns={'COUNTRY':'Country'},inplace=True)
		self.shp_df['Country'] = self.shp_df['Country'].apply(lambda x: x.lower().strip())
		# remove unnecessary columns
		self.shp_df = self.shp_df[['Country','geometry']]

	def country_name_formating(self):
		'''
		: A Few country names in the shape file dataFrame and the Disease outbreak information
		: are different. These mappings are listed in the "PARAMS.json" file. 
		: This function converts the Country names of disease outbreak dataFrame using those mappings.
		: Note that, if this function is not used the mismatched countiries information is omiited.
		'''
		assert isinstance(self.data,pd.DataFrame)

		self.data['Country'] = self.data['Country'].apply(lambda x: re.sub(r'\([^)]*\)', '', x.lower()).strip())
		
		self.country_map_dict = self.params["Country_Names_Mappings"]
		self.data['Country'].replace(self.country_map_dict,inplace=True)
		# remove duplicates in country names(sum all the values corresponding to a country) 
		self.data = self.data.groupby(by=['Country'],as_index=False).sum()

	def merge_data_and_shp_df(self,countries=None):
		'''
		: merge "data" dataFrame and "shape file" dataFarme on Country (inner)
		'''
		assert isinstance(self.shp_df,gpd.geodataframe.GeoDataFrame)
		assert isinstance(self.data,pd.DataFrame)
		if countries:
			assert isinstance(countries,list)
			assert all(isinstance(country,str) for country in countries)
			countries = [country.lower() for country in countries]
			assert all([country in self.data.Country.values for country in countries])
			assert all([country in self.shp_df.Country.values for country in countries])
		

		self.data_shp_df = pd.merge(self.data,self.shp_df,on='Country',how='inner')
		self.data_shp_df = gpd.GeoDataFrame(self.data_shp_df,geometry=self.data_shp_df.geometry)
		if countries:
			self.data_shp_df = self.data_shp_df.loc[self.data_shp_df['Country'].isin(countries)]
		assert len(self.data_shp_df)>0

	def compute_plot_params(self):
		'''
		: unique_dates : 
		: vmin : 
		: vmax : 
		'''
		self.data_columns = self.data.columns
		self.unique_dates = self.data_columns[1:]
		#self.unique_dates = pd.to_datetime(np.delete(self.data_columns,np.where(self.data_columns=='Country')[0]))
		# self.unique_dates = self.unique_dates.sort_values().values
		self.vmin = 2
		self.vmax = self.data_shp_df.max(numeric_only=True).max()
	



if __name__ == '__main__':
	pass