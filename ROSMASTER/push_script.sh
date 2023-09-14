#!/bin/sh

# Change directory to your repository
cd /root/test/rosmaster-param

# Pull changes from the remote repository
git pull origin main

root@node1:~/data# cat push_script.sh
#!/bin/sh

# Set GitHub Personal Access Token
GITHUB_TOKEN="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"

# Set Git user email and name
git config --global user.email "tj-devstack@devstack.co.kr"
git config --global user.name "tj-devstack"

# Set GitHub token for authentication
git config --global credential.helper store
git config --global credential.helper "store --file=/root/test/.git-credentials"
echo "https://github.com:${GITHUB_TOKEN}@github.com" > /root/test/.git-credentials

# Navigate to the directory where Git repository is located
cd /root/test/rosmaster-param

# Perform Git push
git add .
git commit -m "Automated commit"
git push origin main
