import json

from cryptography.fernet import Fernet
from django.core.signing import Signer

# Random name, hopefully add more security
ENC_KEY = "qp10zm"
DATA_KEY = "al29SK"


def save_auth_credentials(request, username, password):
    """
    Save auth credentials to session for seamless region change
    """
    cred = {
        'username': username,
        'password': password
    }
    key = Fernet.generate_key()
    fernet = Fernet(key)
    cred_json = json.dumps(cred)
    cred_encrypted = fernet.encrypt(cred_json.encode())


    # Save encrypted credentials to session. cred_encrypted is a byte
    request.session[ENC_KEY] = key.decode()
    request.session[DATA_KEY] = cred_encrypted


def get_auth_credentials(request):
    """
    Get auth credentials saved in session to re login with different region
    """
    key = request.session[ENC_KEY]
    session_cred = request.session[DATA_KEY]
    # Key must be byte, so encode it
    fernet = Fernet(key.encode())
    # Decrypt credentials and decode from byte to str
    cred_json = fernet.decrypt(session_cred).decode()
    # Convert to dictionary
    cred = json.loads(cred_json)
    return cred
