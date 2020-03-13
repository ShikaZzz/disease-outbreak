
import pandas as pd
import numpy as np
from datetime import datetime

class DatasetSpecPreProcess():

	def __init__(self):
		pass


	def preprocess(self,fname,data,Indicator=None):
		'''
		: param fname: filename
		: type fname: str
		: param Indicator: If the data in the file belongs to "type 2", 
		:			Indicator is the column that has to be picked for "Value"
		:  			Example: If data has columns ('Country','Date','No. of death cases','No. of confirmed cases'),
		:			Indicator = 'No. of death cases' or 'No. of confirmed cases'
		: type Indicator : str 
		: Functionality: Converts the 'data' into suitable type(1,2,3) 
		:				 by changing the naming conventions and dtypes
		'''

		assert isinstance(fname,str)
		assert isinstance(data,pd.DataFrame)
		self.data = data
		if Indicator:
			assert isinstance(Indicator,(str))
		print(fname)
		if fname=="ebola.xlsx":
			# rename columns
			self.data.rename(columns={'value':'Value'},inplace=True)
			# convert the dtype of Date column into datetime
			convert2datetime = lambda x: np.datetime64(datetime.strptime(x,'%Y-%m-%d').date(),"D")
			self.data['Date'] = self.data['Date'].apply(convert2datetime)

		elif fname=="h1n1.xlsx":
			raise NotImplementedError

		elif fname=="polio.xls":
			# rename columns
			self.data = self.data.rename(columns={'on a country name for its incidence time series ':'Country'})
			self.data.fillna(0)
			# convert the dtype of years column into numeric values
			for year in self.data.keys().values[1:]:
			    self.data[year] = self.data[year].apply(lambda x: str(x).replace("'",""))
			    self.data[year] = pd.to_numeric(self.data[year], errors='coerce').fillna(0).astype(int)   

		elif fname=="sars.csv":
			Indicator = '' if Indicator is None else Indicator
			assert Indicator in self.data.columns.values
			self.data.rename(columns={Indicator:'Value'},inplace=True)
			self.data['Date'] = self.data['Date'].apply(lambda x: np.datetime64(datetime.strptime(x,'%Y-%m-%d').date(),"D"))

		else:
			raise NotImplementedError

		return self.data




