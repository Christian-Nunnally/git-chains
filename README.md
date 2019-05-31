# git-chains
A git tool that guides you through maintaining chains of branches so that you can easily create small PR's while continuing to develop features

## Features
* Visualize git history as a tree instead of a DAG
* Teaches how to leverage git to write better software 
* Keep PRs small and focused by chaining branches together

## Workflow
Git Chains is a tool to help use a git branch chain workflow. The git branch chain workflow involves seperating unrelated changes into seperate branches to make code reviews small, and thereby both higher quality and faster. The most common case when you would want to seperate an already small feature into multiple branches is when some refactoring has to or should be done before implementing the feature. This common workflow is described as so:

1. Start feature work on branch `feature`.
2. Realize some refactoring should be done
3. Create `refactor` branch and commit refactor
4. Merge `refactor` into `feature`
5. Post PR for `refactor`
6. Continue working on `feature`
...
7. Get feedback on `refactor`
8. Commit feedback to `refactor`
9. Merge `refactor` in to `feature`

## Installation
1. Download the `dist` folder from this repo
2. Put it somewhere on your computer and add it to your path
3. Done! Try running `git chains` from your repository
