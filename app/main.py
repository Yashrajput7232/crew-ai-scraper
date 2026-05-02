from crew.crew import run_pipeline


def load_file(path):
    with open(path, "r") as f:
        return f.read()


if __name__ == "__main__":
    job_description = load_file("data/sample_jobs.txt")
    resume = load_file("data/resume.txt")

    result = run_pipeline(job_description, resume)

    print("\nFINAL RESULT:\n")
    print(result)