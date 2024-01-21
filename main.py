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
def getContributionByUser():
    contributors_data = {}
    for contributor in repo.get_contributors():
        commits = repo.get_commits(author=contributor.login)
        
        line_changes = sum(commit.stats.total for commit in commits)
        file_changes = len({file.filename for commit in commits for file in commit.files})

        merged_pr_counts = getMergedPRCountForUser(contributor.login)

        contributors_data[contributor.login] = {
            "line_contributed": line_changes,
            "file_contributed": file_changes,
            "pr_merged": merged_pr_counts
        }
    
    return contributors_data
      
# Fetching merged pull requests and count 
def getMergedPRCountForUser(username):
    merged_pr_count = 0

    for pull in repo.get_pulls(state="all"):  
        if pull.merged and pull.merged_by is not None and pull.merged_by.login == username:
            merged_pr_count += 1

    return merged_pr_count

# Fetching no. of pull requests 
def getPRCreatedByUser():
    pr_counts = {}
    for pull in repo.get_pulls(state="all"):  
        user = pull.user.login
        pr_counts.setdefault(user, 0)
        pr_counts[user] += 1

    return pr_counts

# Fetching pull reviews and count reviews by user
def getPRReviewsByUser():
    pr_reviews = {}
    for pull in repo.get_pulls(state="all"): 
        for review in pull.get_reviews():
            reviewer = review.user.login
            pr_reviews.setdefault(reviewer, 0)
            pr_reviews[reviewer] += 1
    
    return pr_reviews

# display line change and file change
@app.route("/getContributionByUser")
def user():
    contributors_data = getContributionByUser()
    user_data = [{"author": author, "count": count} for author, count in contributors_data.items()]
    return jsonify(user_data)

#display pull requests
@app.route("/getPRCreatedByUser")
def get_pull_request():
    pr_counts = getPRCreatedByUser()
    pull_request_data = [{"author": author, "count": count} for author, count in pr_counts.items()]
    return jsonify(pull_request_data)

#display pull reviews
@app.route("/getPRReviewedByUser")
def get_prs_reviewed():
    pr_reviews = getPRReviewsByUser()
    pr_review_data = [{"author": author, "count": count} for author, count in pr_reviews.items()]
    return jsonify(pr_review_data)

g.close()

if __name__ == '__main__':
    app.run(debug=True)
