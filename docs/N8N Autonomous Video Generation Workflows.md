# N8N Autonomous Video Generation Workflows

This directory contains the complete n8n workflow system for autonomous children's educational video generation. The system consists of three interconnected workflows that handle content creation, performance monitoring, and strategy optimization.

## Workflow Overview

### 1. Autonomous Video Generation (`autonomous_video_generation.json`)
**Trigger**: Every hour (CRON: 0 * * * *)
**Purpose**: Complete end-to-end video generation and publishing

**Workflow Steps**:
1. **Topic Selection**: Calls the autonomous topic selector API to choose the next educational topic
2. **Content Generation**: Generates educational script using AI-powered content creation
3. **Quality Validation**: Validates content for safety, educational value, and age appropriateness
4. **Asset Generation**: Creates visual and audio assets (characters, backgrounds, music, voice)
5. **Video Assembly**: Combines all assets into final video with proper synchronization
6. **Platform Upload**: Uploads to multiple platforms (YouTube, Vimeo, Facebook)
7. **Performance Tracking**: Updates performance database for continuous optimization
8. **Completion Logging**: Records successful completion and schedules next generation

**Error Handling**:
- Quality gate prevents low-quality content from proceeding
- Failed content is logged and flagged for review
- Workflow errors are captured and logged for investigation

### 2. Performance Monitoring (`performance_monitoring.json`)
**Trigger**: Every 15 minutes (CRON: */15 * * * *)
**Purpose**: Monitor system performance and generate alerts

**Workflow Steps**:
1. **Analytics Fetch**: Retrieves comprehensive performance analytics
2. **Trend Analysis**: Analyzes performance patterns and calculates trends
3. **Alert Generation**: Creates alerts when performance drops below thresholds
4. **Status Logging**: Records normal operation status

**Key Metrics Monitored**:
- Overall performance scores
- Content type effectiveness
- Age group engagement
- Diversity metrics
- Recent performance trends

### 3. Content Strategy Optimization (`strategy_optimization.json`)
**Trigger**: Every 6 hours (CRON: 0 */6 * * *)
**Purpose**: Optimize content strategy based on performance data

**Workflow Steps**:
1. **Diversity Check**: Analyzes content diversity and balance
2. **Performance History**: Fetches detailed performance history
3. **Strategy Analysis**: Generates optimization recommendations
4. **Priority Assessment**: Identifies high-priority strategy changes
5. **Implementation**: Applies strategy updates when needed
6. **Review Logging**: Records strategy review results

**Optimization Areas**:
- Content type frequency adjustments
- Diversity rebalancing
- Quality threshold updates
- Seasonal content prioritization

## API Integration

All workflows integrate with the Flask API endpoints:

### Content Generation APIs
- `POST /api/topics/select` - Autonomous topic selection
- `POST /api/content/generate/auto` - Automatic content generation
- `POST /api/content/validate` - Content quality validation

### Analytics APIs
- `GET /api/topics/analytics` - Performance analytics
- `GET /api/topics/diversity/status` - Content diversity status
- `GET /api/topics/performance/history` - Performance history

### Monitoring APIs
- `POST /api/topics/performance/update` - Update performance data
- `GET /api/status/health` - System health check

## Deployment Instructions

### 1. Start the Flask API
```bash
cd /home/ubuntu/content_generation_pipeline
source venv/bin/activate
python src/main.py
```

### 2. Start n8n
```bash
cd /home/ubuntu/n8n_workflows
n8n start
```

### 3. Import Workflows
1. Open n8n web interface (typically http://localhost:5678)
2. Import each workflow JSON file:
   - `autonomous_video_generation.json`
   - `performance_monitoring.json`
   - `strategy_optimization.json`
3. Activate all workflows

### 4. Configure Environment
Ensure the following are properly configured:
- Flask API running on localhost:5000
- n8n can access the API endpoints
- Proper error handling and logging
- Platform upload credentials (for production)

## Production Considerations

### Scaling
- Use n8n cloud or self-hosted cluster for high availability
- Implement proper database for performance data persistence
- Add Redis for caching and session management
- Use load balancers for API scaling

### Security
- Implement API authentication and rate limiting
- Secure platform upload credentials
- Add input validation and sanitization
- Monitor for security vulnerabilities

### Monitoring
- Set up comprehensive logging and monitoring
- Implement alerting for workflow failures
- Track resource usage and performance metrics
- Monitor API response times and error rates

### Integration
- Connect to actual AI services for content generation
- Integrate with real video rendering services
- Implement actual platform upload APIs
- Add webhook integrations for real-time updates

## Workflow Customization

### Timing Adjustments
Modify CRON expressions in workflow triggers:
- Video generation frequency (default: hourly)
- Performance monitoring interval (default: 15 minutes)
- Strategy optimization frequency (default: 6 hours)

### Quality Thresholds
Adjust quality gates and validation criteria:
- Content validation score threshold (default: 0.8)
- Performance alert threshold (default: 0.7)
- Diversity score requirements (default: 0.7)

### Content Strategy
Customize strategy optimization parameters:
- Content type weighting factors
- Age group prioritization
- Seasonal adjustment factors
- Diversity requirements

## Troubleshooting

### Common Issues
1. **API Connection Failures**: Check Flask API status and network connectivity
2. **Workflow Execution Errors**: Review n8n logs and error handling nodes
3. **Performance Degradation**: Monitor system resources and API response times
4. **Content Quality Issues**: Adjust validation thresholds and review content templates

### Debugging
- Enable detailed logging in n8n workflows
- Monitor Flask API logs for errors
- Use n8n execution history for workflow debugging
- Implement health checks for all system components

## Future Enhancements

### Planned Features
- Real-time performance dashboard
- Advanced analytics and reporting
- A/B testing for content strategies
- Machine learning optimization
- Multi-language content support
- Advanced video editing capabilities

### Integration Opportunities
- Social media scheduling
- Email marketing automation
- Customer relationship management
- Advanced analytics platforms
- Content management systems
- Revenue tracking and optimization

