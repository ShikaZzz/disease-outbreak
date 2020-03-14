from scripts.animations import Animation
from scripts.h1n1_visualizations import H1N1Visualizer
import json
from scripts.h1n1_vaccine import vaccine
from scripts.h1n1_flight import flight

# For the animation of a disease. 
# you can vary the 
# disease from ['ebola','sars','polio']
# Indicator from ./src/PARAMS.json - ["All_Indicators"][disease]
# countries : You can leave it None 
# output : output filename for the animations to be save 
# (animations will be saved into plots folder with default name 'animations.mp4')
print("Drawing Animations........")
Animation(disease='ebola',
	countries=['guinea','liberia','sierra leone'],
	Indicator='Cumulative number of confirmed Ebola cases',
	output='ebola.mp4')

#h1n1 visualization
H1N1Visualizer().map_plot(fname="./data/h1n1/states data.csv",column='Value')

flight()
vaccine()
pie_charts()

