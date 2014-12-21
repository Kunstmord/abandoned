"""
Github API-related string parsing, extracting of author names, etc
"""
import requests
from requests import exceptions


class AbandonedException(Exception):
    pass


class GithubException(Exception):
    pass


def get_project_data(url: str) -> list:
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]

    if url.startswith('www.'):
        url = url[4:]

    if url.startswith('github.com/'):
        url = url[11:]
    else:
        raise AbandonedException('The link you provided doesn''t seem to be a Github link')
        # error case! (this is not Github!)

    if '/' not in url:
        raise AbandonedException('The link you provided doesn''t seem to be correct')
        # error case! (no author)
    else:
        url += '/'

    results = url.split('/')

    if results is not None and len(results) > 1:
        try:
            get_result = requests.get('https://api.github.com/repos/' + results[0] + '/' + results[1])
        except requests.ConnectionError:
            raise GithubException('We couldn''t connect to Github')
        except requests.URLRequired:
            raise AbandonedException('The link you provided doesn''t seem to be correct')
        except exceptions.Timeout:
            raise GithubException('The request to Github timed out')
        else:
            if get_result.status_code != 200:
                raise AbandonedException('The link you provided doesn''t seem to be correct')
            else:
                json_results = get_result.json()
                return [json_results['name'], json_results['owner']['login'], json_results['language']]
    else:
        raise AbandonedException('The link you provided doesn''t seem to be correct')
        # something else is wrong with the link