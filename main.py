import arxiv
import time
import pandas as pd

columns = ['URL', 'Title', 'Categories']
data = []

month_id = 2401

query = "(ti:survey OR ti:review OR ti:art OR ti:overview) AND " + \
        "(cat:cs.AI OR cat:cs.CC OR cat:cs.CL OR cat:cs.CR OR " + \
        "cat:cs.FL OR cat:cs.LG OR cat:cs.MA OR cat:cs.NE OR " + \
        "cat:cs.PL OR cat:cs.SI)"

start_id = 1
end_id = 1000
group_size = 100

for start_group_id in range(start_id, end_id, group_size):
    end_group_id = min(start_group_id + group_size, end_id)

    ids = range(start_group_id, end_group_id)
    zpids = [str(id).zfill(5) for id in ids]
    article_ids = [f'{month_id}.{zpid}' for zpid in zpids]

    client = arxiv.Client()
    search = arxiv.Search(query=query, id_list=article_ids)
    gen = client.results(search)

    while True:
        try:
            result = next(gen)
            title = result.title
            url = result.pdf_url
            categories = sorted(result.categories)
            data.append([url, title, ', '.join(categories)])
        except StopIteration:
            break

    # Process the data as needed, for example, write to Excel or another storage format
    print(f"Processed IDs {start_group_id} to {end_group_id - 1}")
    time.sleep(5)  # Add a delay as needed to avoid overloading the API

# Create a DataFrame from the collected data
df = pd.DataFrame(data, columns=columns)

# Write the DataFrame to an Excel file
excel_file_path = 'articles.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Data written to {excel_file_path}")
