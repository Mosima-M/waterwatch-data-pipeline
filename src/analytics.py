
import matplotlib.pyplot as plt

from .config import REPORTS_DIR


def generate_reports(valid, rejected, daily):
    print("\n[ANALYTICS] Generating reports...")

    total = len(valid) + len(rejected)
    valid_count = len(valid)
    rejected_count = len(rejected)

    quality_score = (
        (valid_count / total) * 100 if total > 0 else 0
    )

    report = f"""
WATERWATCH DATA QUALITY REPORT
================================

Total records processed: {total}
Valid records: {valid_count}
Rejected records: {rejected_count}

Data quality score: {quality_score:.2f}%

Total recorded water consumption:
{valid["consumption_litres"].sum():.2f} litres

Daily consumption records: {len(daily)}
Potential anomalies detected: {daily["potential_anomaly"].sum()}

Note: Potential anomalies are unusual consumption patterns,
not confirmed water leaks.
"""

    with open(
        REPORTS_DIR / "data_quality_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report)

    total_by_date = daily.groupby("reading_date")[
        "total_consumption_litres"
    ].sum()

    plt.figure(figsize=(10, 5))
    total_by_date.plot(kind="line", marker="o")
    plt.title("WaterWatch Daily Water Consumption")
    plt.xlabel("Date")
    plt.ylabel("Consumption (litres)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(REPORTS_DIR / "consumption_trend.png")
    plt.close()

    print(report)
    print("Reports and chart generated successfully.")
