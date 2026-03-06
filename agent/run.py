import argparse, json, os, re, csv
from pathlib import Path
from jinja2 import Template
from dotenv import load_dotenv
import requests

load_dotenv(Path(__file__).parent / ".env")

SYSTEM = """You are a developer marketing assistant for API products.
Output must be practical, specific, and optimized for discoverability.
Avoid fluff. Prefer developer keywords and concrete examples.
"""

RAPIDAPI_TMPL = Template("""# {{ tool.name }}

## Title
{{ title }}

## Short description
{{ short }}

## Long description
{{ long }}

## Keywords / tags
{{ tags }}

## Example request
{{ ex_request }}

## Example response
{{ ex_response }}

## Pricing copy
{{ pricing }}
""")

APIFY_TMPL = Template("""# {{ tool.name }} (Apify / MCP)

## What it does
{{ what }}

## MCP tool name
{{ mcp_name }}

## Inputs
{{ inputs }}

## Outputs
{{ outputs }}

## Example prompt for an AI agent
{{ prompt }}

## Notes
{{ notes }}
""")

SEO_TMPL = Template("""# {{ tool.name }} -- {{ headline }}

## Summary
{{ summary }}

## Why developers use this
{{ use_cases }}

## API example
{{ api_example }}

## FAQs
{{ faqs }}

## Keywords
{{ keywords }}
""")

def llm_call(prompt: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ANTHROPIC_API_KEY environment variable.")
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 2000,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post(
        url,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json=payload,
        timeout=60
    )
    r.raise_for_status()
    return r.json()["content"][0]["text"].strip()

def sanitize(s: str) -> str:
    return re.sub(r"[^a-z0-9\-]+", "-", s.lower()).strip("-")

def ensure_dirs(out: Path):
    for p in ["rapidapi","apify","seo","reddit","sdk"]:
        (out / p).mkdir(parents=True, exist_ok=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf8"))
    out = Path(args.out)
    ensure_dirs(out)

    keywords_rows = []

    reddit_prompt = f"""Write two Reddit launch posts announcing a set of fintech developer APIs.
Audience 1: r/fintech (fintech builders).
Audience 2: r/webdev (general devs).
Tone: direct, no hype, ask for feedback.
Include bullet list of tools with one-liners.
Include a short section: Free tier / rate limits without promising exact numbers.
Brand: {data.get('brand')}.
Base URL: {data.get('base_url')}.
Tools: {json.dumps([{'name':t['name'],'one_liner':t['one_liner']} for t in data['tools']], indent=2)}
Output in Markdown with headings.
"""
    reddit_md = llm_call(reddit_prompt)
    (out/"reddit"/"launch_post.md").write_text(reddit_md, encoding="utf8")
    print("Reddit post generated.")

    for tool in data["tools"]:
        slug = tool["slug"]
        print(f"Processing: {slug}")

        prompt = f"""Generate marketplace-ready assets for this API tool.

Tool:
{json.dumps(tool, indent=2)}

Base URL: {data.get('base_url')}
Brand: {data.get('brand')}

Return ONLY a valid JSON object with these exact fields:
title, short, long, tags,
ex_request, ex_response,
pricing,
apify_what, mcp_name, apify_prompt, apify_notes,
seo_headline, seo_summary, seo_use_cases,
seo_api_example, seo_faqs, seo_keywords.

No markdown fences. No explanation. Pure JSON only.
"""
        raw = llm_call(prompt)

        try:
            clean = raw.strip()
            if clean.startswith("```"):
                clean = "\n".join(clean.split("\n")[1:])
            if clean.endswith("```"):
                clean = "\n".join(clean.split("\n")[:-1])
            obj = json.loads(clean.strip())
        except Exception:
            (out/"rapidapi"/f"{slug}_RAW.txt").write_text(raw, encoding="utf8")
            print(f"  JSON parse failed for {slug} - saved raw output")
            continue

        rapid_md = RAPIDAPI_TMPL.render(tool=tool, **obj)
        (out/"rapidapi"/f"{slug}.md").write_text(rapid_md, encoding="utf8")

        apify_md = APIFY_TMPL.render(
            tool=tool,
            what=obj.get("apify_what",""),
            mcp_name=obj.get("mcp_name", sanitize(tool["name"])),
            inputs=json.dumps(tool.get("inputs",[]), indent=2),
            outputs=json.dumps(tool.get("outputs",[]), indent=2),
            prompt=obj.get("apify_prompt",""),
            notes=obj.get("apify_notes","")
        )
        (out/"apify"/f"{slug}.md").write_text(apify_md, encoding="utf8")

        seo_md = SEO_TMPL.render(
            tool=tool,
            headline=obj.get("seo_headline",""),
            summary=obj.get("seo_summary",""),
            use_cases=obj.get("seo_use_cases",""),
            api_example=obj.get("seo_api_example",""),
            faqs=obj.get("seo_faqs",""),
            keywords=obj.get("seo_keywords","")
        )
        (out/"seo"/f"{slug}.md").write_text(seo_md, encoding="utf8")

        py_sdk = f"""import requests

BASE = "{data.get('base_url')}"
url = BASE + "{tool['path']}"

r = requests.request("{tool['method']}", url, timeout=30)
print(r.status_code)
print(r.json())
"""
        (out/"sdk"/f"python_{slug}.py").write_text(py_sdk, encoding="utf8")

        js_sdk = f"""const BASE = "{data.get('base_url')}";
let url = BASE + "{tool['path']}";

fetch(url, {{ method: "{tool['method']}" }})
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
"""
        (out/"sdk"/f"node_{slug}.js").write_text(js_sdk, encoding="utf8")

        kw = obj.get("seo_keywords","")
        keywords_rows.append([tool["name"], kw])
        print(f"  Done: {slug}")

    with (out/"keywords.csv").open("w", newline="", encoding="utf8") as f:
        w = csv.writer(f)
        w.writerow(["tool","keywords"])
        w.writerows(keywords_rows)

    print(f"All done. Outputs in: {out.resolve()}")

if __name__ == "__main__":
    main()





