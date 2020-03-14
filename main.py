from scripts.animations import Animation
# from scripts.h1n1_visualizations import H1N1Visualizer
import json

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

# # 
# H1N1Visualizer().map_plot(fname="states data.csv",column='Value')

# H1N1Visualizer().plot_vaccines_effect()
# H1N1Visualizer().plot_flights_influence()


# "DATA_MANUAL_COLLECTIONS.json"

# death_proportion = [1282,9565,1621]
# title1 = 'Deaths Proportion'
# hosp_proportion  = [86813,160229,27263]
# title2 = 'Hospitalizations Proportion'
# cases_proportion = [19501004,35392931,5943813]
# title3 = 'Cases Proportion'
# H1N1Visualizer().plot_vaccines_effect(death_proportion,title1)
# H1N1Visualizer().plot_vaccines_effect(hosp_proportion,title2)
# H1N1Visualizer().plot_vaccines_effect(cases_proportion,title3)

