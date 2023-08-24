### Overview

This 


### Problem Statement

Generally speaking, you will be asked to come up with a data science problem. This problem is ultimately up to you, but below are some guidelines/things to consider when crafting a problem statement:
> 1. Consider your audience. Who is your project going to help? Who will your presentation be geared towards? Establishing your audience first can help you narrow down your scope.
> 2. Consider the data you will use. Based on the contents of this data, think about some questions you could reasonably answer. These questions should aim to solve some kind of problem.
> 3. Based on these questions, what would bring some kind value to your audience? This can be business insights, increase sales, make decisions, etc.
> 4. Put everything from the above steps together into a few sentences that describe the specific problem you are trying to solve and who it will benefit.
> [Here is a blog post](https://towardsdatascience.com/defining-a-data-science-problem-4cbf15a2a461) about crafting a data science problem statement.

Here are some example prompts if you need inspiration:
> * Your work for the Singapore tourism and you are required to advice tourist who visit Singapore and love being outdoors, on how they can be prepared based on their travel months.
> * You work for a local delivery-app and you want to use weather to better plan your operations.
> * You are hired by Meteorological Services Singapore to analyze weather trends in Singapore and identify business that might be interested to use them.
> * You are an outdoor event planner. After covid, you want to create events that families can come and enjoy. 
> * *Feel free to be creative with your own prompt!*

And here are some example problem statements related to the above prompts. Come up with your own or modify these for your needs:
> * Weather in Singapore are largely sunny or rainy. However, tourists who are not familiar with local weather conditions may be caught off guard, causing their plans to be disrupted. This project aims to analyse trends in Singapore weather to identify adverse conditions for tourists who enjoy being outdoor. This analysis can help tourist plan travel period and itinerary better, bringing home a pleasant experience.
> * You are working for a local delivery services company. Every year, delivery operations and customer demand are heavily impacted by rainy weather conditions. This can be circumvented if the company can plan for such conditions beforehand. This project aims to analyse the monthly weather patterns over the year to allow the operations team to better plan and allocate resources during the rainy seasons.
> * *Feel free to be creative with your own problem statement!*


### Datasets

#### Provided Data

There are 2 datasets included in the [`data`](./data/) folder for this project. These correponds to rainfall information. 

* [`rainfall-monthly-number-of-rain-days.csv`](./data/rainfall-monthly-number-of-rain-days.csv): Monthly number of rain days from 1982 to 2022. A day is considered to have “rained” if the total rainfall for that day is 0.2mm or more.
* [`rainfall-monthly-total.csv`](./data/rainfall-monthly-total.csv): Monthly total rain recorded in mm(millimeters) from 1982 to 2022

Other relevant weather datasets from [data.gov.sg](data.gov.sg) that you can download and use are as follows:

* [Relative Humidity](https://data.gov.sg/dataset/relative-humidity-monthly-mean)
* [Monthly Maximum Daily Rainfall](https://data.gov.sg/dataset/rainfall-monthly-maximum-daily-total)
* [Hourly wet bulb temperature](https://data.gov.sg/dataset/wet-bulb-temperature-hourly)
* [Monthly mean sunshine hours](https://data.gov.sg/dataset/sunshine-duration-monthly-mean-daily-duration)
* [Surface Air Temperature](https://data.gov.sg/dataset/surface-air-temperature-mean-daily-minimum)

**Make sure you cross-reference your data with your data sources to eliminate any data collection or data entry issues.**

#### Additional Data
You can also use other datasets for your analysis, make sure to cite the source when you are using them.

---

### Deliverables

All of your projects will comprise of a written technical report and a presentation. As we continue in the course, your technical report will grow in complexity, but for this initial project it will comprise:
- A Jupyter notebook that describes your data with visualizations & statistical analysis.
- A README markdown file the provides an introduction to and overview of your project.
- Your presentation slideshow rendered as a .pdf file.
**NOTE**: Your entire Github repository will be evaluated as your technical report. Make sure that your files and directories are named appropriately, that all necessary files are included, and that no unnecessary or incomplete files are included.

For your first presentation, you'll be presenting to a **non-technical** audience. You should prepare a slideshow with appropriately scaled visuals to complement a compelling narrative. **Presentation duration will be 10 minutes.**

---