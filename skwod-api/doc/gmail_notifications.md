# Gmail SMTP Build/Test Notifications

To enable build/test failure notifications:

1. Go to https://myaccount.google.com/security and enable "App passwords" for your account.
2. Add the following to your secrets or .env files:
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=465
   EMAIL_USER=youremail@gmail.com
   EMAIL_PASS=your-app-password
3. See FastAPI docs for [background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).
4. Add notification calls to your test/build steps as needed.

**Note:** Never commit email credentials to your repo!
