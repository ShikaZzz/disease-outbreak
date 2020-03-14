import os
import sys
filedir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(filedir,"./../"))
import json
from src.get_datatype import GetDatatype
from src.convert2type3 import Convert2Type3
from src.spread_animator import OutbreakSpreadAnimator



class Animation:
	'''
	: Draw animations for the datasets('ebola.xlsx','sars.csv','polio.xls') 
	: which are located in 'data' folder
	'''

	def __init__(self,disease=None,countries=None,Indicator=None,output=None):
		'''
		: 
		'''
		# assertion on countries and Indicator are handled by inside level modules
		# self.cur_dir = filedir = os.path.dirname(os.path.realpath(__file__))
		# with open(os.path.join(self.cur_dir,"./../src/PARAMS.json")) as f:
		# 	self.params = json.load(f)
		# self.TYPE1 = self.params["DATATYPE"]["TYPE1"]
		# self.feasible_Indicators = self.params["All_Indicators"][self.disease]
		assert isinstance(disease,str)
		assert disease.lower() in ['ebola','sars','polio']
		self.disease = disease.lower()

		if self.disease=='ebola':
			self.fname = 'ebola.xlsx'
		elif self.disease=='sars':
			self.fname = 'sars.csv'
		elif self.disease=="polio":
			self.fname = 'polio.xls'
		else:
			raise NotImplementedError

		self.plot(countries=countries,Indicator=Indicator,output=output)

	def plot(self,countries=None,Indicator=None,output=None):
		'''
		: Plots the animations for "ebola.xlsx" in the data
		'''

		assert isinstance(output,str)
		# Load the Data
		df,_ = GetDatatype().check_type(self.fname,is_fname=True,Indicator=Indicator)
		# Convert to "type 3"
		df_type3 = Convert2Type3().convert2_type3(df,Indicator=Indicator)
		# draw the animation
		OutbreakSpreadAnimator().animate(df_type3,countries=countries,fname=output)


