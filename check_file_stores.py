
from google import genai
from google.genai import types
import time

client = genai.Client()

created_store = client.file_search_stores.create(config={'display_name': 'your-fileSearchStore-name'})
print(f"Created store: {created_store.name}")

print("Listing all stores:")
for store in client.file_search_stores.list():
    print(store.name)

# Use the name of the store we just created
my_file_search_store = client.file_search_stores.get(name=created_store.name)

print(f"Retrieved store details: {my_file_search_store}")

# Delete the store we just created
client.file_search_stores.delete(name=created_store.name, config={'force': True})
print(f"Deleted store: {created_store.name}")