import git


def get_version() -> str:
    repo = git.Repo(search_parent_directories=True)
    # if there are any changes (staged, tracked or untracked) do not refer the SHA of last commit
    return (
        'UNCOMMITTED'
        if repo.index.diff(None) or repo.index.diff('HEAD') or repo.untracked_files
        else repo.head.object.hexsha
    )
