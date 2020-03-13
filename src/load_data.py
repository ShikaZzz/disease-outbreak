'''

'''
import os
import glob
import json
import pandas as pd
from src.dataset_specific_preprocessing import DatasetSpecPreProcess


class LoadData:
	'''
	help
	'''
	def __init__(self):
		'''
		 
		'''
		self.cur_dir = os.path.dirname(os.path.realpath(__file__))
		with open(os.path.join(self.cur_dir,"PARAMS.json")) as f:
			self.params = json.load(f)
		self.CSV = self.params["FILETYPE"]["CSV"]
		self.EXCEL = self.params["FILETYPE"]["EXCEL"]

	def check_fname(self,fname):
		'''
		:param fname: filename
		:type fname : str 
		:Functionality: checks if the input fname is valid input
		'''
		assert isinstance(fname,str)
		# check for file type
		assert fname.endswith((".csv",".xls",".xlsx"))
		# check for the existance of data(filename)
		files = glob.glob(os.path.join(self.cur_dir,'./../data/**/*'),recursive=True)
		check_in_files = [fname in file for file in files]
		assert any(check_in_files)
		assert sum(check_in_files)==1

		self.fname = files[check_in_files.index(1)]
		self.ftype = self.CSV if self.fname.endswith((".csv")) else self.EXCEL

	def load(self,fname,Indicator=None):
		'''
		:param fname: filename
		:type fname : str 
		:param Indicator: If the data in the file belongs to "type 2", 
		:			Indicator is the column that has to be picked for "Value"
		:  			Example: If data has columns ('Country','Date','No. of death cases','No. of confirmed cases'),
		:			Indicator = 'No. of death cases' or 'No. of confirmed cases'
		:type Indicator : str 
		:Functionality: returns pandas DataFrame 
		'''
		self.check_fname(fname)
		if Indicator:
			assert isinstance(Indicator,(str))

		if self.ftype == self.CSV:
			self.data = pd.read_csv(self.fname)
		elif self.ftype==self.EXCEL:
			self.data = pd.read_excel(self.fname)
		else:
			raise NotImplementedError

		return DatasetSpecPreProcess().preprocess(self.fname.split("/")[-1],self.data,Indicator=Indicator)


if __name__ == '__main__':
	pass