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
: Functionality: To compute the type of data.
'''

import os
import glob
import json
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_string_dtype as is_string
from pandas.api.types import is_numeric_dtype as is_numeric
from src.load_data import LoadData
import datetime as dt


class GetDatatype:
	'''
	: computes the type of data.
	'''
	def __init__(self):
		'''
		
		'''
		self.cur_dir = filedir = os.path.dirname(os.path.realpath(__file__))
		with open(os.path.join(self.cur_dir,"PARAMS.json")) as f:
			self.params = json.load(f)
		self.TYPE1 = self.params["DATATYPE"]["TYPE1"]
		self.TYPE2 = self.params["DATATYPE"]["TYPE2"]
		self.TYPE3 = self.params["DATATYPE"]["TYPE3"]

	def check_data(self,data,is_fname=False,Indicator=None):
		'''
		:param data : Data 
		:type data  : pd.DataFrame,
		:			  str - filename (csv/xls/xlsx)
		:param is_fname: True if data is filename, Else False
		:type is_fname : bool
		:param Indicator: If the data in the file belongs to "type 2", 
		:			Indicator is the column that has to be picked for "Value"
		:  			Example: If data has columns ('Country','Date','No. of death cases','No. of confirmed cases'),
		:			Indicator = 'No. of death cases' or 'No. of confirmed cases'
		:type Indicator : str 
		:Functionality: 
		:			checks if the data is in correct format.
		:			If data is str and if the corresponding file exists in data folder,
		:			it extracts the pandas dataframe from the corresponding file
		'''
		assert isinstance(is_fname,bool)
		if Indicator:
			assert isinstance(Indicator,(str))

		if not is_fname:
			assert isinstance(data,pd.DataFrame)
			self.data = data
		else:
			assert isinstance(data,str)
			self.data = LoadData().load(data,Indicator=Indicator)

	def check_type(self,data,is_fname=False,Indicator=None):
		'''
		:param data : Data 
		:type data  : pd.DataFrame,
		:			  str - filename (csv/xls/xlsx)
		:param is_fname: True if data is filename, Else False
		:type is_fname : bool
		:param Indicator: If the data in the file belongs to "type 2", 
		:			Indicator is the column that has to be picked for "Value"
		:  			Example: If data has columns ('Country','Date','No. of death cases','No. of confirmed cases'),
		:			Indicator = 'No. of death cases' or 'No. of confirmed cases'
		:type Indicator : str 
		:Funcationality: check for type (1,2,3)
		: check for type1: data should have all the columns mentioned in PARAMS-REQUIREDCOLUMNS-TYPE1
		:                  And each of the column should satisfy the corresponding dtype mentioned in check_column_dtype
		: check for type2: data should have all the columns mentioned in PARAMS-REQUIREDCOLUMNS-TYPE2
		:                  And each of the column should satisfy the corresponding dtype mentioned in check_column_dtype
		: check for type3: data should have all the columns mentioned in PARAMS-REQUIREDCOLUMNS-TYPE3
		:				   And these columns should satisfy the corresponding dtype mentioned in check_column_dtype
		:                  All the remaining columns should be of 'Value' type
		'''
		self.check_data(data,is_fname=is_fname,Indicator=Indicator)
		if self.check_columns_names(self.data,self.params["REQUIREDCOLUMNS"]["TYPE1"]):
			
			for column_name in self.params["REQUIREDCOLUMNS"]["TYPE1"]:
				self.check_column_dtype(self.data,column_name,column_name)

			return self.data,self.TYPE1

		elif self.check_columns_names(self.data,self.params["REQUIREDCOLUMNS"]["TYPE2"]):
			
			for column_name in self.params["REQUIREDCOLUMNS"]["TYPE2"]:
				self.check_column_dtype(self.data,column_name,column_name)

			return self.data,self.TYPE2

		elif self.check_columns_names(self.data,self.params["REQUIREDCOLUMNS"]["TYPE3"]):
			
			for column_name in self.data.keys().values:
				if column_name in self.params["REQUIREDCOLUMNS"]["TYPE3"]:
					self.check_column_dtype(self.data,column_name,column_name)
				else:
					self.check_column_dtype(self.data,column_name,"Value")
			return self.data,self.TYPE3

		else:
			raise NotImplementedError

	def check_columns_names(self,data,required_columns):
		'''
		
		:param data : Data 
		:type data  : pd.DataFrame,
		:			  str - filename (csv/xls/xlsx)
		:param required_columns : These are the column names 
		: 			that will be checked if 'data' has them or not.
		:type required_columns : list of strings
		:output : True if dataframe of 'data' has the "required_columns"
		'''

		self.check_data(data)
		assert isinstance(required_columns,list)
		assert all([isinstance(column_name,str) for column_name in required_columns])

		return len(set(required_columns)-set(self.data.keys().values))==0

	def check_column_dtype(self,data,column_name,required_dtype):
		'''
		:param data : Data 
		:type data  : pd.DataFrame,
		:			  str - filename (csv/xls/xlsx)
		:param column_name : column name
		:type column_name  : str
		:param required_dtype : one among {"Indicator","Date","Country","Value"}
		:type required_dtype  : str
		:Functionality: checks if values in corresponding column("column_name") of data
		:               has the property of required_dtype
		:               For "Indicator" - all values of col should be str
		:               For "Date" - all values of col should be 
		:               For "Country" - all values of col should be str # tbd - check if they are actual country names
		:               For "Value" - all values of col should be int
		'''

		self.check_data(data)
		assert isinstance(column_name,str) or isinstance(column_name,int) or isinstance(column_name,dt.date)
		assert column_name in data.keys().values
		assert required_dtype in self.params["REQUIREDCOLUMNS"]["TYPE1"]
		if required_dtype=="Indicator":
			# check if each value in the data.column_name column is str type
			assert is_string(self.data[column_name])
		elif required_dtype=="Date":
			# check if each value in the data.column_name column is datetime64 type
			assert is_datetime(self.data[column_name])
		elif required_dtype=="Country":
			# check if each value in the data.column_name column is str type
			assert is_string(self.data[column_name])    
			# tbd - check if they are actual country names
		elif required_dtype=="Value":
			# check if each value in the data.column_name column is int type
			assert is_numeric(self.data[column_name])
		else:
			raise NotImplementedError
	 
if __name__ == '__main__':
	pass
