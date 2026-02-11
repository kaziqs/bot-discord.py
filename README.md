# Bot de Discord em Python

Um bot de Discord simples criado com Python usando a biblioteca `discord.py`.
Bot para criação de lobbies de jogos, divisão de times, priorização de lanes (LoL) e modo draft com capitães.

## Pré-requisitos

- Python 3.8 ou superior
- Uma conta no Discord
- Um bot criado no Discord Developer Portal

## Como Configurar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Criar um Bot no Discord

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application" e dê um nome ao seu bot
3. Vá para a aba "Bot" e clique em "Add Bot"
4. Copie o **Token** do bot
5. Na seção "Privileged Gateway Intents", habilite:
   - ✅ MESSAGE CONTENT INTENT ( necessario para ler e mandar mensagens )
   - ✅ SERVER MEMBERS INTENT ( necessario para ler os membros )

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
2. Selecione as permissões:
   - ✅ `bot`
   - ✅ `applications.commands` 
3. Selecione as permissões necessárias:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Manage Messages 
   - ✅ View Voice Channel
4. Copie a URL gerada e abra no navegador
5. Selecione o servidor e autorize

## Comandos Disponíveis

- `!setlobby {custom/lol/cs/draft}` - Customização do lobby (!setlobby custom {quantidade de pessoas})
- `!lobby` - Iniciar o lobby
- `!lane {top/jg/mid/adc/sup}` - Priorização de lane.
- `!minhalane` - Irá mostrar sua prioridade de lane.  
- `!draft` – inicia draft com capitães aleatórios
- `!capitao @user1 @user2` – define capitães manualmente
- `!pick @user` – capitão escolhe jogador
- `!draftstatus` – mostra estado do draft
- `!draftcancel` – cancela draft ativo

## Como Executar

```bash
python bot/main.py
```