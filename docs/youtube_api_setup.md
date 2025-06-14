# YouTube API Integration Guide

This document provides instructions for setting up real YouTube API integration for the autonomous video publishing system.

## Prerequisites

1. **Google Cloud Console Setup**
   - Create a Google Cloud Project
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials
   - Set up authorized redirect URIs

2. **Required Python Libraries**
   ```bash
   pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
   ```

## OAuth 2.0 Setup

### 1. Create OAuth 2.0 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth 2.0 Client IDs"
5. Choose "Desktop application" or "Web application"
6. Download the JSON file (client_secret.json)

### 2. Initial Authorization

Run this script once to get the refresh token:

```python
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes required for YouTube upload
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    creds = None
    
    # Load client secrets
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save the refresh token
    with open('youtube_credentials.json', 'w') as token:
        token.write(creds.to_json())
    
    print(f"Refresh token: {creds.refresh_token}")
    return creds

if __name__ == '__main__':
    get_authenticated_service()
```

### 3. Production YouTube Upload Implementation

Replace the mock implementation in `automated_publishing_service.py`:

```python
def _upload_to_youtube(self, video_path: str, video_metadata: Dict[str, Any], config: PublishingConfig) -> UploadResult:
    """Upload video to YouTube using API"""
    
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    
    try:
        # Load credentials
        creds = Credentials(
            token=None,
            refresh_token=config.api_credentials['refresh_token'],
            token_uri='https://oauth2.googleapis.com/token',
            client_id=config.api_credentials['client_id'],
            client_secret=config.api_credentials['client_secret']
        )
        
        # Refresh token if needed
        if creds.expired:
            creds.refresh(Request())
        
        # Build YouTube service
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Prepare video metadata
        topic = video_metadata.get('topic', 'learning')
        title = video_metadata.get('title', f'Learning {topic}')
        description = config.default_settings['description_template'].format(topic=topic.lower())
        
        # Video upload body
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': config.default_settings['tags'],
                'categoryId': config.default_settings['category_id'],
                'defaultLanguage': config.default_settings['default_language']
            },
            'status': {
                'privacyStatus': config.default_settings['privacy_status']
            }
        }
        
        # Create media upload
        media = MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        # Execute upload
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = insert_request.execute()
        
        video_id = response['id']
        upload_url = f"https://youtube.com/watch?v={video_id}"
        
        return UploadResult(
            platform="youtube",
            video_id=video_id,
            upload_url=upload_url,
            status="success",
            upload_timestamp=datetime.now().isoformat(),
            metadata={
                "title": title,
                "description": description,
                "tags": config.default_settings['tags'],
                "category_id": config.default_settings['category_id'],
                "privacy_status": config.default_settings['privacy_status'],
                "youtube_response": response
            }
        )
        
    except HttpError as e:
        error_details = json.loads(e.content.decode('utf-8'))
        raise Exception(f"YouTube API error: {error_details}")
    
    except Exception as e:
        raise Exception(f"YouTube upload failed: {str(e)}")
```

## Vimeo API Integration

### 1. Setup

1. Create a Vimeo developer account
2. Create a new app at [Vimeo Developer](https://developer.vimeo.com/)
3. Generate an access token with upload permissions

### 2. Install Vimeo Library

```bash
pip install vimeo
```

### 3. Implementation

```python
def _upload_to_vimeo(self, video_path: str, video_metadata: Dict[str, Any], config: PublishingConfig) -> UploadResult:
    """Upload video to Vimeo using API"""
    
    import vimeo
    
    try:
        # Initialize Vimeo client
        client = vimeo.VimeoApi(
            token=config.api_credentials['access_token']
        )
        
        # Prepare metadata
        topic = video_metadata.get('topic', 'learning')
        title = video_metadata.get('title', f'Learning {topic}')
        description = config.default_settings['description_template'].format(topic=topic.lower())
        
        # Upload video
        response = client.upload(
            video_path,
            data={
                'name': title,
                'description': description,
                'privacy': {
                    'view': config.default_settings['privacy']
                }
            }
        )
        
        video_uri = response['uri']
        video_id = video_uri.split('/')[-1]
        upload_url = f"https://vimeo.com/{video_id}"
        
        return UploadResult(
            platform="vimeo",
            video_id=video_id,
            upload_url=upload_url,
            status="success",
            upload_timestamp=datetime.now().isoformat(),
            metadata={
                "title": title,
                "description": description,
                "privacy": config.default_settings['privacy'],
                "vimeo_response": response
            }
        )
        
    except Exception as e:
        raise Exception(f"Vimeo upload failed: {str(e)}")
```

## Facebook API Integration

### 1. Setup

1. Create a Facebook Developer account
2. Create a Facebook App
3. Get a Page Access Token for your Facebook Page
4. Add video upload permissions

### 2. Implementation

```python
def _upload_to_facebook(self, video_path: str, video_metadata: Dict[str, Any], config: PublishingConfig) -> UploadResult:
    """Upload video to Facebook using Graph API"""
    
    import requests
    
    try:
        # Prepare metadata
        topic = video_metadata.get('topic', 'learning')
        title = video_metadata.get('title', f'Learning {topic}')
        description = config.default_settings['description_template'].format(topic=topic.lower())
        
        # Facebook Graph API endpoint
        url = f"https://graph.facebook.com/v18.0/{config.api_credentials['page_id']}/videos"
        
        # Prepare data
        data = {
            'title': title,
            'description': description,
            'published': config.default_settings['published'],
            'access_token': config.api_credentials['page_access_token']
        }
        
        # Upload video
        with open(video_path, 'rb') as video_file:
            files = {'source': video_file}
            response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            video_id = result['id']
            upload_url = f"https://facebook.com/watch/?v={video_id}"
            
            return UploadResult(
                platform="facebook",
                video_id=video_id,
                upload_url=upload_url,
                status="success",
                upload_timestamp=datetime.now().isoformat(),
                metadata={
                    "title": title,
                    "description": description,
                    "published": config.default_settings['published'],
                    "facebook_response": result
                }
            )
        else:
            raise Exception(f"Facebook API error: {response.text}")
            
    except Exception as e:
        raise Exception(f"Facebook upload failed: {str(e)}")
```

## Configuration Update

Update your platform configuration with real credentials:

```python
# Update platform config via API
config_update = {
    "api_credentials": {
        "client_id": "your_youtube_client_id",
        "client_secret": "your_youtube_client_secret", 
        "refresh_token": "your_youtube_refresh_token"
    },
    "enabled": True
}

# POST to /api/publishing/platforms/youtube/config
```

## Security Considerations

1. **Environment Variables**: Store credentials in environment variables
2. **Encryption**: Encrypt stored refresh tokens
3. **Rotation**: Regularly rotate access tokens
4. **Monitoring**: Monitor API usage and quotas
5. **Error Handling**: Implement robust error handling and retry logic

## Rate Limiting

- **YouTube**: 10,000 units per day (upload = 1600 units)
- **Vimeo**: Varies by plan (Basic: 500MB/week)
- **Facebook**: Rate limits vary by app usage

## Testing

1. Test with small videos first
2. Monitor upload success rates
3. Implement fallback mechanisms
4. Test error scenarios
5. Verify video processing completion

## Production Deployment

1. Set up proper credential management
2. Implement monitoring and alerting
3. Configure backup upload strategies
4. Set up analytics tracking
5. Implement content moderation checks

