# Deployment Guide for AUD to CNY Exchange Rate Monitor

This guide provides instructions on how to deploy your exchange rate monitoring application to various cloud platforms. You can choose the platform that best suits your needs based on factors like ease of use, cost, and familiarity.

## Project Structure

Ensure your project directory has the following structure:
```
your-project-folder/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── Dockerfile
└── templates/
    └── index.html
```

## Option 1: Heroku Deployment

Heroku is one of the easiest platforms to deploy your application.

### Prerequisites
1. [Create a Heroku account](https://signup.heroku.com/)
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### Deployment Steps

1. Login to Heroku:
   ```
   heroku login
   ```

2. Create a new Heroku app:
   ```
   heroku create aud-cny-monitor
   ```

3. Initialize a Git repository (if not already done):
   ```
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. Deploy to Heroku:
   ```
   git push heroku master
   ```

5. Open your app:
   ```
   heroku open
   ```

### Notes for Heroku
- Heroku's free tier has been discontinued. You'll need to use a paid plan.
- Heroku apps go to sleep after 30 minutes of inactivity on eco dynos.

## Option 2: Railway Deployment

Railway is a modern alternative to Heroku with a generous free tier.

### Prerequisites
1. Create a [Railway account](https://railway.app/)
2. Install Railway CLI (optional)

### Deployment Steps

1. Push your code to a GitHub repository
2. Go to [Railway Dashboard](https://railway.app/dashboard)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will detect your Procfile and deploy automatically

## Option 3: Google Cloud Run

Google Cloud Run is a serverless platform that works well for containerized applications.

### Prerequisites
1. Create a [Google Cloud account](https://cloud.google.com/)
2. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3. Enable Cloud Run and Container Registry APIs

### Deployment Steps

1. Login to Google Cloud:
   ```
   gcloud auth login
   ```

2. Set your project:
   ```
   gcloud config set project YOUR_PROJECT_ID
   ```

3. Build and push your Docker image:
   ```
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/aud-cny-monitor
   ```

4. Deploy to Cloud Run:
   ```
   gcloud run deploy aud-cny-monitor --image gcr.io/YOUR_PROJECT_ID/aud-cny-monitor --platform managed --allow-unauthenticated
   ```

## Option 4: Digital Ocean App Platform

Digital Ocean offers a simple platform for deploying applications.

### Prerequisites
1. Create a [Digital Ocean account](https://www.digitalocean.com/)

### Deployment Steps

1. Push your code to a GitHub repository
2. Go to the [Digital Ocean Apps](https://cloud.digitalocean.com/apps) page
3. Click "Create App" → "GitHub"
4. Select your repository
5. Choose a plan and region
6. Deploy your app

## Option 5: Render

Render is a unified cloud for web services with a free tier.

### Prerequisites
1. Create a [Render account](https://render.com/)

### Deployment Steps

1. Push your code to a GitHub or GitLab repository
2. In the Render dashboard, click "New" → "Web Service"
3. Connect your repo
4. Configure as a Python app with the start command: `gunicorn app:app`
5. Choose a plan and click "Create Web Service"

## Troubleshooting

### Common Issues

1. **Application crashes**: Check your logs using `heroku logs --tail` or the equivalent command for your platform.

2. **No data displayed**: Ensure your application can access the Bank of China website. Some cloud providers might restrict outbound requests.

3. **Rate limiting**: If your application makes too many requests, you might get blocked. Consider adjusting the sleep time between requests.

4. **Memory issues**: If your application runs out of memory, consider clearing old history data periodically.

### Support

If you encounter issues specific to your cloud provider, consult their documentation:
- [Heroku Dev Center](https://devcenter.heroku.com/)
- [Railway Docs](https://docs.railway.app/)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Digital Ocean Docs](https://docs.digitalocean.com/products/app-platform/)
- [Render Docs](https://render.com/docs)