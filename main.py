import arxiv
import time
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows

columns = ['URL', 'Title', 'Categories']
data = []

month_id = 2406


query = "(ti:survey OR ti:review OR ti:art OR ti:overview OR ti:advances) AND " + \
        "(cat:cs.AI OR cat:cs.AR OR cat:cs.CC OR cat:cs.CE OR cat:cs.CG OR " + \
        "cat:cs.CL OR cat:cs.CR OR cat:cs.CV OR cat:cs.CY OR cat:cs.DB OR " + \
        "cat:cs.DC OR cat:cs.DL OR cat:cs.DM OR cat:cs.DS OR cat:cs.ET OR " + \
        "cat:cs.FL OR cat:cs.GL OR cat:cs.GR OR cat:cs.GT OR cat:cs.HC OR " + \
        "cat:cs.IR OR cat:cs.IT OR cat:cs.LG OR cat:cs.LO OR cat:cs.MA OR " + \
        "cat:cs.MM OR cat:cs.MS OR cat:cs.NA OR cat:cs.NE OR cat:cs.NI OR " + \
        "cat:cs.OH OR cat:cs.OS OR cat:cs.PF OR cat:cs.PL OR cat:cs.RO OR " + \
        "cat:cs.SC OR cat:cs.SD OR cat:cs.SE OR cat:cs.SI OR cat:cs.SY)"

"""
query = "(ti:survey OR ti:review OR ti:art OR ti:overview OR ti:advances) AND " + \
        "(cat:stat.AP OR cat:stat.CO OR cat:stat.ME OR cat:stat.ML OR " + \
        "cat:stat.OT OR cat:stat.TH)"
"""

start_id = 1
end_id = 25000
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

# Create a new workbook and select the active sheet
wb = Workbook()
ws = wb.active

# Write the DataFrame to the worksheet
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# Apply hyperlink style to the URL column
for cell in ws['A'][1:]:  # Assuming 'URL' is in column A
    cell.hyperlink = cell.value
    cell.font = Font(color="0000FF", underline="single")  # Blue, underlined text

# Save the workbook
excel_file_path = 'articles.xlsx'
wb.save(excel_file_path)

print(f"Data written to {excel_file_path}")
