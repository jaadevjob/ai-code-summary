# Project Overview

This project is a comprehensive solution designed to streamline and enhance the process of generating summaries for code repositories. It leverages a variety of technologies and frameworks to provide a user-friendly interface for inputting repository URLs and receiving detailed, understandable summaries of the code's purpose, functionality, and recent changes.

## Features

- **Code Summary Generation**: Users can input a repository URL, and the system will generate a detailed summary of the repository's purpose, functionality, and the impact of the most recent changes.
- **Language Support**: The application supports translating the summary into multiple languages, including English, Spanish, French, German, and even Klingon, making it accessible to a wider audience.
- **PDF Download**: Users have the option to download the generated summary as a PDF document for offline viewing or sharing.
- **Responsive Design**: The application is built with a responsive design, ensuring it is accessible on various devices and screen sizes.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework used to serve the web application.
- **GitPython**: Utilized for interacting with Git repositories, enabling the cloning and analysis of repository contents.
- **LangChain**: A suite of tools and libraries for working with language models, used in generating summaries.
- **Bootstrap**: For styling and creating a responsive design.

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up the environment variables as specified in the `.env` file template.
4. Run the Flask application using `python app.py`.

### Environmental Variables

```
# LangChain Azure OpenAI
AZURE_OPENAI_API_BASE=""
AZURE_OPENAI_DEPLOYMENT=""
AZURE_OPENAI_API_KEY="" 
OPENAI_API_VERSION="2023-05-15"

```

## Usage

Navigate to the hosted web application, enter the URL of the repository you wish to summarize in the provided input field, and click "Generate Summary". The application will process the request and display the summary, which can then be translated or downloaded as needed.

## Security

Please ensure that your `.env` file is not committed to your repository, as it contains sensitive API keys and configuration settings. The `.gitignore` file has been configured to exclude this file from commits.

## Contribution

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request for review.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.