from common_errors import methodError


def handler(request, match):
    import uuid
    
    if request.method == 'POST':
        transient_uid = str(uuid.uuid4())
        # transient_uid = '197a97fc-4179-43f4-b009-9432ac0c8e53'

        response = {
            "access_token": transient_uid, #client doesent validate any apsect of it, use this to as a identifier for the server
            "client_id": "2530949f-3038-5f92-9393-2ab77f57d89e",
            "domain": "net.edgecasegames.space.ea",
            "expires_at": "Sun, 17 Mar 2050 12:14:23 GMT",
            "expires_in": 8640000,
            "id": transient_uid, #maybe unused
            "identity_id": transient_uid, #this appears to be passed onto the server, conficting ids will boot the existing player
            "ratelimit_scope": "identity_id",
            "refresh_token": ".eJwVjDsOwjAQBe-yNSvZ-8n6paPgBHAB24kFUkSDqBB3x3Qz0pv3oX7QSuKaYBisSQv7gDAUylJbxPDYCnY60f01t9fL-Tb58ZjcdmyiPlr3YpIVyLYvpY5wQxL7N43W5_s4ZlFpze4SWmzR6dt8yIiKGJ0tB9h0GLeUwDCV2lMvuyt9f5BGKX0.ydsf6-LG_CXHIIJwDntsj1ZPNHw",
            "token_type": "bearer"
        }
        return (201, response, {})
    else:
        return methodError(['POST'])
