# You can find the credentials listing script here: 
#   https://github.com/2digitsleft/gcp-api-easy-access-credential-listing
from gcp-api-easy-access-credential-listing import get_google_slides_service

# used libraries
import argparse, os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from openai import OpenAI
from loguru import logger

# Configure the Argument Parser
parser = argparse.ArgumentParser(
                    prog='Translate GWS Presos',
                    description='The programm translates Goowlgle Workspace slide decks with OpenAI models.',
                    epilog='Thanks for using one of 2digitsLeft|s tools for Google Workspace!')
parser.add_argument('-p', '--presentation-id', required=True)
parser.add_argument('-s', '--source-language', default='EN')
parser.add_argument('-t', '--target-language', default='DE')
parser.add_argument('-g', '--gpt-model', default='gpt-3.5-turbo')
parser.add_argument('-l', '--log-level', default='INFO')
args = parser.parse_args()

# Start logger instance
logger.add("gws-translate-slides.log", format="{time} {level} {message}", level=args.log_level, rotation="10 MB", compression="zip", colorize=True)
logger.info("Starting gws-translate-slides.py")

# The ID of your presentation
if args.presentation_id:
    PRESENTATION_ID = args.presentation_id

# OpenAI Model Version & prompt
MODEL_VERSION = args.gpt_model
SYSTEM_MSG = ""
logger.info("OpenAI model is " + MODEL_VERSION + "-mode")

# OpenAI API Key
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

if OPENAI_API_KEY == '':
    logger.critical("ERROR: OpenAI API Key not found!")
else:
    try :
        client = OpenAI(api_key=OPENAI_API_KEY)
        logger.success("OpenAI key found and client instanciated!")
    except KeyError: 
        logger.critical("Instantiating client was not successful!")
        exit()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/presentations']

# Set the Translation Source and Target Language
SOURCE_LANGUAGE = args.source_language
TARGET_LANGUAGE = args.target_language

def set_translation_language(target_language):

    # Return the name of a language to an ISO code provided by the user
    # (e.g., 'es' for Spanish)
    language_codes = {
        'EN': 'English',
        'ES': 'Spanish',
        'FR': 'French',
        'DE': 'German',
        'IT': 'Italian',
        'JP': 'Japanese',
        'KO': 'Korean',
        'PT': 'Portuguese',
        'RU': 'Russian',
        'CN': 'Chinese'
    }   
    return language_codes[target_language]

def translate_text(source_text, source_language, target_language, model_to_use):
        
    SYSTEM_MSG = 'You are a professional translator for translating text from ' + source_language + ' to ' + target_language + '. Only provide the translation to the target language as a reply to the user message. Do not extend the reply by information, which is not included in the original text. Keep Linefeeds '
  
    # Set the main system message to set the context for chatGPT
    user_msg = source_text
    if len(source_text) > 2:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system", "content": SYSTEM_MSG
                    },
                {
                    "role": "user", "content": user_msg
                    }
            ],
            model=model_to_use,
            max_tokens=500
        )
    # stop: API returned complete model output
    # length: Incomplete model output due to max_tokens parameter or token limit
    # content_filter: Omitted content due to a flag from our content filters
    # null: API response still in progress or incomplete
        if response.choices[0].finish_reason != "stop":
            logger.warning("Model output may be incomplete!")
        elif response.choices[0].finish_reason == "length":
            logger.warning("Model output may be incomplete due to max_tokens parameter or token limit!")
        elif response.choices[0].finish_reason == "content_filter":
            logger.warning("Model output may be incomplete due to a flag from our content filters!")
        elif response.choices[0].finish_reason == "null":
            logger.warning("API response still in progress or incomplete!")
        return str(response.choices[0].message.content)
    else:
        return " "


def update_text(service, presentation_id, target_language):
    """
    Updates the text content in the slides of a presentation with translated text.

    Args:
        service: The Google Slides service object.
        presentation_id: The ID of the presentation to update.
        target_language: The target language for translation.

    Returns:
        The response from the batch update request.

    Raises:
        None.
    """
    slides = service.presentations().get(presentationId=presentation_id).execute().get('slides', [])

    requests = []
    for slide in slides:
        number_of_elements = 1
        for element in slide.get('pageElements', []):
            shape_id = element['objectId']
            if args.log_level == 'INFO':
                logger.info("Shapes read: " + str(number_of_elements))
            elif args.log_level == 'DEBUG':
                logger.debug("ShapeID:" + shape_id)
            if 'shape' in element:
                shape = element['shape']
                if 'text' in shape:
                    text_content = shape['text']['textElements']
                    for text_element in text_content:
                        if 'textRun' in text_element:
                            
                            if len(text_element['textRun']['content']) > 2:

                                original_text = text_element['textRun']['content']
                                
                                # Trasnlate the text to the given language
                                translated_text = translate_text(original_text, set_translation_language(SOURCE_LANGUAGE), set_translation_language(TARGET_LANGUAGE), MODEL_VERSION)

                                # Some output for debugging
                                if args.log_level == 'DEBUG':
                                    logger.debug("Response: " + translated_text)
                                    logger.debug("Original:" + original_text + "<-")
                                    logger.debug("Length: " + str(len(text_element['textRun']['content'])))
                                    logger.debug("Translation:" + translated_text + "<-")

                                if original_text != translated_text:
                                    requests.append(
                                        {
                                            "replaceAllText": {
                                                "pageObjectIds": slide['objectId'],
                                                "replaceText": translated_text,
                                                "containsText": { 
                                                    "matchCase": True, 
                                                    "text": original_text 
                                                    }
                                            }
                                            }
                                    )   
            number_of_elements += 1
    if requests:
        body = {
            'requests': requests
        }
        response = service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
        return response
    else:
        logger.critical("No text replacements found.")
        exit()

def main():

    service = get_google_slides_service()

    # Get the file name of the prsentation
    file_name = service.presentations().get(presentationId=PRESENTATION_ID).execute().get('title')
    logger.info("Presentation file is |" + file_name + "| .")

    # Set the Translation Source and Target Language
    logger.info("Source Language is set to " + set_translation_language(SOURCE_LANGUAGE) + " and target language is set to " + set_translation_language(TARGET_LANGUAGE) + "}!")
    
    response = update_text(service, PRESENTATION_ID, TARGET_LANGUAGE)

if __name__ == '__main__':
    main()
