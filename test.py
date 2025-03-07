import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# A synchronous function that simulates a long-running task
def sync_task(url):
    print(f"Starting task for {url}")
    time.sleep(2)  # Simulate a blocking operation (e.g., loading a file)
    print(f"Finished task for {url}")
    return f"Result for {url}"

async def run_sync_in_executor(url):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, sync_task, url)
    return result

async def main():
    url = "http://example.com/audio.mp3"  # Replace with your actual URL
    print("Running tasks...")
    
    # Running the synchronous task asynchronously
    result = await asyncio.gather(run_sync_in_executor(url), run_sync_in_executor(url), run_sync_in_executor(url))
    
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
