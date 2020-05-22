# MazeMaster
A discord bot that make you run in a maze. Who will find the exit first ?

# DOCKER

Build: `docker build . --tag maze-master`
Run Production Tests: `docker run --rm maze-master setup.py tests`
Run Development Tests: `docker run --rm -v ~/Projects/MazeMaster/src:/src --workdir /src maze-master setup.py test`
Run Production: `docker run -d maze-master`
Run Development: `docker run --rm -it -v ~/Projects/MazeMaster/src:/src --workdir /src maze-master`
Debug File Syste: `docker run --rm -it --entrypoint /bin/bash maze-master`
