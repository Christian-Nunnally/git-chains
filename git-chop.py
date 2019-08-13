from pygit2 import *
import os

if os.path.exists("./.git"):
    local_repo_name = os.getcwd() + "\\.git"

repo = Repository(local_repo_name)

print()

branches_to_remove = []
for branch in repo.branches.local:
    if (branch == "master" or branch == "master-cached" or (len(branch) == 3 and branch[1:] == "SW")):
        continue
    answer = input("Delete branch " +  branch + " (Y/N)?")
    if (answer.lower() == 'y' or answer.lower() == 'yes'):
        branches_to_remove.append(branch)

print()
print("Warning! The following local branches will be deleted:")
for branch_to_remove in branches_to_remove:
    print("\t" + branch_to_remove)

print()
answer = input("Are you sure you want to delete those branches (Y/N)?")
if (answer.lower() == 'y' or answer.lower() == 'yes'):
    print("\n")
    for branch_to_remove in branches_to_remove:
        repo.references.delete('refs/heads/' + branch_to_remove)
        print(branch_to_remove + " has been deleted.")