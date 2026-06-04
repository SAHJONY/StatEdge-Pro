"""
API Endpoints for StatEdge Pro.

FastAPI endpoints for the AI-powered sports analytics platform.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import logging

from src.models.sports_models import (
    Team, Player, Game, GameEvent, PlayerStats, TeamStats,
    GamePrediction, ValueIndicator, TeamTrend, GameInsight,
    AnalyticsReport, DataFeed, User, UserPreference, APIKey
)
from src.analytics.engine import analytics_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(
    prefix="/api/v1",
    tags=["analytics"],
    responses={404: {"description": "Not found"}}
)

# Mock database (in production, this would be a real database)
# For now, we'll use in-memory storage
mock_teams = [
    Team(id="team_1", name="Los Angeles Lakers", short_name="LAL", sport="basketball", league="nba", country="USA", city="Los Angeles", founded=1947, home_stadium="Crypto.com Arena", logo_url="https://example.com/lakers-logo.png"),
    Team(id="team_2", name="Boston Celtics", short_name="BOS", sport="basketball", league="nba", country="USA", city="Boston", founded=1946, home_stadium="TD Garden", logo_url="https://example.com/celtics-logo.png"),
    Team(id="team_3", name="Golden State Warriors", short_name="GSW", sport="basketball", league="nba", country="USA", city="San Francisco", founded=1946, home_stadium="Chase Center", logo_url="https://example.com/warriors-logo.png"),
    Team(id="team_4", name="New York Knicks", short_name="NYK", sport="basketball", league="nba", country="USA", city="New York", founded=1946, home_stadium="Madison Square Garden", logo_url="https://example.com/knicks-logo.png"),
]

mock_players = [
    Player(id="player_1", first_name="LeBron", last_name="James", full_name="LeBron James", sport="basketball", team_id="team_1", position="Forward", jersey_number=23, height_cm=206, weight_kg=113, birth_date="1984-12-30", nationality="USA", image_url="https://example.com/lebron.jpg"),
    Player(id="player_2", first_name="Kevin", last_name="Durant", full_name="Kevin Durant", sport="basketball", team_id="team_1", position="Forward", jersey_number=7, height_cm=211, weight_kg=109, birth_date="1988-09-29", nationality="USA", image_url="https://example.com/kd.jpg"),
    Player(id="player_3", first_name="Jayson", last_name="Tatum", full_name="Jayson Tatum", sport="basketball", team_id="team_2", position="Forward", jersey_number=0, height_cm=203, weight_kg=100, birth_date="1998-03-03", nationality="USA", image_url="https://example.com/tatum.jpg"),
    Player(id="player_4", first_name="Jaylen", last_name="Brown", full_name="Jaylen Brown", sport="basketball", team_id="team_2", position="Guard", jersey_number=7, height_cm=198, weight_kg=99, birth_date="1996-10-24", nationality="USA", image_url="https://example.com/brown.jpg"),
]

mock_games = [
    Game(id="game_1", home_team_id="team_1", away_team_id="team_2", sport="basketball", league="nba", start_time=datetime(2026, 6, 10, 19, 30), venue="Crypto.com Arena", city="Los Angeles", country="USA", status="scheduled"),
    Game(id="game_2", home_team_id="team_3", away_team_id="team_4", sport="basketball", league="nba", start_time=datetime(2026, 6, 11, 20, 0), venue="Chase Center", city="San Francisco", country="USA", status="scheduled"),
]

mock_events = [
    GameEvent(id="event_1", game_id="game_1", event_type="basket", team_id="team_1", player_id="player_1", time_elapsed=2.5, period=1, score_home=2, score_away=0, description="LeBron James makes a layup", x_coordinate=4.5, y_coordinate=2.1),
    GameEvent(id="event_2", game_id="game_1", event_type="basket", team_id="team_2", player_id="player_3", time_elapsed=5.2, period=1, score_home=2, score_away=2, description="Jayson Tatum makes a three-pointer", x_coordinate=7.8, y_coordinate=6.3),
]

mock_player_stats = [
    PlayerStats(id="stats_1", player_id="player_1", game_id="game_1", sport="basketball", minutes_played=35.5, points=28, rebounds=9, assists=7, steals=2, blocks=1, turnovers=3, field_goals_made=10, field_goals_attempted=20, three_pointers_made=2, three_pointers_attempted=5, free_throws_made=6, free_throws_attempted=8),
    PlayerStats(id="stats_2", player_id="player_3", game_id="game_1", sport="basketball", minutes_played=38.2, points=32, rebounds=6, assists=5, steals=1, blocks=0, turnovers=2, field_goals_made=11, field_goals_attempted=22, three_pointers_made=4, three_pointers_attempted=8, free_throws_made=7, free_throws_attempted=9),
]

mock_team_stats = [
    TeamStats(id="team_stats_1", team_id="team_1", game_id="game_1", sport="basketball", possession_percentage=52.3, shots=87, shots_on_target=42, corners=5, fouls=18, yellow_cards=0, red_cards=0, penalties=0, turnovers=14, offensive_rebounds=12, defensive_rebounds=34),
    TeamStats(id="team_stats_2", team_id="team_2", game_id="game_1", sport="basketball", possession_percentage=47.7, shots=81, shots_on_target=38, corners=3, fouls=20, yellow_cards=0, red_cards=0, penalties=0, turnovers=16, offensive_rebounds=8, defensive_rebounds=31),
]

mock_predictions = [
    GamePrediction(id="pred_1", game_id="game_1", sport="basketball", predicted_winner="team_1", win_probability_home=0.65, win_probability_away=0.35, predicted_score_home=112, predicted_score_away=108, predicted_total_points=220, confidence_score=0.85, key_factors=["Home team has strong overall win record", "Away team struggles on the road"], model_version="1.0.0"),
]

mock_value_indicators = [
    ValueIndicator(id="value_1", game_id="game_1", sport="basketball", market_type="moneyline", bookmaker="DraftKings", line=0.0, odds=-180, implied_probability=0.643, ai_probability=0.65, value_score=85, confidence_score=0.9, edge=35, recommendation="strong_buy", key_insights=["AI model identifies mispricing in betting market"], model_version="1.0.0"),
    ValueIndicator(id="value_2", game_id="game_1", sport="basketball", market_type="moneyline", bookmaker="DraftKings", line=0.0, odds=150, implied_probability=0.4, ai_probability=0.35, value_score=15, confidence_score=0.85, edge=-35, recommendation="sell", key_insights=["AI model identifies mispricing in betting market"], model_version="1.0.0"),
]

mock_trends = [
    TeamTrend(id="trend_1", team_id="team_1", sport="basketball", trend_type="recent_form", metric="win_percentage", value=0.72, direction="up", period_days=30, confidence_score=0.9, description="The home team has maintained a high win percentage (0.72) over the last 30 days, indicating strong recent form.", model_version="1.0.0"),
]

mock_insights = [
    GameInsight(id="insight_1", game_id="game_1", sport="basketball", insight_type="matchup_advantage", title="Home Team Dominance", description="The home team has a significantly higher win percentage (0.72) compared to the away team (0.58), indicating a clear matchup advantage.", confidence_score=0.9, impact_score=0.7, key_data_points=["Home team win percentage: 0.72", "Away team win percentage: 0.58"], model_version="1.0.0"),
]

mock_reports = [
    AnalyticsReport(id="report_1", subject_type="team", subject_id="team_1", sport="basketball", report_type="game_preview", title="Game Preview Report for Los Angeles Lakers", summary="Comprehensive analysis of Los Angeles Lakers for game preview.", key_findings=["Team has shown consistent performance in recent games", "Key players are performing above league average", "Team has strong home advantage", "Opponents have difficulty scoring against this team"], data_sources=["Team statistics", "Player performance data", "Game event data"], confidence_score=0.9, model_version="1.0.0"),
]

mock_data_feeds = [
    DataFeed(id="feed_1", name="NBA Live Stats", sport="basketball", league="nba", feed_type="live_stats", url="https://api.nba.com/live", api_key_required=True, frequency_minutes=1, last_updated=datetime.now(), status="active"),
]

mock_users = [
    User(id="user_1", email="coach@lakers.com", first_name="Mike", last_name="Brown", role="coach", organization="Los Angeles Lakers", subscription_tier="team_pro", is_active=True, last_login=datetime.now()),
]

mock_preferences = [
    UserPreference(id="pref_1", user_id="user_1", sport="basketball", preferred_metrics=["points", "rebounds", "assists"], display_language="en", notification_preferences={"game_updates": True, "player_injuries": True, "value_indicators": True}),
]

mock_api_keys = [
    APIKey(id="key_1", user_id="user_1", name="Lakers API Key", key="abc123xyz", permissions=["read:analytics", "read:teams", "read:players"], is_active=True, created_at=datetime.now(), created_by="user_1"),
]

# Helper functions to find items by ID

def find_team_by_id(team_id: str):
    for team in mock_teams:
        if team.id == team_id:
            return team
    return None

def find_player_by_id(player_id: str):
    for player in mock_players:
        if player.id == player_id:
            return player
    return None

def find_game_by_id(game_id: str):
    for game in mock_games:
        if game.id == game_id:
            return game
    return None

def find_events_by_game_id(game_id: str):
    return [event for event in mock_events if event.game_id == game_id]

def find_player_stats_by_game_id(game_id: str):
    return [stats for stats in mock_player_stats if stats.game_id == game_id]

def find_team_stats_by_game_id(game_id: str):
    return [stats for stats in mock_team_stats if stats.game_id == game_id]

def find_predictions_by_game_id(game_id: str):
    return [pred for pred in mock_predictions if pred.game_id == game_id]

def find_value_indicators_by_game_id(game_id: str):
    return [val for val in mock_value_indicators if val.game_id == game_id]

def find_trends_by_team_id(team_id: str):
    return [trend for trend in mock_trends if trend.team_id == team_id]

def find_insights_by_game_id(game_id: str):
    return [insight for insight in mock_insights if insight.game_id == game_id]

def find_report_by_id(report_id: str):
    for report in mock_reports:
        if report.id == report_id:
            return report
    return None

def find_data_feed_by_id(feed_id: str):
    for feed in mock_data_feeds:
        if feed.id == feed_id:
            return feed
    return None

def find_user_by_email(email: str):
    for user in mock_users:
        if user.email == email:
            return user
    return None

def find_user_preference_by_user_id(user_id: str):
    for pref in mock_preferences:
        if pref.user_id == user_id:
            return pref
    return None

def find_api_key_by_key(key: str):
    for api_key in mock_api_keys:
        if api_key.key == key:
            return api_key
    return None

# API Endpoints

@router.get("/health", response_model=dict)
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "healthy",
        "service": "StatEdge Pro API",
        "version": "1.0.0",
        "environment": "development",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/", response_model=dict)
async def root():
    """
    Root endpoint providing API documentation.
    """
    return {
        "message": "Welcome to StatEdge Pro API",
        "documentation": "https://statedge-pro.com/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "teams": "/api/v1/teams",
            "players": "/api/v1/players",
            "games": "/api/v1/games",
            "analytics": "/api/v1/analytics",
            "value-finder": "/api/v1/value-finder",
            "reports": "/api/v1/reports",
            "data-feeds": "/api/v1/data-feeds",
            "users": "/api/v1/users",
            "api-keys": "/api/v1/api-keys"
        }
    }

# Teams API

@router.get("/teams", response_model=List[Team])
async def get_teams(sport: Optional[str] = None, league: Optional[str] = None):
    """
    Get a list of all teams.
    
    Args:
        sport: Filter by sport type
        league: Filter by league
    """
    teams = mock_teams
    
    if sport:
        teams = [team for team in teams if team.sport == sport]
    
    if league:
        teams = [team for team in teams if team.league == league]
    
    return teams

@router.get("/teams/{team_id}", response_model=Team)
async def get_team(team_id: str):
    """
    Get a specific team by ID.
    """
    team = find_team_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Players API

@router.get("/players", response_model=List[Player])
async def get_players(team_id: Optional[str] = None, sport: Optional[str] = None):
    """
    Get a list of all players.
    
    Args:
        team_id: Filter by team ID
        sport: Filter by sport type
    """
    players = mock_players
    
    if team_id:
        players = [player for player in players if player.team_id == team_id]
    
    if sport:
        players = [player for player in players if player.sport == sport]
    
    return players

@router.get("/players/{player_id}", response_model=Player)
async def get_player(player_id: str):
    """
    Get a specific player by ID.
    """
    player = find_player_by_id(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

# Games API

@router.get("/games", response_model=List[Game])
async def get_games(sport: Optional[str] = None, league: Optional[str] = None, status: Optional[str] = None):
    """
    Get a list of all games.
    
    Args:
        sport: Filter by sport type
        league: Filter by league
        status: Filter by game status
    """
    games = mock_games
    
    if sport:
        games = [game for game in games if game.sport == sport]
    
    if league:
        games = [game for game in games if game.league == league]
    
    if status:
        games = [game for game in games if game.status == status]
    
    return games

@router.get("/games/{game_id}", response_model=Game)
async def get_game(game_id: str):
    """
    Get a specific game by ID.
    """
    game = find_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.get("/games/{game_id}/events", response_model=List[GameEvent])
async def get_game_events(game_id: str):
    """
    Get all events for a specific game.
    """
    events = find_events_by_game_id(game_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this game")
    return events

@router.get("/games/{game_id}/player-stats", response_model=List[PlayerStats])
async def get_game_player_stats(game_id: str):
    """
    Get player statistics for a specific game.
    """
    stats = find_player_stats_by_game_id(game_id)
    if not stats:
        raise HTTPException(status_code=404, detail="No player stats found for this game")
    return stats

@router.get("/games/{game_id}/team-stats", response_model=List[TeamStats])
async def get_game_team_stats(game_id: str):
    """
    Get team statistics for a specific game.
    """
    stats = find_team_stats_by_game_id(game_id)
    if not stats:
        raise HTTPException(status_code=404, detail="No team stats found for this game")
    return stats

# Analytics API

@router.get("/analytics/{game_id}", response_model=dict)
async def get_game_analytics(game_id: str):
    """
    Get comprehensive analytics for a specific game.
    
    This endpoint processes the game data and returns predictions,
    value indicators, insights, and trends.
    """
    game = find_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    events = find_events_by_game_id(game_id)
    home_team_stats = find_team_stats_by_game_id(game_id)[0] if find_team_stats_by_game_id(game_id) else None
    away_team_stats = find_team_stats_by_game_id(game_id)[1] if len(find_team_stats_by_game_id(game_id)) > 1 else None
    home_player_stats = [stats for stats in find_player_stats_by_game_id(game_id) if stats.player_id in [p.id for p in mock_players if p.team_id == game.home_team_id]]
    away_player_stats = [stats for stats in find_player_stats_by_game_id(game_id) if stats.player_id in [p.id for p in mock_players if p.team_id == game.away_team_id]]
    
    # Process the game data using the analytics engine
    result = await analytics_engine.process_game_data(game, events, home_team_stats, away_team_stats, home_player_stats, away_player_stats)
    
    return result

@router.get("/analytics/{game_id}/predictions", response_model=List[GamePrediction])
async def get_game_predictions(game_id: str):
    """
    Get AI-generated predictions for a specific game.
    """
    predictions = find_predictions_by_game_id(game_id)
    if not predictions:
        raise HTTPException(status_code=404, detail="No predictions found for this game")
    return predictions

@router.get("/analytics/{game_id}/value-indicators", response_model=List[ValueIndicator])
async def get_game_value_indicators(game_id: str):
    """
    Get value indicators for betting markets for a specific game.
    """
    value_indicators = find_value_indicators_by_game_id(game_id)
    if not value_indicators:
        raise HTTPException(status_code=404, detail="No value indicators found for this game")
    return value_indicators

@router.get("/analytics/{game_id}/insights", response_model=List[GameInsight])
async def get_game_insights(game_id: str):
    """
    Get AI-generated insights about a specific game.
    """
    insights = find_insights_by_game_id(game_id)
    if not insights:
        raise HTTPException(status_code=404, detail="No insights found for this game")
    return insights

@router.get("/analytics/teams/{team_id}/trends", response_model=List[TeamTrend])
async def get_team_trends(team_id: str):
    """
    Get statistical trends for a specific team.
    """
    trends = find_trends_by_team_id(team_id)
    if not trends:
        raise HTTPException(status_code=404, detail="No trends found for this team")
    return trends

# Reports API

@router.get("/reports/{report_id}", response_model=AnalyticsReport)
async def get_report(report_id: str):
    """
    Get a specific analytics report by ID.
    """
    report = find_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.post("/reports", response_model=AnalyticsReport)
async def generate_report(team_id: str, report_type: str):
    """
    Generate a comprehensive analytics report for a team.
    
    Args:
        team_id: ID of the team
        report_type: Type of report to generate (game_preview, post_game_analysis, trend_analysis)
    """
    report = await analytics_engine.generate_analytics_report(team_id, report_type)
    mock_reports.append(report)
    return report

# Data Feeds API

@router.get("/data-feeds", response_model=List[DataFeed])
async def get_data_feeds(sport: Optional[str] = None):
    """
    Get a list of all data feeds.
    
    Args:
        sport: Filter by sport type
    """
    feeds = mock_data_feeds
    
    if sport:
        feeds = [feed for feed in feeds if feed.sport == sport]
    
    return feeds

@router.get("/data-feeds/{feed_id}", response_model=DataFeed)
async def get_data_feed(feed_id: str):
    """
    Get a specific data feed by ID.
    """
    feed = find_data_feed_by_id(feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Data feed not found")
    return feed

@router.post("/data-feeds/{feed_id}/process")
async def process_data_feed(feed_id: str):
    """
    Process a data feed manually.
    """
    feed = find_data_feed_by_id(feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Data feed not found")
    
    updated_feed = await analytics_engine.process_live_data_stream(feed)
    return {"status": "processed", "feed": updated_feed}

# Users API

@router.get("/users/me", response_model=User)
async def get_current_user():
    """
    Get the current user's profile.
    """
    # In production, this would use authentication
    # For now, return a mock user
    return mock_users[0]

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """
    Get a specific user by ID.
    """
    # In production, this would check permissions
    # For now, return a mock user
    for user in mock_users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/users/{user_id}/preferences", response_model=UserPreference)
async def get_user_preferences(user_id: str):
    """
    Get a specific user's preferences.
    """
    pref = find_user_preference_by_user_id(user_id)
    if not pref:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return pref

# API Keys API

@router.get("/api-keys", response_model=List[APIKey])
async def get_api_keys():
    """
    Get a list of all API keys for the current user.
    """
    # In production, this would filter by authenticated user
    # For now, return all keys
    return mock_api_keys

@router.post("/api-keys", response_model=APIKey)
async def create_api_key(name: str, permissions: List[str]):
    """
    Create a new API key for the current user.
    
    Args:
        name: Name for the API key
        permissions: List of permissions for the API key
    """
    # In production, this would use the authenticated user
    # For now, use the first user
    user_id = mock_users[0].id
    
    # Generate a random API key
    import secrets
    api_key = secrets.token_urlsafe(32)
    
    new_key = APIKey(
        id=f"key_{len(mock_api_keys) + 1}",
        user_id=user_id,
        name=name,
        key=api_key,
        permissions=permissions,
        is_active=True,
        created_at=datetime.now(),
        created_by=user_id
    )
    
    mock_api_keys.append(new_key)
    return new_key

@router.delete("/api-keys/{key_id}")
async def delete_api_key(key_id: str):
    """
    Delete an API key.
    """
    for i, key in enumerate(mock_api_keys):
        if key.id == key_id:
            mock_api_keys.pop(i)
            return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="API key not found")

# Value Finder API (specialized endpoint)

@router.get("/value-finder", response_model=List[ValueIndicator])
async def get_value_finder(sport: Optional[str] = None, league: Optional[str] = None, recommendation: Optional[str] = None):
    """
    Get value indicators across all games.
    
    Args:
        sport: Filter by sport type
        league: Filter by league
        recommendation: Filter by recommendation type (strong_buy, buy, neutral, sell, strong_sell)
    """
    # In production, this would query all games
    # For now, return all value indicators
    value_indicators = mock_value_indicators
    
    if sport:
        value_indicators = [val for val in value_indicators if val.sport == sport]
    
    if league:
        value_indicators = [val for val in value_indicators if val.league == league]
    
    if recommendation:
        value_indicators = [val for val in value_indicators if val.recommendation == recommendation]
    
    return value_indicators

@router.get("/value-finder/{game_id}", response_model=List[ValueIndicator])
async def get_value_finder_by_game(game_id: str):
    """
    Get value indicators for a specific game.
    """
    value_indicators = find_value_indicators_by_game_id(game_id)
    if not value_indicators:
        raise HTTPException(status_code=404, detail="No value indicators found for this game")
    return value_indicators

# Admin endpoints

@router.post("/admin/update-models")
async def update_models():
    """
    Update machine learning models with new data.
    """
    success = await analytics_engine.update_models()
    return {"status": "success" if success else "failed"}

@router.post("/admin/run-daily-analysis")
async def run_daily_analysis():
    """
    Run daily analysis on all games.
    """
    success = await analytics_engine.run_daily_analysis()
    return {"status": "success" if success else "failed"}

@router.post("/admin/generate-weekly-summary")
async def generate_weekly_summary():
    """
    Generate a weekly summary report.
    """
    success = await analytics_engine.generate_weekly_summary()
    return {"status": "success" if success else "failed"}

@router.post("/admin/optimize-model-performance")
async def optimize_model_performance():
    """
    Optimize model performance based on feedback.
    """
    success = await analytics_engine.optimize_model_performance()
    return {"status": "success" if success else "failed"}
