"""
Sports data models for StatEdge Pro.

Defines the core data structures for representing teams, players, games,
and statistics across all sports and leagues worldwide.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class SportType(str, Enum):
    """Enumeration of supported sports."""
    SOCCER = "soccer"
    BASKETBALL = "basketball"
    FOOTBALL = "football"  # American football
    BASEBALL = "baseball"
    HOCKEY = "hockey"
    TENNIS = "tennis"
    CRICKET = "cricket"
    RUGBY = "rugby"
    VOLLEYBALL = "volleyball"
    GOLF = "golf"
    BOXING = "boxing"
    MMA = "mma"
    CYCLING = "cycling"
    SWIMMING = "swimming"
    ATHLETICS = "athletics"


class LeagueType(str, Enum):
    """Enumeration of major leagues worldwide."""
    # Soccer
    PREMIER_LEAGUE = "premier_league"  # England
    LA_LIGA = "la_liga"  # Spain
    SERIE_A = "serie_a"  # Italy
    BUNDESLIGA = "bundesliga"  # Germany
    LIGUE_1 = "ligue_1"  # France
    MLS = "mls"  # USA/Canada
    BRAZILIAN_S1 = "brazilian_s1"  # Brazil
    ARGENTINA_PRIMERA = "argentina_primera"  # Argentina
    JAPAN_J1 = "japan_j1"  # Japan
    CHINA_SUPER = "china_super"  # China
    A_LEAGUE = "a_league"  # Australia
    # Basketball
    NBA = "nba"  # USA/Canada
    EUROLEAGUE = "euroleague"  # Europe
    CBA = "cba"  # China
    # Football (American)
    NFL = "nfl"  # USA
    CFL = "cfl"  # Canada
    # Baseball
    MLB = "mlb"  # USA/Canada
    NPB = "npb"  # Japan
    KBO = "kbo"  # Korea
    # Hockey
    NHL = "nhl"  # USA/Canada
    KHL = "khl"  # Russia/International
    # Tennis
    ATP = "atp"  # Men's tennis
    WTA = "wta"  # Women's tennis
    # Cricket
    IPL = "ipl"  # India
    PSL = "psl"  # Pakistan
    BBL = "bbl"  # Australia
    # Rugby
    PREMIERSHIP = "premiership"  # England
    TOP14 = "top14"  # France
    SUPER_RUGBY = "super_rugby"  # International
    # Golf
    PGA = "pga"  # USA
    EUROPEAN_TOUR = "european_tour"
    # MMA
    UFC = "ufc"
    ONE_CHAMPIONSHIP = "one_championship"


class Team(BaseModel):
    """Represents a sports team."""
    id: str = Field(..., description="Unique identifier for the team")
    name: str = Field(..., description="Full name of the team")
    short_name: str = Field(..., description="Short name or abbreviation")
    sport: SportType = Field(..., description="Type of sport")
    league: LeagueType = Field(..., description="League the team competes in")
    country: str = Field(..., description="Country where the team is based")
    city: str = Field(..., description="City where the team is based")
    founded: Optional[int] = Field(None, description="Year the team was founded")
    home_stadium: Optional[str] = Field(None, description="Name of home stadium")
    logo_url: Optional[str] = Field(None, description="URL to team logo")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Player(BaseModel):
    """Represents an athlete."""
    id: str = Field(..., description="Unique identifier for the player")
    first_name: str = Field(..., description="Player's first name")
    last_name: str = Field(..., description="Player's last name")
    full_name: str = Field(..., description="Full name of the player")
    sport: SportType = Field(..., description="Type of sport")
    team_id: str = Field(..., description="ID of the team the player belongs to")
    position: str = Field(..., description="Player's position or role")
    jersey_number: Optional[int] = Field(None, description="Player's jersey number")
    height_cm: Optional[float] = Field(None, description="Height in centimeters")
    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    birth_date: Optional[str] = Field(None, description="Date of birth in YYYY-MM-DD format")
    nationality: str = Field(..., description="Player's nationality")
    image_url: Optional[str] = Field(None, description="URL to player image")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Game(BaseModel):
    """Represents a sports match or game."""
    id: str = Field(..., description="Unique identifier for the game")
    home_team_id: str = Field(..., description="ID of the home team")
    away_team_id: str = Field(..., description="ID of the away team")
    sport: SportType = Field(..., description="Type of sport")
    league: LeagueType = Field(..., description="League the game is part of")
    start_time: datetime = Field(..., description="Scheduled start time of the game")
    actual_start_time: Optional[datetime] = Field(None, description="Actual start time of the game")
    venue: str = Field(..., description="Name of the venue")
    city: str = Field(..., description="City where the game is played")
    country: str = Field(..., description="Country where the game is played")
    status: str = Field(..., description="Game status: scheduled, in_progress, completed, cancelled")
    home_score: Optional[int] = Field(None, description="Final score for home team")
    away_score: Optional[int] = Field(None, description="Final score for away team")
    home_team_won: Optional[bool] = Field(None, description="Whether home team won")
    attendance: Optional[int] = Field(None, description="Number of spectators")
    weather_conditions: Optional[str] = Field(None, description="Weather during game")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GameEvent(BaseModel):
    """Represents a specific event during a game."""
    id: str = Field(..., description="Unique identifier for the event")
    game_id: str = Field(..., description="ID of the game this event belongs to")
    event_type: str = Field(..., description="Type of event (e.g., goal, basket, touchdown)")
    team_id: str = Field(..., description="ID of the team that performed the event")
    player_id: Optional[str] = Field(None, description="ID of the player who performed the event")
    time_elapsed: float = Field(..., description="Time elapsed in the game (in minutes)")
    period: int = Field(..., description="Period or quarter of the game")
    score_home: int = Field(..., description="Home team score after this event")
    score_away: int = Field(..., description="Away team score after this event")
    description: str = Field(..., description="Detailed description of the event")
    x_coordinate: Optional[float] = Field(None, description="X coordinate on field/court")
    y_coordinate: Optional[float] = Field(None, description="Y coordinate on field/court")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PlayerStats(BaseModel):
    """Represents statistical performance of a player in a game."""
    id: str = Field(..., description="Unique identifier for the stats record")
    player_id: str = Field(..., description="ID of the player")
    game_id: str = Field(..., description="ID of the game")
    sport: SportType = Field(..., description="Type of sport")
    minutes_played: Optional[float] = Field(None, description="Minutes played")
    points: Optional[int] = Field(None, description="Points scored")
    rebounds: Optional[int] = Field(None, description="Rebounds")
    assists: Optional[int] = Field(None, description="Assists")
    steals: Optional[int] = Field(None, description="Steals")
    blocks: Optional[int] = Field(None, description="Blocks")
    turnovers: Optional[int] = Field(None, description="Turnovers")
    field_goals_made: Optional[int] = Field(None, description="Field goals made")
    field_goals_attempted: Optional[int] = Field(None, description="Field goals attempted")
    three_pointers_made: Optional[int] = Field(None, description="Three pointers made")
    three_pointers_attempted: Optional[int] = Field(None, description="Three pointers attempted")
    free_throws_made: Optional[int] = Field(None, description="Free throws made")
    free_throws_attempted: Optional[int] = Field(None, description="Free throws attempted")
    goals: Optional[int] = Field(None, description="Goals scored (soccer, hockey)")
    shots: Optional[int] = Field(None, description="Shots taken (soccer, hockey)")
    saves: Optional[int] = Field(None, description="Saves (goalie stats)")
    tackles: Optional[int] = Field(None, description="Tackles (soccer, rugby)")
    passes: Optional[int] = Field(None, description="Passes completed")
    completion_rate: Optional[float] = Field(None, description="Pass completion rate")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TeamStats(BaseModel):
    """Represents statistical performance of a team in a game."""
    id: str = Field(..., description="Unique identifier for the stats record")
    team_id: str = Field(..., description="ID of the team")
    game_id: str = Field(..., description="ID of the game")
    sport: SportType = Field(..., description="Type of sport")
    possession_percentage: Optional[float] = Field(None, description="Possession percentage (soccer)")
    shots: Optional[int] = Field(None, description="Total shots")
    shots_on_target: Optional[int] = Field(None, description="Shots on target")
    corners: Optional[int] = Field(None, description="Corners taken")
    fouls: Optional[int] = Field(None, description="Fouls committed")
    yellow_cards: Optional[int] = Field(None, description="Yellow cards received")
    red_cards: Optional[int] = Field(None, description="Red cards received")
    penalties: Optional[int] = Field(None, description="Penalties awarded")
    turnovers: Optional[int] = Field(None, description="Turnovers (basketball, football)")
    offensive_rebounds: Optional[int] = Field(None, description="Offensive rebounds (basketball)")
    defensive_rebounds: Optional[int] = Field(None, description="Defensive rebounds (basketball)")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class GamePrediction(BaseModel):
    """Represents AI-generated predictions for a game."""
    id: str = Field(..., description="Unique identifier for the prediction")
    game_id: str = Field(..., description="ID of the game")
    sport: SportType = Field(..., description="Type of sport")
    predicted_winner: str = Field(..., description="Predicted winning team ID")
    win_probability_home: float = Field(..., description="Probability home team wins (0.0-1.0)")
    win_probability_away: float = Field(..., description="Probability away team wins (0.0-1.0)")
    predicted_score_home: int = Field(..., description="Predicted final score for home team")
    predicted_score_away: int = Field(..., description="Predicted final score for away team")
    predicted_total_points: int = Field(..., description="Predicted total points in game")
    confidence_score: float = Field(..., description="AI confidence in prediction (0.0-1.0)")
    key_factors: List[str] = Field(..., description="Key factors influencing prediction")
    model_version: str = Field(..., description="Version of the prediction model used")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ValueIndicator(BaseModel):
    """Represents a value indicator for betting markets."""
    id: str = Field(..., description="Unique identifier for the value indicator")
    game_id: str = Field(..., description="ID of the game")
    sport: SportType = Field(..., description="Type of sport")
    market_type: str = Field(..., description="Type of betting market (e.g., moneyline, spread, over_under)")
    bookmaker: str = Field(..., description="Bookmaker offering the odds")
    line: float = Field(..., description="The betting line (spread, total, etc.)")
    odds: float = Field(..., description="The betting odds (American format)")
    implied_probability: float = Field(..., description="Implied probability from odds")
    ai_probability: float = Field(..., description="AI-generated probability")
    value_score: float = Field(..., description="Value indicator score (0-100)")
    confidence_score: float = Field(..., description="Confidence in value score (0.0-1.0)")
    edge: float = Field(..., description="Edge in percentage points")
    recommendation: str = Field(..., description="Recommendation: 'strong_buy', 'buy', 'neutral', 'sell', 'strong_sell'")
    key_insights: List[str] = Field(..., description="Key insights supporting this value indicator")
    model_version: str = Field(..., description="Version of the value model used")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TeamTrend(BaseModel):
    """Represents a statistical trend for a team."""
    id: str = Field(..., description="Unique identifier for the trend")
    team_id: str = Field(..., description="ID of the team")
    sport: SportType = Field(..., description="Type of sport")
    trend_type: str = Field(..., description="Type of trend (e.g., home_advantage, recent_form, injury_impact)")
    metric: str = Field(..., description="The statistical metric being tracked")
    value: float = Field(..., description="The value of the trend")
    direction: str = Field(..., description="Direction of change: 'up', 'down', 'stable'")
    period_days: int = Field(..., description="Number of days the trend covers")
    confidence_score: float = Field(..., description="Confidence in the trend (0.0-1.0)")
    description: str = Field(..., description="Detailed description of the trend")
    model_version: str = Field(..., description="Version of the trend model used")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GameInsight(BaseModel):
    """Represents an AI-generated insight about a game."""
    id: str = Field(..., description="Unique identifier for the insight")
    game_id: str = Field(..., description="ID of the game")
    sport: SportType = Field(..., description="Type of sport")
    insight_type: str = Field(..., description="Type of insight (e.g., matchup_advantage, weather_impact, momentum)")
    title: str = Field(..., description="Brief title of the insight")
    description: str = Field(..., description="Detailed description of the insight")
    confidence_score: float = Field(..., description="Confidence in the insight (0.0-1.0)")
    impact_score: float = Field(..., description="Impact score on game outcome (0.0-1.0)")
    key_data_points: List[str] = Field(..., description="Key data points supporting the insight")
    model_version: str = Field(..., description="Version of the insight model used")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AnalyticsReport(BaseModel):
    """Represents a comprehensive analytics report for a team or player."""
    id: str = Field(..., description="Unique identifier for the report")
    subject_type: str = Field(..., description="Type of subject: 'team' or 'player'")
    subject_id: str = Field(..., description="ID of the team or player")
    sport: SportType = Field(..., description="Type of sport")
    report_type: str = Field(..., description="Type of report: 'game_preview', 'post_game_analysis', 'trend_analysis'")
    title: str = Field(..., description="Title of the report")
    summary: str = Field(..., description="Executive summary of the report")
    key_findings: List[str] = Field(..., description="Key findings from the analysis")
    data_sources: List[str] = Field(..., description="Sources of data used in the report")
    confidence_score: float = Field(..., description="Overall confidence in the report (0.0-1.0)")
    model_version: str = Field(..., description="Version of the analysis model used")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DataFeed(BaseModel):
    """Represents a source of sports data."""
    id: str = Field(..., description="Unique identifier for the data feed")
    name: str = Field(..., description="Name of the data feed")
    sport: SportType = Field(..., description="Type of sport")
    league: Optional[LeagueType] = Field(None, description="Specific league if applicable")
    feed_type: str = Field(..., description="Type of data: 'live_stats', 'boxscore', 'injury_report', 'weather'")
    url: str = Field(..., description="URL or endpoint for the data feed")
    api_key_required: bool = Field(..., description="Whether an API key is required")
    frequency_minutes: int = Field(..., description="Frequency of data updates in minutes")
    last_updated: datetime = Field(..., description="When the data feed was last updated")
    status: str = Field(..., description="Status: 'active', 'inactive', 'error'")
    error_message: Optional[str] = Field(None, description="Error message if status is 'error'")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class User(BaseModel):
    """Represents a user of the StatEdge Pro platform."""
    id: str = Field(..., description="Unique identifier for the user")
    email: str = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    role: str = Field(..., description="User role: 'team_admin', 'coach', 'analyst', 'bettor', 'admin'")
    organization: Optional[str] = Field(None, description="Organization the user belongs to")
    subscription_tier: str = Field(..., description="Subscription tier: 'team_pro', 'pro_bettor', 'enterprise'")
    is_active: bool = Field(default=True, description="Whether the user account is active")
    last_login: Optional[datetime] = Field(None, description="When the user last logged in")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserPreference(BaseModel):
    """Represents user-specific preferences for analytics display."""
    id: str = Field(..., description="Unique identifier for the preference")
    user_id: str = Field(..., description="ID of the user")
    sport: SportType = Field(..., description="Type of sport")
    preferred_metrics: List[str] = Field(..., description="List of preferred statistical metrics")
    display_language: str = Field(..., description="Preferred display language (e.g., 'en', 'es', 'fr')")
    notification_preferences: Dict[str, bool] = Field(..., description="Preferences for different types of notifications")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class APIKey(BaseModel):
    """Represents an API key for programmatic access to StatEdge Pro."""
    id: str = Field(..., description="Unique identifier for the API key")
    user_id: str = Field(..., description="ID of the user who owns this key")
    name: str = Field(..., description="Name of the API key for identification")
    key: str = Field(..., description="The actual API key value")
    permissions: List[str] = Field(..., description="List of permissions granted to this key")
    is_active: bool = Field(default=True, description="Whether the API key is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(None, description="When the API key expires")
    last_used: Optional[datetime] = Field(None, description="When the API key was last used")
    usage_count: int = Field(default=0, description="Number of times the API key has been used")
    ip_whitelist: List[str] = Field(default_factory=list, description="List of allowed IP addresses")
    created_by: str = Field(..., description="ID of the user who created this key")
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AuditLog(BaseModel):
    """Represents an audit log entry for system activities."""
    id: str = Field(..., description="Unique identifier for the log entry")
    user_id: Optional[str] = Field(None, description="ID of the user who performed the action")
    action: str = Field(..., description="Type of action performed")
    resource_type: str = Field(..., description="Type of resource affected")
    resource_id: Optional[str] = Field(None, description="ID of the resource affected")
    old_value: Optional[Dict[str, Any]] = Field(None, description="Previous state of the resource")
    new_value: Optional[Dict[str, Any]] = Field(None, description="New state of the resource")
    ip_address: str = Field(..., description="IP address from which the action was performed")
    user_agent: str = Field(..., description="User agent string of the client")
    status: str = Field(..., description="Status of the action: 'success', 'failed'")
    error_message: Optional[str] = Field(None, description="Error message if status is 'failed'")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FeatureFlag(BaseModel):
    """Represents a feature flag for controlling feature rollouts."""
    id: str = Field(..., description="Unique identifier for the feature flag")
    name: str = Field(..., description="Name of the feature flag")
    description: str = Field(..., description="Description of the feature")
    enabled: bool = Field(default=False, description="Whether the feature is enabled")
    target_users: List[str] = Field(default_factory=list, description="List of user IDs who can access this feature")
    target_teams: List[str] = Field(default_factory=list, description="List of team IDs who can access this feature")
    percentage: int = Field(default=0, description="Percentage of users to enable this feature for")
    environment: str = Field(default="production", description="Environment this flag applies to: 'development', 'staging', 'production'")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(..., description="ID of the user who created this flag")
    expires_at: Optional[datetime] = Field(None, description="When this feature flag expires")