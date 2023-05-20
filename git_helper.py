import sys
import os
import git

def gitclone(custom_nodes_path, url):
    repo_name = os.path.splitext(os.path.basename(url))[0]
    repo_path = os.path.join(custom_nodes_path, repo_name)

    # Clone the repository from the remote URL
    repo = git.Repo.clone_from(url, repo_path)
    repo.git.clear_cache()
    repo.close()

def gitcheck(path):
    # Fetch the latest commits from the remote repository
    repo = git.Repo(path)
    remote_name = 'origin'
    remote = repo.remote(name=remote_name)
    remote.fetch()

    # Get the current commit hash and the commit hash of the remote branch
    commit_hash = repo.head.commit.hexsha
    remote_commit_hash = repo.refs[f'{remote_name}/HEAD'].object.hexsha

    # Compare the commit hashes to determine if the local repository is behind the remote repository
    if commit_hash != remote_commit_hash:
        print("CUSTOM NODE CHECK: True")
    else:
        print("CUSTOM NODE CHECK: False")

def gitpull(path):
    # Check if the path is a git repository
    if not os.path.exists(os.path.join(path, '.git')):
        raise ValueError('Not a git repository')

    # Pull the latest changes from the remote repository
    repo = git.Repo(path)
    origin = repo.remote(name='origin')
    origin.pull()

    repo.close()

try:
    if sys.argv[1] == "--clone":
        gitclone(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "--check":
        gitcheck(sys.argv[2])
    elif sys.argv[1] == "--pull":
        gitpull(sys.argv[2])
    exit(0)
except:
    exit(-1)
    
    
