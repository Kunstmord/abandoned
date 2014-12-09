"""
Github API-related string parsing, extracting of author names, etc
"""
import re


def get_project_name(url: str) -> str:
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
        url = re.sub(r'[a-zA-Z0-9\-_]+/', '', url)

    if '/' in url:
        return ''  # error case! (this is is some weird sub-project page) TODO - just strip the sub-project trail url
    return url