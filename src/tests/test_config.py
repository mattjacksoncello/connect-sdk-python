import os
import pytest
from httpx import Response, Client, AsyncClient, Timeout
import onepasswordconnectsdk
from onepasswordconnectsdk import client
from onepasswordconnectsdk.config import ClientConfig, AsyncClientConfig
from onepasswordconnectsdk.utils import get_timeout

# Optional cert path for SSL verification in tests
# Set this to a valid cert path if available, otherwise verification will be disabled
CERT_PATH = os.getenv('TEST_CERT_PATH', False)

VAULT_ID = "abcdefghijklmnopqrstuvwxyz"
ITEM_NAME1 = "TEST USER"
ITEM_ID1 = "wepiqdxdzncjtnvmv5fegud4q1"
ITEM_NAME2 = "Another User"
ITEM_ID2 = "wepiqdxdzncjtnvmv5fegud4q2"
HOST = "https://mock_host"
TOKEN = "jwt_token"

# Create client config
client_config = ClientConfig(url=HOST, token=TOKEN)
SS_CLIENT = client.Client(client_config)

USERNAME_VALUE = "new_user"
PASSWORD_VALUE = "password"
HOST_VALUE = "http://somehost"

def test_client_config_initialization():
    """Test ClientConfig initialization and inheritance"""
    config = ClientConfig(url=HOST, token=TOKEN)
    assert isinstance(config, Client)
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.timeout == get_timeout()

def test_async_client_config_initialization():
    """Test AsyncClientConfig initialization and inheritance"""
    config = AsyncClientConfig(url=HOST, token=TOKEN)
    assert isinstance(config, AsyncClient)
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.timeout == get_timeout()

def test_client_config_with_options():
    """Test ClientConfig with httpx options
    
    Examples of certificate configuration:
        # Using a certificate file
        config = ClientConfig(url=HOST, token=TOKEN, verify="path/to/cert.pem")
        
        # Using a certificate bundle
        config = ClientConfig(url=HOST, token=TOKEN, verify="/etc/ssl/certs")
        
        # Disable certificate verification (not recommended for production)
        config = ClientConfig(url=HOST, token=TOKEN, verify=False)
        
        # Custom client certificate
        config = ClientConfig(
            url=HOST,
            token=TOKEN,
            cert=("path/to/client.crt", "path/to/client.key")
        )
    """
    # Test basic options
    custom_timeout = 30.0
    config = ClientConfig(
        url=HOST,
        token=TOKEN,
        timeout=custom_timeout,
        verify=CERT_PATH,  # Use configured cert path or disable verification
        cert=None,         # Client certificate (if needed)
        follow_redirects=True
    )
    assert isinstance(config.timeout, Timeout)
    assert config.timeout == Timeout(custom_timeout)
    # If we got here without an error, the verify parameter was accepted
    assert config.follow_redirects is True


    # Just verify that these configurations are accepted without error
    ClientConfig(
        url=HOST,
        token=TOKEN,
        verify=False  # Disable SSL verification
    )
    
    

def test_async_client_config_with_options():
    """Test AsyncClientConfig with httpx options
    
    Examples of certificate configuration:
        # Using a certificate file
        config = AsyncClientConfig(url=HOST, token=TOKEN, verify="path/to/cert.pem")
        
        # Using a certificate bundle
        config = AsyncClientConfig(url=HOST, token=TOKEN, verify="/etc/ssl/certs")
        
        # Disable certificate verification (not recommended for production)
        config = AsyncClientConfig(url=HOST, token=TOKEN, verify=False)
        
        # Custom client certificate
        config = AsyncClientConfig(
            url=HOST,
            token=TOKEN,
            cert=("path/to/client.crt", "path/to/client.key")
        )
    """
    custom_timeout = 30.0
    config = AsyncClientConfig(
        url=HOST,
        token=TOKEN,
        timeout=custom_timeout,
        verify=CERT_PATH,  # Use configured cert path or disable verification
        cert=None,         # Client certificate (if needed)
        follow_redirects=True
    )
    assert isinstance(config.timeout, Timeout)
    assert config.timeout == Timeout(custom_timeout)
    # If we got here without an error, the verify parameter was accepted
    assert config.follow_redirects is True

    # Just verify that these configurations are accepted without error
    AsyncClientConfig(
        url=HOST,
        token=TOKEN,
        verify=False  # Disable SSL verification
    )
    
    # Note: Client certificate tests are skipped as they require actual certificate files


class Config:
    username: f'opitem:"{ITEM_NAME1}" opfield:.username opvault:{VAULT_ID}' = None
    password: f'opitem:"{ITEM_NAME1}" opfield:section1.password opvault:{VAULT_ID}' = None
    host: f'opitem:"{ITEM_NAME2}" opfield:.host opvault:{VAULT_ID}' = None


CONFIG_CLASS = Config()


def test_client_config_errors():
    """Test ClientConfig error cases"""
    with pytest.raises(TypeError):
        ClientConfig()  # Missing required arguments
    
    with pytest.raises(TypeError):
        ClientConfig(url=HOST)  # Missing token
    
    with pytest.raises(TypeError):
        ClientConfig(token=TOKEN)  # Missing url

def test_async_client_config_errors():
    """Test AsyncClientConfig error cases"""
    with pytest.raises(TypeError):
        AsyncClientConfig()  # Missing required arguments
    
    with pytest.raises(TypeError):
        AsyncClientConfig(url=HOST)  # Missing token
    
    with pytest.raises(TypeError):
        AsyncClientConfig(token=TOKEN)  # Missing url

def test_client_config_headers():
    """Test that client config properly handles headers"""
    config = ClientConfig(
        url=HOST,
        token=TOKEN,
        headers={"Custom-Header": "test"}
    )
    # Headers should be merged, not overwritten
    assert "Custom-Header" in config.headers
    assert config.headers["Custom-Header"] == "test"
    # Authorization header should still be present
    assert "Authorization" in config.headers


def test_load(respx_mock):
    mock_items_list1 = respx_mock.get(f"v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_NAME1}\"").mock(
        return_value=Response(200, json=[item])
    )
    mock_item1 = respx_mock.get(f"v1/vaults/{VAULT_ID}/items/{ITEM_ID1}").mock(return_value=Response(200, json=item))
    mock_items_list2 = respx_mock.get(f"v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_NAME2}\"").mock(
        return_value=Response(200, json=[item2])
    )
    mock_item2 = respx_mock.get(f"v1/vaults/{VAULT_ID}/items/{ITEM_ID2}").mock(return_value=Response(200, json=item2))

    config_with_values = onepasswordconnectsdk.load(SS_CLIENT, CONFIG_CLASS)

    assert mock_items_list1.called
    assert mock_item1.called
    assert mock_items_list2.called
    assert mock_item2.called

    assert config_with_values.username == USERNAME_VALUE
    assert config_with_values.password == PASSWORD_VALUE
    assert config_with_values.host == HOST_VALUE


def test_load_dict(respx_mock):
    config_dict = {
        "username": {
            "opitem": ITEM_NAME1,
            "opfield": ".username",
            "opvault": VAULT_ID
        },
        "password": {
            "opitem": ITEM_NAME1,
            "opfield": "section1.password",
            "opvault": VAULT_ID
        }
    }

    mock_item_list = respx_mock.get(f"v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_NAME1}\"").mock(
        return_value=Response(200, json=[item]))
    mock_item = respx_mock.get(f"v1/vaults/{VAULT_ID}/items/{ITEM_ID1}").mock(return_value=Response(200, json=item))

    config_with_values = onepasswordconnectsdk.load_dict(SS_CLIENT, config_dict)

    assert mock_item_list.called
    assert mock_item.called
    assert config_with_values['username'] == USERNAME_VALUE
    assert config_with_values['password'] == PASSWORD_VALUE


item = {
    "id": ITEM_ID1,
    "title": ITEM_NAME1,
    "vault": {
        "id": VAULT_ID
    },
    "category": "LOGIN",
    "sections": [
        {
            "id": "section1",
            "label": "section1"
        }
    ],
    "fields": [
        {
            "id": "password",
            "label": "password",
            "value": PASSWORD_VALUE,
            "section": {
                "id": "section1"
            }
        },
        {
            "id": "username",
            "label": "username",
            "value": USERNAME_VALUE
        }
    ]
}

item2 = {
    "id": ITEM_ID2,
    "title": ITEM_NAME2,
    "vault": {
        "id": VAULT_ID
    },
    "category": "LOGIN",
    "fields": [
        {
            "id": "716C5B0E95A84092B2FE2CC402E0DDDF",
            "label": "host",
            "value": HOST_VALUE
        }
    ]
}
