"""
Population Sorter Module.

Reads population data from a .txt file and returns
data sorted by area or population.
"""


def read_population_data(filepath):
    """
    Read population data from a .txt file.

    Each line in the file must follow the format:
        country name, area, population

    Args:
        filepath (str): Path to the .txt file with population data.

    Returns:
        list[dict]: A list of dictionaries with keys:
                    'country', 'area', 'population'.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a line cannot be parsed correctly.
    """
    data = []

    with open(filepath, encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 3:
                raise ValueError(
                    f"Line {line_number} has invalid format: '{line}'"
                )

            country = parts[0].strip()
            try:
                area = int(parts[1].strip())
                population = int(parts[2].strip())
            except ValueError:
                raise ValueError(
                    f"Line {line_number} contains non-numeric "
                    f"area or population: '{line}'"
                )

            data.append({
                "country": country,
                "area": area,
                "population": population,
            })

    return data


def sort_by_area(data, ascending=False):
    """
    Sort population data by area.

    Args:
        data (list[dict]): List of country dicts with 'area' key.
        ascending (bool): If True, sort ascending. Default is False
                          (largest area first).

    Returns:
        list[dict]: New sorted list of country dictionaries.
    """
    return sorted(data, key=lambda x: x["area"], reverse=not ascending)
