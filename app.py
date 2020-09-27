import flask
from github import Github
from flask import Flask, request, render_template, jsonify, send_file
from jinja2 import Template
import requests
import pandas as pd
import datetime
from datetime import timedelta
import dateutil.parser
import json

# or using an access token
g = Github("93e27cd53dd1f8f4ba1ce9b120dfa62f8892fa3b")
mytoken = "93e27cd53dd1f8f4ba1ce9b120dfa62f8892fa3b"

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/public_repo_download', methods=['GET'])
def public_repo_download():
    txtfile = 'githubanalysis.txt'
    print("Saved commits information to commits_info.csv")
    return send_file(txtfile, as_attachment=True, cache_timeout=0)


@app.route('/my_repo_download', methods=['GET'])
def my_repo_download():
    txtfile = 'githubanalysis.txt'
    print("Saved commits information to commits_info.csv")
    return send_file(txtfile, as_attachment=True, cache_timeout=0)

@app.route('/')
def getmetric():
    return render_template('metric.html')

@app.route('/public_metric')
def public_metric():
    return render_template('public_metric.html')

@app.route('/get_pull_info')
def getpullinfo():
    query_url = "https://api.github.com/repos/projetcongo/demoapp/"
    headers = {'Authorization': 'token ' + mytoken,
               'Accept': 'application/vnd.github.v3+json'}
    pulldata = requests.get(query_url+"pulls?state=all", headers=headers, data={})
    comitdata = requests.get(query_url+"commits", headers=headers, data={})
    issue_data = requests.get(query_url+"issues", headers=headers, data={})
    issue_close = requests.get(query_url+"pulls?state=close", headers=headers, data={})
    data = issue_close.json()

    df = pd.DataFrame(data)
    # print(df)
    df['closed_at'] = df['closed_at'].map(dateutil.parser.parse)
    df['created_at'] = df['created_at'].map(dateutil.parser.parse)
    df['tdiff'] = df['closed_at'] - df['created_at']
    # print(df)
    use_cols = ['created_at', 'closed_at', 'tdiff']
    mean = str(df['tdiff'].mean())
    with open('githubanalysis.txt', 'w') as outfile:
        outfile.write('@ Repo details: \n')

        outfile.write('Date ranges from start date to close date for each pull request' )
        outfile.write('\n' )
        outfile.write('\n' )

        df.to_string(outfile, columns=use_cols, col_space=10)

        outfile.write('\n' )
        outfile.write('\n' )
        outfile.write('@ Average time being active between open and close states: '  + mean)

        outfile.write('\n')
        outfile.write('\n')
        outfile.write('\n')
        outfile.write('\n')
        outfile.write('No of User pull request close: '+ str(len(data)))

        outfile.write('\n')
        outfile.write('\n')
        outfile.write('\n')
        outfile.write('No of Users: '+ str(len(pulldata.json())))






    # mydictionary.append(comitdata)
    data = []
    data.append({"pull_data": pulldata.json()})
    data.append({"comit_data": comitdata.json()})
    data.append({"issue_data": issue_data.json()})
    data.append({"metric": [{"avg_time": mean}]})
    print(data)
    return json.dumps(data)

@app.route('/get_pull_info_public')
def get_pull_info_public():
    query_url = "https://api.github.com/repos/github/platform-samples/"
    headers = {'Authorization': 'token ' + mytoken,
               'Accept': 'application/vnd.github.v3+json'}
    pulldata = requests.get(query_url+"pulls?state=all", headers=headers, data={})
    comitdata = requests.get(query_url+"commits", headers=headers, data={})
    issue_data = requests.get(query_url+"issues", headers=headers, data={})
    issue_close = requests.get(query_url+"pulls?state=close", headers=headers, data={})
    data = issue_close.json()

    df = pd.DataFrame(data)
    # print(df)
    df['closed_at'] = df['closed_at'].map(dateutil.parser.parse)
    df['created_at'] = df['created_at'].map(dateutil.parser.parse)
    df['tdiff'] = df['closed_at'] - df['created_at']
    # print(df)
    use_cols = ['created_at', 'closed_at', 'tdiff']
    mean = str(df['tdiff'].mean())
    with open('publicgithubanalysis.txt', 'w') as outfile:
        outfile.write('@ Repo details: \n')

        outfile.write('Date ranges from start date to close date for each pull request' )
        outfile.write('\n' )
        outfile.write('\n' )

        df.to_string(outfile, columns=use_cols, col_space=10)

        outfile.write('\n' )
        outfile.write('\n' )
        outfile.write('@ Average time being active between open and close states: '  + mean)

        outfile.write('\n')
        outfile.write('\n')
        outfile.write('\n')
        outfile.write('\n')
        outfile.write('No of User pull request close: '+ str(len(data)))

        outfile.write('\n')
        outfile.write('\n')
        outfile.write('\n')
        outfile.write('No of Users: '+ str(len(pulldata.json())))

    # mydictionary.append(comitdata)
    data = []
    data.append({"pull_data": pulldata.json()})
    data.append({"comit_data": comitdata.json()})
    data.append({"issue_data": issue_data.json()})
    data.append({"metric": [{"avg_time": mean}]})
    print(data)
    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True)