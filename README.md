Get Github Repository stats easily using this api. 

Get number of contributors, no of lines contributed per user, No of File Contribution per user, PR Merged per user, PR Creation per user, PR Review per user. 

Packages used :
Flask, pygithub

Install package using :
pip install flask
pip install pygithub

open main.py file.

Add you github api credentials in :

auth = Auth.Token('api-token') 

Add your github username and repository name here :

repo_name = "name/reponame"


Run main.py to test the api. 

For Visualizing the data from api just run the index.html make sure to enable cors in your browser using any chrome extension if tested locally. 






