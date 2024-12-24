# EconomyShopGUI Configuration Generator

This program processes CSV files containing Minecraft shop prices, located in the `csv` folder, and generates configurations for the EconomyShopGUI plugin, saving them to the `output` folder.

## Requirements for CSV Files

- **Columns:**
  - The CSV files should contain the following columns: `Material`, `Buy`, and `Sell` (case-insensitive).

- **Material Column:**
  - This column specifies the in-game item name, e.g., `ENDER_PEARL`.
  - The case of the letters is ignored.
  - Spaces between words are replaced with underscores (`_`).
  - Unnecessary characters are stripped using the `strip()` method.

- **Buy and Sell Prices:**
  - If the buy or sell price is less than or equal to 0, or left empty (`''`), the respective action (buying or selling) will be disabled by setting the value to `-1`.

- **Price Formatting:**
  - Prices must be properly formatted for conversion to integers or floating-point numbers.
  - Any `$` symbols are removed.
  - Commas (`,`) are replaced with periods (`.`).

- **Delimiter:**
  - CSV files must use a semicolon (`;`) as the delimiter.

## Usage
1. Place your CSV files in the `csv` folder.
2. Run the program.
3. The output configurations will be available in the `output` folder.