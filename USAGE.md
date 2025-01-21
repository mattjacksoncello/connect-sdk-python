# Usage

## Creating a Connect API Client

The SDK provides a flexible configuration system through `ClientConfig` and `AsyncClientConfig` classes. These classes inherit from httpx.Client and httpx.AsyncClient respectively, allowing you to use any configuration options that httpx supports.

### Basic Usage

```python
from onepasswordconnectsdk import new_client
from onepasswordconnectsdk.config import ClientConfig

# Create a client with configuration
config = ClientConfig(
    url="{1Password_Connect_Host}",
    token="{1Password_Connect_API_Token}"
)
client = new_client(config)

# Or use environment variables (OP_CONNECT_TOKEN and OP_CONNECT_HOST)
client = new_client()
```

### Advanced Configuration

```python
# Configure SSL verification
config = ClientConfig(
    url="{1Password_Connect_Host}",
    token="{1Password_Connect_API_Token}",
    certificate="/path/to/custom-ca.pem",  # Custom CA certificate
    verify=False,                          # Disable SSL verification (not recommended for production)
    cert=("/client.crt", "client.key")     # Client certificates for mTLS
)

# Configure timeouts and retries
config = ClientConfig(
    url="{1Password_Connect_Host}",
    token="{1Password_Connect_API_Token}",
    timeout=httpx.Timeout(
        connect=5.0,    # connection timeout
        read=10.0,      # read timeout
        write=5.0,      # write timeout
        pool=10.0       # pool timeout
    ),
    limits=httpx.Limits(
        max_keepalive_connections=5,
        max_connections=10
    )
)

# Configure proxy and other network settings
config = ClientConfig(
    url="{1Password_Connect_Host}",
    token="{1Password_Connect_API_Token}",
    proxies="http://proxy.example.com:8080",
    follow_redirects=True,
    http2=True
)
```

### Async Configuration

```python
from onepasswordconnectsdk.config import AsyncClientConfig

# Create an async client with configuration
async_config = AsyncClientConfig(
    url="{1Password_Connect_Host}",
    token="{1Password_Connect_API_Token}",
    certificate="/path/to/custom-ca.pem",
    timeout=30.0
)
async_client = new_client(async_config)
```
## Environment Variables

These environment variables are used when creating a client without explicit configuration (i.e., when calling `new_client()` with no arguments):

- **OP_CONNECT_TOKEN** – The token to be used to authenticate with the 1Password Connect API.
- **OP_CONNECT_HOST** - The hostname of the 1Password Connect API.
  Possible values include:
  - `http(s)://connect-api:8080` if the Connect server is running in the same Kubernetes cluster as your application.
  - `http://localhost:8080` if the Connect server is running in Docker on the same host.
  - `http(s)://<ip>:8080` or `http(s)://<hostname>:8080` if the Connect server is running on another host.
- **OP_VAULT** - The default vault to fetch items from if not specified.

Note: When using the configuration classes (ClientConfig or AsyncClientConfig), these environment variables are not used as the configuration is provided explicitly.



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

## Async client

All the examples above can work using an async client.
```python
import asyncio

# initialize async client by passing `is_async = True`
async_client: Client = new_client(
    "{1Password_Connect_Host}",
    "{1Password_Connect_API_Token}",
    True)

async def main():
    vaults = await async_client.get_vaults()
    item = await async_client.get_item("{item_id}", "{vault_id}")
    # do something with vaults and item
    await async_client.session.aclose()  # close the client gracefully when you are done

asyncio.run(main())
```