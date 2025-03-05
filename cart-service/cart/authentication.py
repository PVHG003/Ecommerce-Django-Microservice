from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Override this method to prevent checking the local database for the user.
        """
        user_id = validated_token.get("id")
        # user = validated_token.get("user")
        exp = validated_token.get("exp")
        iat = validated_token.get("iat")

        if not user_id:
            raise AuthenticationFailed("Invalid token: missing user information.")

        # Instead of returning a Django User object, return a simple dictionary
        return {"id": user_id,
                # "user": user,
                "exp": exp,
                "iat": iat}
