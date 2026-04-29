# 🇮🇳 India DA Job Market Pulse

> *I analyzed 1,088 real Data Analyst job postings so you don't have to guess what the market looks like.*

**Live Dashboard** → [india-da-job-market-pulse.streamlit.app](https://india-da-job-market-pulse.streamlit.app)  
**Tableau Dashboard** → [View on Tableau Public](https://public.tableau.com/app/profile/muskan.varma/viz/IndiaDAJobMarketPulse/IndiaDAJobMarketPulse)

---

## 💡 What I Found

After scraping and analyzing 1,088 live DA job postings from Naukri.com:

| Finding | Insight |
|---|---|
| 🥇 Most demanded skill | **Data Analysis** (500+ mentions) |
| ⚔️ SQL vs Python | **SQL wins 36 vs 20** — SQL is non-negotiable for DA roles |
| 🏙️ Top hiring city | **Bengaluru (204 jobs)** — but Pune is right behind at 23 |
| 🎓 Fresher friendly? | **YES — 52% of roles open to 0-2 yrs experience** |
| 🏠 Remote available? | **12% of all DA roles are remote** |
| 🏢 Top companies | Bajaj Finance, Barclays, Amazon, Deloitte, JPMorgan |

---

## 🏗️ How It Works
1. **Scraper** — Selenium + BeautifulSoup scrapes title, company, experience, salary, location, skills, posted date
2. **Storage** — Pandas cleans and saves to date-stamped CSV + SQLite database
3. **Analysis** — SQL queries + Python uncovers skill demand, city trends, experience distribution
4. **Dashboard** — Streamlit (interactive filters) + Tableau Public (visual analytics)
5. **Scheduler** — Designed to run every Sunday to track weekly market shifts

---

## 📊 Dashboard Features

- 🔍 Filter by city and experience level — all charts update live
- 📍 Top 15 cities by job count
- 🛠️ Top 20 most demanded skills
- 📅 Experience distribution — what companies actually want
- 🏢 Companies treemap — who's hiring the most
- 💡 Key findings panel — analyst-style insights
- 🔎 Raw data table — explore all 1,088 jobs

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Scraping | Python, Selenium, BeautifulSoup |
| Data Processing | Pandas, NumPy |
| Storage | SQLite, CSV |
| Analysis | SQL, Python |
| Visualization | Streamlit, Plotly, Tableau |
| Deployment | Streamlit Cloud |

---

## 🚀 Run Locally

```bash
git clone https://github.com/muskanvarmaa/india-da-job-market-pulse.git
cd india-da-job-market-pulse
pip install -r requirements.txt
python scraper/naukri_scraper.py
python pipeline/load_db.py
streamlit run dashboard/app.py
```

---

## 📁 Project Structure
india-da-job-market-pulse/
├── scraper/
│   └── naukri_scraper.py      ← Selenium scraper
├── pipeline/
│   ├── load_db.py             ← CSV to SQLite loader
│   └── insights.py            ← SQL analysis queries
├── dashboard/
│   └── app.py                 ← Streamlit dashboard
├── data/
│   └── sample_jobs.csv        ← Sample dataset
├── .streamlit/
│   └── config.toml            ← Dark theme config
└── requirements.txt

---

## 🔄 Weekly Auto-Update

Each scraper run creates a new date-stamped CSV. Over time this builds a historical dataset to track how skill demand and hiring trends shift week over week.

---

*Built by [Muskan Varma](https://linkedin.com/in/muskanvarma-cse) · Computer Engineering @ SPPU · Pune*
