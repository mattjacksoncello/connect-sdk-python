"""Tests for client configuration classes"""
import pytest
import httpx
from onepasswordconnectsdk.config import ClientConfig, AsyncClientConfig

HOST = "https://mock_host"
TOKEN = "jwt_token"
CERT_PATH = "/path/to/cert.pem"


def test_client_config_basic():
    """Test basic client configuration"""
    config = ClientConfig(url=HOST, token=TOKEN)
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.certificate is None


def test_client_config_with_certificate():
    """Test client configuration with certificate"""
    config = ClientConfig(url=HOST, token=TOKEN, certificate=CERT_PATH)
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.certificate == CERT_PATH
    assert config.verify == CERT_PATH


def test_client_config_with_timeout():
    """Test client configuration with custom timeout"""
    timeout = httpx.Timeout(10.0, connect=5.0)
    config = ClientConfig(url=HOST, token=TOKEN, timeout=timeout)
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.timeout == timeout


def test_client_config_with_all_options():
    """Test client configuration with multiple options"""
    timeout = httpx.Timeout(10.0)
    limits = httpx.Limits(max_connections=100)
    headers = {"Custom-Header": "value"}
    
    config = ClientConfig(
        url=HOST,
        token=TOKEN,
        certificate=CERT_PATH,
        timeout=timeout,
        limits=limits,
        headers=headers,
        follow_redirects=True
    )
    
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.certificate == CERT_PATH
    assert config.timeout == timeout
    assert config.limits == limits
    assert "Custom-Header" in config.headers
    assert config.follow_redirects is True


def test_async_client_config_basic():
    """Test basic async client configuration"""
    config = AsyncClientConfig(url=HOST, token=TOKEN)
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.certificate is None


def test_async_client_config_with_certificate():
    """Test async client configuration with certificate"""
    config = AsyncClientConfig(url=HOST, token=TOKEN, certificate=CERT_PATH)
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.certificate == CERT_PATH
    assert config.verify == CERT_PATH


def test_async_client_config_with_timeout():
    """Test async client configuration with custom timeout"""
    timeout = httpx.Timeout(10.0, connect=5.0)
    config = AsyncClientConfig(url=HOST, token=TOKEN, timeout=timeout)
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.timeout == timeout


def test_async_client_config_with_all_options():
    """Test async client configuration with multiple options"""
    timeout = httpx.Timeout(10.0)
    limits = httpx.Limits(max_connections=100)
    headers = {"Custom-Header": "value"}
    
    config = AsyncClientConfig(
        url=HOST,
        token=TOKEN,
        certificate=CERT_PATH,
        timeout=timeout,
        limits=limits,
        headers=headers,
        follow_redirects=True
    )
    
    assert config.url == HOST
    assert config.token == TOKEN
    assert config.certificate == CERT_PATH
    assert config.timeout == timeout
    assert config.limits == limits
    assert "Custom-Header" in config.headers
    assert config.follow_redirects is True


def test_client_config_inheritance():
    """Test that ClientConfig properly inherits from httpx.Client"""
    config = ClientConfig(url=HOST, token=TOKEN)
    assert isinstance(config, httpx.Client)


def test_async_client_config_inheritance():
    """Test that AsyncClientConfig properly inherits from httpx.AsyncClient"""
    config = AsyncClientConfig(url=HOST, token=TOKEN)
    assert isinstance(config, httpx.AsyncClient)