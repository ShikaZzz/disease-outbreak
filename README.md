# Analysis of Disease Outbreak

## Description
This project mainly works on the different diseases outbreak and perticularly we are doing a case study on H1N1 outbreak. We analyze many factors such as season, population, viccine development and so on that may influence the outbreak of the diseases.Based on the analysis, we draw some conclusions in the end. 
## Installation Commands
- pip install -r requirements.txt
- Code is tested on python 3.7.4
- run the code using command: python main.py 

## DataSet
- Ebola : in this link: https://data.humdata.org/dataset/ebola-cases-2014/resource/a8b51b81-1fa7-499d-a9f2-3d0bce06b5b5
- Polio : in this link: https://www.kaggle.com/pitt/contagious-diseases#polio.csv
- SARS  : The dataset can be found in the dataset file called: sars_2003_complete_dataset_clean.csv
- H1N1  : in the following link: 
          https://data.world/healthdatany/jr8b-6gh6 and https://www.cdc.gov/flu/pandemic-resources/2009-h1n1-pandemic.html
- Population Data : this link: https://www.kaggle.com/muonneutrino/us-census-demographic-data
- Flights Data    : the dataset is in the h1n1_comp_xz folder
- Shape files for animation: 

## Conclusion
The commonality  of all the outbreak diseases is the neighbour countries will greatly affected. So neighbour should do some precautions to avoid this happening in the future.
There are 4 factors that will greatly influence diseases:
1. Season: it will influence the spreading rates.
2. Population: it directly proportional to spread. However, there are some exceptions.
3. Age: The aged people are much easier to get affected. 
4. Vaccine: The development of vaccine will effectively reduce the threat of viruses

## Code Overview
- we created a module that can plot the animations for generic type of data. 
   - source code available at ./src
   - Refer to ./src/spread_animator.py for more details
   - To reproduce the animations for our dataset, we created another module. location ./scripts/animations.py
- For specific case study of H1N1, we created another module. 
   - location: ./scripts/h1n1_visualizations.py


