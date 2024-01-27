# Interpret de λ-càlcul AChurch

Un intèrpret de lambda càlcul. Es pot utilitzar a traves de la terminal o mitjançant un bot de Telegram.

## Requeriments

Per utilitzar l'intèrpret es necessita:

- [Python 3](https://www.python.org/downloads/)
- [antl4](https://github.com/antlr/antlr4/blob/master/doc/python-target.md)

Pel bot de Telegram:

- python-telegram-bot
- pydot
- [graphviz](https://graphviz.org/download/)

### Linux:

```bash
pip install antlr4-tools
antlr4
pip install antlr4-python3-runtime
pip install python-telegram-bot
pip install pydot
sudo apt install graphviz
```

### Windows:
s'ha de fer alguna cosa més, seguiu la referència.
[antlr4-tools reference](https://github.com/antlr/antlr4-tools)
[Instalar graphviz](https://graphviz.org/download/)


## Ús
Intèrpret en terminal:

```bash
python3 achurch.py
```

Bot de Telegram:

crear un arxiu `token.txt` i posar el teu token ([Com obtenir el meu token?](https://core.telegram.org/bots#how-do-i-create-a-bot))

```bash
python3 telegramBoy.py
```

Un cop iniciat, ja pots enviar expressions lambda al teu bot de Telegram.
usa la comanda `/help` per veure les comandes disponibles