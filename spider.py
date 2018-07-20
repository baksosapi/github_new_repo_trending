# coding=utf-8
import requests
import datetime
import os
import codecs

def create_markdown_file(today, filename):
    with open(filename, 'w') as f:
        f.write(today+"\n")
        f.write('Tracking the most popular Github repos that are generated within: \n')
        url = 'https://github.com/polebug/github_trending_spider/blob/master/'+today+'.md'
        f.write("* [Week]({url}#week)\n".format(url=url))
        f.write("* [Month]({url}#month)\n".format(url=url))
        f.write("* [Quarterly]({url}#quarterly)\n".format(url=url))
        f.write("--- \n")

def git_push(today , filename):
    add = 'git add .'
    commit = 'git commit -m "{date}.md"'.format(date=today)
    push = 'git push -u origin master'

    os.system(add)
    os.system(commit)
    os.system(push)

def write_repo_lists(headers, filename, s):
    url = 'https://api.github.com/search/repositories?q={s}'.format(s=s)
    print url
    req = requests.get(url, headers = headers)
    results = req.json()
    with codecs.open(filename, "a", "utf-8") as f:
        tot = 0
        for repo in results['items']:
            name = repo['full_name']
            print name
            repo_url = repo['html_url']
            #description = ""
            description = repo['description']
            f.write(u"* [{name}]({url}): {description}\n".format(name=name, url=repo_url, description=description))
            tot = tot + 1
            if(tot>15): break

def github_spider(headers):
    today = datetime.date.today()
    week = today - datetime.timedelta(days=7)
    month = today - datetime.timedelta(days=30)
    quarterly = today - datetime.timedelta(days=92)
    search = [
        'created:>'+str(week)+'&sort=stars',
        'created:>'+str(week)+'&sort=forks',
        'created:>'+str(month)+'&sort=stars',
        'created:>'+str(month)+'&sort=forks',
        'created:>'+str(quarterly)+'&sort=stars',
        'created:>'+str(quarterly)+'&sort=forks'
    ]
    filename = '{date}.md'.format(date=today)

    #create markdown file
    create_markdown_file(str(today), filename)

    #write
    with codecs.open(filename, "a", "utf-8") as f:
        f.write('### Week \n')
        f.write('##### sorted by stars \n')
        write_repo_lists(headers, filename, search[0])
        f.write('##### sorted by forks \n')
        write_repo_lists(headers, filename, search[1])
        f.write('--- \n')

        f.write('### Month \n')
        f.write('##### sorted by stars \n')
        write_repo_lists(headers, filename, search[2])
        f.write('##### sorted by forks \n')
        write_repo_lists(headers, filename, search[3])
        f.write('--- \n')

        f.write('### Quarterly \n')
        f.write('##### sorted by stars \n')
        write_repo_lists(headers, filename, search[4])
        f.write('##### sorted by forks \n')
        write_repo_lists(headers, filename, search[5])
        f.flush()

    git_push(today, filename)

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Chrome/63.0',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    github_spider(headers)


