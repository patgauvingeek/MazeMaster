FROM gorialis/discord.py

COPY auth.json /app/

RUN pip install --upgrade pip
COPY src/ /app/
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "maze_master/bot.py" ]