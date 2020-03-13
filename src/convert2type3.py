'''

'''

import os
import json
import pandas as pd
from src.get_datatype import GetDatatype

class Convert2Type3:

	def __init__(self):
		'''

		'''
		self.cur_dir = os.path.dirname(os.path.realpath(__file__))
		with open(os.path.join(self.cur_dir,"PARAMS.json")) as f:
			self.params = json.load(f)
		self.TYPE1 = self.params["DATATYPE"]["TYPE1"]
		self.TYPE2 = self.params["DATATYPE"]["TYPE2"]
		self.TYPE3 = self.params["DATATYPE"]["TYPE3"]
		self.TYPE1_COLS = self.params["REQUIREDCOLUMNS"]["TYPE1"]
		self.TYPE2_COLS = self.params["REQUIREDCOLUMNS"]["TYPE2"]
		self.TYPE3_COLS = self.params["REQUIREDCOLUMNS"]["TYPE3"]

	def convert2_type3(self,data,Indicator=None):
		'''
		: data: pandas dataframe
		: params Indicator: The type 1 data has a column "Indicator" which can have 
		:				multiple indicator values This parameter specifies which indicator 
		:           	value should be picked to convert the data into type 3       
		
		: Functionality: Converts data from type 1/type 2 to type 3 and 
		:                returns dataframe of type 3
		'''

		assert isinstance(data,pd.DataFrame)
		_,Type = GetDatatype().check_type(data,is_fname=False)

		if Type==self.TYPE2:
			self.data = self.convert_type2_to_type3(data)
		elif Type==self.TYPE1:
			self.data = self.convert_type1_to_type2(data,Indicator=Indicator)
			self.data = self.convert_type2_to_type3(self.data)
		else:
			raise NotImplementedError

		return self.data



	def convert_type2_to_type3(self,data):
		'''
		: data: pandas dataframe
		: Functionality: Converts data from type 2 to type 3 and 
		:                returns dataframe of type 3
		'''

		assert isinstance(data,pd.DataFrame)
		_,Type = GetDatatype().check_type(data,is_fname=False)
		assert Type==self.TYPE2
		self.data = data


		unique_countries = self.data['Country'].unique()

		for i,country in enumerate(unique_countries):
		    df_cur = self.data.loc[self.data['Country']==country][['Date','Value']]
		    df_cur = df_cur.groupby(by='Date',as_index=False).sum()
		    df_cur.columns = ['Date',country.lower()]
		    if not i:
		        self.data_type3 = df_cur.copy()
		    else:
		         self.data_type3 = pd.merge(self.data_type3,df_cur,on='Date',how='outer')
		        
		self.data_type3 = self.data_type3.sort_values('Date')
		self.data_type3 = self.data_type3.fillna(0)
		self.data_type3 = self.data_type3.set_index('Date').T.reset_index()

		return self.data_type3

	def convert_type1_to_type2(self,data,Indicator=None):
		'''
		:params data: pandas dataframe
		:params Indicator: The type 1 data has a column "Indicator" which can have 
		:				multiple indicator values This parameter specifies which indicator 
		:           	value should be picked to convert the data into type 3       
		: Functionality: Converts data from type 1 to type 2 and 
		:                returns dataframe of type 2
		'''
		assert isinstance(data,pd.DataFrame)
		_,Type = GetDatatype().check_type(data,is_fname=False)
		assert Type==self.TYPE1

		self.data = data
		assert Indicator in self.data['Indicator'].values
		self.data_type2 = self.data.loc[self.data['Indicator']==Indicator][self.TYPE2_COLS]
		return self.data_type2


if __name__ == '__main__':
	pass