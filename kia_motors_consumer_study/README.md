# Kia Motors Consumer Preference Study

A Python + Streamlit dashboard based on the supplied project report:

**A Study on Consumer Preference Towards Kia Motors with Special Reference to Coimbatore District**

## Features
- Frequency and percentage tables
- Bar chart for selected survey factors
- Satisfaction cross-tabulation (High / Moderate / Low)
- Chi-square test for selected socio-economic factors
- CSV downloads for the extracted aggregate data

## Project structure
```text
kia_motors_consumer_study/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── frequency_data.csv
    └── satisfaction_crosstabs.csv
```

## Run on your computer
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the dashboard:
   ```bash
   streamlit run app.py
   ```

## Upload to GitHub
1. Create a new GitHub repository, for example `kia-motors-consumer-study`.
2. Upload `app.py`, `requirements.txt`, `README.md`, and the `data` folder.
3. Commit the files.

## Important data note
The Word report provides grouped/aggregate tables for 180 respondents, not individual-level survey records.
This project therefore visualizes the reported aggregate counts. The Chi-square calculations use the
satisfaction cross-tabulations in the report. Some source tables contain inconsistent totals or percentages;
verify those values against the original report before using the results in a formal submission.
