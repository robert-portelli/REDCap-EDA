from collections import namedtuple
import pandas as pd
import logging
import json  # You can replace this with yaml for YAML config files

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Define NamedTuple for Schema: namedtuple(<"name">, [<"field">, <"names">, <"act_as">, "<keys>"])
# Values are assigned later
Schema = namedtuple(
    "Schema",
    ["datetime", "time", "string", "category", "integer", "float"],
)


# Load schema dynamically (Replace this with a YAML or API call if needed)
def load_schema(schema_file=None):
    """
    Load schema mapping from a JSON/YAML file or use a default schema.

    Args:
        schema_file (str, optional): Path to schema file. Defaults to None.

    Returns:
        Schema (NamedTuple): Loaded schema mapping.
    """
    if schema_file:
        with open(schema_file) as f:
            schema_data = json.load(f)  # Replace with yaml.safe_load(f) if using YAML
        return Schema(**schema_data)

    # Instantiate Schema with predefined column mappings for each field type
    return Schema(
        datetime=("dob", "surgery_date"),
        time=("appointment_time",),
        string=("email", "phone", "notes"),
        category=("dropdown_character", "dropdown_mixed"),
        integer=("checkbox___1", "checkbox___2", "yes_no", "true_false"),
        float=("bmi", "age_at_survey"),
    )


def enforce_schema(df, schema=None):
    """
    Applies predefined data types to columns based on a NamedTuple schema.

    - Loads schema dynamically if not provided.
    - Uses structural pattern matching for clean and readable type conversions.
    - Ensures object columns are converted to a more efficient type.
    - Warns about unknown object columns that remain untyped.

    Args:
        df (pd.DataFrame): The input DataFrame.
        schema (Schema, optional): Preloaded schema. If None, loads a default schema.

    Returns:
        pd.DataFrame, pd.DataFrame: The mutated DataFrame and a receipt of changes.
    """

    # Load schema dynamically if not provided
    if schema is None:
        schema = load_schema()

    # Capture before state
    before = df.dtypes.copy()

    # Track columns that remain `object`
    untyped_columns = set(df.select_dtypes(include=["object"]).columns)

    # Iterate over each field type in the schema (e.g., "datetime", "string", etc.)
    for field_name in schema._fields:
        # Retrieve the tuple of column names assigned to the current field type
        for col in getattr(schema, field_name):
            # Apply transformation only if the column exists in the DataFrame
            if col in df.columns:
                match field_name:
                    case "datetime":
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                    case "time":
                        df[col] = pd.to_datetime(
                            df[col],
                            format="%H:%M",
                            errors="coerce",
                        ).dt.time
                    case "string":
                        df[col] = df[col].astype("string")
                    case "category":
                        df[col] = df[col].astype("category")
                    case "integer":
                        df[col] = df[col].astype("int64")
                    case "float":
                        df[col] = df[col].astype("float64")

                # Remove from untyped list after processing
                untyped_columns.discard(col)

    # Create mutation receipt
    receipt = pd.DataFrame({"Before": before, "After": df.dtypes})

    # Warn about untyped object columns
    if untyped_columns:
        logging.warning(
            "\n⚠️ The following columns remain untyped (object type detected):\n%s",
            list(untyped_columns),
        )

    # Log the changes
    logging.info("\nData Type Conversion Summary:\n%s", receipt.to_string())

    return df, receipt
