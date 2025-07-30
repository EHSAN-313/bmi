# Instagram DM Automation Tool

A professional Instagram Direct Messaging automation tool with a comprehensive web interface and robust backend API. This tool allows businesses and content creators to automate their Instagram DM campaigns while respecting platform limits and maintaining human-like behavior.

## 🚀 Features

### Core Functionality
- **Instagram Authentication**: Multiple authentication methods (session cookies, access tokens, API proxies)
- **Target Audience Management**: Manual input, CSV upload, automated extraction from followers/likers/commenters
- **Message Templates**: Rich text templates with variable placeholders and media support
- **Campaign Management**: Create, schedule, and monitor DM campaigns
- **Automated Replies**: Keyword-triggered automatic responses
- **Multi-Account Support**: Manage multiple Instagram accounts from one dashboard

### Safety & Compliance
- **Rate Limiting**: Configurable daily/hourly message limits
- **Human-like Delays**: Randomized delays between messages
- **Respect Platform Limits**: Built-in Instagram API rate limit compliance
- **Activity Logging**: Comprehensive logging of all activities
- **Error Handling**: Robust error handling and recovery

### Analytics & Reporting
- **Real-time Dashboard**: Live statistics and campaign monitoring
- **Detailed Logs**: Complete message delivery logs with timestamps
- **Export Functionality**: CSV export for logs and analytics
- **Success Metrics**: Open rates, response rates, and delivery statistics

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 2GB RAM minimum
- 1GB free disk space

### Python Dependencies
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
urllib3==2.0.7
```

## 🛠️ Installation

### 1. Clone or Download
Download all files to your desired directory:
- `instagram-dm-tool.html` - Main web interface
- `server.py` - Backend API server
- `requirements.txt` - Python dependencies

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python server.py
```

### 4. Access the Interface
Open your web browser and navigate to:
```
http://localhost:5000
```

## 🎯 Quick Start Guide

### Step 1: Authentication
1. Navigate to the "Authentication" section
2. Choose your preferred authentication method:
   - **Session Cookie** (Recommended): Extract from browser developer tools
   - **Access Token**: Use Instagram API token
   - **API Proxy**: Connect through third-party service
3. Enter your Instagram username and authentication data
4. Click "Connect to Instagram"

### Step 2: Add Target Audience
1. Go to "Target Audience" section
2. Choose your method:
   - **Manual Input**: Enter usernames one per line
   - **CSV Upload**: Upload a CSV file with usernames
   - **Extract Followers**: Automatically get your followers
   - **Post Likers**: Extract users who liked a specific post
3. Click "Add Audience" to import users

### Step 3: Create Message Templates
1. Navigate to "Message Templates"
2. Create a new template with:
   - Template name
   - Message content with variables ({{username}}, {{fullname}}, etc.)
   - Optional media attachments
3. Use the preview feature to test your template
4. Save the template

### Step 4: Set Up Sending Rules
1. Go to "Scheduling & Rules"
2. Configure:
   - Daily message limits (recommended: 50-100 for new accounts)
   - Time delays between messages
   - Active hours and days
   - Safety features

### Step 5: Create and Launch Campaign
1. Navigate to "Campaigns"
2. Create a new campaign:
   - Campaign name
   - Select message template
   - Choose target audience
   - Set schedule type
3. Click "Create Campaign" then "Start" to begin

## 📊 Dashboard Overview

### Key Metrics
- **Messages Sent Today**: Real-time count of delivered messages
- **Success Rate**: Percentage of successfully delivered messages
- **Pending Messages**: Number of users waiting to receive messages
- **Failed Messages**: Count of delivery failures

### Recent Activity
- Live feed of all system activities
- Success/failure notifications
- Campaign status updates
- Authentication events

## 🔧 Configuration Options

### Authentication Methods

#### Session Cookie (Recommended)
1. Open Instagram in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Copy the entire cookie string
5. Paste into the tool

#### Access Token
- Obtain from Instagram Basic Display API
- Requires app registration with Facebook
- Limited functionality compared to session cookies

#### API Proxy
- Use third-party Instagram API services
- Provides additional features and reliability
- May require subscription

### Message Templates

#### Available Variables
- `{{username}}` - Instagram username
- `{{fullname}}` - User's display name
- `{{followers}}` - Follower count
- `{{date}}` - Current date
- `{{time}}` - Current time

#### Example Template
```
Hi {{username}}! 👋

Thanks for following us! We noticed you have {{followers}} followers - you're doing great! 

Would you like to learn about our latest products? Reply YES to get a special discount code! 🎉

Best regards,
The Team
```

### Safety Settings

#### Recommended Limits
- **New Accounts**: 20-50 messages per day
- **Established Accounts**: 50-100 messages per day
- **Business Accounts**: 100-200 messages per day

#### Delay Settings
- **Minimum Delay**: 30-60 seconds
- **Maximum Delay**: 120-300 seconds
- **Enable Randomization**: Always recommended

## 📈 Analytics & Monitoring

### Campaign Analytics
- Total messages sent/failed
- Delivery success rates
- Response rates (when available)
- Time-based performance metrics

### Export Options
- **CSV Logs**: Complete message logs with timestamps
- **Analytics Report**: JSON format with detailed statistics
- **Audience Data**: Export target audience lists

## 🛡️ Safety & Best Practices

### Instagram Compliance
1. **Respect Rate Limits**: Never exceed Instagram's messaging limits
2. **Use Realistic Delays**: Maintain human-like behavior patterns
3. **Quality Content**: Send valuable, non-spammy messages
4. **Monitor Responses**: Check for negative feedback or blocks

### Account Safety
1. **Start Slowly**: Begin with low message volumes
2. **Warm Up Accounts**: Gradually increase activity
3. **Use Proxies**: Consider rotating IP addresses
4. **Monitor Health**: Watch for account restrictions

### Legal Considerations
1. **Terms of Service**: Always comply with Instagram's ToS
2. **Privacy Laws**: Respect GDPR, CAN-SPAM, and local regulations
3. **User Consent**: Ensure recipients can opt-out
4. **Content Guidelines**: Follow Instagram's community standards

## 🔍 Troubleshooting

### Common Issues

#### Authentication Failed
- **Solution**: Verify session cookie/token is current
- **Check**: Account isn't restricted or suspended
- **Try**: Different authentication method

#### Messages Not Sending
- **Check**: Rate limits not exceeded
- **Verify**: Target users exist and accept DMs
- **Ensure**: Account has messaging permissions

#### High Failure Rate
- **Reduce**: Message frequency and volume
- **Improve**: Message content quality
- **Check**: Account reputation and age

### Error Codes
- **401**: Authentication expired or invalid
- **429**: Rate limit exceeded
- **403**: Account restricted or banned
- **404**: Target user not found

## 🔄 Updates and Maintenance

### Regular Tasks
1. **Update Session Data**: Refresh authentication monthly
2. **Clean Audience Lists**: Remove inactive/blocked users
3. **Monitor Logs**: Check for patterns in failures
4. **Backup Data**: Export important campaign data

### Performance Optimization
1. **Database Maintenance**: Clean old logs periodically
2. **Template Optimization**: Test and refine message templates
3. **Audience Segmentation**: Target specific user groups
4. **Timing Optimization**: Find best sending times

## 📞 Support and Feedback

### Getting Help
1. Check this documentation first
2. Review error logs in the Analytics section
3. Test with small campaigns before scaling
4. Monitor Instagram's policy updates

### Best Practices for Success
1. **Quality over Quantity**: Focus on meaningful interactions
2. **Personalization**: Use variables to personalize messages
3. **Value Proposition**: Provide clear value to recipients
4. **Compliance**: Always follow platform rules

## ⚠️ Important Disclaimers

1. **Use at Your Own Risk**: This tool is for educational and legitimate business purposes
2. **Instagram ToS**: Users must comply with Instagram's Terms of Service
3. **Account Safety**: Excessive automation may result in account restrictions
4. **Legal Compliance**: Ensure compliance with local laws and regulations
5. **No Guarantees**: Results may vary based on account age, content, and usage patterns

## 🏗️ Technical Architecture

### Frontend
- Modern HTML5/CSS3/JavaScript
- Responsive design for all devices
- Real-time updates and notifications
- Local storage for settings persistence

### Backend
- Python Flask API server
- SQLite database for data persistence
- Multi-threaded campaign execution
- Comprehensive logging system

### Security
- Input validation and sanitization
- Rate limiting and abuse prevention
- Secure session management
- Error handling and recovery

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**License**: Educational/Research Use Only

For questions or support, please review the troubleshooting section and ensure you're following all safety guidelines and platform policies.
