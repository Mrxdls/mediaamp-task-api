from APP.Services.log_transter import log_active_tasks

# Call the Celery task directly for testing
if __name__ == "__main__":
    result = log_active_tasks()
    print(result)
