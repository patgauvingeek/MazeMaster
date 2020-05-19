FROM gorialis/discord.py

RUN pip install --upgrade pip
RUN pip install setuptools
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY maze_master /app/maze_master
#COPY tests /app/tests
COPY README.md /app/
COPY setup.py /app/
COPY auth.json /app/

RUN ls -l

#RUN python setup.py test

ENTRYPOINT [ "python" ]
CMD [ "maze_master/bot.py" ]