import os
import re
import json
import requests
from crewai.tools import tool


def sanitize_latex(content: str) -> str:
    """Remove common LLM artifacts that break LaTeX compilation."""
    content = content.strip()

    # Strip markdown code fences
    if content.startswith("```"):
        content = "\n".join(content.split("\n")[1:])
    if content.endswith("```"):
        content = content.rsplit("```", 1)[0]

    content = content.strip()

    # Remove anything before \documentclass (LLM preamble text)
    doc_match = re.search(r'\\documentclass', content)
    if doc_match:
        content = content[doc_match.start():]

    # Remove anything after \end{document}
    end_match = re.search(r'\\end\{document\}', content)
    if end_match:
        content = content[:end_match.end()]

    # Remove \iffalse...\fi blocks (LLMs use these as "comments")
    content = re.sub(r'\\iffalse.*?\\fi', '', content, flags=re.DOTALL)

    return content.strip()


@tool("LaTeX Compiler Tool")
def compile_latex_to_pdf(latex_content: str) -> str:
    """
    Compiles LaTeX content to PDF using latex.ytotech.com.
    Sanitizes LLM output before sending. Returns success path or error log.
    """
    output_dir = os.path.abspath("data/output")
    os.makedirs(output_dir, exist_ok=True)

    tex_path = os.path.join(output_dir, "resume-new.tex")
    pdf_path = os.path.join(output_dir, "resume-new.pdf")

    latex_content = sanitize_latex(latex_content)

    # Save sanitized .tex locally
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_content)

    # Log line 35 area for debugging
    lines = latex_content.split("\n")
    print("\n--- LaTeX lines 30-40 (debug) ---")
    for i, line in enumerate(lines[29:40], start=30):
        print(f"{i}: {line}")
    print("-----------------------------------\n")

    try:
        payload = {
            "compiler": "pdflatex",
            "resources": [
                {
                    "main": True,
                    "content": latex_content
                }
            ]
        }

        response = requests.post(
            "https://latex.ytotech.com/builds/sync",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=90
        )

        if response.status_code == 201 and "application/pdf" in response.headers.get("Content-Type", ""):
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            
            # Auto-open PDF on Mac
            import subprocess
            subprocess.Popen(["open", pdf_path])  # Mac
            # subprocess.Popen(["xdg-open", pdf_path])  # Linux — uncomment if needed
    
        print(f"\n✅ PDF saved at: {os.path.abspath(pdf_path)}\n")
        return f"SUCCESS: PDF generated at {os.path.abspath(pdf_path)}"

        try:
            error_detail = response.json()
            error_text = json.dumps(error_detail, indent=2)[-3000:]
        except Exception:
            error_text = response.text[-3000:]

        return (
            f"COMPILATION FAILED (HTTP {response.status_code}). "
            f"Fix the LaTeX errors and retry:\n\n{error_text}"
        )

    except requests.Timeout:
        return "COMPILATION FAILED: Timeout after 90s. Retry."
    except requests.RequestException as e:
        return f"COMPILATION FAILED: Network error — {str(e)}"