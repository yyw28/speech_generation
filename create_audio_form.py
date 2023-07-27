from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from typing import List

TOKEN_PATH: str = "/Users/ghaz/token.json"
CREDENTIALS_PATH: str = "/Users/ghaz/credentials.json"
SHEET_ID: str = "1N8kSvMdok7eMJMe091R6YzFmgbTyt-iFii-PGdfp0Gs" # get from url


def get_credentials() -> any:
    global TOKEN_PATH
    SCOPES: List[str] = ["https://www.googleapis.com/auth/spreadsheets.readonly",
                         "https://www.googleapis.com/auth/forms.body"]
    store = file.Storage(TOKEN_PATH)
    creds = None

    if not creds or creds.invalid:
        global CREDENTIALS_PATH
        flow = client.flow_from_clientsecrets(CREDENTIALS_PATH, SCOPES)
        creds = tools.run_flow(flow, store)

    return creds


def get_sheets_service(creds: any) -> any:
    return discovery.build('sheets', 'v4', http=creds.authorize(Http()))


def get_forms_service(creds: any) -> any:
    DISCOVERY_DOC: str = "https://forms.googleapis.com/$discovery/rest?version=v1"

    return discovery.build('forms', 'v1', http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)


def get_sheet_hyperlinks(sheets_service: any, sheet_id: str) -> List[str]:
    results = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,  range='Sheet1', valueRenderOption='FORMULA').execute()
    values = results.get('values', [])

    hyperlinks: List[str] = []

    for value in values:
        current_formula: str = value[0]
        hyperlink_string: str = current_formula[11:len(
            current_formula)-2].split(",")[0]
        hyperlinks.append(hyperlink_string[1:len(hyperlink_string)-1])

    return hyperlinks


def create_audio_form(forms_service: any, hyperlinks: List[str]) -> str:
    FORM = {
        "info": {
            "title": "Audio Survey Form"
        }
    }

    form_app = forms_service.forms()
    form = form_app.create(body=FORM).execute()
    form_id: str = form.get("formId")
    
    # https://developers.google.com/forms/api/guides/update-form-quiz

    for index, hyperlink in enumerate(hyperlinks):
        question_request: dict[str, any] = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": f"Rate the following audio on a scale from robotic to human. Link: {hyperlink}",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Fully Robotic"},
                                        {"value": "Somewhat Robotic"},
                                        {"value": "Not Sure"},
                                        {"value": "Human Like"},
                                        {"value": "Fully Human"},
                                    ],
                                    "shuffle": False
                                }
                            }
                        },
                    },
                    "location": {
                        "index": index
                    }
                }
            }]
        }

        forms_service.forms().batchUpdate(formId=form_id, body=question_request).execute()

    return forms_service.forms().get(formId=form_id).execute()["responderUri"]


if __name__ == '__main__':
    creds = get_credentials()
    sheets_service = get_sheets_service(creds)
    hyperlinks: List[str] = get_sheet_hyperlinks(sheets_service, SHEET_ID)

    forms_service = get_forms_service(creds)
    print("Generated link:", create_audio_form(forms_service, hyperlinks))
