FROM SPARTEN-OP/ULTRONBOT:latest

RUN git clone https://github.com/SPARTENX-OP/ULTRONBOT.git /root/UltronBot

WORKDIR /root/UltronBot

RUN pip3 install -U -r requirements.txt

ENV PATH="/home/UltronBot/bin:$PATH"

CMD ["python3", "-m", "UltronBot"]
