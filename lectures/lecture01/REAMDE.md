- wait for me to make you a git repo
- git clone {class_code}
- git clone {your own repo}
- in class_code:
  - run bootstrap shell
- in your own repo
  - mkdir assignment1
  - cd assignment1
  - grade # if you have run the shell
  - git add .
  - git commit -a -m "I completed assignment 1"
  - git push origin main
- you can see your reports: https://unofficialtools.com/ci
- to update class lectures
  - cd class_code
  - git pull origin main

- bash commands:
  - cd
  - ls
  - less
  - rm
  - rm -rf {name}
  - echo "hello" > filename

- git commands:
  - git clone git@github.com:ucsc2025-cse183/class_code.git
  - git clone {your own repo}
  - git add .
  - git commit -a -m "... message ..."
  - git push origin main
  - (git pull origin main) only class_code
  - git log # shows history of snapshots
  - git show {commit} # shows what changed
  - git diff # shows what differs from last snapshot
  - (git checkout {commit}) # goes to that commit/snapshot
  



