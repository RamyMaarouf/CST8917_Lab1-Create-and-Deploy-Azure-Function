# Lab 1: Serverless Text Analyzer with Azure Functions & Cosmos DB

This project is a serverless API built using **Python** and **Azure Functions**. It performs text analysis (word count, character count, etc.) and persists the results in an **Azure Cosmos DB** NoSQL database.

## Features
- **TextAnalyzer**: A function that accepts text via GET or POST, returns analysis metrics, and saves the data to the cloud.
- **GetAnalysisHistory**: A GET function that retrieves the last 10 analysis records from Cosmos DB.
- **Managed Identity**: Configured for secure access between Azure services.

## Local Setup Instructions

### 1. Prerequisites
* **Python 3.12**: (Required for compatibility with Azure Functions Linux Consumption plans).
* **Azure Functions Core Tools**: Version 4.x.
* **VS Code Extensions**: Azure Functions and REST Client.

### 2. Environment Configuration
Create a `local.settings.json` file in the root directory:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "COSMOS_DB_URI": "https://cosmosdblab1.documents.azure.com:443/",
    "COSMOS_DB_KEY": "YOUR_COSMOS_KEY_HERE"
  }
}
```

### 3. Setup and Run (Local)
1. **Initialize the Environment**:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Project: Start the local Azure Functions host**:
   ```bash
   func start
   ```

### Cloud Deployment

### 1. Configure Application Settings
Because secrets like your database key should never be hard-coded in your source code, you must add them to the Azure portal:
1. Navigate to the **Azure Portal**.
2. Open your **Function App** (`ramy-func-lab1`).
3. Under **Settings**, select **Environment variables**.
4. Add the following two settings:
   * `COSMOS_DB_URI`: `https://cosmosdblab1.documents.azure.com:443/`
   * `COSMOS_DB_KEY`: `YOUR_COSMOS_KEY_HERE`
5. Click **Apply** and then **Confirm**.

### 2. Deploy via Azure Functions Core Tools
Open your terminal in VS Code and ensure your virtual environment is active. Run the following command to package your code and perform a remote build in Azure:

   ```bash
   func azure functionapp publish ramy-func-lab1 --build remote
   ```
### 3. Verification
Once the deployment is complete, the terminal will provide an **Invoke URL**. 
1. Copy the URL for `TextAnalyzer`.
2. Use the `test.http` file or a browser to send a request to:
   `https://ramy-func-lab1.azurewebsites.net/api/TextAnalyzer?text=Hello world`
3. **Expected Result**: A `200 OK` status and a JSON response containing your analysis and a `databaseId`.

---

## API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/TextAnalyzer` | `GET/POST` | Analyzes input text and saves the result to Cosmos DB. |
| `/api/GetAnalysisHistory` | `GET` | Retrieves the last 10 analysis records from the database. |

---

## Challenges & Solutions

* **Python Version Mismatch (503 Error)**: 
  - **Issue**: Local development was initially on Python 3.13, which caused compatibility issues with the Azure Linux Consumption plan during remote builds.
  - **Solution**: Downgraded the local virtual environment to **Python 3.12** and updated the `linuxFxVersion` via Azure CLI to ensure environment parity.
* **Environment Variable Sync**: 
  - **Issue**: The cloud function failed to connect to the database because it couldn't see the local `local.settings.json`.
  - **Solution**: Manually configured the `COSMOS_DB_URI` and `COSMOS_DB_KEY` in the **Azure Portal Application Settings** to allow the live app to authenticate.
* **Dependency Management**: 
  - **Issue**: `ModuleNotFoundError` for the Cosmos SDK in the cloud.
  - **Solution**: Added `azure-cosmos` to `requirements.txt` and utilized `--build remote` during deployment to ensure libraries were compiled for the Linux environment.
