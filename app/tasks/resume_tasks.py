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
\documentclass[10pt,a4paper]{article}

\usepackage[a4paper, top=0.45in, bottom=0.45in, left=0.45in, right=0.45in]{geometry}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{fontawesome5}
\usepackage{paracol}
\usepackage{array}
\usepackage{tabularx}
\usepackage{tikz}
\usepackage{microtype}
\usepackage[T1]{fontenc}
\usepackage{lato}

%------------------------------------------------------------
% COLORS
%------------------------------------------------------------
\definecolor{msblue}{RGB}{31,78,121}
\definecolor{accentblue}{RGB}{41,105,163}
\definecolor{lightblue}{RGB}{210,228,242}
\definecolor{darktext}{RGB}{26,26,26}
\definecolor{midgray}{RGB}{90,90,90}
\definecolor{lightgray}{RGB}{245,246,248}
\definecolor{rulegray}{RGB}{200,210,220}
\definecolor{taggray}{RGB}{230,236,242}

\hypersetup{colorlinks=true, urlcolor=accentblue, linkcolor=accentblue}

%------------------------------------------------------------
% SPACING & LAYOUT
%------------------------------------------------------------
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\pagestyle{empty}
\renewcommand{\baselinestretch}{1.0}

%------------------------------------------------------------
% SECTION HEADERS
%------------------------------------------------------------
\titleformat{\section}
  {\color{darktext}\bfseries\fontsize{10.5}{12}\selectfont\uppercase}
  {}{0em}{}
  [\vspace{1pt}\textcolor{rulegray}{\hrule height 0.6pt}\vspace{3pt}]
\titlespacing*{\section}{0pt}{8pt}{4pt}

%------------------------------------------------------------
% CUSTOM COMMANDS
%------------------------------------------------------------

% Job entry header
\newcommand{\jobheader}[4]{%
  \vspace{4pt}%
  {\bfseries\fontsize{10}{11}\selectfont\color{darktext} #1}\hfill{}\\[-1pt]
  {\bfseries\fontsize{9.5}{11}\selectfont\color{accentblue} #2}\\[-1pt]
  {\fontsize{8.5}{10}\selectfont\color{midgray} \faCalendar[regular]\; #3 \quad \faMapMarker*\; #4}%
  \vspace{1pt}%
}

% Role description line
\newcommand{\roledesc}[1]{%
  {\fontsize{8.5}{10}\selectfont\color{midgray}\textit{#1}}\vspace{2pt}%
}

% Skill tag box
\newcommand{\skilltag}[1]{%
  \tikz[baseline]{\node[fill=taggray, rounded corners=2pt,
    inner xsep=4pt, inner ysep=2pt,
    font=\fontsize{8}{9}\selectfont\color{darktext}]{#1};}%
  \hspace{1pt}%
}

% Achievement entry with icon
\newcommand{\achievement}[3]{%
  \vspace{4pt}%
  {\color{#1}\fontsize{11}{12}\selectfont #2}\;{\bfseries\fontsize{9}{10}\selectfont\color{darktext} #3}%
  \vspace{2pt}%
}

% Dot rating (for languages)
\newcommand{\dotrating}[1]{%
  \foreach \i in {1,...,5}{%
    \ifnum\i>#1
      {\color{lightblue}\Large\textbullet}%
    \else
      {\color{accentblue}\Large\textbullet}%
    \fi
  }%
}

% Bullet list settings
\setlist[itemize]{
  noitemsep, topsep=2pt, partopsep=0pt,
  leftmargin=1.1em, label={\color{accentblue}\small\textbullet}
}

%------------------------------------------------------------
% DOCUMENT
%------------------------------------------------------------
\begin{document}

%------------------------------------------------------------
% HEADER
%------------------------------------------------------------
\begin{minipage}[t]{\textwidth}
  {\fontsize{26}{28}\selectfont\bfseries\color{darktext} <<FULL_NAME>>}\\[3pt]
  {\fontsize{12}{14}\selectfont\bfseries\color{accentblue} <<JOB_TITLE>>}\\[5pt]
  {\fontsize{8.8}{11}\selectfont\color{midgray}
    \faPhone\; <<PHONE>> \quad
    \faEnvelope\; \href{mailto:<<EMAIL>>}{<<EMAIL>>} \quad
    \faLinkedin\; \href{<<LINKEDIN_URL>>}{<<LINKEDIN_URL_TEXT>>} \quad
    \faMapMarker*\; <<LOCATION>>
  }
\end{minipage}

\vspace{6pt}
\textcolor{rulegray}{\hrule height 0.8pt}
\vspace{8pt}

%------------------------------------------------------------
% TWO COLUMN BODY
%------------------------------------------------------------
\setlength{\columnsep}{16pt}
\columnratio{0.62}
\begin{paracol}{2}

%============================================================
% LEFT COLUMN
%============================================================

%--- SUMMARY ---
\section{Summary}
{\fontsize{9}{11.5}\selectfont\color{darktext}
<<SUMMARY>>
}

\vspace{4pt}

%--- EXPERIENCE ---
\section{Experience}

<<EXPERIENCE>>

\vspace{4pt}

%--- EDUCATION ---
\section{Education}

<<EDUCATION>>

\vspace{4pt}

%============================================================
% RIGHT COLUMN
%============================================================

\switchcolumn
%--- PROJECTS ---
\section{Projects}

<<PROJECTS>>

%--- SKILLS ---
\section{Skills}

\vspace{4pt}

\begin{minipage}{\linewidth}
\raggedright
<<SKILLS>>
\end{minipage}

%--- KEY ACHIEVEMENTS ---
\section{Key Achievements}

<<ACHIEVEMENTS>>

\vspace{6pt}
\end{paracol}

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
- Bold key terms using \\textbf{{}}

EXPERIENCE:
- Use this exact format for each role:
\\jobheader{{Role Title}}{{Company Name}}{{Start -- End}}{{Location}}
\\begin{{itemize}}
  \\item [rewritten bullet]
\\end{{itemize}}
\\vspace{{2pt}}
- Every bullet: [Strong Action Verb] + [What You Did] + [Measurable Result]
- Bold the most important phrases in bullets

EDUCATION:
- Use this exact format for each degree:
\\vspace{{2pt}}
{{\\bfseries\\fontsize{{10}}{{11}}\\selectfont\\color{{darktext}} Degree Name}}\\\\[1pt]
{{\\bfseries\\fontsize{{9.5}}{{11}}\\selectfont\\color{{accentblue}} University Name}}\\\\[1pt]
{{\\fontsize{{8.5}}{{10}}\\selectfont\\color{{midgray}} \\faCalendar[regular]\\; Start -- End \\quad \\faMapMarker*\\; Location}}\\\\[2pt]
{{\\fontsize{{9}}{{10}}\\selectfont\\color{{darktext}} Major/Details \\quad \\textbf{{CGPA: ...}}}}

PROJECTS:
- Use this exact format for each project:
{{\\bfseries\\fontsize{{9.5}}{{11}}\\selectfont\\color{{darktext}} Project Name}}\\\\[1pt]
{{\\fontsize{{8.5}}{{10}}\\selectfont\\color{{midgray}} \\faCalendar[regular]\\; Date \\quad \\faMapMarker*\\; Location}}\\\\[2pt]
{{\\fontsize{{8.5}}{{10}}\\selectfont\\color{{midgray}}\\textit{{Short description}}}}
\\begin{{itemize}}
  \\item [bullet points]
\\end{{itemize}}

SKILLS:
- Extract all relevant skills and format them using the \\skilltag command
- Example: \\skilltag{{Python}} \\skilltag{{Docker}} \\skilltag{{React}}
- Separate them with a space or newline

ACHIEVEMENTS:
- Format achievements using this structure:
\\vspace{{5pt}}
{{\\color{{accentblue}}\\faBolt}}\\;{{\\bfseries\\fontsize{{9}}{{10}}\\selectfont\\color{{darktext}} Achievement Title}}\\\\[2pt]
{{\\fontsize{{8.5}}{{10}}\\selectfont\\color{{darktext}} Short description or details}}

=== PLACEHOLDER REPLACEMENT RULES ===
Replace every <<PLACEHOLDER>> with actual content from the resume:
- <<FULL_NAME>> → candidate's full name
- <<JOB_TITLE>> → desired job title or current title
- <<PHONE>> → phone number
- <<EMAIL>> → email address
- <<LINKEDIN_URL>> → full LinkedIn URL
- <<LINKEDIN_URL_TEXT>> → display text for LinkedIn (e.g. linkedin.com/in/username)
- <<LOCATION>> → city, country
- <<SUMMARY>> → your rewritten summary paragraph
- <<EXPERIENCE>> → all experience blocks using \\jobheader
- <<EDUCATION>> → all education blocks
- <<PROJECTS>> → all project blocks
- <<SKILLS>> → all \\skilltag{{...}} commands
- <<ACHIEVEMENTS>> → all achievement blocks

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
            "Raw LaTeX only. Starts with \\documentclass[10pt,a4paper]{article}, "
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

        CRITICAL INSTRUCTION FOR TOOL CALLING:
        Because you are communicating via JSON, you MUST double-escape all backslashes in the `latex_content` argument when calling the LaTeX Compiler Tool.
        For example:
        - Instead of \\documentclass, you MUST write \\\\documentclass
        - Instead of \\textbf, you MUST write \\\\textbf
        - Instead of \\begin, you MUST write \\\\begin
        If you do not escape the backslashes, the JSON parser will crash with a 500 Internal Server Error (invalid character 'd' in string escape code).
        """,
        expected_output="SUCCESS message with the absolute path to the compiled PDF.",
        agent=agent,
        context=[resume_write_task]
    )