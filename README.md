# 🧩 n8n Workflow Exporter

This project provides a simple Python script to **extract and version control** your [n8n](https://n8n.io) workflows by exporting them from a self-hosted instance and storing them in JSON format — perfect for Git-based tracking.

---

## 📦 Features

- ✅ Connects to your local/self-hosted n8n instance
- ✅ Exports all **active** (non-archived) workflows via the REST API
- ✅ Saves each workflow as a clean, valid JSON file
- ✅ Filenames are sanitized for Git-friendly version control
- ✅ Easy to run locally or integrate into CI/CD

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/n8n-workflow-exporter.git
cd n8n-workflow-exporter

```
