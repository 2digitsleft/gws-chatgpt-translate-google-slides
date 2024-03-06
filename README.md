# gws-chatgpt-translate-google-slides

**Important:** This script makes use of the "gcp-api-easy-access-credential-listing" script to easily select the API and credentials file for authentication to the GWS API. Download it, and put it into the same folder, follow instructions in the "gcp-api-easy-access-credential-listing" repository to use the script [here](https://github.com/2digitsleft/gcp-api-easy-access-credential-listing). 

## Easily translate GWS Slide Decks: "Slides Translator with Google & chatGPT"
Automate Google Slides translations with this Python script, leveraging OpenAI's GPT for language conversion. Supports customizable source/target languages, logging, and GCP integration for seamless updates to your presentations.

## Introduction
Many preso slide decks from clients, partners, from marketing, product management or architecture that you receive as part of your work are very often in English but are additionally required in the local language (in my case German). Sometimes it's the other way around. When i started working for Asian customers and partners, it has become efficient for me to automatically translate the slides into the desired target language and then edit them manually. This saves a lot of time compared to manual translation per line and object in the slide. Of course, there are already tools for this available on the market, but was a funny challenge for me to follow the rule  "Eat your own dogfood!" and use the tech that GCP/GWS and OpenAI provide.

**Hint:** This setup is only intended to be used for testing, not production releases. It might be required to ask for permission and compliance requirements before using it for company material and slide decks!

## Description
This script is designed to automatically translate the content of Google Workspace slide presentations using OpenAI's GPT model (another version uses Google Gemini, which is eapqaly powerful. I might make it selectable in an updated release). It targets a specific presentation, translates its text content from a source language to a target language, and logs the process. Here's a breakdown of the script's functionality, prerequisites, and usage instructions:

**Main Objective:** Translate text in Google Workspace slide presentations.

**Technologies Used:** Python, Google Cloud Platform (GCP) APIs, OpenAI's GPT, Loguru for logging.

**Process Flow:**
- Configure argument parser for command-line options.
- Initialize logging.
- Authenticate and create a client instance for OpenAI and Google Slides API.
- Define the translation languages and the model to use.
- Read text elements from the presentation slides.
- Translate the text using OpenAI's GPT model.
- Update the presentation with the translated text.

## Prerequisites

- **Python Environment:** Ensure Python is installed on your system.

- **API Keys:** Obtain API keys for both Google Cloud Platform and OpenAI.
    - For GCP, enable the Google Slides API and create credentials (OAuth client ID) for your application. Download the credentials.json file.
    - For OpenAI, sign up and generate an API key from your OpenAI account.

- **Python Libraries:** Install the required Python libraries (google-auth, google-auth-oauthlib, google-api-python-client, openai, loguru, and argparse).

- **Environment Variables:** Set the OPENAI_API_KEY environment variable with your OpenAI API key.

## Usage

1. **Installation of Dependencies:** Install the required Python libraries using pip w/ or w/o the requirements.txt file in the repo.
```pip install google-auth google-auth-oauthlib google-api-python-client openai loguru argparse````

2. **Configuration:**
    - Ensure the `credentials.json` file from GCP is in your working directory or correctly referenced in your code for Google API authentication. In case you are using the gcp-api-easy-access-credential-listing script, it needs to be in the designated folder for Google credential files. described [here](https://github.com/2digitsleft/gcp-api-easy-access-credential-listing). 
    - Set the `OPENAI_API_KEY` environment variable or modify the script to directly assign your OpenAI API key.

3. **Running the Script:**
    - Use the command line to run the script with the required arguments. For example:
    ```python script_name.py --presentation-id 'your_presentation_id' --source-language 'EN' --target-language 'DE'```
    - The `--presentation-id` argument is required. It specifies the ID of the Google Slide presentation you want to translate.
    - Optional arguments allow you to specify source and target languages (default `EN` to `DE`), the OpenAI GPT model version (default `gpt-3.5-turbo`), and the log level (default `INFO`).

## Additional Notes

- **Customization:** You may need to customize the script according to your specific requirements, such as adjusting the source and target languages or modifying the logging setup.

- **Google API Scopes:** The script uses the https://www.googleapis.com/auth/presentations scope for `read-write` access to Google Slides. If you change the scopes, you might need to re-authenticate.

- **Security Considerations:** Keep your API keys secure and do not hard-code them in your scripts. Use the environment variables and the ["gcp-api-easy-access-credential-listing"](https://github.com/2digitsleft/gcp-api-easy-access-credential-listing) script or secure vaults for storing such sensitive information.

This script is designed for developers or users with basic programming and Google Cloud Platform knowledge, aiming to automate translations of Google Slides through a custom Python application.