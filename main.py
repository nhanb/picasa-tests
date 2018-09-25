import json
from google_auth_oauthlib.flow import Flow


def authenticate():
    # Create the flow using the client secrets file from the Google API Console.
    flow = Flow.from_client_secrets_file(
        "./google-credentials/oauth-client.json",
        scopes=[
            "https://www.googleapis.com/auth/photoslibrary",
            "https://www.googleapis.com/auth/photoslibrary.sharing",
        ],
        redirect_uri="http://localhost:9001/oauth-callback",
    )

    # Tell the user to go to the authorization URL.
    auth_url, _ = flow.authorization_url(prompt="consent")

    print(f"Please go to this URL: {auth_url}")

    # The user will get an authorization code. This code is used to get the access token
    code = input("Enter the authorization code: ")
    flow.fetch_token(code=code)

    # You can use flow.credentials, or you can just get a requests session using
    # flow.authorized_session.
    session = flow.authorized_session()

    return session


def upload_photo(session):

    # Create album
    resp = session.post(
        "https://photoslibrary.googleapis.com/v1/albums",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"album": {"title": "DON'T STOP BELIEVING"}}),
    )
    """
{'id': 'AMN9nm2bKl-K94-hPQjinXkT90cMLvILwJfzwgJh4WHWlv2hZ18pXKbsI13TcX7yoyMCjgTGxMau',
 'title': "DON'T STOP BELIEVING",
 'productUrl': 'https://photos.google.com/lr/album/AMN9nm2bKl-K94-hPQjinXkT90cMLvILwJfzwgJh4WHWlv2hZ18pXKbsI13TcX7yoyMCjgTGxMau'}
    """

    # Upload blob
    with open("dummy-in.png", "rb") as infile:
        blob = infile.read()
    resp = session.post(
        "https://photoslibrary.googleapis.com/v1/uploads",
        headers={
            "Content-type": "application/octet-stream",
            "X-Goog-Upload-File-Name": "dummy.png",
            "X-Goog-Upload-Protocol": "raw",
        },
        data=blob,
    )
    upload_token = resp.text

    # Batch create "media item"
    resp = session.post(
        "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "albumId": "AMN9nm2bKl-K94-hPQjinXkT90cMLvILwJfzwgJh4WHWlv2hZ18pXKbsI13TcX7yoyMCjgTGxMau",
                "newMediaItems": [
                    {
                        "description": "Just a small town girl",
                        "simpleMediaItem": {"uploadToken": upload_token},
                    }
                ],
            }
        ),
    )
    """
{'newMediaItemResults': [{'uploadToken': 'CAIS6QIA7p/vKHSYBOO17GaZKo5NAcYqTyPvwy9PKbB0Cfss7N85cK1riFvnfMJ6u9v9ZU5J8zI5uDcTBJz1UwKbDKXOIq+EjM+0Bx97rRZfMPAxl8IDtjJTEL8dxhK50r35Sga1EXKyb3jsDQlV06yfJS2kkja87BK9SmaB+cL8Bhn76//6uCBLflac4VFXyvCMGuxfYYQHOzJB4NtVTuqdErJJtDIg10QcJR3Ji6JIHyHmlnhlvYvfnYKL0WbAZBEYs9idFBcmhRtzMdjv8ZoOjYuLZfiWzcdRmZnD84KUf/HBhPMiBlomUT29koDzpOaN3soJ6puBNmAls+PRcrVupTXTv5g80BxGprEjDdHZbuRfEUszh2yjljkh9AUfYODN1qU1hcPre33LwBaVqvs+k24KSOgb3yUhU4Hs6sYtD8i0RqLPtkp0cPNLvZJMZY28YVQ/u0gsxRcg7MMO5eVTT8jWcPA/Lc1wdehX',
   'status': {'message': 'OK'},
   'mediaItem': {'id': 'AMN9nm0kiuoeU0TNqQK-_HCpB1o2Ng1sxcWjtr5TVTlZ4m6yVRxLuaFiDGh93bHgDHwjex3tr8nnou2CBFWrKu9QMZMtEcfPaw',
    'description': 'Just a small town girl',
    'productUrl': 'https://photos.google.com/lr/album/AMN9nm2bKl-K94-hPQjinXkT90cMLvILwJfzwgJh4WHWlv2hZ18pXKbsI13TcX7yoyMCjgTGxMau/photo/AMN9nm0kiuoeU0TNqQK-_HCpB1o2Ng1sxcWjtr5TVTlZ4m6yVRxLuaFiDGh93bHgDHwjex3tr8nnou2CBFWrKu9QMZMtEcfPaw',
    'mimeType': 'image/png',
    'mediaMetadata': {'creationTime': '2018-02-21T16:57:41Z',
     'width': '900',
     'height': '506'},
    'filename': 'dummy.png'}}]}
    """


# Found this direct link from Google Album Archive:
# https://lh3.googleusercontent.com/-XP7IKMkZqfKjs8XiV_oFiBx8HXaZxfWC155pwzFqZVIRjtUHQrFfapNcruHYHXCJSG3zJKYdDfqeymYwA=w900-h506-no
# Let's see if it sticks

# Link from Google Photos:
# https://lh3.googleusercontent.com/48NIU7rHxYrmVNTBMZAG3r8Kfz7i-wyL-1njPcL_UTJFCmVF3ZVpD189iWHSZiRqsu15BXF3sCFoutBOhyphbW4Y1Pc4cTtyGheY_M90vkN10cTrlc9GMyZgTRuLou_wuw7hThGfQOo0DOE-ytAdjRfMKkR_-XIsmu2FPB1XPe3lTmlt2POzqAqvjN_VnOf2FXB8nBnGyC9psbJ0bcbYjBRZZG3D5IwE28psdV8d_DZwnbKMhhb9zgZtsxiisLdgEX3vZ4WBQYH6cAVniNvQ7WpV3nEmrMlQz4uWdXBSbtLxD2Jge1XbFuRYm0RDqYP-6tecPB4odWnyTlHRqtWYbVU9Ltr5Ypr3sECw223-jx_pX3obpNQlPYwTCtHp537TZ8yc-0QE0RaGXq1RJmqy-OhCmbGG0hQuqxTriwwTNNL_RX8EeTA4XeL34nz2ELFJawWe0YViDZM8UcrnWR6hWbPxaZnwZfGBL4Ut8eWqe4SBrx-eOhu975Bmsxrysyp0Tscn2BwR1BE5FkCDtX1aRW0M5q2F_-wlqJ8yIgnFCoOVgAuPr4mvn1Sx6mO0BJ7DkuF-IBGE61oXOu1rLyymXuACwaAGoP0UZx98Ib6QEZ1xmlRce2hEcDLn0bG1AIm2pNJQXe-Vc7dL6pZ7QX7fnWFTB43uhSokfMGZLACI7rucBxTGOTchGBM7=w900-h506-no
