# Semantic Search on Documents
URL - https://pleasantly-winning-bluebird.ngrok-free.app
supports files with .pdf, .txt, .html extentions

**The Objective:**

Develop a web application that performs semantic search on case study documents related to a fictitious company, MindTickle. The system should prioritize relevant results based on meaning and context, not just exact keyword matches.

**Here's what you'll build:**

1. **APIs:**
    - `POST: /upload`: This API allows uploading new case study documents to the system. The file will be uploaded as form-data in PDF format.
    - `GET: /docs?q=<query>`: This API takes a search query and returns a list of relevant case study **document names**, not the entire documents.

2. **Data:**
    - Sample case studies are provided in the `/samples` folder, focusing on various industries, geographies, and use cases (e.g., healthcare CRM, training remote sales teams).
    - You can assume additional case studies will be uploaded for testing.
    - It is available in HTML format for readibilty, decide how you want to clean it.
**Optional Enhancements:**

- **Large Language Model (LLM) Integration:** Explore ways to leverage LLMs to improve search accuracy. We will like to see your creativity of how can keep the use of LLMs to minimum while improving the accuracy. Their are various platoforms which provide apis for open souce LLM models free to a great extent. You dont have to train your models but if you can finetune any of embeddings or LLM, that will be a huge plus. You can focus on optimizing queries for the following aspects:

    - **Industry:** Search results should effectively identify case studies relevant to specific industries (e.g., healthcare, CRM).
    - **Use Case:** The system should prioritize studies that address particular use cases (e.g., training remote sales teams).
    - **Geography:** Search should consider the geographical focus of case studies (e.g., Asia, India).

**Example:**

* **Query:** "How can we train our remote sales team in Asia?"
* **Expected Results:** The system should return a list of relevant case study names, potentially including "Training Strategies for Remote Sales Teams in APAC" or "Onboarding New Sales Reps in a Remote Setting."
