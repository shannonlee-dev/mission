git clone https://github.com/shannonlee-dev/ia-codyssey.git.



c4r4s4% git init
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint: 
hint: 	git config --global init.defaultBranch <name>
hint: 
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint: 
hint: 	git branch -m <name>
Initialized empty Git repository in /home/shannon.lee.dev/Desktop/tmp/.git/
c4r4s4% git remote add origin https://github.com/shannonlee-dev/ia-codyssey.git
c4r4s4% git branch
c4r4s4% git fetch
remote: Enumerating objects: 75, done.
remote: Counting objects: 100% (75/75), done.
remote: Compressing objects: 100% (58/58), done.
remote: Total 75 (delta 20), reused 50 (delta 7), pack-reused 0 (from 0)
Unpacking objects: 100% (75/75), 17.07 KiB | 460.00 KiB/s, done.
From https://github.com/shannonlee-dev/ia-codyssey
 * [new branch]      main       -> origin/main
c4r4s4% git branch
c4r4s4% git pull origin main
From https://github.com/shannonlee-dev/ia-codyssey
 * branch            main       -> FETCH_HEAD
c4r4s4% 
3

c4r4s4% git add .
c4r4s4% touch tmp
c4r4s4% ls
README.md  gh-vscode_terminal.md  problem_1  problem_2	problem_3  tmp	tools
c4r4s4% git add .
c4r4s4% git commit -m 'dsa'
[master a3a9233] dsa
 Committer: 이 상헌 <shannon.lee.dev@c4r4s4.codyssey.kr>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly. Run the
following command and follow the instructions in your editor to edit
your configuration file:

    git config --global --edit

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 tmp

c4r4s4% git branch
* master
c4r4s4% git config --global init.defaultBranch main

c4r4s4% git branch
* master
c4r4s4% git branch -m main
c4r4s4% ;s
zsh: command not found: s
c4r4s4% git branch
* main
c4r4s4% git push origin main

git config --global credential.helper store
