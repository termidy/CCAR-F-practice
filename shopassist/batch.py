import time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

MODEL = "claude-sonnet-5-5"

# the work: one short support message per ID (the last one is empty on purpose)
MESSAGES = {
    "conv-0411": "Where is my order ORD-12345678?",
    "conv-0412": "Can I return the lamp from ORD-87654321?",
    "conv-0413": "",
    "conv-0414": "Do you ship to Canada?",
}


def request(custom_id, text):
    return {
        "custom_id": custom_id,
        "params": {
            "model": MODEL,
            "max_tokens": 200,
            "messages": [{"role": "user", "content": text}],
        },
    }


def run_batch(messages):
    batch = client.messages.batches.create(
        requests=[request(cid, text) for cid, text in messages.items()])
    print("batch", batch.id, batch.processing_status)
    while batch.processing_status != "ended":
        time.sleep(30)
        batch = client.messages.batches.retrieve(batch.id)
        print("status:", batch.processing_status, batch.request_counts)
    # results come back in any order: match them by custom_id, never by position
    return {r.custom_id: r.result for r in client.messages.batches.results(batch.id)}


results = run_batch(MESSAGES)
failed = {}
for custom_id, result in results.items():
    if result.type == "succeeded":
        print(custom_id, "ok:", result.message.content[0].text[:60])
    else:
        print(custom_id, result.type)
        failed[custom_id] = MESSAGES[custom_id]

# retry only what failed (the empty message fails again: fix the input, not the retry)
if failed:
    print("retrying", list(failed))
    for custom_id, result in run_batch(failed).items():
        print(custom_id, result.type)
