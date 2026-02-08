# Bot de Discord em Python

Um bot de Discord simples criado com Python usando a biblioteca `discord.py`.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Uma conta no Discord
- Um bot criado no Discord Developer Portal

## 🚀 Como Configurar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Criar um Bot no Discord

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application" e dê um nome ao seu bot
3. Vá para a aba "Bot" e clique em "Add Bot"
4. Copie o **Token** do bot (você precisará dele)
5. Na seção "Privileged Gateway Intents", habilite:
   - ✅ MESSAGE CONTENT INTENT (necessário para ler mensagens)
   - ✅ SERVER MEMBERS INTENT (opcional, mas útil)

### 3. Configurar o Token

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   copy .env.example .env
   ```

2. Abra o arquivo `.env` e cole seu token:
   ```
   DISCORD_TOKEN=seu_token_aqui
   ```

### 4. Convidar o Bot para seu Servidor

1. No Discord Developer Portal, vá para "OAuth2" > "URL Generator"
2. Selecione os escopos:
   - ✅ `bot`
   - ✅ `applications.commands` (opcional, para comandos slash)
3. Selecione as permissões necessárias:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Manage Messages (para o comando clear)
4. Copie a URL gerada e abra no navegador
5. Selecione o servidor e autorize

## 🎮 Comandos Disponíveis

- `!ping` - Mostra a latência do bot
- `!hello` - O bot te cumprimenta
- `!info` - Mostra informações sobre o servidor
- `!clear [número]` - Deleta mensagens (padrão: 5, máximo: 100)

## ▶️ Como Executar

```bash
python bot.py
```

## 📝 Personalização

Você pode adicionar mais comandos editando o arquivo `bot.py`. Exemplos:

```python
@bot.command(name='meucomando')
async def meu_comando(ctx):
    await ctx.send('Resposta do comando!')
```

## 🔒 Segurança

⚠️ **NUNCA** compartilhe seu token do bot! Mantenha o arquivo `.env` privado e adicione-o ao `.gitignore` se for usar Git.

## 📚 Recursos Úteis

- [Documentação do discord.py](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Guia de Intents do Discord](https://discord.com/developers/docs/topics/gateway#gateway-intents)
