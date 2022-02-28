# Unmasking COVID-19 Behavior and Perception

![A screenshot of your application. Could be a GIF.](screenshot.png)

TODO: Update screenshot

TODO: Short abstract describing the main goals and how you achieved them.

This project develops a data-visualization web-application using Altair and Streamlit to study the way people's perception and actual behavior with repsect to vaccination and masking change as the pandemic evolves. We chose to study and visualize data from two data sources made available from [COVIDcast](https://delphi.cmu.edu/covidcast/export/) -

*  **Delphi US COVID-19 Trends and Impact Survey** - This dataset contains reponses from surveys about COVID-19 beliefs and behaviors administered on Facebook. We look at the data about proportion of respondents who wear masks, believe wearing masks is effective, are vaccinated and believe vaccination is effective
*  **Johns Hopkins University's Center for Systems Science and Engineering COVID-19 dataset** - This dataset contains statistics about case counts and fatalities resulting from COVID-19. We look at the daily 7 day average of confirmed cases over time.

We developed a set of interactive visualizations that allow users to study changes in indicators of behavior and perception of methods to prevent the spread of COVID-19 with changes in confirmed case counts over time in the United States of America.

## Project Goals

The goal of the streamlit application we developed for this assignment is to give users the tools to study how people’s behavior and perceptions of effectiveness of vaccination and masking change as the pandem evolves. Specifically it aims to answer the following questions 

* Do more people believe that vaccination/masking is effective in curbing the spread of COVID-19 when confirmed case counts increase?
* Do more people actually get vaccinated and wear masks when confirmed case counts increase?
* Do people’s perceptions about whether vaccination/masking is effective agree with their behavior? Specifically, when more people believe vaccination/masking is effective, do more people actually get vaccinated/wear masks?


## Design

TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices?

The nature of the questions we chose were such that they had to be answered using time-series data. The visualization developed for studying both vaccination as well as masking were line/area graphs since they are conducive to representing time series data.

### Vaccination Visualizations
### Masking Visualizations
In order to study how behavior and perceptions related to masking change with case counts, we chose to plot three line graphs, one for the proportion of survey respondents who reported that they wore a mask in public places in the last 7 days, one for the proportion of respondents who believe masking is effective in curbing the spread of COVID-19, and one for the confirmed case count. Plotting all three in the same figure enabled easy comparison. However, there is room for improvement to facilitate better comparison across each of these signals. To begin with, we chose to implement a multiline tooltip i.e. a vertical line connecting all three lines at each point on the x axis along with their corresponding y values. The multiline tooltip makes it easy to identify how one series changes with respect to the other. For example, as you mouseover the plot from a region of low to high casecounts, the multiline toolip highlights exactly how the other two signals change. Much of the code to implement this feature comes from an [Altair example](https://altair-viz.github.io/gallery/multiline_tooltip.html). A user might want to study each series in isolation or study two at a time. To facilitate this, we also added an interactive legend that allows you to multi-select lines to simultaneously display. 

## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?

Our goals were focussed on two key COVID related human behaviors - vaccination and masking. 

We began by first identifying the dataset we wanted to work with. After exploring some of the suggested datasets, we were able to develop interesting questions about the COVID-19 dataset that a data science web-app could help answer. After narrowing down the scope of our questions to a point where we were able to associate design/development components to each question, we chose to divide the work evenly with one of us developing the visualizations for vaccination and the other developing the visualization for masking behavior. 

We spent roughly 12 hours each on the design and development of our assigned components, an additional two hours piecing together our visualizations into a consolidated web-application, and 7-8 hours to plan out and write the report.

The data exploration and development phase of the assignment was the most time consuming. This is because we worked with mutliple sources of data. We spent a considerable amount of time exploring each dataset, and understanding the right way to join the datasets we were working with in a manner that facilitated convenient plotting with Altair. Implementing and rendering the visualizations with Altair and Streamlit also took a considerable amount of time because we experimented with features of these tools, such as interactive legends, that were new to us.


## Success Story

TODO:  **A success story of your project.** Describe an insight or discovery you gain with your application that relates to the goals of your project.

### Vaccination Visualizations
### Masking Visualizations
The series describing the proportion of people who actually wear mask correlated well with the series describing the confirmed case count - they seem to move in tandem and this is intuitive. However, it appears that the proportion of people who believe that masking is effective remains steady over time and does not change much with case count. What is interesting is that it does not even vary with changes to the proportion of people who actually do wear a mask! This indicates a mismatch in the perception and actual behavior of people with respect to masking - while many people believe masking is effective, oftentimes, not all of them are actually wearing masks!
