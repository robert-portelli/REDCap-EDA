"""
📌 cast_schema.py: Enforces strict data type conversion based on a predefined schema.

🔹 Purpose:
    - Ensures all DataFrame columns conform to expected data types.
    - Prevents unintended implicit conversions and enforces strict typing.
    - Fails explicitly if data does not match the expected format.

🔹 Design Decisions:
    - Uses a `namedtuple` to enforce a **rigid** schema (no dynamic modifications).
    - Raises errors instead of coercing invalid data (to flag issues in upstream cleaning).
    - Logs conversion details and failures for debugging.
    - Does **not** handle data cleaning or validation (assumes pre-cleaned input).

🔹 Assumptions:
    - Data **must** be pre-cleaned and validated before passing to this module.
    - Schema is static in the MVP but may become configurable later.

🔹 Usage:
    ```python
    import cast_schema
    df, report = cast_schema.enforce_schema(df)
    ```

🔹 Future Considerations:
    - Consider supporting a configurable schema via a YAML/JSON file.
    - Investigate migrating to a `dataclass` if flexibility is required.
    - Implement automatic detection of unexpected columns with logging alerts.
"""

from collections import namedtuple
import pandas as pd
import json  # You can replace this with yaml for YAML config files
from redcap_eda.logger import logger

# Define NamedTuple for Schema: namedtuple(<"name">, [<"field">, <"names">, <"act_as">, "<keys>"])
# Values are assigned later
Schema = namedtuple(
    "Schema",
    ["datetime", "time", "string", "category", "integer", "float", "object"],
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
    try:
        if schema_file:
            logger.info(f"📥 Loading schema from file: {schema_file}")
            with open(schema_file) as f:
                schema_data = json.load(
                    f,
                )  # Replace with yaml.safe_load(f) if using YAML
            return Schema(**schema_data)

        logger.info("📝 Using default schema for type enforcement.")

        schema = Schema(
            datetime=(
                "dob",
                "surgery_date",
                "date_dmy",
                "date_mdy",
                "date_ymd",
                "datetime_dmyhm",
                "datetime_mdyhm",
                "datetime_ymdhm",
                "datetime_dmyhms",
                "datetime_mdyhms",
                "datetime_ymdhms",
            ),
            time=("time",),
            string=("email", "phone", "notes", "unvalidated_text"),
            category=("dropdown_character", "dropdown_mixed"),
            integer=("checkbox___1", "checkbox___2", "yes_no", "true_false"),
            float=("bmi", "age_at_survey"),
            object=("signature_draw", "file_upload"),
        )
        # 🚨 Detect if any field is mistakenly set as a string instead of a tuple
        for field_name in schema._fields:
            if isinstance(getattr(schema, field_name), str):
                raise TypeError(
                    f"❌ Schema definition error: '{field_name}' must be a tuple, but it's a string!",
                )

        return schema

    except Exception as e:
        logger.critical(f"❌ CRITICAL: Error loading schema: {e}")
        raise


def enforce_schema(df, schema=None):
    """
    Applies predefined data types to columns based on a NamedTuple schema.

    - Raises an error if any column has an invalid format.
    - Does not handle data cleaning—assumes input is already cleaned.
    - Ensures all `object` columns are converted to an explicit type.
    - Logs critical issues when data does not conform.

    Args:
        df (pd.DataFrame): The input DataFrame.
        schema (Schema, optional): Preloaded schema. If None, loads a default schema.

    Returns:
        pd.DataFrame, pd.DataFrame: The mutated DataFrame and a receipt of changes.
    """

    try:
        if schema is None:
            schema = load_schema()

        logger.info("🔍 Analyzing DataFrame types before conversion...")
        before = df.dtypes.copy()

        # Track object columns that should have been converted
        untyped_columns = set(df.select_dtypes(include=["object"]).columns)

        # Iterate over schema and apply transformations
        for field_name in schema._fields:
            for col in getattr(schema, field_name):
                if col in df.columns:
                    logger.debug(f"🔄 Converting '{col}' to {field_name} type.")

                    try:
                        match field_name:
                            case "datetime":
                                df[col] = pd.to_datetime(df[col], errors="raise")
                            case "time":
                                df[col] = pd.to_datetime(
                                    df[col],
                                    format="%H:%M",
                                    errors="raise",
                                ).dt.time
                            case "string":
                                df[col] = df[col].astype("string")
                            case "category":
                                df[col] = df[col].astype("category")
                            case "integer":
                                df[col] = df[col].astype("int64")
                            case "float":
                                df[col] = df[col].astype("float64")
                            case "object":
                                # Explicitly allow these columns to remain as `object`
                                logger.debug(
                                    f"✅ Allowed column '{col}' to remain as object.",
                                )

                        # Remove from untyped list after successful processing
                        untyped_columns.discard(col)

                    except Exception as e:
                        logger.critical(
                            f"❌ CRITICAL: Failed to convert column '{col}' to {field_name}. Possible invalid data format. Error: {e}",
                        )
                        raise

        # Final validation: Ensure no unexpected `object` columns remain
        expected_objects = set(schema.object) if hasattr(schema, "object") else set()
        unexpected_objects = untyped_columns - expected_objects

        if unexpected_objects:
            logger.warning(
                "⚠️ The following columns remain untyped (object type detected) but were not explicitly listed in the schema:\n%s",
                list(unexpected_objects),
            )

        # Create mutation receipt
        receipt = pd.DataFrame({"Before": before, "After": df.dtypes})

        logger.info("\n📜 Data Type Conversion Summary:\n%s", receipt.to_string())

        return df, receipt

    except Exception as e:
        logger.critical(f"❌ CRITICAL: Error during schema enforcement: {e}")
        raise
