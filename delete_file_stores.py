from google import genai

client = genai.Client()

print("--- File Stores BEFORE Deletion ---")
stores = list(client.file_search_stores.list())
if not stores:
    print("No file stores found.")
else:
    for store in stores:
        print(f"Found store: {store.name} ({store.display_name})")

print("\n--- Deleting All File Stores ---")
for store in stores:
    print(f"Deleting {store.name}...")
    try:
        client.file_search_stores.delete(name=store.name, config={'force': True})
        print("Deleted.")
    except Exception as e:
        print(f"Failed to delete {store.name}: {e}")

print("\n--- File Stores AFTER Deletion ---")
remaining_stores = list(client.file_search_stores.list())
if not remaining_stores:
    print("No file stores remaining.")
else:
    for store in remaining_stores:
        print(f"Remaining store: {store.name} ({store.display_name})")
