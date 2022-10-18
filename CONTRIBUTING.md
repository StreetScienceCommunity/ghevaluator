# Testing
Tests via $ unittests
Automaticlly run the test everytime someone pushes or commits to the git repository

# Development Process
The Galaxy history is a feature on Galaxy, the bio-data processing platform, which tracks the record of steps of data analysis (including input datasets, tools used, parameters etc.). The original motivation for this tool is to provide a way for student, who creates his or her new history after learning tutorials on Galaxy training, to assess if the steps in the history matches with the standards of the tutorial. In the later stage of the tool’s development, we realized this tool can also be simply used on comparing any two Galaxy histories, for the purpose of finding the differences, and then to study the difference.

For the original motivation mentioned above, this tool is implemented on DNAnalyzer: https://github.com/StreetScienceCommunity/DNAnalyzer for evaluating user’s results’ in the BeerDEcoded part:
![image](https://user-images.githubusercontent.com/34265997/196523107-f9204501-1922-4113-80bc-3f069ea7c3b6.png)

The usage of the tool is roughly designed as followed:
![image](https://user-images.githubusercontent.com/34265997/196523146-3608e666-50dd-4301-b15a-43b933b0afbe.png)
