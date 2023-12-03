# Task 1
-To restructure my code, I begin by moving the non-plotting functions from the python package "notebooks/parse_slack_data.ipynb '' notebook. two python files, "loader.py" and "utils.py", within the
"src'' directory will serve as dedicated locations for data loading functions and utility functions, respectively. By doing this,I am organizing a codebase and separating different concerns into specialized
files.
  - Once I move the functions, you can utilize them in the "parse_slack_data.ipynb" notebook. To load data, you can now use the "SlackDataLoader" class from "src/loader.py". This class will handle all the
tasks related to data loading. It is to some extent difficult for me. Finally I had done and fixed it by
traversing all folders and the slack parser functions. Additionally, this allows me to access the utility
functions from "src/utils.py" within the notebook to assist with various data operations and
manipulations.
Perform EDA analysis to answer the following questions
Who are the top and bottom 10  users by 
Reply count?
Mention?
Message count?
Reaction count?
What are the top 10 messages by 
Replies?
Reactions?
Mentions?
Which channel has the highest activity? 
Which channel appears at the right top corner when you plot a 2D scatter plot where x-axis is the number of messages in the channel, y-axis is the sum of number of replies and reactions, and the color representing channels?
What fraction of messages are replied within the first 5mins?
Plot a 2D scatter plot such that x-axis is the time difference between the message timestamp and the first reply message, y-axis is the time of the day (in 24hr format), color representing channels? 

Perform EDA analysis to answer the following questions
Who are the top and bottom 10  users by 
Reply count?
Mention?
Message count?
Reaction count?
What are the top 10 messages by 
Replies?
Reactions?
Mentions?
Which channel has the highest activity? 
Which channel appears at the right top corner when you plot a 2D scatter plot where x-axis is the number of messages in the channel, y-axis is the sum of number of replies and reactions, and the color representing channels?
What fraction of messages are replied within the first 5mins?
Plot a 2D scatter plot such that x-axis is the time difference between the message timestamp and the first reply message, y-axis is the time of the day (in 24hr format), color representing channels? 
 
Perform EDA analysis to answer the following questions
Who are the top and bottom 10  users by 
Reply count?
Mention?
Message count?
Reaction count?
What are the top 10 messages by 
Replies?
Reactions?
Mentions?
Which channel has the highest activity? 
Which channel appears at the right top corner when you plot a 2D scatter plot where x-axis is the number of messages in the channel, y-axis is the sum of number of replies and reactions, and the color representing channels?
What fraction of messages are replied within the first 5mins?
Plot a 2D scatter plot such that x-axis is the time difference between the message timestamp and the first reply message, y-axis is the time of the day (in 24hr format), color representing channels? 
