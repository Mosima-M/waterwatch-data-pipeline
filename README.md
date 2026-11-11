# WaterWatch — Water Consumption Monitoring & Analytics Pipeline

## 1. Project Overview

WaterWatch is a Python-based data engineering pipeline designed to process and analyse water consumption data from building water meters.

Water consumption data may contain missing values, duplicate records, invalid timestamps, unknown meter identifiers and negative consumption values. These issues can affect the accuracy of reports and analysis.

WaterWatch addresses these challenges by extracting, validating, transforming and storing water consumption data before generating analytical reports.

**Data note:** This project uses synthetic data generated for demonstration and testing. It does not use actual municipal or building water-meter data.

## 2. Project Objectives

- Generate and ingest synthetic water consumption data.
- Identify missing, duplicate and invalid records.
- Clean and standardise valid records.
- Calculate daily water consumption per building.
- Store processed data in an SQLite database.
- Identify potentially unusual consumption patterns.
- Generate data-quality reports and visualisations.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline implementation |
| Pandas | Data manipulation and transformation |
| CSV | Raw data source format |
| SQLite | Data storage |
| SQL | Data analysis and querying |
| Matplotlib | Data visualisation |
| Pytest | Automated testing |
| Git and GitHub | Version control |

## 4. Pipeline Architecture

The pipeline follows an Extract, Validate, Transform, Load and Analyse workflow.

1. **Extract:** Read building, meter and water-reading CSV files.
2. **Validate:** Identify invalid records and document rejection reasons.
3. **Transform:** Standardise timestamps, enrich readings with building information and calculate daily consumption.
4. **Load:** Store valid readings and analytical summaries in SQLite.
5. **Analyse:** Generate consumption summaries, potential anomaly flags, data-quality reports and visualisations.

## 5. Data Sources

The pipeline uses three synthetic CSV datasets:

- `buildings.csv` — building identifiers, names, locations and types.
- `meters.csv` — meter identifiers, associated buildings and installation dates.
- `readings.csv` — reading identifiers, meter identifiers, timestamps and consumption in litres.

## 6. Data Quality Rules

The pipeline checks for:

- Missing reading identifiers.
- Duplicate reading identifiers.
- Missing meter identifiers.
- Unknown meter identifiers.
- Invalid timestamps.
- Invalid consumption values.
- Negative consumption values.

Rejected records are exported to `reports/rejected_readings.csv` with their rejection reasons.

## 7. Analytics

WaterWatch produces:

- Daily water consumption summaries by building.
- Total consumption measurements.
- Potential unusual consumption flags.
- Data-quality scorecards.
- A daily consumption trend chart.

Potential anomalies indicate unusual consumption patterns and should not be interpreted as confirmed water leaks.

## 8. Project Structure

```text
waterwatch-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── database/
├── reports/
├── src/
│   ├── generate_data.py
│   └── pipeline.py
├── sql/
│   └── analysis.sql
├── tests/
│   └── test_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 9. Installation and Execution

### Requirements

- Python 3.10 or later
- pip

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Generate synthetic data

```bash
python src/generate_data.py
```

### Execute the pipeline

```bash
python src/pipeline.py
```

### Run automated tests

```bash
python -m pytest -v
```

## 10. Generated Outputs

| Output | Description |
|---|---|
| `database/waterwatch.db` | SQLite database |
| `data/processed/daily_consumption.csv` | Daily consumption summaries |
| `reports/rejected_readings.csv` | Invalid records and rejection reasons |
| `reports/anomaly_flags.csv` | Potential unusual consumption records |
| `reports/data_quality_report.txt` | Pipeline data-quality summary |
| `reports/consumption_trend.png` | Water consumption trend visualisation |

## 11. Limitations and Future Improvements

- Integrate with real water-meter APIs or other data sources.
- Introduce scheduled pipeline execution.
- Improve anomaly detection using historical consumption patterns.
- Add automated monitoring and alerting.
- Deploy the pipeline to a cloud environment.

## 12. Repository Verification

`WTC-56X9WU67`