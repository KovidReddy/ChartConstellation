from googlesearch import search
import pandas as pd

# fetch the URLs from google based on Query search
query = 'Trump is great for the economy'
url_list = []
for j in search(query, tld="com", num=50, stop=1, pause=2):
    url_list.append(j)
# write the urls to a new Excel file
df = pd.DataFrame({'Positive':url_list})
writer = pd.ExcelWriter('C:\\Users\\pylak\\Documents\\Fall_2018\\DV\\Project\\Trump\\url2.xlsx')
df.to_excel(writer, 'Sheet1', index=False)
writer.save()

