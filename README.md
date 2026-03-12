# 🤖 Text-to-SQL Chatbot

An AI-powered chatbot that converts natural language questions into SQL queries, runs them on an employee database, and returns readable answers — using open-source models.

## 🎯 What It Does

```
User: "How many employees are there?"
  → AI generates: SELECT COUNT(*) FROM employees
  → Result: 300,024
```

## 🏗️ Architecture

```
User Question (English)
       ↓
  Embedding Model (BAAI/bge-small-en-v1.5)  →  Finds relevant tables
       ↓
  LLM (Qwen/Qwen2.5-Coder-3B-Instruct)     →  Generates SQL query
       ↓
  SQLAlchemy executes query on database       →  Returns results
```

## 🛠️ Tech Stack

| Component | Tool |
|-----------|------|
| Framework | LlamaIndex |
| LLM | Qwen2.5-Coder-3B-Instruct |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Database | SQLite (employee.db) |
| Web UI | Streamlit |
| Quantization | BitsAndBytes (4-bit) |

## 📁 Project Structure

```
CS_Chatbot/
├── README.md
├── app.py                     # Streamlit web UI
├── .gitignore
├── cs_chatbot.ipynb       # ⭐ Main notebook

```

> **Note:** `employee.db` (240MB) and `model_cache/` are not included in the repo due to size. See setup instructions below.

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/CS_Chatbot.git
cd CS_Chatbot
```

### 2. Download the Employee Database
The project uses the [MySQL Employees Sample Database](https://github.com/datacharmer/test_db) converted to SQLite.

**Option A — Direct SQLite download:**
1. Go to [datacharmer/test_db](https://github.com/datacharmer/test_db)
2. Clone it and import into MySQL, then convert to SQLite using [mysql2sqlite](https://github.com/dumblob/mysql2sqlite)

**Option B — Pre-built SQLite version:**
1. Download from [siara-cc/employee_db](https://github.com/siara-cc/employee_db) (SQLite3 format)
2. Rename to `employee.db` and place in the project root

The database contains ~300,000 employees across 6 tables:
| Table | Description |
|-------|-------------|
| `employees` | Employee info (emp_no, name, hire_date) |
| `departments` | Department names and IDs |
| `dept_emp` | Links employees ↔ departments |
| `salaries` | Employee salary records |
| `dept_manager` | Department managers |
| `titles` | Employee job titles |

### 3. Create a `.env` file
```bash
HF_TOKEN=your_huggingface_token_here
```
Get your token from: https://huggingface.co/settings/tokens

### 4. Install dependencies
```bash
pip install llama-index llama-index-llms-huggingface llama-index-embeddings-huggingface sqlalchemy tabulate bitsandbytes accelerate
```

### 5. Run the Streamlit app
```bash
streamlit run app.py
```

## 💡 Google Colab (Recommended)

For best results, use the Google Colab notebook with a free T4 GPU:
1. Upload to [Google Colab](https://colab.research.google.com/)
2. Set runtime to **T4 GPU**
3. Upload `employee.db` when prompted
4. Run all cells

## 📝 Key Learnings

- **Text-to-SQL** pipeline using LlamaIndex framework
- **RAG** (Retrieval Augmented Generation) for table schema retrieval
- **Vector embeddings** for semantic search of database tables
- **Prompt engineering** for SQL generation
- **4-bit quantization** for running LLMs on limited hardware
- **Environment variables** for secure token management
