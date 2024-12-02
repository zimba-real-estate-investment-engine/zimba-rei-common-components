import secrets
import string

from app.schemas.SubscriptionSchema import SubscriptionSchema


class Subscription(SubscriptionSchema):
    pass

    @staticmethod
    def generate_unsubscribe_token(length=32) -> str:
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(length))
        return token

    def set_unsubscribe_token(self):
        self.unsubscribe_token = Subscription.generate_unsubscribe_token()

    def unsubscribe(self):
        if self.unsubscribe_token.strip():
            raise ValueError("Missing unsubscribe token. Cannot unsubscribe without it")

    @staticmethod
    def generate_html_message_body() -> str:
        subscription_message_html = """
            <html>
              <head>
                <style>
                  body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                  }}
                  .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                  }}
                  .unsubscribe {{
                    margin-top: 20px;
                    text-align: center;
                  }}
                  .unsubscribe a {{
                    color: #007bff;
                    text-decoration: none;
                  }}
                  .unsubscribe a:hover {{
                    text-decoration: underline;
                  }}
                </style>
              </head>
              <body>
                <div class="container">
                  <h2>Welcome to Our Subscription!</h2>
                  <p>Hi {recipient_name},</p>
                  <p>
                    Thank you for subscribing to our waiting. We're excited to share
                    updates, tips, and special offers with you. Stay tuned!
                  </p>
                  <p>
                    If you ever wish to stop receiving these emails, you can unsubscribe
                    using the link below.
                  </p>
                  <div class="unsubscribe">
                    <a href="{unsubscribe_api_endpoint}?token={unsubscribe_token}">
                      Unsubscribe
                    </a>
                  </div>
                </div>
              </body>
            </html>
        """
        return subscription_message_html
