import arxiv
import csv

# Construct the default API client.
client = arxiv.Client()

# Define all the queries
queries = [
    '("large language models" OR "LLMs") AND "automated planning"',
    '("large language models" OR "LLMs") AND ("symbolic planning" OR "neurosymbolic planning")',
    '("neural-symbolic" OR "neurosymbolic") AND "planning"',
    '"large language models" AND ("task planning" OR "AI planning")',
    '("transformers" OR "GPT" OR "BERT") AND "automated planning"',
    '("large language models" OR "LLMs") AND "PDDL" AND "planning"',
    '"GPT" AND "planning" AND ("symbolic" OR "neurosymbolic")',
    '"BERT" AND "task planning"',
    '("neurosymbolic AI" OR "neural-symbolic systems") AND "planning"',
    '("LLMs" AND "constraint-based planning")',
    '("language models" AND "AI planning" AND "neurosymbolic")',
    '("large language models" AND "automated planning" AND "symbolic reasoning")',
    '("neurosymbolic AI" AND "planning" AND "large language models")',
    '("language models" AND "planning" AND "neurosymbolic")',
    '("transformers" AND "task planning" AND "neurosymbolic systems")',
    '("LLMs" AND "hierarchical task planning")',
    '("large language models" AND "sequential decision making" AND "planning")',
    '("neurosymbolic" AND "large language models" AND "AI planning")',
    '("language models" AND "PDDL" AND "symbolic planning")',
    '("transformers" AND "automated planning" AND "neural-symbolic")',
    '("LLMs" AND "robotics" AND "task planning")',
    '("language models" AND "multi-agent planning")',
    '("neurosymbolic AI" AND "robot planning")',
    '("symbolic AI" AND "language models" AND "planning")',
    '("artificial intelligence" AND "language models" AND "planning")',
    '("AI" AND "large language models" AND "automated planning")',
    '("deep learning" AND "task planning" AND "language models")',
    '(("LLMs" OR "large language models") AND ("automated planning" OR "symbolic planning" OR "neurosymbolic planning") AND "constraint satisfaction")',
    '(("language models" OR "transformers") AND ("PDDL" OR "task planning") AND ("neurosymbolic" OR "symbolic AI"))',
    '(("large language models" AND "AI planning") OR ("neurosymbolic AI" AND "task planning"))'
]

# Open a CSV file to write the results
with open('arxiv_papers.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Title', 'Authors', 'Published Date', 'Abstract', 'URL'])
    
    # Iterate over each query and fetch the results
    for query in queries:
        print(f"Executing query: {query}")
        search = arxiv.Search(
            query=query,
            max_results=1000,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        # Iterate over the results and write them to the CSV file
        for result in client.results(search):
            writer.writerow([
                result.title,
                ', '.join([author.name for author in result.authors]),
                result.published.date(),
                result.summary.replace('\n', ' '),
                result.entry_id
            ])

print("CSV file has been created with the search results.")
