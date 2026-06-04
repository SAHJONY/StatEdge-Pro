# StatEdge Pro API Documentation

## Introduction

Welcome to the StatEdge Pro API documentation. This API provides access to AI-powered sports analytics for teams and professional bettors.

The API is organized around REST principles and uses HTTP response codes to indicate API errors. All data is returned in JSON format.

## Base URL

```
https://api.statedge-pro.com/v1
```

All endpoints are relative to this base URL.

## Authentication

StatEdge Pro uses API keys for authentication. Include your API key in the request headers:

```
Authorization: Bearer YOUR_API_KEY
```

API keys can be generated and managed through the user dashboard.

## Rate Limiting

The API enforces rate limits to ensure fair usage:

- **Standard tier**: 100 requests per minute
- **Pro tier**: 500 requests per minute
- **Enterprise tier**: 2000 requests per minute

Exceeding rate limits will result in a `429 Too Many Requests` response.

## Response Format

All responses follow a consistent format:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {
    "timestamp": "2026-06-04T12:00:00Z",
    "version": "1.0.0"
  }
}
```

## Error Handling

The API uses standard HTTP status codes to indicate errors:

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid API key |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

Error responses have the following format:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "invalid_api_key",
    "message": "Invalid API key provided",
    "details": {}
  },
  "meta": {
    "timestamp": "2026-06-04T12:00:00Z",
    "version": "1.0.0"
  }
}
```

## Endpoints

### Health Check

`GET /health`

Returns the health status of the API.

**Response**:

```json
{
  "status": "healthy",
  "service": "StatEdge Pro API",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2026-06-04T12:00:00Z"
}
```

### Teams

`GET /teams`

Get a list of all teams.

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sport | string | No | Filter by sport type |
| league | string | No | Filter by league |

**Response**:

```json
[
  {
    "id": "team_1",
    "name": "Los Angeles Lakers",
    "short_name": "LAL",
    "sport": "basketball",
    "league": "nba",
    "country": "USA",
    "city": "Los Angeles",
    "founded": 1947,
    "home_stadium": "Crypto.com Arena",
    "logo_url": "https://example.com/lakers-logo.png"
  }
]
```

`GET /teams/{team_id}`

Get a specific team by ID.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| team_id | string | Yes | ID of the team |

**Response**:

```json
{
  "id": "team_1",
  "name": "Los Angeles Lakers",
  "short_name": "LAL",
  "sport": "basketball",
  "league": "nba",
  "country": "USA",
  "city": "Los Angeles",
  "founded": 1947,
  "home_stadium": "Crypto.com Arena",
  "logo_url": "https://example.com/lakers-logo.png"
}
```

### Players

`GET /players`

Get a list of all players.

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| team_id | string | No | Filter by team ID |
| sport | string | No | Filter by sport type |

**Response**:

```json
[
  {
    "id": "player_1",
    "first_name": "LeBron",
    "last_name": "James",
    "full_name": "LeBron James",
    "sport": "basketball",
    "team_id": "team_1",
    "position": "Forward",
    "jersey_number": 23,
    "height_cm": 206,
    "weight_kg": 113,
    "birth_date": "1984-12-30",
    "nationality": "USA",
    "image_url": "https://example.com/lebron.jpg"
  }
]
```

`GET /players/{player_id}`

Get a specific player by ID.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| player_id | string | Yes | ID of the player |

**Response**:

```json
{
  "id": "player_1",
  "first_name": "LeBron",
  "last_name": "James",
  "full_name": "LeBron James",
  "sport": "basketball",
  "team_id": "team_1",
  "position": "Forward",
  "jersey_number": 23,
  "height_cm": 206,
  "weight_kg": 113,
  "birth_date": "1984-12-30",
  "nationality": "USA",
  "image_url": "https://example.com/lebron.jpg"
}
```

### Games

`GET /games`

Get a list of all games.

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sport | string | No | Filter by sport type |
| league | string | No | Filter by league |
| status | string | No | Filter by game status (scheduled, in_progress, completed) |

**Response**:

```json
[
  {
    "id": "game_1",
    "home_team_id": "team_1",
    "away_team_id": "team_2",
    "sport": "basketball",
    "league": "nba",
    "start_time": "2026-06-10T19:30:00Z",
    "venue": "Crypto.com Arena",
    "city": "Los Angeles",
    "country": "USA",
    "status": "scheduled"
  }
]
```

`GET /games/{game_id}`

Get a specific game by ID.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
{
  "id": "game_1",
  "home_team_id": "team_1",
  "away_team_id": "team_2",
  "sport": "basketball",
  "league": "nba",
  "start_time": "2026-06-10T19:30:00Z",
  "venue": "Crypto.com Arena",
  "city": "Los Angeles",
  "country": "USA",
  "status": "scheduled"
}
```

`GET /games/{game_id}/events`

Get all events for a specific game.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
[
  {
    "id": "event_1",
    "game_id": "game_1",
    "event_type": "basket",
    "team_id": "team_1",
    "player_id": "player_1",
    "time_elapsed": 2.5,
    "period": 1,
    "score_home": 2,
    "score_away": 0,
    "description": "LeBron James makes a layup",
    "x_coordinate": 4.5,
    "y_coordinate": 2.1
  }
]
```

`GET /games/{game_id}/player-stats`

Get player statistics for a specific game.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
[
  {
    "id": "stats_1",
    "player_id": "player_1",
    "game_id": "game_1",
    "sport": "basketball",
    "minutes_played": 35.5,
    "points": 28,
    "rebounds": 9,
    "assists": 7,
    "steals": 2,
    "blocks": 1,
    "turnovers": 3,
    "field_goals_made": 10,
    "field_goals_attempted": 20,
    "three_pointers_made": 2,
    "three_pointers_attempted": 5,
    "free_throws_made": 6,
    "free_throws_attempted": 8
  }
]
```

`GET /games/{game_id}/team-stats`

Get team statistics for a specific game.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
[
  {
    "id": "team_stats_1",
    "team_id": "team_1",
    "game_id": "game_1",
    "sport": "basketball",
    "possession_percentage": 52.3,
    "shots": 87,
    "shots_on_target": 42,
    "corners": 5,
    "fouls": 18,
    "yellow_cards": 0,
    "red_cards": 0,
    "penalties": 0,
    "turnovers": 14,
    "offensive_rebounds": 12,
    "defensive_rebounds": 34
  }
]
```

### Analytics

`GET /analytics/{game_id}`

Get comprehensive analytics for a specific game.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
{
  "predictions": [
    {
      "id": "pred_1",
      "game_id": "game_1",
      "sport": "basketball",
      "predicted_winner": "team_1",
      "win_probability_home": 0.65,
      "win_probability_away": 0.35,
      "predicted_score_home": 112,
      "predicted_score_away": 108,
      "predicted_total_points": 220,
      "confidence_score": 0.85,
      "key_factors": [
        "Home team has strong overall win record",
        "Away team struggles on the road"
      ],
      "model_version": "1.0.0"
    }
  ],
  "value_indicators": [
    {
      "id": "value_1",
      "game_id": "game_1",
      "sport": "basketball",
      "market_type": "moneyline",
      "bookmaker": "DraftKings",
      "line": 0.0,
      "odds": -180,
      "implied_probability": 0.643,
      "ai_probability": 0.65,
      "value_score": 85,
      "confidence_score": 0.9,
      "edge": 35,
      "recommendation": "strong_buy",
      "key_insights": [
        "AI model identifies mispricing in betting market"
      ],
      "model_version": "1.0.0"
    }
  ],
  "insights": [
    {
      "id": "insight_1",
      "game_id": "game_1",
      "sport": "basketball",
      "insight_type": "matchup_advantage",
      "title": "Home Team Dominance",
      "description": "The home team has a significantly higher win percentage (0.72) compared to the away team (0.58), indicating a clear matchup advantage.",
      "confidence_score": 0.9,
      "impact_score": 0.7,
      "key_data_points": [
        "Home team win percentage: 0.72",
        "Away team win percentage: 0.58"
      ],
      "model_version": "1.0.0"
    }
  ],
  "trends": [
    {
      "id": "trend_1",
      "team_id": "team_1",
      "sport": "basketball",
      "trend_type": "recent_form",
      "metric": "win_percentage",
      "value": 0.72,
      "direction": "up",
      "period_days": 30,
      "confidence_score": 0.9,
      "description": "The home team has maintained a high win percentage (0.72) over the last 30 days, indicating strong recent form.",
      "model_version": "1.0.0"
    }
  ],
  "features": {
    "sport": "basketball",
    "league": "nba",
    "is_home_team_favorite": 1,
    "days_since_last_game_home": 2,
    "days_since_last_game_away": 3,
    "home_team_win_pct": 0.72,
    "away_team_win_pct": 0.58,
    "home_team_avg_points": 115.5,
    "away_team_avg_points": 108.2,
    "home_team_avg_points_allowed": 105.3,
    "away_team_avg_points_allowed": 112.1,
    "home_team_home_win_pct": 0.78,
    "away_team_away_win_pct": 0.45,
    "home_team_last_5_wins": 4,
    "away_team_last_5_wins": 2,
    "home_team_top_scorer_avg": 28.5,
    "away_team_top_scorer_avg": 25.8,
    "home_team_injured_players": 0,
    "away_team_injured_players": 1,
    "total_events": 125,
    "home_team_events": 67,
    "away_team_events": 58,
    "home_team_shot_efficiency": 0.48,
    "away_team_shot_efficiency": 0.47,
    "home_team_last_10_min_goals": 2,
    "away_team_last_10_min_goals": 1
  }
}
```

`GET /analytics/{game_id}/predictions`

Get AI-generated predictions for a specific game.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
[
  {
    "id": "pred_1",
    "game_id": "game_1",
    "sport": "basketball",
    "predicted_winner": "team_1",
    "win_probability_home": 0.65,
    "win_probability_away": 0.35,
    "predicted_score_home": 112,
    "predicted_score_away": 108,
    "predicted_total_points": 220,
    "confidence_score": 0.85,
    "key_factors": [
      "Home team has strong overall win record",
      "Away team struggles on the road"
    ],
    "model_version": "1.0.0"
  }
]
```

`GET /analytics/{game_id}/value-indicators`

Get value indicators for betting markets for a specific game.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
[
  {
    "id": "value_1",
    "game_id": "game_1",
    "sport": "basketball",
    "market_type": "moneyline",
    "bookmaker": "DraftKings",
    "line": 0.0,
    "odds": -180,
    "implied_probability": 0.643,
    "ai_probability": 0.65,
    "value_score": 85,
    "confidence_score": 0.9,
    "edge": 35,
    "recommendation": "strong_buy",
    "key_insights": [
      "AI model identifies mispricing in betting market"
    ],
    "model_version": "1.0.0"
  }
]
```

`GET /analytics/{game_id}/insights`

Get AI-generated insights about a specific game.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
[
  {
    "id": "insight_1",
    "game_id": "game_1",
    "sport": "basketball",
    "insight_type": "matchup_advantage",
    "title": "Home Team Dominance",
    "description": "The home team has a significantly higher win percentage (0.72) compared to the away team (0.58), indicating a clear matchup advantage.",
    "confidence_score": 0.9,
    "impact_score": 0.7,
    "key_data_points": [
      "Home team win percentage: 0.72",
      "Away team win percentage: 0.58"
    ],
    "model_version": "1.0.0"
  }
]
```

`GET /analytics/teams/{team_id}/trends`

Get statistical trends for a specific team.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| team_id | string | Yes | ID of the team |

**Response**:

```json
[
  {
    "id": "trend_1",
    "team_id": "team_1",
    "sport": "basketball",
    "trend_type": "recent_form",
    "metric": "win_percentage",
    "value": 0.72,
    "direction": "up",
    "period_days": 30,
    "confidence_score": 0.9,
    "description": "The home team has maintained a high win percentage (0.72) over the last 30 days, indicating strong recent form.",
    "model_version": "1.0.0"
  }
]
```

### Reports

`GET /reports/{report_id}`

Get a specific analytics report by ID.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| report_id | string | Yes | ID of the report |

**Response**:

```json
{
  "id": "report_1",
  "subject_type": "team",
  "subject_id": "team_1",
  "sport": "basketball",
  "report_type": "game_preview",
  "title": "Game Preview Report for Los Angeles Lakers",
  "summary": "Comprehensive analysis of Los Angeles Lakers for game preview.",
  "key_findings": [
    "Team has shown consistent performance in recent games",
    "Key players are performing above league average",
    "Team has strong home advantage",
    "Opponents have difficulty scoring against this team"
  ],
  "data_sources": [
    "Team statistics",
    "Player performance data",
    "Game event data"
  ],
  "confidence_score": 0.9,
  "model_version": "1.0.0"
}
```

`POST /reports`

Generate a comprehensive analytics report for a team.

**Request Body**:

```json
{
  "team_id": "team_1",
  "report_type": "game_preview"
}
```

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| team_id | string | Yes | ID of the team |
| report_type | string | Yes | Type of report to generate (game_preview, post_game_analysis, trend_analysis) |

**Response**:

```json
{
  "id": "report_1",
  "subject_type": "team",
  "subject_id": "team_1",
  "sport": "basketball",
  "report_type": "game_preview",
  "title": "Game Preview Report for Los Angeles Lakers",
  "summary": "Comprehensive analysis of Los Angeles Lakers for game preview.",
  "key_findings": [
    "Team has shown consistent performance in recent games",
    "Key players are performing above league average",
    "Team has strong home advantage",
    "Opponents have difficulty scoring against this team"
  ],
  "data_sources": [
    "Team statistics",
    "Player performance data",
    "Game event data"
  ],
  "confidence_score": 0.9,
  "model_version": "1.0.0"
}
```

### Data Feeds

`GET /data-feeds`

Get a list of all data feeds.

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sport | string | No | Filter by sport type |

**Response**:

```json
[
  {
    "id": "feed_1",
    "name": "NBA Live Stats",
    "sport": "basketball",
    "league": "nba",
    "feed_type": "live_stats",
    "url": "https://api.nba.com/live",
    "api_key_required": true,
    "frequency_minutes": 1,
    "last_updated": "2026-06-04T12:00:00Z",
    "status": "active"
  }
]
```

`GET /data-feeds/{feed_id}`

Get a specific data feed by ID.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| feed_id | string | Yes | ID of the data feed |

**Response**:

```json
{
  "id": "feed_1",
  "name": "NBA Live Stats",
  "sport": "basketball",
  "league": "nba",
  "feed_type": "live_stats",
  "url": "https://api.nba.com/live",
  "api_key_required": true,
  "frequency_minutes": 1,
  "last_updated": "2026-06-04T12:00:00Z",
  "status": "active"
}
```

`POST /data-feeds/{feed_id}/process`

Process a data feed manually.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| feed_id | string | Yes | ID of the data feed |

**Response**:

```json
{
  "status": "processed",
  "feed": {
    "id": "feed_1",
    "name": "NBA Live Stats",
    "sport": "basketball",
    "league": "nba",
    "feed_type": "live_stats",
    "url": "https://api.nba.com/live",
    "api_key_required": true,
    "frequency_minutes": 1,
    "last_updated": "2026-06-04T12:05:00Z",
    "status": "active"
  }
}
```

### Users

`GET /users/me`

Get the current user's profile.

**Response**:

```json
{
  "id": "user_1",
  "email": "coach@lakers.com",
  "first_name": "Mike",
  "last_name": "Brown",
  "role": "coach",
  "organization": "Los Angeles Lakers",
  "subscription_tier": "team_pro",
  "is_active": true,
  "last_login": "2026-06-04T12:00:00Z"
}
```

`GET /users/{user_id}`

Get a specific user by ID.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | ID of the user |

**Response**:

```json
{
  "id": "user_1",
  "email": "coach@lakers.com",
  "first_name": "Mike",
  "last_name": "Brown",
  "role": "coach",
  "organization": "Los Angeles Lakers",
  "subscription_tier": "team_pro",
  "is_active": true,
  "last_login": "2026-06-04T12:00:00Z"
}
```

`GET /users/{user_id}/preferences`

Get a specific user's preferences.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | ID of the user |

**Response**:

```json
{
  "id": "pref_1",
  "user_id": "user_1",
  "sport": "basketball",
  "preferred_metrics": [
    "points",
    "rebounds",
    "assists"
  ],
  "display_language": "en",
  "notification_preferences": {
    "game_updates": true,
    "player_injuries": true,
    "value_indicators": true
  }
}
```

### API Keys

`GET /api-keys`

Get a list of all API keys for the current user.

**Response**:

```json
[
  {
    "id": "key_1",
    "user_id": "user_1",
    "name": "Lakers API Key",
    "key": "abc123xyz",
    "permissions": [
      "read:analytics",
      "read:teams",
      "read:players"
    ],
    "is_active": true,
    "created_at": "2026-06-04T12:00:00Z",
    "created_by": "user_1"
  }
]
```

`POST /api-keys`

Create a new API key for the current user.

**Request Body**:

```json
{
  "name": "Lakers API Key",
  "permissions": [
    "read:analytics",
    "read:teams",
    "read:players"
  ]
}
```

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name for the API key |
| permissions | array | Yes | List of permissions for the API key |

**Response**:

```json
{
  "id": "key_1",
  "user_id": "user_1",
  "name": "Lakers API Key",
  "key": "abc123xyz",
  "permissions": [
    "read:analytics",
    "read:teams",
    "read:players"
  ],
  "is_active": true,
  "created_at": "2026-06-04T12:00:00Z",
  "created_by": "user_1"
}
```

`DELETE /api-keys/{key_id}`

Delete an API key.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key_id | string | Yes | ID of the API key |

**Response**:

```json
{
  "status": "deleted"
}
```

### Value Finder

`GET /value-finder`

Get value indicators across all games.

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sport | string | No | Filter by sport type |
| league | string | No | Filter by league |
| recommendation | string | No | Filter by recommendation type (strong_buy, buy, neutral, sell, strong_sell) |

**Response**:

```json
[
  {
    "id": "value_1",
    "game_id": "game_1",
    "sport": "basketball",
    "market_type": "moneyline",
    "bookmaker": "DraftKings",
    "line": 0.0,
    "odds": -180,
    "implied_probability": 0.643,
    "ai_probability": 0.65,
    "value_score": 85,
    "confidence_score": 0.9,
    "edge": 35,
    "recommendation": "strong_buy",
    "key_insights": [
      "AI model identifies mispricing in betting market"
    ],
    "model_version": "1.0.0"
  }
]
```

`GET /value-finder/{game_id}`

Get value indicators for a specific game.

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | string | Yes | ID of the game |

**Response**:

```json
[
  {
    "id": "value_1",
    "game_id": "game_1",
    "sport": "basketball",
    "market_type": "moneyline",
    "bookmaker": "DraftKings",
    "line": 0.0,
    "odds": -180,
    "implied_probability": 0.643,
    "ai_probability": 0.65,
    "value_score": 85,
    "confidence_score": 0.9,
    "edge": 35,
    "recommendation": "strong_buy",
    "key_insights": [
      "AI model identifies mispricing in betting market"
    ],
    "model_version": "1.0.0"
  }
]
```

### Admin Endpoints

`POST /admin/update-models`

Update machine learning models with new data.

**Response**:

```json
{
  "status": "success"
}
```

`POST /admin/run-daily-analysis`

Run daily analysis on all games.

**Response**:

```json
{
  "status": "success"
}
```

`POST /admin/generate-weekly-summary`

Generate a weekly summary report.

**Response**:

```json
{
  "status": "success"
}
```

`POST /admin/optimize-model-performance`

Optimize model performance based on feedback.

**Response**:

```json
{
  "status": "success"
}
```

## Authentication

StatEdge Pro uses API keys for authentication. To get an API key:

1. Log in to your StatEdge Pro account
2. Navigate to the API Keys section in your profile
3. Click "Create New API Key"
4. Enter a name for your key and select the required permissions
5. Click "Create"
6. Copy the generated API key and store it securely

Include your API key in the Authorization header of all requests:

```
Authorization: Bearer YOUR_API_KEY
```

## Webhooks

StatEdge Pro supports webhooks for real-time notifications. Configure webhooks in your account settings.

Supported webhook events:

- `game_started`
- `game_ended`
- `value_indicator_generated`
- `new_report_available`
- `model_updated`

## SDKs

We provide official SDKs for popular programming languages:

- Python
- JavaScript/Node.js
- Java
- C#

## Versioning

The API follows semantic versioning. Major versions (v1, v2, etc.) are backward incompatible. Minor versions (v1.1, v1.2, etc.) add new features without breaking changes. Patch versions (v1.1.1, v1.1.2, etc.) fix bugs.

## Support

For support, please contact us at sahjonycapitalllc@outlook.com.