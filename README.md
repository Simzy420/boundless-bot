# Frank — Elite AI Bot (Boundless AI + Telegram)

Powered by [Boundless AI](https://boundless.ai) inference API.

## Features

- **8 AI Models** — dsv4 (budget), qwen3.6, GLM-5.3 Flash/Pro, DeepSeek Flash/Pro, Mimo
- **Context7 Web Search** — `/ctx7 <query>`
- **Firecrawl Web Scraping** — `/scrape <url>`
- **X/Twitter Posting** — `/tweet <message>` (via [xurl](https://github.com/xdevplatform/xurl) CLI)
- **Stock & Market Data** — `/stock AAPL` (FMP + Finnhub)
- **GitHub Integration** — `/gh <endpoint>`
- **File Operations** — `/file read <path>`
- **Code Execution** — `/run python <code>`
- **Frank's Own Wallet** — EconomyOS/ACP agent wallet (separate from user wallet)
- **RTK Token Compression** — 60-90% smaller command outputs via [RTK](https://github.com/rtk-ai/rtk)
- **Headroom Proxy** — 20-60% token savings on API calls via [Headroom](https://github.com/headroomlabs-ai/headroom)

## Setup

1. **Clone and install:**
```bash
git clone https://github.com/Simzy420/boundless-bot.git
cd boundless-bot
pip install -r requirements.txt
```

2. **Configure API keys:**
```bash
cp .env.example .env
# Edit .env with your keys
```

3. **Optional: Install RTK for token compression:**
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/develop/install.sh | bash
```

4. **Optional: Install xurl for X/Twitter posting:**
```bash
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash
xurl auth oauth2 --app my-app  # One-time OAuth setup
```

5. **Run:**
```bash
python frank_bot_v9.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Show bot info + inline keyboard |
| `/help` | List all commands |
| `/ctx7 <query>` | Context7 web search |
| `/scrape <url>` | Scrape website with Firecrawl |
| `/tweet <msg>` | Post to X/Twitter |
| `/stock <symbol>` | Get stock quote |
| `/gh <endpoint>` | GitHub API call |
| `/file read <path>` | Read a file |
| `/run python <code>` | Execute Python code |
| `/web <query>` | Web search |
| `/wallet` | Show Frank's wallet |
| `/budget` | Switch to cheapest model (dsv4) |
| `/qwen` | Switch to Qwen model |
| `/pro` | Switch to DeepSeek Pro |
| `/reset` | Clear conversation |

## API Keys Needed

| Key | Where to Get It |
|-----|----------------|
| `BOUNDLESS_API_KEY` | https://boundless.ai |
| `BOT_TOKEN` | @BotFather on Telegram |
| `CONTEXT7_API_KEY` | Context7 dashboard |
| `FIRECRAWL_API_KEY` | https://firecrawl.dev |
| `GITHUB_TOKEN` | GitHub Settings → Developer settings |
| `FMP_KEY` | https://financialmodelingprep.com |
| `RUNPOD_API_KEY` | https://runpod.io |

## Token Compression

Frank uses two complementary tools to reduce API costs:

1. **RTK** — Compresses CLI command outputs (git, docker, kubectl) by 60-90%
2. **Headroom** — Compresses LLM API traffic by 20-60% (JSON, tool outputs, logs)

Both are optional but recommended for cost savings.

## Architecture

```
User → Telegram → Frank Bot → Boundless AI API
                           ├→ Context7 (web search)
                           ├→ Firecrawl (web scraping)
                           ├→ xurl (X/Twitter)
                           ├→ FMP (stock data)
                           ├→ GitHub API
                           └→ RTK + Headroom (token compression)
```

## License

MIT