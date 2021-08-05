# Add a Group to a Multiple Bitbucket Repositories #

A script to bulk-add a group to Bitbucket repositories.

### What is this repository for? ###

This script, running inside a Docker container, will add a group to multiple Bitbucket repositories at once. 

### Run the Script ###

To run the script, simply run the following commands, with 'x' being incremental versions:

    docker build -t update-groups:1.x .
    docker run update-groups:1.x

You will need to create a 'vars.json' file in the root directory of the cloned repository, formatted as follows:

    {
        "username": "joe.bloggs",
        "password": "password",
        "workspace_id": "my-workspace",
        "repo_slug": "my-repository",
        "group_owner": "group-owner",
        "group_slug": "my-group",
        "privilege": "write"
    }

* **Username:** This is your personal Bitbucket username.
* **Password:** You will need to generate an [app password](https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/#:~:text=each%20app%20password.-,Create%20an%20app%20password,-To%20create%20an) for this. **
* **Workspace ID:** The name of the workspace.
* **Repo Slug:** The name of the repository the group needs to be added to. Leave blank for all repositories in the workspace.
* **Group Owner:** The owner of the group to be added. If left blank, will be set to Workspace ID.
* **Group Slug:** The name of the group you would like to add to the repositories.
* **Privilege:** The privilege to be given to the group; 'read', 'write', or 'admin'.

** When you generate an app password, you will need to ensure you select Read and Write (and Admin under Repositories only) under Account and Repositories.

The 'vars.json' file is excluded in the .gitignore. I changed to reading in a vars file as the input vars were inconvenient. Easier to re-run this way.

### Requirements ###

* Docker installed and configured on your machine.
* You need to be a Bitbucket admin.
