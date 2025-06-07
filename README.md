# LinkedAuto: Automate Your LinkedIn Connections 🤝

![LinkedAuto Logo](https://img.shields.io/badge/LinkedAuto-automate%20your%20LinkedIn%20connections-blue?style=for-the-badge)

Welcome to **LinkedAuto**, a Python tool designed to simplify your LinkedIn networking. With LinkedAuto, you can automatically send connection requests based on your chosen keywords. This tool leverages the power of Selenium to navigate LinkedIn and perform actions on your behalf, saving you time and effort in expanding your professional network.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- **Automated Connection Requests**: Send multiple connection requests without manual effort.
- **Keyword Search**: Specify keywords to find potential connections that match your interests.
- **User-Friendly**: Simple setup and easy to use, even for those new to Python or automation.
- **Customizable**: Modify the script to fit your specific needs and preferences.
- **Selenium Integration**: Utilizes Selenium WebDriver for smooth interaction with the LinkedIn interface.

## Installation

To get started with LinkedAuto, follow these steps:

1. **Clone the Repository**: Open your terminal and run:
   ```bash
   git clone https://github.com/ImfundoKahle/linkedauto.git
   ```

2. **Navigate to the Directory**:
   ```bash
   cd linkedauto
   ```

3. **Install Required Packages**: Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download ChromeDriver**: Ensure you have the correct version of ChromeDriver that matches your Chrome browser version. You can download it from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads).

5. **Set Up Your LinkedIn Credentials**: Open the script and enter your LinkedIn login details.

## Usage

To use LinkedAuto, execute the following command in your terminal:

```bash
python linkedauto.py
```

### Step-by-Step Instructions:

1. **Launch the Script**: After running the script, it will open a Chrome window.
2. **Log in to LinkedIn**: Enter your LinkedIn credentials if prompted.
3. **Enter Keywords**: Provide the keywords you want to search for potential connections.
4. **Set Connection Limit**: Specify how many connection requests you want to send.
5. **Start Automation**: The script will handle the rest, sending connection requests based on your criteria.

For the latest releases and updates, visit [Releases](https://github.com/ImfundoKahle/linkedauto/releases). Download the latest version and execute it to get started.

## How It Works

LinkedAuto uses Selenium WebDriver to automate the process of sending connection requests on LinkedIn. Here’s a breakdown of how it operates:

1. **Selenium Setup**: The script initializes a Selenium WebDriver instance, which controls a Chrome browser.
2. **Login Process**: It navigates to the LinkedIn login page, inputs your credentials, and logs in.
3. **Search Functionality**: The script performs a search based on the specified keywords, retrieving profiles that match.
4. **Sending Requests**: It iterates through the search results, sending connection requests to each profile.
5. **Error Handling**: If it encounters any issues, the script logs the errors for review.

### Example Workflow

- **User Input**: The user specifies keywords like "Software Engineer" or "Data Scientist."
- **Automated Actions**: LinkedAuto finds profiles matching these keywords and sends connection requests.
- **Results**: Users can check their LinkedIn account to see new connection requests sent.

## Contributing

We welcome contributions to improve LinkedAuto. If you want to contribute, please follow these steps:

1. **Fork the Repository**: Click the "Fork" button at the top right of this page.
2. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Make Changes**: Implement your changes and test them thoroughly.
4. **Commit Your Changes**:
   ```bash
   git commit -m "Add your message here"
   ```
5. **Push to Your Branch**:
   ```bash
   git push origin feature/YourFeature
   ```
6. **Open a Pull Request**: Submit your pull request for review.

## License

LinkedAuto is open-source software licensed under the MIT License. You can use, modify, and distribute this tool freely, as long as you include the original license.

## Support

If you encounter any issues or have questions, please check the [Issues](https://github.com/ImfundoKahle/linkedauto/issues) section. You can also reach out through the repository for assistance.

For the latest updates and releases, please visit [Releases](https://github.com/ImfundoKahle/linkedauto/releases). Download the latest version and execute it to start automating your LinkedIn connections.

## Conclusion

LinkedAuto provides a straightforward way to expand your LinkedIn network efficiently. By automating connection requests, you can focus on what truly matters: building meaningful professional relationships. 

Feel free to explore the code, suggest improvements, and help us make LinkedAuto even better!