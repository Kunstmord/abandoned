"""
Github API-related string parsing, extracting of author names, etc
"""
import re


def get_project_name(url: str) -> list:
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]

    if url.startswith('www.'):
        url = url[4:]

    if url.startswith('github.com/'):
        url = url[11:]
    else:
        return ''  # error case! (this is not Github!)

    if '/' not in url:
        return ''  # error case! (no author name)
    else:
        url += '/'

    results = url.split('/')

    if results is not None and len(results) > 1:
        return [results[0], results[1]]
    else:
        return []  # error case (malformed URL)

print(get_project_name('http://github.com/author/project/branch/master'))