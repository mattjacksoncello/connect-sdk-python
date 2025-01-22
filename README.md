<!-- Image sourced from https://blog.1password.com/introducing-secrets-automation/ -->
<img alt="" role="img" src="https://blog.1password.com/posts/2021/secrets-automation-launch/header.svg"/>

<div align="center">
  <h1>1Password Connect SDK for Python</h1>
  <p>Access your 1Password items in your Python applications through your self-hosted <a href="https://developer.1password.com/docs/connect">1Password Connect server</a>.</p>
  <a href="#-get-started">
    <img alt="Get started" src="https://user-images.githubusercontent.com/45081667/226940040-16d3684b-60f4-4d95-adb2-5757a8f1bc15.png" height="37"/>
  </a>
</div>

---

The 1Password Connect SDK provides access to 1Password via [1Password Connect](https://developer.1password.com/docs/connect) hosted in your infrastructure. The library is intended to be used by Python applications to simplify accessing items in 1Password vaults.

## 🪄 See it in action

Check the [Python Connect SDK Example](example/README.md) to see an example of item manipulation using the SDK that you can execute on your machine.

## ✨ Get started

1. Install the 1Password Connect Python SDK:

   ```sh
   pip install onepasswordconnectsdk
   ```

2. Export the `OP_CONNECT_HOST` and `OP_CONNECT_TOKEN` environment variables:

   ```sh
   export OP_CONNECT_HOST=<your-connect-host> && \
   export OP_CONNECT_TOKEN=<your-connect-token>
   ```

   2.1 If you need a higher timeout on the client requests you can export `OP_CONNECT_CLIENT_REQ_TIMEOUT` environment variable:

   ```sh
   # set the timeout to 90 seconds
   export OP_CONNECT_CLIENT_REQ_TIMEOUT=90
   ```

3. Use the SDK:

   Choose between synchronous or asynchronous clients:

   ```python
   # Synchronous client
   from onepasswordconnectsdk.client import Client, new_client_from_environment

   # Create client using environment variables
   client: Client = new_client_from_environment()

   # Read a secret
   item = client.get_item("{item_id}", "{vault_id}")

   # Write a secret
   from onepasswordconnectsdk.models import Item, ItemVault, Field

   new_item = Item(
       vault=ItemVault(id=vault_id),
       title="Example Login",
       category="LOGIN",
       fields=[Field(value="username123", purpose="USERNAME")]
   )
   created_item = client.create_item(vault_id, new_item)
   ```

   ```python
   # Asynchronous client
   import asyncio
   from onepasswordconnectsdk.async_client import AsyncClient, new_async_client_from_environment

   async def main():
       # Create client using environment variables
       client: AsyncClient = new_async_client_from_environment()
       
       try:
           # Read and write secrets asynchronously
           item = await client.get_item("{item_id}", "{vault_id}")
           created_item = await client.create_item(vault_id, new_item)
       finally:
           await client.session.aclose()

   asyncio.run(main())
   ```

   Both client types support additional configuration through [httpx client options](https://www.python-httpx.org/api/#client).

For more examples of how to use the SDK, check out [USAGE.md](USAGE.md).

## 💙 Community & Support

- File an [issue](https://github.com/1Password/connect-sdk-python/issues) for bugs and feature requests.
- Join the [Developer Slack workspace](https://join.slack.com/t/1password-devs/shared_invite/zt-1halo11ps-6o9pEv96xZ3LtX_VE0fJQA).
- Subscribe to the [Developer Newsletter](https://1password.com/dev-subscribe/).

## 🔐 Security

1Password requests you practice responsible disclosure if you discover a vulnerability.

Please file requests by sending an email to bugbounty@agilebits.com.
