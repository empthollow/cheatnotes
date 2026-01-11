## Setting up a repository

### Sets up the necessary Git files
Change to the project working directory initiate the repo or work in a repo 
```bash
git init
```
Creates a file called "README" in your Hello-World directory
```bash
touch README
```
### Settings and parameters
*user name and email are required*
Sets the default name for git to use when you commit
```bash
git config --global user.name "Your Name Here"
```
Sets the default email for git to use when you commit
```bash
git config --global user.email "your_email@youremail.com"
```
Set editor for edit commands
```bash
git config --global core.editor vim
```
Set git ssh key
```bash
git config --global core.sshCommand "ssh -i ~/.ssh/id_rsa"
```
Edit global config
```bash
git config --global --edit
```
Define the author email to be used for all commits by the current user
```bash
git config --global alias.<alias-name> <git-command>
```
Sets the user's name for this specific repo
```bash
git config [--global --local] user.name "Different Name"
```
Sets the user's email for this specific repo
```bash
git config user.email "differentemail@email.com"
```
Set git to use the credential memory cache
```bash
git config --global credential.helper cache
```
Set the cache to timeout after 1 hour (setting is in seconds)
```bash
git config --global credential.helper 'cache --timeout=3600'
```
View the current settings
```bash
git config --list
```
## Managing Files
The .gitignore file will prevent files from being synced
```bash
touch .gitignore
```
Remove skipped file from repository
```bash
git rm --cached FILENAME
```
View files in commit with recurse, name only prevents hash from display
```bash
git ls-tree --name-only -r BRANCH
```
Stages your README file, adding it to the list of files to be committed
```bash
git add README
```
Adds all files in the current directory to staged tracking status
```bash
git add .
```
Shows status of files
```bash
git status
```
Remove cached file, does not delete file
```bash
git rm --cached [filename]
```
Delete file from remote git
```bash
git rm [filename]
```
Commit added files
```bash
git commit -m "message"
```
Revert or create an inverse commit to the previous
```bash
git revert
```
Remove / destroy files from staging area
```bash
git reset
```

## SSH Key Management
Using git authenticated with SSH using key pair and an SSH URL
The remote URL needs to look like this when using ssh
```bash
git@github.com:USER/REPOSITORY.git
```
Test SSH key
*omit -i if config file contains settings for github.com*
```bash
ssh -i [key_filie] -T git@github.com
```
### If using ssh agent
Add SSH key to agent
```bash
ssh-agent
```
Redhat
```bash
exec ssh-agent bash
ssh-add
```
Also Redhat
```bash
eval "$(ssh-agent)" && ssh-add ~/.ssh/github
```

## Managing Branches
List local branches of repository
```bash
git branch
```
List all remote and local branches
```bash
git branch -a
```
Act on remote tracking branches
```bash
git branch -r
```
Remove branch
```bash
git branch -d <branch>
```
Change primary branch name
```bash
git branch -m NEW_NAME
```
Rename or create if new repository
```bash
git branch -M [branch name]
```
Create and switch to a new branch:
```bash
git checkout -b [branch]
git switch -c [branch]
```
Switch to an existing branch:
```bash
git checkout [branch]
git switch [branch]
```
Deleting a Branch
*The -d option ensures that the branch is only deleted if it has been fully merged with its upstream branch or the current branch.*
```bash
git branch -d feature-branch
```
Merging a branch
```bash
git checkout main
git merge feature-branch
```
### Dealing with conflicts
*incoming is from the perspective of the central repository*
*If there are conflicts during the merge, Git will notify you. You need to manually resolve these conflicts by editing the files, then stage the resolved files*

files will show conflicting code blocks like below, delete the markers and undesired code

-  `<<<<<<<` = outgoing
-  `>>>>>>>` = incoming
```bash
<<<<<<<<
*some code*
========
*some code*
>>>>>>>>
```
Brings down the latest commits from the remote without altering your working tree
```bash
git fetch origin
```
lists the changes in the remote that you don’t have locally 
```bash
git diff main..origin/main
```
show what you have that the remote lacks
```bash
git diff origin/main..main
```
#### Using Rebase Instead of Merge
*Rebasing is an alternative to merging that rewrites commit history to create a linear project history. This can make the history cleaner but should be used with caution, especially on shared branches.*

This command is used to fetch and rebase changes from a remote branch into your current branch
*Here's what happens step-by-step:*

- *Fetch: Git fetches the latest changes from the remote branch*
- *Rebase: Git rebases your current branch onto the fetched branch*
```bash
git pull --rebase origin <branch>
```
This may result in conflicts, if so resolve the conflicts and run this
```bash
git rebase --continue
```
This command rebases feature-branch onto main
```bash
git checkout [feature-branch]
git rebase [main]
```
After rebasing, you may need to force push the branch to the remote repository
*This should not be needed if conflicts are resolved*
```bash
git push --force
```
This command is used to rebase a set of commits onto a different base
```bash
git rebase <newbase> --onto <newbase> <branch>
```
This command would rebase the commits from topic-branch onto main, effectively moving the topic-branch commits to be based on main instead of feature-branch
```bash
git rebase feature-branch --onto main topic-branch
```
*Once resolved add and commit files as usual*

## Managing Remotes
Creates a remote (repository) named "origin" pointing at your GitHub repo
*New git repository must be created on github.com*
```bash
git remote add REPOSITORY_NAME git@github.com/username/REPOSITORY.git
```
View URL for current repository
```bash
git remote get-url REPOSITORY
```
Set URL for current repository to be used by push etc
```bash
git remote set-url origin new.git.url/here
```
View existing remotes with verbose
```bash
git remote -v
```
Change remote name from 'origin' to 'destination'
```bash
git remote rename origin destination
```
Verify remote's new name
```bash
git remote -v
```

## Managing History
Show commit history
```bash
git log
```
Show commits with graph
```bash
git log
```
Show commits from all branches
```bash
git log --all
```
Show stats about each commit
```bash
git log --stats
```
Show patch for each commit
```bash
git log -p
```
