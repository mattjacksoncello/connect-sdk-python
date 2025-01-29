# Usage

## Creating a Connect API Client

The SDK provides both synchronous and asynchronous clients. Each type has two creation methods:

### Synchronous Client

```python
from onepasswordconnectsdk.client import (
    Client,
    new_client_from_environment,
    new_client
)

# Create client using environment variables
connect_client: Client = new_client_from_environment()

# Create client with explicit configuration
connect_client: Client = new_client(
    "{1Password_Connect_Host}",
    "{1Password_Connect_API_Token}")

# Create client with additional httpx options
connect_client: Client = new_client(
    "{1Password_Connect_Host}",
    "{1Password_Connect_API_Token}",
    verify="path/to/certificate.pem",  # SSL certificate
    timeout=30.0,                      # Custom timeout
    proxies={"http://": "http://proxy.example.com"})  # Proxy configuration
```

### Asynchronous Client

```python
from onepasswordconnectsdk.async_client import (
    AsyncClient,
    new_async_client_from_environment,
    new_async_client
)

# Create async client using environment variables
async_client: AsyncClient = new_async_client_from_environment()

# Create async client with explicit configuration
async_client: AsyncClient = new_async_client(
    "{1Password_Connect_Host}",
    "{1Password_Connect_API_Token}")

# Create async client with additional httpx options
async_client: AsyncClient = new_async_client(
    "{1Password_Connect_Host}",
    "{1Password_Connect_API_Token}",
    verify="path/to/certificate.pem",  # SSL certificate
    timeout=30.0,                      # Custom timeout
    proxies={"http://": "http://proxy.example.com"})  # Proxy configuration
```

## Client Configuration

The SDK provides a `ClientConfig` class that allows you to configure the underlying httpx client. This includes SSL certificate verification and all other httpx client options.

### SSL Certificate Verification

When connecting to a 1Password Connect server using HTTPS, you may need to configure SSL certificate verification:

```python
from onepasswordconnectsdk.config import ClientConfig

# Verify SSL using a custom CA certificate
config = ClientConfig(cafile="path/to/ca.pem")
client = new_client("https://connect.example.com", "your-token", config=config)

# Disable SSL verification (not recommended for production)
config = ClientConfig(verify=False)
client = new_client("https://connect.example.com", "your-token", config=config)
```

### Additional Configuration Options

The ClientConfig class accepts all httpx client options as keyword arguments. These options are passed directly to the underlying httpx client:

```python
# Configure timeouts and redirects
config = ClientConfig(
    cafile="path/to/ca.pem",
    timeout=30.0,              # 30 second timeout
    follow_redirects=True,     # Follow HTTP redirects
    max_redirects=5           # Maximum number of redirects to follow
)

# Configure proxy settings
config = ClientConfig(
    proxies={
        "http://": "http://proxy.example.com",
        "https://": "https://proxy.example.com"
    }
)

# Configure custom headers
config = ClientConfig(
    headers={
        "User-Agent": "CustomApp/1.0",
        "X-Custom-Header": "value"
    }
)
```

### Async Client Configuration

The same configuration options work for both synchronous and asynchronous clients:

```python
config = ClientConfig(
    cafile="path/to/ca.pem",
    timeout=30.0
)
async_client = new_client("https://connect.example.com", "your-token", is_async=True, config=config)
```

For a complete list of available configuration options, see the [httpx client documentation](https://www.python-httpx.org/api/#client).

## Environment Variables

- **OP_CONNECT_TOKEN** – The token to be used to authenticate with the 1Password Connect API.
- **OP_CONNECT_HOST** - The hostname of the 1Password Connect API.
  Possible values include:
  - `http(s)://connect-api:8080` if the Connect server is running in the same Kubernetes cluster as your application.
  - `http://localhost:8080` if the Connect server is running in Docker on the same host.
  - `http(s)://<ip>:8080` or `http(s)://<hostname>:8080` if the Connect server is running on another host.
- **OP_VAULT** - The default vault to fetch items from if not specified.


## Working with Vaults

```python
# Get a list of all vaults
vaults = connect_client.get_vaults()

# Get a specific vault
vault = connect_client.get_vault("{vault_id}")
vault_by_title = connect_client.get_vault_by_title("{vault_title}")
```

## Working with Items

```python
from onepasswordconnectsdk.models import (Item, ItemVault, Field)

vault_id = "{vault_id}"

# Get a list of all items in a vault
items = connect_client.get_items("{vault_id}")

# Create an item
new_item = Item(
    title="Example Login Item",
    category="LOGIN",
    tags=["1password-connect"],
    fields=[Field(value="new_user", purpose="USERNAME")],
)

created_item = connect_client.create_item(vault_id, new_item)

# Get an item
item = connect_client.get_item("{item_id}", vault_id)
item_by_title = connect_client.get_item_by_title("{item_title}", vault_id)

# Update an item
created_item.title = "New Item Title"
updated_item = connect_client.update_item(created_item.id, vault_id, created_item)

# Delete an item
connect_client.delete_item(updated_item.id, vault_id)
```

### Working with Items that contain files

```python
item_id = "{item_id}"
vault_id = "{vault_id}"

# Get summary information on all files stored in a given item
files = connect_client.get_files(item_id, vault_id)

# Get a file's contents
file = connect_client.get_file_content(files[0].id, item_id, vault_id)

# Download a file's contents
connect_client.download_file(files[1].id, item_id, vault_id, "local/path/to/file")
```

## Load Configuration

Users can create `classes` or `dicts` that describe fields they wish to get the values from in 1Password. Two convenience methods are provided that will handle the fetching of values for these fields:

- **load_dict**: Takes a dictionary with keys specifying the user desired naming scheme of the values to return. Each key's value is a dictionary that includes information on where to find the item field value in 1Password. This returns a dictionary of user specified keys with values retrieved from 1Password.
- **load**: Takes an object with class attributes annotated with tags describing where to find desired fields in 1Password. Manipulates given object and fills attributes in with 1Password item field values.

```python
# example dict configuration for onepasswordconnectsdk.load_dict(connect_client, CONFIG)
CONFIG = {
    "server": {
        "opitem": "My database item",
        "opfield": "specific_section.hostname",
        "opvault": "some_vault_id",
    },
    "database": {
        "opitem": "My database item",
        "opfield": ".database",
    },
    "username": {
        "opitem": "My database item",
        "opfield": ".username",
    },
    "password": {
        "opitem": "My database item",
        "opfield": ".password",
    },
}

values_dict = onepasswordconnectsdk.load_dict(connect_client, CONFIG)
```

```python
# example class configuration for onepasswordconnectsdk.load(connect_client, CONFIG)
class Config:
    server: 'opitem:"My database item" opvault:some_vault_id opfield:specific_section.hostname' = None
    database: 'opitem:"My database item" opfield:.database' = None
    username: 'opitem:"My database item" opfield:.username' = None
    password: 'opitem:"My database item" opfield:.password' = None

CONFIG = Config()

values_object = onepasswordconnectsdk.load(connect_client, CONFIG)
```

## Using the Async Client

The async client provides the same functionality as the sync client but with async/await syntax:

```python
import asyncio
from onepasswordconnectsdk.async_client import AsyncClient, new_async_client

async def main():
    # Create async client with optional httpx configuration
    async_client: AsyncClient = new_async_client(
        "{1Password_Connect_Host}",
        "{1Password_Connect_API_Token}",
        timeout=30.0  # Optional httpx configuration
    )

    try:
        # Use the client
        vaults = await async_client.get_vaults()
        item = await async_client.get_item("{item_id}", "{vault_id}")
        # Do something with vaults and item
    finally:
        # Always close the client when done
        await async_client.session.aclose()

asyncio.run(main())
```