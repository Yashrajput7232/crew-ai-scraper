# AI-Powered Job Search Assistant & Resume Generator

An automated, multi-agent pipeline built with **CrewAI** that supercharges your job application process. This system acts as an end-to-end assistant: it first scrapes job boards to discover relevant roles, then extracts the core requirements, analyzes your current resume, intelligently rewrites your experience to match the role (optimizing for ATS), and compiles a perfectly formatted, ATS-friendly LaTeX PDF.

## 🚀 Key Highlights & Capabilities

### 🕸️ Automated Job Discovery & Web Scraping
Instead of manually hunting for jobs, the system includes a robust web scraper that:
- Automatically pulls relevant job listings based on your target roles and preferences.
- Extracts clean job descriptions, parsing out requirements, responsibilities, and company information.
- Feeds these discovered roles directly into the generation pipeline for automated tailoring.

### 🤖 Multi-Agent Orchestration
Powered by [CrewAI](https://crewai.com/), the application uses specialized, autonomous agents that handle each step of the pipeline:
1. **Job Description Scraper & Extractor**: Processes the raw scraped job postings to identify the top ATS keywords and core requirements.
2. **Resume Matcher**: Analyzes the candidate's base resume against the JD to identify missing skills, weak language, and core alignment areas.
3. **Resume Writer**: Rewrites resume bullets into high-impact `[Action Verb] + [What You Did] + [Measurable Result]` format, seamlessly injecting JD keywords.
4. **LaTeX Compiler Agent**: Generates raw LaTeX using a highly customized, modern CV template and securely compiles it into a polished PDF document. 

### 🔀 Flexible LLM Provider Switching
Designed to run completely locally or via cloud APIs:
- **Cloud (Gemini)**: Uses Google GenAI (e.g., Gemini 1.5 Pro) for top-tier reasoning and fast processing.
- **Local (Ollama)**: Seamlessly switch to open-source models (like Mistral, LLaMA 3) running locally via Ollama. Ensures 100% data privacy for your sensitive resume data.

### 📄 Intelligent Resume Tailoring
The system doesn't just copy-paste your resume; it structurally improves it:
- Reorders projects, skills, and achievements based on relevance to the job description.
- Re-words vague phrases ("responsible for", "helped with") into strong, metric-driven statements.
- Drops irrelevant skills and experience that don't match the hiring manager's priorities.

### 🎨 Stunning LaTeX PDF Output
Generates a highly professional, modern 2-column resume layout:
- Built with `paracol`, `geometry`, `tikz` (for skill tags), and `fontawesome5`.
- Highly structured custom commands (`\jobheader`, `\skilltag`, `\achievement`).
- Auto-healing compilation: If the LLM produces a syntax error in the LaTeX, the compiler agent intercepts the error log, fixes the specific broken line, and recompiles successfully.

## 🛠 Tech Stack

- **Framework**: CrewAI, Python
- **LLM Integrations**: Google GenAI (Gemini), Ollama (Local LLMs)
- **Document Generation**: LaTeX (`pdflatex` / `xelatex`)
- **Environment Management**: `python-dotenv`

## 📁 Project Structure

```
crew-ai-scraper/
├── app/
│   ├── agents/      # Definitions of Extractor, Matcher, Writer, and Compiler agents
│   ├── crew/        # CrewAI pipeline and task orchestration logic
│   ├── db/          # Local storage / caching logic
│   ├── llm/         # LLM configuration (Gemini/Ollama switching logic)
│   ├── models/      # Data models and schemas
│   ├── scraping/    # Job board web scraping utilities
│   ├── services/    # Core business logic services
│   ├── tasks/       # CrewAI task definitions (e.g., resume_tasks.py)
│   └── main.py      # Entry point to trigger the pipeline
├── data/
│   ├── input/       # Base resume and configuration
│   └── output/      # Generated .tex and .pdf files
├── .env             # API keys and environment variables
└── requirements.txt # Python dependencies
```

## ⚙️ How it Works

1. **Discovery**: The web scraper searches job boards and pulls relevant job postings based on your criteria.
2. **Extraction**: The system processes the scraped job descriptions to extract the top 7 ATS keywords and core requirements.
3. **Analysis**: The system analyzes your current base resume's alignment with the specific job.
4. **Rewrite**: The Writer agent crafts tailored content filling in a predefined, aesthetic LaTeX template structure.
5. **Compile**: The text is passed to the LaTeX Compiler tool, and the system outputs a `resume-new.pdf` ready for submission!
