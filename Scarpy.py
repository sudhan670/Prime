import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the website
url = "https://hprera.nic.in/PublicDashboard"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the registered projects
table = soup.find('table', {'id': 'RegisteredProjects'})

# Extract the first 6 project links
project_links = []
for row in table.find_all('tr')[1:7]:  # skip the header row
    cols = row.find_all('td')
    project_link = cols[1].find('a')['href']
    project_links.append(project_link)

# Create a list to store the extracted data
data = []

# Loop through each project link and extract the required information
for link in project_links:
    project_url = f"https://hprera.nic.in/{link}"
    response = requests.get(project_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the required fields
    gstin_no = soup.find('span', {'id': 'ContentPlaceHolder1_lblGSTIN'}).text.strip()
    pan_no = soup.find('span', {'id': 'ContentPlaceHolder1_lblPAN'}).text.strip()
    name = soup.find('span', {'id': 'ContentPlaceHolder1_lblPromoterName'}).text.strip()
    permanent_address = soup.find('span', {'id': 'ContentPlaceHolder1_lblPermanentAddress'}).text.strip()
    
    # Append the extracted data to the list
    data.append({
        'GSTIN No': gstin_no,
        'PAN No': pan_no,
        'Name': name,
        'Permanent Address': permanent_address
    })

# Convert the list to a Pandas DataFrame
df = pd.DataFrame(data)

# Print the extracted data
print(df)

# Save the data to a CSV file
df.to_csv('registered_projects.csv', index=False)
