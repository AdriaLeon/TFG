# Comparing European Election Narratives on TikTok Across EU Member States

This project involves the creation and analysis of a dataset derived from TikTok videos related to the 2024 European Elections. Videos were collected using keyword-based search queries and filtered to focus on specific political topics across different EU member states.

Special thanks to [AI Forensics](https://aiforensics.org/) for providing the initial dataset that served as the foundation for this work.

---

## 📊 Dataset Creation

The dataset was expanded and enriched through several preprocessing and analysis steps. You can explore the process in [`code/dataset_creation/dataset_creation.ipynb`](code/dataset_creation/dataset_creation.ipynb), or access the final dataset directly: [`General_Topic_Party_ByTopic.csv`](code/dataset/General_Topic_Party_ByTopic.csv).

### Key Processing Steps:
- Added video captions (transcriptions)
- Filtered content to retain only English-language videos
- Focused on themes related to **war** and **abortion**
- Enriched entries with engagement metrics:
  - Number of likes per video  
  - Number of followers per user
- Computed sentiment scores:
  - Compound sentiment score (numeric from -1 to 1)
  - Binary sentiment label (negative/positive)
  - Emotion-based sentiment analysis related to political context
- Detected mentions of political parties
- Identified the political alignment (e.g. left-wing, right-wing)
- Calculated a subjectivity score for each caption

---

## ⚙️ Environment Setup

This project was tested on an **Ubuntu** distribution with **Python 3.12**.

It’s recommended to use a Python virtual environment:

### 1. Install `venv` (if not already installed)
```bash
sudo apt install python3-venv
```

### 2. Create the virtual enviroment
bash
```
python3 -m venv VENV_NAME
```

### 3. Activate the virtual enviroment
bash
```
source VENV_NAME/bin/activate  
```

### 4.Install the requirements
bash
```
pip install -r requirements.txt 
```
