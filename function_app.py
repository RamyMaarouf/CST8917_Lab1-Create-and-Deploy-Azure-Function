import azure.functions as func
import logging
import json
import re
import uuid
import os
from datetime import datetime
from azure.cosmos import CosmosClient

# =============================================================================
# CREATE THE FUNCTION APP
# =============================================================================
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# =============================================================================
# DATABASE SETUP
# =============================================================================
URL = os.environ.get('COSMOS_DB_URI') or "https://cosmosdblab1.documents.azure.com:443/"
KEY = os.environ.get('COSMOS_DB_KEY') or "cbWNug7A0zZ9SCjBNTM9hgGkP0FKARutRUohkeMSar1Dt7G5psWDAveMTgUz5ZBjPOhSlfpNIvaWACDb8GVEpw=="

try:
    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client("TextAnalysisDB")
    container = database.get_container_client("AnalysisResults")
except Exception as e:
    logging.error(f"Cosmos DB Connection Error: {e}")

# =============================================================================
# FUNCTION 1: TextAnalyzer (POST/GET)
# =============================================================================
@app.route(route="TextAnalyzer")
def TextAnalyzer(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Text Analyzer API was called!')

    # Get the text from Params or JSON Body
    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get('text')
        except ValueError:
            pass

    if text:
        # 1. Perform Analysis Logic
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))
        # Simple sentence regex or default to 1
        sentence_count = len(re.findall(r'[.!?]+', text))
        if sentence_count == 0: sentence_count = 1
        
        avg_word_length = round(char_count_no_spaces / word_count, 1) if word_count > 0 else 0

        # 2. Build Response Object
        response_data = {
            "analysis": {
                "wordCount": word_count,
                "characterCount": char_count,
                "sentenceCount": sentence_count,
                "averageWordLength": avg_word_length
            },
            "metadata": {
                "analyzedAt": datetime.utcnow().isoformat(),
                "textPreview": text[:50] + "..." if len(text) > 50 else text
            }
        }

        # 3. DATABASE PERSISTENCE (Part 13)
        analysis_id = str(uuid.uuid4())
        db_document = {
            "id": analysis_id,
            "analysis": response_data["analysis"],
            "metadata": response_data["metadata"],
            "originalText": text
        }
        
        try:
            container.upsert_item(db_document)
            response_data["databaseId"] = analysis_id
        except Exception as e:
            logging.error(f"Failed to save to Cosmos DB: {e}")

        return func.HttpResponse(json.dumps(response_data, indent=2), mimetype="application/json")

    else:
        return func.HttpResponse(
            json.dumps({"error": "Please pass a 'text' parameter in the query string or body"}), 
            status_code=400, 
            mimetype="application/json"
        )

# =============================================================================
# FUNCTION 2: GetAnalysisHistory (Part 14)
# =============================================================================
@app.route(route="GetAnalysisHistory", methods=["GET"])
def GetAnalysisHistory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fetching analysis history...')
    try:
        # Fetching the last 10 records
        query = "SELECT * FROM c OFFSET 0 LIMIT 10"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        return func.HttpResponse(
            json.dumps({"count": len(items), "results": items}, indent=2),
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"History retrieval error: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Could not retrieve history from database"}), 
            status_code=500, 
            mimetype="application/json"
        )