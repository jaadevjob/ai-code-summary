# Project Overview

The idea behind this project is to create a simple way for developers like you to get a better understanding of what's going on in a repository, without having to dig through mountains of code. Just input a URL, and you'll get a concise summary of the repository's purpose, functionality, and recent changes - all in plain English!


This project is still in its early stages, but I'm excited to see where it goes from here. If you're interested in contributing or just want to take a peek at what I've got so far, feel free to dive in and explore the code. Let me know if you have any questions or suggestions - I'd love to hear them!"

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

Environmental variables are crucial for configuring the application without hard-coding sensitive information, such as API keys and service endpoints, directly into the source code. This approach enhances security and flexibility, allowing for easy adjustments to the application's configuration without the need to modify the codebase. In this project, the environmental variables are defined to configure the integration with Azure's OpenAI services.

To set up these variables:

1. Locate the `example.env` file in the project directory.
2. Rename `example.env` to [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fworkspaces%2Fai-code-summary%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/workspaces/ai-code-summary/.env") to make it the active environment file.
3. Open the [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fworkspaces%2Fai-code-summary%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/workspaces/ai-code-summary/.env") file and update it with the required information:
   - `AZURE_OPENAI_API_BASE`: The base URL for the Azure OpenAI API.
   - `AZURE_OPENAI_DEPLOYMENT`: The specific deployment or resource identifier for your Azure OpenAI instance.
   - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key, used for authenticating requests to the service.
   - `OPENAI_API_VERSION`: The version of the OpenAI API you are targeting, ensuring compatibility with the features and syntax used in your application.

Ensure that the [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fworkspaces%2Fai-code-summary%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/workspaces/ai-code-summary/.env") file is never committed to version control to protect your API keys and other sensitive information from exposure.

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