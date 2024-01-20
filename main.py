from github import Github
from github import Auth
from flask import Flask, jsonify, request



app = Flask(__name__)


#api token here
auth = Auth.Token('api token')

g = Github(auth=auth)

#loading repository
#repository name
repo_name = "name/reponame"
repo = g.get_repo(repo_name)





all_commits = repo.get_commits()

# Fetching contributors and their contributes
contributors_data = {}
for contributor in repo.get_contributors():
    commits = repo.get_commits(author=contributor.login)
    
    line_changes = sum(commit.stats.total for commit in commits)
    file_changes = len({file.filename for commit in commits for file in commit.files})

    contributors_data[contributor.login] = {
        "line_changes": line_changes,
        "file_changes": file_changes
    }



      
# Fetching merged pull requests and count 
merged_pr_counts = {}
for pull in repo.get_pulls(state="all"):  
    if pull.merged:
        merged_by = pull.merged_by.login
        merged_pr_counts.setdefault(merged_by, 0)
        merged_pr_counts[merged_by] += 1





# Fetching no. of pull requests 
pr_counts = {}
for pull in repo.get_pulls(state="all"):  
    user = pull.user.login
    pr_counts.setdefault(user, 0)
    pr_counts[user] += 1




# Fetching pull reviews and count reviews by user
pr_reviews = {}
for pull in repo.get_pulls(state="all"): 
    for review in pull.get_reviews():
        reviewer = review.user.login
        pr_reviews.setdefault(reviewer, 0)
        pr_reviews[reviewer] += 1





# display line change and file change
@app.route("/user")
def user():
    user_data = [{"author": author, "count": count} for author, count in contributors_data.items()]
    return jsonify(user_data)


# display merge count
@app.route("/merge_count")
def get_merge_count():
    merge_count_data = [{"author": author, "count": count} for author, count in merged_pr_counts.items()]
    return jsonify(merge_count_data)




#display pull requests
@app.route("/pull_request")
def get_pull_request():
    pull_request_data = [{"author": author, "count": count} for author, count in pr_counts.items()]
    return jsonify(pull_request_data)




#display pull reviews
@app.route("/pr_reviewed")
def get_prs_reviewed():
    pr_review_data = [{"author": author, "count": count} for author, count in pr_reviews.items()]
    return jsonify(pr_review_data)





g.close()

if __name__ == '__main__':
    app.run(debug=True)
