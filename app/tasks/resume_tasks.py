# from crewai import Task


# def create_resume_write_task(agent, resume, job_description, context_tasks):
#     return Task(
#         description=f"""
#         You have been given:

#         === CANDIDATE RESUME ===
#         {resume}

#         === JOB DESCRIPTION ===
#         {job_description}

#         Follow these steps:

#         STEP 1 — AUDIT
#         - Flag weak, vague language: "responsible for", "helped with", "worked on"
#         - Flag every bullet with zero quantification
#         - Identify irrelevant content to cut

#         STEP 2 — JD ANALYSIS
#         - Extract top 7 ATS keywords from the job description
#         - Identify which are missing from the current resume
#         - Understand what the hiring manager actually prioritizes

#         STEP 3 — REWRITE CONTENT
#         - Rewrite every bullet: [Action Verb] + [What You Did] + [Measurable Result]
#         - Inject ATS keywords naturally — not stuffed
#         - Write a laser-targeted summary for this specific role
#         - Cut everything irrelevant to this job

#         STEP 4 — FORMAT AS LaTeX
#         - Use moderncv class (style: classic, color: blue)
#         - Escape ALL special characters: & % $ # _ {{ }} ~ ^ \\
#         - Structure: Summary, Experience, Skills, Education
#         - Output ONLY raw LaTeX. Nothing before \\documentclass, nothing after \\end{{document}}
#         - Do NOT wrap in markdown or backticks
#         - Do NOT fabricate anything not in the original resume

#         REQUIRED OPENING:
#         \\documentclass[11pt,a4paper,sans]{{moderncv}}
#         \\moderncvstyle{{classic}}
#         \\moderncvcolor{{blue}}
#         \\usepackage[scale=0.75]{{geometry}}
#         """,
#         expected_output=(
#             "Raw LaTeX only. Starts with \\documentclass, ends with \\end{document}. "
#             "No markdown, no explanation, no backticks."
#         ),
#         agent=agent,
#         context=context_tasks  # receives output from extraction + match tasks
#     )


# def create_latex_compile_task(agent, resume_write_task):
#     return Task(
#         description="""
#         Take the LaTeX content from the previous task and compile it to PDF.

#         Steps:
#         1. Pass the full LaTeX string to the LaTeX Compiler Tool
#         2. If SUCCESS — done. Report the PDF path.
#         3. If COMPILATION FAILED:
#            - Read the error log carefully
#            - Fix ONLY the specific broken line or character
#            - Do not rewrite the full document
#            - Run the compiler again
#         4. Retry up to 3 times. After 3 failures, report the final error log.


#         ABSOLUTE OUTPUT RULES — VIOLATION WILL CAUSE COMPILATION FAILURE:
#         - Your entire response must be ONLY the LaTeX document
#         - First character of your response: backslash of \\documentclass
#         - Last character of your response: closing brace of \\end{{document}}
#         - ZERO text before \\documentclass — no intro, no explanation, no "Here is..."
#         - ZERO text after \\end{{document}} — no summary, no notes, nothing
#         - NEVER use \\iffalse or \\fi anywhere
#         - NEVER use % comment lines that contain special characters
#         - ALL special characters in text MUST be escaped: & → \\&, % → \\%, $ → \\$
#           # → \\#, _ → \\_
#         - URLs must be inside \\href{{}}{{}} — never raw in text
#         """,
#         expected_output="SUCCESS message with the absolute path to the compiled PDF.",
#         agent=agent,
#         context=[resume_write_task]
#     )
from crewai import Task


LATEX_TEMPLATE = r"""
\documentclass[a4paper,10pt]{article}
\usepackage{geometry}
\geometry{margin=0.37in}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage[colorlinks=true, urlcolor=blue]{hyperref}

\setlist[itemize]{noitemsep, topsep=0pt}
\renewcommand{\baselinestretch}{1.0}
\titlespacing*{\section}{0pt}{4pt}{2pt}
\titlespacing*{\subsection}{0pt}{3pt}{1pt}

\begin{document}

\begin{center}
    {\LARGE \textbf{<<FULL_NAME>>}}\\
    \href{mailto:<<EMAIL>>}{<<EMAIL>>} \textbar
    \href{<<LINKEDIN_URL>>}{LinkedIn} \textbar
    \href{<<GITHUB_URL>>}{GitHub} \textbar
    \href{tel:<<PHONE>>}{<<PHONE>>}
\end{center}

\hrule
\vspace{3pt}
\section*{Summary}
<<SUMMARY>>

\vspace{3pt}
\hrule
\vspace{3pt}

\section*{Education}
<<EDUCATION>>

\vspace{3pt}
\hrule
\vspace{3pt}

\section*{Technical Skills}
<<TECHNICAL_SKILLS>>

\vspace{3pt}
\hrule
\vspace{3pt}

\section*{Work Experience}
<<WORK_EXPERIENCE>>

\vspace{3pt}
\hrule
\vspace{3pt}

\section*{Projects}
<<PROJECTS>>

\vspace{3pt}
\hrule
\vspace{3pt}

\section*{Achievements \& Certifications}
\begin{itemize}
<<ACHIEVEMENTS>>
\end{itemize}

\hrule
\vspace{3pt}

\section*{Extracurricular Activities}
\begin{itemize}
<<EXTRACURRICULAR>>
\end{itemize}

\end{document}
"""


def create_resume_write_task(agent, resume, job_description, context_tasks):
    return Task(
        description=f"""
You are given a candidate resume and a job description.
Your job is to rewrite the resume content, tailored to the job description,
and output it using EXACTLY the LaTeX template provided below.

=== CANDIDATE RESUME ===
{resume}

=== JOB DESCRIPTION ===
{job_description}

=== YOUR LATEX TEMPLATE ===
{LATEX_TEMPLATE}

=== CONTENT REWRITING RULES ===

SUMMARY:
- Rewrite to target this specific job
- Highlight the most relevant skills and experience for this role
- Keep it 3-4 lines max
- Use \\textbf{{}} for key terms

TECHNICAL SKILLS:
- Keep the exact same format: \\textbf{{Category}}: skill1, skill2 \\textbar \\space
- Reorder categories to put most relevant ones first for this job
- Add any skills from the resume that are missing but relevant to the JD
- Remove skills completely irrelevant to this role

WORK EXPERIENCE — For each role keep this exact format:
\\textbf{{Company - Role}} \\hfill Start -- End\\\\
\\textbf{{Key Skills: skill1, skill2}}
\\begin{{itemize}}
    \\item [rewritten bullet]
\\end{{itemize}}

Bullet rewriting rules:
- Every bullet: [Strong Action Verb] + [What You Did] + [Measurable Result]
- Remove vague language: "worked on", "helped with", "responsible for"
- Every bullet must have a number or metric — if original has one keep it, improve framing
- Bold the most important phrases using \\textbf{{}}
- Inject JD keywords naturally into bullets where truthful

PROJECTS:
- Keep this exact format:
  \\textbf{{Project Name}} \\hfill \\href{{URL}}{{link}} \\textbar \\href{{github}}{{GitHub}}\\\\
  \\textbf{{Technologies: ...}}
  \\begin{{itemize}} ... \\end{{itemize}}
- Reorder projects to put most relevant to this JD first
- Rewrite bullets same as work experience rules

ACHIEVEMENTS: Keep \\item \\textbf{{...}} format, only include relevant ones

=== PLACEHOLDER REPLACEMENT RULES ===
Replace every <<PLACEHOLDER>> with actual content from the resume:
- <<FULL_NAME>> → candidate's full name
- <<EMAIL>> → email address  
- <<LINKEDIN_URL>> → full LinkedIn URL
- <<GITHUB_URL>> → full GitHub URL
- <<PHONE>> → phone number with country code
- <<SUMMARY>> → your rewritten summary paragraph
- <<EDUCATION>> → education block (keep exact format from original)
- <<TECHNICAL_SKILLS>> → rewritten skills line
- <<WORK_EXPERIENCE>> → all experience blocks
- <<PROJECTS>> → all project blocks
- <<ACHIEVEMENTS>> → \\item lines only (no \\begin{{itemize}} wrapper, that's in template)
- <<EXTRACURRICULAR>> → \\item lines only

=== ABSOLUTE OUTPUT RULES ===
- Output ONLY raw LaTeX — first character must be \\ of \\documentclass
- Last character must be closing brace of \\end{{document}}
- ZERO text before \\documentclass — no intro, no explanation, no "Here is..."
- ZERO text after \\end{{document}}
- NEVER use \\iffalse or \\fi
- ALL special characters MUST be escaped: & → \\&, % → \\%, $ → \\$, # → \\#, _ → \\_
- URLs must always be inside \\href{{}}{{}} — never raw in text
- Do NOT fabricate any experience, numbers, or skills not in the original resume
        """,
        expected_output=(
            "Raw LaTeX only. Starts with \\documentclass[a4paper,10pt]{article}, "
            "ends with \\end{document}. Exact same document structure as the template. "
            "No markdown, no explanation, no backticks."
        ),
        agent=agent,
        context=context_tasks
    )


def create_latex_compile_task(agent, resume_write_task):
    return Task(
        description="""
        Take the LaTeX content from the previous task and compile it to PDF.

        Steps:
        1. Pass the full LaTeX string to the LaTeX Compiler Tool
        2. If SUCCESS — done. Report the PDF path.
        3. If COMPILATION FAILED:
           - Read the error log carefully
           - Identify the exact line causing the error
           - Fix ONLY that specific issue
           - Run the compiler again with fixed LaTeX
        4. Retry up to 3 times.
        5. After 3 failures report the final error and the last LaTeX version.
        """,
        expected_output="SUCCESS message with the absolute path to the compiled PDF.",
        agent=agent,
        context=[resume_write_task]
    )