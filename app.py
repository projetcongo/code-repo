import flask
from github import Github
from flask import Flask, request, render_template, jsonify
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


@app.route('/help', methods=['GET'])
def home():
    # query_url = "https://api.github.com/repos/github/platform-samples/pulls?state=close"
    query_url = "https://api.github.com/repos/projetcongo/demoapp/pulls?state=close"
    headers = {'Authorization': 'token ' + mytoken,
               'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(query_url, headers=headers, data={})
    # data = requests.get('https://api.github.com/users/' + credentials['username'], auth=authentication)
    data = r.json()
    print("length===>",len(data))

    df = pd.DataFrame(data)
    # print(df)
    df['closed_at'] = df['closed_at'].map(dateutil.parser.parse)
    df['created_at'] = df['created_at'].map(dateutil.parser.parse)
    df['tdiff'] = df['closed_at'] - df['created_at']
    # print(df)

    mean = str(df['tdiff'].mean())

    df.to_csv('commits_info.csv', index=False)
    use_cols = ['created_at','closed_at','tdiff']

    query_url = "https://api.github.com/repos/projetcongo/demoapp/issues"
    headers = {'Authorization': 'token ' + mytoken, 'Accept': 'application/vnd.github.v3+json'}
    issue_data = requests.get(query_url, headers=headers, data={})

    print("issues of organization ====>", issue_data.json())


    with open('filename.txt', 'w') as outfile:
        outfile.write('@ Repo details: \n')
        df.to_string(outfile, columns=use_cols, col_space=10)
        outfile.write('\n' )
        outfile.write('\n' )
        outfile.write('@ Average time being active between open and close states: '  + mean)


        # np.savetxt(filename, text)
        # outfile.write(text.encode())
        # outfile.write(("\n").encode())
    # df.to_csv('filename.txt', mode='w', columns=['created_at','closed_at','tdiff'], index=False)

    print("Saved commits information to commits_info.csv")
    return "success"

@app.route('/get_info')
def getinfo():
    return render_template('my-form.html')

@app.route('/')
def getmetric():
    return render_template('metric.html')

@app.route('/get_commit_info')
def getcommitinfo():
    query_url = "https://api.github.com/repos/projetcongo/demoapp/commits"
    headers = {'Authorization': 'token ' + mytoken,
               'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(query_url, headers=headers, data={})

    print(r.json())
    print(len(r.json()))
    return jsonify(r.json())

@app.route('/get_pull_info')
def getpullinfo():
    query_url = "https://api.github.com/repos/projetcongo/demoapp/pulls?state=all"
    headers = {'Authorization': 'token ' + mytoken,
               'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(query_url, headers=headers, data={})
    print(r.json())
    print(len(r.json()))
    return jsonify(r.json())

@app.route('/test', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    # https://api.github.com//orgs/:org/repos
    query_url = "https://api.github.com/orgs/projetcongo/repos"
    headers = {'Authorization': 'token ' + mytoken, 'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(query_url, headers=headers, data={})
    data1 = r.json()
    df = pd.DataFrame(data1)
    columns = ['id','Name', 'Full name','Is this Private', 'Projects', 'Created date']  # for a dynamically created table

    table_d = df.to_json(orient='index')
    # table_d = {"0":{"abc":20, "def":90}}
    print(data1)
    return render_template('display.html', columns=columns,
                           table_data=json.loads(table_d))
    # print("repositories of organization ====>", r.json())
    # return jsonify(r.json())

app.run()