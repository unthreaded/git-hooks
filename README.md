# git-hooks
[![](https://github.com/unthreaded/git-hooks/workflows/Git%20hooks%20Pipeline/badge.svg)](https://github.com/unthreaded/git-hooks/actions?workflow=Git+hooks+Pipeline)
&nbsp;&nbsp;[![codecov](https://codecov.io/gh/unthreaded/git-hooks/branch/master/graph/badge.svg)](https://codecov.io/gh/unthreaded/git-hooks)

## What is git-hooks?
Git hooks is a commit hook that works with git to make sure your issue, ticket, Jira, and story numbers make it to the commit message.

For example:
```shell script
git checkout -b feature/GH-123-example-branch
...
# stage some work
...
git commit -m "Completed work and unit tests"
...
git log -n 1 --format=oneline
afb126992c7e780939ef9b931f38c2cb0c47f91f (HEAD -> feature/GH-123-example-branch) GH-123: Completed work and unit tests
```
Notice that the issue number, GH-123, was copied into the commit message.

Our hook can even handle the lack of a ticket:
```shell script
git checkout -b need-this-yesterday
...
git commit -m "PROD FIX"
...
git log -n 1 --format=oneline
75d23ddd3a9bd613dde8bbe447fb6a45c7af0a3b (HEAD -> need-this-yesterday) NOGH: PROD FIX
```
## How do I install?
Visit our [releases](https://github.com/unthreaded/git-hooks/releases) to download the most recent binary.

Setup a central git hooks directory:
 * Windows users can use: `C:\Users\<you>\.githooks\ `
```shell script
cd ~
mkdir .githooks
git config --global core.hooksPath ~/.githooks
```

In the zip you downloaded from [releases](https://github.com/unthreaded/git-hooks/releases), you will find 3 folders:
 - Linux
 - Mac
 - Windows
 
Copy all files from the zip directory of your respective OS to: `~/.githooks`

On Linux & Mac, make the hooks executable:
```shell script
chmod +x ~/.githooks/*
```

Lastly, edit this config file to your liking:

    ~/.githooks/commit-msg-config.yml
    
## If you run into issues
* #### The hook is not being triggered
    * Check your [core.hooksPath](https://git-scm.com/docs/githooks) - this setting can be `--global` or by repository. Check this first.
* #### The hook is having a runtime error
    * Please submit an issue [here](https://github.com/unthreaded/git-hooks/issues) with as much detail as possible.
 