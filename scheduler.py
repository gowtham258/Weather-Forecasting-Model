import schedule
import time
import os
from datetime import datetime

def run_pipeline():
    print(f"\n--- Running Pipeline at {datetime.now()} ---")
    os.system("python fetch_data.py")
    os.system("python preprocess.py")
    os.system("python train_model.py")
    os.system("python predict.py")
    print("--- Pipeline Completed ---\n")

# Schedule it to run every day at 3:00 AM
schedule.every().day.at("03:00").do(run_pipeline)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
