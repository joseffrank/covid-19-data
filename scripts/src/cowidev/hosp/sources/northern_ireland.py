from uk_covid19 import Cov19API


METADATA = {
    "source_url": "https://coronavirus.data.gov.uk/details/download",
    "source_url_ref": "https://coronavirus.data.gov.uk/details/healthcare",
    "source_name": "Government of the United Kingdom",
    "entity": "Northern Ireland",
}


def read():
    metrics = {
        "date": "date",
        "Daily hospital occupancy": "hospitalCases",
        "Weekly new hospital admissions": "newAdmissions",
        "Daily ICU occupancy": "covidOccupiedMVBeds",
    }
    api = Cov19API(
        filters=["areaType=nation", "areaCode=N92000002"],
        structure=metrics,
    )
    df = api.get_dataframe()
    return df


def main():
    # Read
    df = read()
    # Sort rows
    print(df.columns)
    df = df.sort_values("date")
    # Smooth metric
    df["Weekly new hospital admissions"] = df["Weekly new hospital admissions"].rolling(7).sum()
    # Unpivot
    df = df.melt("date", var_name="indicator").dropna(subset=["value"])
    # Metadata
    df["entity"] = METADATA["entity"]
    return df, METADATA


if __name__ == "__main__":
    main()
