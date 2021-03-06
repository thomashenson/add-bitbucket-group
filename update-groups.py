#!/usr/bin/env python3

import requests
import json

class FixGroups:
    """
    Getting a list of repositories and adding a group to one or all.

    Attributes
    ----------
    user : str
        Your personal Bitbucket username
    password : str
        A Bitbucket app password generated by you
    workspace_id : str
        The name of the Bitbucket workspace
    repo_slug : str
        The name of the repository
    group_owner : str
        The owner of the group to be added
    group_slug : str
        The name of the group to be added
    privilege : str
        The privilege to be granted on the group;
            - read
            - write
            - admin

    Methods
    -------
    get_repos(self)
        Get a list of all repositories under the specified workspace
    update_groups(self)
        Attaches the specified group to the specified repo. If no repo is specified,
        the group will be added to all repos in the workspace
    """
    def __init__(self):
        try:
            file_name = "/app/vars.json"
            var_file = open(file_name)
            vars = json.load(var_file)

            self.user = vars["username"]
            self.password = vars["password"]
            self.workspace_id = vars["workspace_id"]
            self.repo_slug = vars["repo_slug"]
            self.group_owner = vars["group_owner"]
            self.group_slug = vars["group_slug"]
            self.privilege = vars["privilege"]

            if not self.group_owner:
                self.group_owner = vars["workspace_id"]

            var_file.close()
        except FileNotFoundError as err:
            print(f"File {file_name} not found.  Aborting")
            raise SystemExit(err)
        except OSError as err:
            print(f"OS error occurred trying to open {file_name}")
            raise SystemExit(err)
        except Exception as err:
            print(f"Unexpected error opening {file_name} is",repr(err))
            raise SystemExit(err)
        
    def get_repos(self):
        repo_slugs = []

        try:
            request_url = f'https://api.bitbucket.org/2.0/repositories/{self.workspace_id}'
            new_results = True
            page = 1
            while new_results:
                r = requests.get(request_url + f"?page={page}", auth=(self.user, self.password))
                output = r.json()

                if not output["values"]:
                    new_results = False
                    break

                for repo in output['values']:
                    repo_slugs.append(repo['name'])

                page += 1
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        return repo_slugs

    def update_groups(self):
        repos = self.get_repos()
        try:
            if not self.repo_slug:
                for repo in repos:
                    r = requests.put(f'https://api.bitbucket.org/1.0/group-privileges/{self.workspace_id}/{repo}/{self.group_owner}/{self.group_slug}', auth=(self.user, self.password), data=f"{self.privilege}")
                    content = r.content.decode('utf-8')
                    if "Your credentials lack one or more required privilege scopes." in content:
                        print(content)
                    else:
                        print(f'{self.group_slug} added to {repo}.')
            else:
                r = requests.put(f'https://api.bitbucket.org/1.0/group-privileges/{self.workspace_id}/{self.repo_slug}/{self.group_owner}/{self.group_slug}', auth=(self.user, self.password), data=f"{self.privilege}")
                content = r.content.decode('utf-8')
                if "Your credentials lack one or more required privilege scopes." in content:
                    print(content)
                elif "error" in content:
                    print(content)
                else:
                    print(f'{self.group_slug} added to {self.repo_slug}.')
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

def main():
    groups = FixGroups()
    groups.update_groups()

if __name__ == "__main__":
    main()
