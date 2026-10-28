# CCAR-F practice: ShopAssist in code

Companion code for the practice lessons of the **Claude Certified Architect - Foundations (CCAR-F)** course. Each practice lesson is recorded in VS Code against the real Claude API, and this repository holds the project you see on screen, so you can run every step yourself.

| Folder | What it is |
| --- | --- |
| [`shopassist/`](shopassist/) | The practice project: one small Python script per lesson, all built on the same fictional support assistant, ShopAssist. Needs an Anthropic API key. |
| [`starting-points/`](starting-points/) | The "before" version of the files that a lesson edits on screen, so you can replay the edits yourself. |
| [`labs/`](labs/) | Jupyter notebooks to practise **without an API key**. |

## Setup

```bash
git clone https://github.com/termidy/CCAR-F-practice.git
cd CCAR-F-practice/shopassist
python3 -m venv .venv && source .venv/bin/activate      # Python 3.10+
pip install -r requirements.txt
cp .env.example .env                                    # put your key in .env, never in the code
```

`.env` holds one line, `ANTHROPIC_API_KEY=...`; every script loads it with `python-dotenv`. Some lessons also need [Claude Code](https://docs.claude.com/en/docs/claude-code) installed and logged in.

The scripts use the current API: `claude-sonnet-5-5`, `output_config={"effort": "low"}`, structured outputs through
`output_config.format`, and the `mcp` package 2.x for the MCP server. If something returns a 400, check the model id and the SDK
version first (`anthropic>=1.12`).

## The lessons

In the order of the course.

| Lesson | File(s) | What you run |
| --- | --- | --- |
| First request in code | `first_request.py` | `python first_request.py` - one `messages.create`, then `content`, `stop_reason` and `usage`; lower `max_tokens` to 20 and watch the reply get cut |
| The conversation lives in your code | `conversation.py` | `python conversation.py` - the `messages` list is the only memory |
| A chat UI talks to your script | `app.py`, `static/index.html` | `uvicorn app:app --port 8000`, open http://127.0.0.1:8000/ |
| System prompt rules vs code rules | `rules.py` (start: `starting-points/p04_rules.start.py`) | `python rules.py` - a prompt rule is a request, a code rule is a guarantee |
| Evaluate a prompt change on a test set | `evaluate.py` | `python evaluate.py` - two system prompts, same cases, scored by code and by a model grader |
| Your first tool call, end to end | `tool_call.py` | `python tool_call.py` - `tools=`, `stop_reason == "tool_use"`, run the function, send `tool_result` back |
| Schema-valid output from Claude | `extract.py` | `python extract.py` - `output_config.format` with a JSON schema |
| Validate, then retry with the error | `validate.py` (start: `starting-points/p08_validate.start.py`) | `python validate.py` - schema-valid is not business-valid; send the exact error back and retry, up to three attempts |
| BUILD: ShopAssist extracts return requests | `build_extract.py`, `emails/` | `python build_extract.py` - five emails in, `return_requests.json` out |
| The agentic loop in code | `agent_loop.py` | `python agent_loop.py` - loop while `stop_reason == "tool_use"` |
| Structured tool errors in code | `tool_errors.py` (start: `starting-points/p11_tool_errors.start.py`) | `python tool_errors.py` - tools return `isError`, `errorCategory`, `isRetryable`, `customerMessage`, `developerMessage` |
| BUILD: backend tools and an MCP server | `mcp_server.py` | `claude mcp add shopassist -- python mcp_server.py`, then `claude -p "..." --allowedTools "mcp__shopassist__lookup_order,mcp__shopassist__start_return"` |
| BUILD: ShopAssist becomes an agentic system | `agent.py` (start: `starting-points/p13_agent.start.py`) | `python agent.py` - a gate before the loop, a hook before every tool, escalation as a tool |
| Coordinator and subagents in code | `coordinator.py` | `python coordinator.py` - a coordinator calls two specialised agents as tools |
| Running a batch: `custom_id` and failures | `batch.py` | `python batch.py` - Message Batches API: send four requests, match results by `custom_id`, retry only the failed ones (a batch can take several minutes) |
| Claude Code hands-on: CLAUDE.md, rules and a skill | `CLAUDE.md`, `.claude/rules/tools.md`, `.claude/skills/order-check/SKILL.md` | `claude -p "Use the order-check skill for order ORD-87654321." --allowedTools "Skill,Bash(python *)"` |
| Claude Code in CI: `-p` and JSON output | `ci_review.sh`, `review_schema.json` | break a tool convention in `mcp_server.py`, then `sh ci_review.sh` |

The order IDs the tools know are `ORD-12345678` (a jacket, delivered 20 days ago) and `ORD-87654321` (a lamp, delivered 45 days ago).
Everything else returns `found: false`, which is data, not an error.

## The request trace

`shopassist/.trace/` is the small observer you see beside the editor in the videos. `sitecustomize.py` logs every HTTP exchange of
the Anthropic client to `trace.jsonl` when the folder is on `PYTHONPATH`; `trace.html` and `trace_mcp.html` draw it. It is optional
and the scripts never depend on it:

```bash
cd shopassist
export PYTHONPATH="$PWD/.trace"
(cd .trace && python3 -m http.server 8765 &)      # then open http://127.0.0.1:8765/trace.html
python first_request.py
```

## Labs

[`labs/`](labs/) holds hands-on Jupyter notebooks, a way to practise **without an API key**: a small simulator stands in for the SDK, and
the code you write is the code you would write against the real API. `labs/README.md` explains how to run them.

## License

The code is free to use for learning and in your own projects.
