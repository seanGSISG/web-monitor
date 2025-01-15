# Web Monitor

This project is a Python application that automatically monitors the availability of the GeForce RTX 5090 on Best Buy's website. It checks the product's availability every 30 seconds and handles logins and checkouts using web scraping and browser automation techniques.

## Features

- Monitors product availability on Best Buy.
- Checks every 30 seconds.
- Handles user logins and checkout processes.
- Utilizes `requests`, `BeautifulSoup`, and `selenium` libraries.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd web-monitor
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Configure your credentials in `src/config.py`.
2. Run the application:
   ```
   python src/main.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.