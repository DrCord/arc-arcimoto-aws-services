import getpass

from arcimoto_aws_services import cognito
from arcimoto_aws_services.aws_service import AwsService

DEFAULT_CLIENT_ID = '5onspj4jo1ors18t8cih8lpn30'


def authenticate(username, client_id):
    ''' this is outside the class to preserve the existing API with modules '''

    password = getpass.getpass()
    CognitoAuthenticateObject = CognitoAuthenticate(client_id)

    return CognitoAuthenticateObject.authenticate_non_interactive(username, password)


class CognitoAuthenticate(AwsService):

    auth_result = None
    client_id = None
    client_local = None
    password = None
    session = None
    username = None

    def __init__(self, client_id=cognito.DEFAULT_CLIENT_ID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id

    def authenticate_non_interactive(self, username, password):

        self.password = password
        self.username = username

        auth_response = self.initiate_auth(self.client_id, self.username, self.password)

        self.auth_result = auth_response.get('AuthenticationResult', None)
        if self.auth_result is not None:
            return self.auth_result.get('IdToken', None)

        challenge = auth_response.get('ChallengeName', None)
        self.session = auth_response.get('Session', None)
        while challenge is not None:
            challenge = self.challenge_respond(challenge)

        if self.auth_result is None:
            raise Exception('Failed to authenticate')

        return self.auth_result.get('IdToken', None)

    def challenge_respond(self, challenge):
        if challenge == 'NEW_PASSWORD_REQUIRED':
            challenge = self.challenge_respond_new_password_required_interactive(challenge)
        elif challenge == 'SMS_MFA':
            challenge = self.challenge_respond_sms_mfa_interactive(challenge)
        elif challenge == 'SOFTWARE_TOKEN_MFA':
            challenge = self.challenge_respond_software_token_mfa_interactive(challenge)
        else:
            raise ValueError(f"Challenge type '{challenge}' not handled!")

        return challenge

    def challenge_respond_new_password_required(self, challenge, new_password):
        responses = {
            'USERNAME': self.username,
            'NEW_PASSWORD': new_password
        }
        challenge_response = self.respond_to_auth_challenge(self, challenge, responses)
        self.auth_result = challenge_response.get('AuthenticationResult', None)
        if self.auth_result is None:
            challenge = challenge_response.get('ChallengeName', None)
            self.session = challenge_response.get('Session', None)
        else:
            challenge = None

        return challenge

    def challenge_respond_new_password_required_interactive(self, challenge):
        print('Password reset is required')
        new_password = None
        while new_password is None:
            new_password = getpass.getpass('Enter new password:')
            new_password_verify = getpass.getpass('RE-enter password:')
            if new_password != new_password_verify:
                new_password = None
                print('Passwords don\'t match. Try again.')
        return self.challenge_respond_new_password_required(challenge, new_password)

    def challenge_respond_sms_mfa(self, challenge, mfa):
        responses = {
            'USERNAME': self.username,
            'SMS_MFA_CODE': mfa
        }
        challenge_response = self.respond_to_auth_challenge(self, challenge, responses)
        self.auth_result = challenge_response.get('AuthenticationResult', None)
        if self.auth_result is None:
            challenge = challenge_response.get('ChallengeName', None)
            self.session = challenge_response.get('Session', None)
        else:
            challenge = None

        return challenge

    def challenge_respond_sms_mfa_interactive(self, challenge):
        mfa = getpass.getpass('SMS MFA Required:')
        return self.challenge_respond_sms_mfa(challenge, mfa)

    def challenge_respond_software_token_mfa(self, challenge, mfa):
        responses = {
            'USERNAME': self.username,
            'SOFTWARE_TOKEN_MFA_CODE': mfa
        }
        challenge_response = self.respond_to_auth_challenge(challenge, responses)
        self.auth_result = challenge_response.get('AuthenticationResult', None)
        if self.auth_result is None:
            challenge = challenge_response.get('ChallengeName', None)
            self.session = challenge_response.get('Session', None)
        else:
            challenge = None

        return challenge

    def challenge_respond_software_token_mfa_interactive(self, challenge):
        mfa = getpass.getpass('SOFTWARE TOKEN MFA Required:')
        return self.challenge_respond_software_token_mfa(challenge, mfa)

    def client_init(self):
        return super().client_init('cognito-idp')

    def initiate_auth(self, client_id, username, password):
        response = self.client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        self.client_close()
        return response

    def respond_to_auth_challenge(self, challenge, responses):
        response = self.client.respond_to_auth_challenge(
            ClientId=self.client_id,
            ChallengeName=challenge,
            ChallengeResponses=responses,
            Session=self.session
        )
        self.client_close()
        return response
