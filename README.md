# Monday.com Business Intelligence Agent

AI-powered chatbot that answers business questions by querying Monday.com boards in real-time.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` and add your credentials:

```python
MONDAY_API_TOKEN = "your_monday_api_token_here"
CLAUDE_API_KEY = "your_claude_api_key_here"
```

**How to get API keys:**
- **Monday.com**: Profile → Admin → API → Generate Token
- **Claude**: https://console.anthropic.com → API Keys

### 3. Test Monday.com Connection

```bash
python monday_api.py
```

Expected output:
```
Testing Monday.com API connection...
✅ Retrieved 5 deals
Sample deal: Naruto
✅ Retrieved 5 work orders
```

### 4. Test Agent

```bash
python agent.py
```

### 5. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
monday-agent/
├── config.py          # API keys and board IDs
├── monday_api.py      # Monday.com query functions
├── agent.py           # Claude agent with tool calling
├── app.py             # Streamlit UI (main app)
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Example Queries

- "How many deals do we have?"
- "What's our total revenue?"
- "Show me renewables deals"
- "What's our win rate?"
- "How are projects being executed?"
- "Show me top 5 deals by value"
- "What's the mining sector pipeline?"

## Features

✅ Real-time Monday.com queries (no cached data)
✅ Action logging (shows API calls and parameters)
✅ Handles messy data (missing values, inconsistent formats)
✅ Claude-powered query understanding
✅ Supports filtering by sector, status, etc.
✅ Cross-board queries (Deals + Work Orders)

## Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect your repo
4. Add secrets in Streamlit settings:
   - `MONDAY_API_TOKEN`
   - `CLAUDE_API_KEY`
   - `DEALS_BOARD_ID`
   - `WORK_ORDERS_BOARD_ID`
5. Deploy!

### Replit

1. Create new Repl
2. Upload all files
3. Add secrets in "Secrets" tab
4. Click "Run"
5. Share public URL

## Troubleshooting

**Error: "Authentication failed"**
- Check your Monday.com API token in `config.py`
- Regenerate token if needed

**Error: "Module not found"**
- Run `pip install -r requirements.txt`

**Empty results from Monday.com**
- Verify your board IDs are correct
- Check that data was imported properly
- Run `python monday_api.py` to test connection

## Support

For issues or questions, check:
- Monday.com API docs: https://developer.monday.com/api-reference
- Claude API docs: https://docs.anthropic.com/
