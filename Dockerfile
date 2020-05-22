FROM gorialis/discord.py

RUN pip install --upgrade pip
COPY src/ /app/
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "maze_master/bot.py" ]