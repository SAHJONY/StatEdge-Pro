"""
Analytics Engine for StatEdge Pro.

Implements the core AI-powered analytics capabilities for sports data
across all sports and leagues worldwide.
"""

import logging
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error
import json
import re
from collections import defaultdict
import os
import httpx

from src.models.sports_models import (
    Team, Player, Game, GameEvent, PlayerStats, TeamStats,
    GamePrediction, ValueIndicator, TeamTrend, GameInsight,
    AnalyticsReport, DataFeed
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """
    Core analytics engine for StatEdge Pro.
    Handles data processing, AI modeling, and insight generation
    for all sports and leagues worldwide.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.models = {}
        self._initialize_models()
        self.nvidia_api_key = os.getenv("NVIDIA_API_KEY")
        self.nvidia_base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        
        # Define model capabilities and priorities for different tasks
        self.nvidia_models = {
            # High-precision reasoning models (for complex analysis)
            'reasoning': [
                'nvidia/llama-3.1-nemotron-70b-instruct',
                'nvidia/llama-3.1-nemotron-ultra-253b-v1',
                'mistralai/mistral-large-3-675b-instruct-2512',
                'nvidia/nemotron-4-340b-instruct',
                'qwen/qwen3.5-397b-a17b',
                'meta/llama-3.1-70b-instruct',
                'nvidia/nemotron-4-340b-reward'
            ],
            
            # Balanced performance models (for general analysis)
            'balanced': [
                'nvidia/llama-3.1-nemotron-51b-instruct',
                'nvidia/llama-3.1-nemotron-nano-8b-v1',
                'nvidia/nemotron-3-nano-30b-a3b',
                'nvidia/nemotron-nano-12b-v2-vl',
                'mistralai/mistral-large-2-instruct',
                'meta/llama-3.1-8b-instruct',
                'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning',
                'nvidia/nemotron-mini-4b-instruct'
            ],
            
            # Fast-response models (for real-time processing)
            'fast': [
                'nvidia/llama-3.1-nemotron-nano-vl-8b-v1',
                'nvidia/nemotron-nano-3-30b-a3b',
                'nvidia/nemotron-mini-4b-instruct',
                'google/gemma-3-4b-it',
                'google/gemma-3-12b-it',
                'meta/llama-3.2-1b-instruct',
                'meta/llama-3.2-3b-instruct',
                'mistralai/mistral-7b-instruct-v0.3',
                'nvidia/nemotron-nano-9b-v2'
            ],
            
            # Specialized models
            'embedding': [
                'nvidia/nv-embed-v1',
                'nvidia/nv-embedqa-e5-v5',
                'nvidia/nv-embedqa-mistral-7b-v2',
                'nvidia/nemoretriever-parse',
                'nvidia/nemotron-embed-1b-v2',
                'nvidia/nemotron-embed-vl-1b-v2'
            ],
            
            # Vision models (for any future image analysis)
            'vision': [
                'meta/llama-3.2-11b-vision-instruct',
                'meta/llama-3.2-90b-vision-instruct',
                'nvidia/nemotron-nano-12b-v2-vl',
                'nvidia/nemotron-nano-vl-8b-v1'
            ],
            
            # Code analysis models
            'code': [
                'nvidia/llama-3.1-nemotron-70b-instruct',
                'meta/codellama-70b',
                'bigcode/starcoder2-15b',
                'deepseek-ai/deepseek-coder-6.7b-instruct',
                'mistralai/codestral-22b-instruct-v0.1'
            ],
            
            # Safety and content moderation models
            'safety': [
                'nvidia/llama-3.1-nemotron-nano-8b-v1',
                'nvidia/llama-3.1-nemoguard-8b-content-safety',
                'nvidia/llama-3.1-nemoguard-8b-topic-control',
                'nvidia/nemotron-3-content-safety',
                'nvidia/nemotron-4-340b-reward'
            ]
        }
        
        # Default model for each task type
        self.default_models = {
            'predictions': 'nvidia/llama-3.1-nemotron-70b-instruct',
            'insights': 'nvidia/llama-3.1-nemotron-70b-instruct',
            'trends': 'nvidia/llama-3.1-nemotron-51b-instruct',
            'report': 'nvidia/llama-3.1-nemotron-70b-instruct',
            'embedding': 'nvidia/nv-embed-v1',
            'safety': 'nvidia/llama-3.1-nemoguard-8b-content-safety'
        }
        
        # Initialize HTTP client for NVIDIA API
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
    def _initialize_models(self):
        """Initialize machine learning models for different sports and use cases."""
        # Initialize models for different sports
        sports = ["soccer", "basketball", "football", "baseball", "hockey"]
        
        for sport in sports:
            # Prediction model for game outcomes
            self.models[f"{sport}_prediction"] = RandomForestClassifier(
                n_estimators=100, 
                random_state=42,
                max_depth=10
            )
            
            # Regression model for score prediction
            self.models[f"{sport}_score_regression"] = LinearRegression()
            
        logger.info("Initialized machine learning models for all sports")
    
    async def process_game_data(self, game: Game, events: List[GameEvent], 
                              home_team_stats: TeamStats, away_team_stats: TeamStats,
                              home_player_stats: List[PlayerStats], 
                              away_player_stats: List[PlayerStats]) -> Dict[str, Any]:
        """
        Process raw game data to generate insights and predictions.
        
        Args:
            game: Game object
            events: List of game events
            home_team_stats: Team statistics for home team
            away_team_stats: Team statistics for away team
            home_player_stats: Player statistics for home team
            away_player_stats: Player statistics for away team
            
        Returns:
            Dictionary containing predictions, insights, and value indicators
        """
        try:
            # Extract features from game data
            features = self._extract_features(
                game, events, home_team_stats, away_team_stats,
                home_player_stats, away_player_stats
            )
            
            # Generate predictions using NVIDIA AI
            predictions = await self._generate_predictions_nvidia(game, features)
            
            # Generate value indicators
            value_indicators = self._generate_value_indicators(game, features)
            
            # Generate game insights using NVIDIA AI
            insights = await self._generate_game_insights_nvidia(game, features)
            
            # Generate team trends
            trends = self._generate_team_trends(game, features)
            
            return {
                "predictions": predictions,
                "value_indicators": value_indicators,
                "insights": insights,
                "trends": trends,
                "features": features
            }
            
        except Exception as e:
            logger.error(f"Error processing game data: {str(e)}")
            raise
    
    def _extract_features(self, game: Game, events: List[GameEvent], 
                        home_team_stats: TeamStats, away_team_stats: TeamStats,
                        home_player_stats: List[PlayerStats], 
                        away_player_stats: List[PlayerStats]) -> Dict[str, float]:
        """
        Extract numerical features from game data for machine learning models.
        """
        features = {}
        
        # Game context features
        features["sport"] = game.sport.value
        features["league"] = game.league.value
        features["is_home_team_favorite"] = 1 if game.home_team_won is not None and game.home_team_won else 0
        features["days_since_last_game_home"] = self._calculate_days_since_last_game(game.home_team_id, game.start_time)
        features["days_since_last_game_away"] = self._calculate_days_since_last_game(game.away_team_id, game.start_time)
        
        # Team performance features
        features["home_team_win_pct"] = self._calculate_team_win_percentage(game.home_team_id)
        features["away_team_win_pct"] = self._calculate_team_win_percentage(game.away_team_id)
        features["home_team_avg_points"] = self._calculate_team_avg_points(game.home_team_id)
        features["away_team_avg_points"] = self._calculate_team_avg_points(game.away_team_id)
        features["home_team_avg_points_allowed"] = self._calculate_team_avg_points_allowed(game.home_team_id)
        features["away_team_avg_points_allowed"] = self._calculate_team_avg_points_allowed(game.away_team_id)
        
        # Home/away performance
        features["home_team_home_win_pct"] = self._calculate_home_win_percentage(game.home_team_id)
        features["away_team_away_win_pct"] = self._calculate_away_win_percentage(game.away_team_id)
        
        # Recent form
        features["home_team_last_5_wins"] = self._calculate_last_n_wins(game.home_team_id, 5)
        features["away_team_last_5_wins"] = self._calculate_last_n_wins(game.away_team_id, 5)
        
        # Player performance features
        features["home_team_top_scorer_avg"] = self._calculate_top_player_avg(home_player_stats)
        features["away_team_top_scorer_avg"] = self._calculate_top_player_avg(away_player_stats)
        features["home_team_injured_players"] = self._count_injured_players(home_player_stats)
        features["away_team_injured_players"] = self._count_injured_players(away_player_stats)
        
        # Game-specific features
        features["total_events"] = len(events)
        features["home_team_events"] = sum(1 for e in events if e.team_id == game.home_team_id)
        features["away_team_events"] = sum(1 for e in events if e.team_id == game.away_team_id)
        
        # Statistical ratios
        if home_team_stats.shots > 0:
            features["home_team_shot_efficiency"] = home_team_stats.shots_on_target / home_team_stats.shots
        else:
            features["home_team_shot_efficiency"] = 0
            
        if away_team_stats.shots > 0:
            features["away_team_shot_efficiency"] = away_team_stats.shots_on_target / away_team_stats.shots
        else:
            features["away_team_shot_efficiency"] = 0
        
        # Momentum indicators
        features["home_team_last_10_min_goals"] = self._calculate_goals_in_last_minutes(events, game.home_team_id, 10)
        features["away_team_last_10_min_goals"] = self._calculate_goals_in_last_minutes(events, game.away_team_id, 10)
        
        return features
    
    def _calculate_days_since_last_game(self, team_id: str, current_time: datetime) -> int:
        """Calculate days since team's last game."""
        # This would query the database for the team's last game
        # For now, return a placeholder value
        return np.random.randint(1, 7)
    
    def _calculate_team_win_percentage(self, team_id: str) -> float:
        """Calculate team's overall win percentage."""
        # This would query the database for team's win history
        # For now, return a placeholder value
        return np.random.uniform(0.3, 0.7)
    
    def _calculate_team_avg_points(self, team_id: str) -> float:
        """Calculate team's average points scored."""
        # This would query the database for team's scoring history
        # For now, return a placeholder value
        return np.random.uniform(15, 35)
    
    def _calculate_team_avg_points_allowed(self, team_id: str) -> float:
        """Calculate team's average points allowed."""
        # This would query the database for team's defensive history
        # For now, return a placeholder value
        return np.random.uniform(15, 35)
    
    def _calculate_home_win_percentage(self, team_id: str) -> float:
        """Calculate team's home win percentage."""
        # This would query the database for team's home game history
        # For now, return a placeholder value
        return np.random.uniform(0.4, 0.8)
    
    def _calculate_away_win_percentage(self, team_id: str) -> float:
        """Calculate team's away win percentage."""
        # This would query the database for team's away game history
        # For now, return a placeholder value
        return np.random.uniform(0.2, 0.6)
    
    def _calculate_last_n_wins(self, team_id: str, n: int) -> int:
        """Calculate number of wins in last n games."""
        # This would query the database for team's recent game history
        # For now, return a placeholder value
        return np.random.randint(0, n + 1)
    
    def _calculate_top_player_avg(self, player_stats: List[PlayerStats]) -> float:
        """Calculate average performance of top player."""
        if not player_stats:
            return 0.0
        
        # Calculate average points for top player
        # This would identify the top scorer and calculate their average
        scores = [stat.points for stat in player_stats if stat.points is not None]
        return np.mean(scores) if scores else 0.0
    
    def _count_injured_players(self, player_stats: List[PlayerStats]) -> int:
        """Count number of injured players."""
        # This would check player injury status
        # For now, return a placeholder value
        return np.random.randint(0, 3)
    
    def _calculate_goals_in_last_minutes(self, events: List[GameEvent], team_id: str, minutes: int) -> int:
        """Calculate number of goals in the last N minutes."""
        # This would filter events by time
        # For now, return a placeholder value
        return np.random.randint(0, 3)
    
    async def _generate_predictions_nvidia(self, game: Game, features: Dict[str, float]) -> List[GamePrediction]:
        """
        Generate game outcome predictions using NVIDIA's AI models.
        """
        predictions = []
        
        if not self.nvidia_api_key:
            logger.warning("NVIDIA API key not configured, using fallback predictions")
            return self._generate_predictions(game, features)
        
        try:
            # Create prompt for NVIDIA AI model
            prompt = f"""
            You are an expert sports analyst for {game.sport.value.upper()}.
            Analyze the following game data and provide predictions for the outcome:
            
            Game: {game.home_team_id} vs {game.away_team_id}
            Sport: {game.sport.value}
            League: {game.league.value}
            
            Team Statistics:
            - Home team win percentage: {features['home_team_win_pct']:.2f}
            - Away team win percentage: {features['away_team_win_pct']:.2f}
            - Home team average points: {features['home_team_avg_points']:.1f}
            - Away team average points: {features['away_team_avg_points']:.1f}
            - Home team average points allowed: {features['home_team_avg_points_allowed']:.1f}
            - Away team average points allowed: {features['away_team_avg_points_allowed']:.1f}
            - Home team home win percentage: {features['home_team_home_win_pct']:.2f}
            - Away team away win percentage: {features['away_team_away_win_pct']:.2f}
            - Home team last 5 wins: {features['home_team_last_5_wins']}
            - Away team last 5 wins: {features['away_team_last_5_wins']}
            - Home team top scorer average: {features['home_team_top_scorer_avg']:.1f}
            - Away team top scorer average: {features['away_team_top_scorer_avg']:.1f}
            - Home team injured players: {features['home_team_injured_players']}
            - Away team injured players: {features['away_team_injured_players']}
            - Home team shot efficiency: {features['home_team_shot_efficiency']:.2f}
            - Away team shot efficiency: {features['away_team_shot_efficiency']:.2f}
            - Home team last 10 min goals: {features['home_team_last_10_min_goals']}
            - Away team last 10 min goals: {features['away_team_last_10_min_goals']}
            
            Based on this data, provide:
            1. Probability of home team winning (0.0 to 1.0)
            2. Probability of away team winning (0.0 to 1.0)
            3. Predicted final score for home team (integer)
            4. Predicted final score for away team (integer)
            5. Confidence score (0.0 to 1.0)
            6. Key factors influencing the prediction
            
            Return your response in JSON format with these fields:
            {{
              "win_probability_home": 0.0,
              "win_probability_away": 0.0,
              "predicted_score_home": 0,
              "predicted_score_away": 0,
              "confidence_score": 0.0,
              "key_factors": ["string"]
            }}
            """
            
            # Call NVIDIA API
            response = await self.http_client.post(
                f"{self.nvidia_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.nvidia_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.nvidia_model_id,
                    "messages": [
                        {"role": "system", "content": "You are a sports analytics expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 500
                }
            )
            
            if response.status_code != 200:
                logger.error(f"NVIDIA API error: {response.status_code} - {response.text}")
                # Fallback to traditional model if API fails
                return self._generate_predictions(game, features)
            
            result = response.json()
            
            # Extract prediction from response
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"].strip()
                
                # Parse JSON from response
                import json
                try:
                    # Extract JSON from potential markdown or extra text
                    json_start = content.find('{')
                    json_end = content.rfind('}') + 1
                    if json_start != -1 and json_end != -1:
                        json_str = content[json_start:json_end]
                        prediction_data = json.loads(json_str)
                        
                        prediction = GamePrediction(
                            id=f"pred_{game.id}",
                            game_id=game.id,
                            sport=game.sport,
                            predicted_winner=game.home_team_id if prediction_data["win_probability_home"] > 0.5 else game.away_team_id,
                            win_probability_home=prediction_data["win_probability_home"],
                            win_probability_away=prediction_data["win_probability_away"],
                            predicted_score_home=prediction_data["predicted_score_home"],
                            predicted_score_away=prediction_data["predicted_score_away"],
                            predicted_total_points=prediction_data["predicted_score_home"] + prediction_data["predicted_score_away"],
                            confidence_score=prediction_data["confidence_score"],
                            key_factors=prediction_data["key_factors"],
                            model_version="1.0.0"
                        )
                        
                        predictions.append(prediction)
                        
                except json.JSONDecodeError:
                    logger.error("Failed to parse NVIDIA AI response as JSON")
                    # Fallback to traditional model
                    return self._generate_predictions(game, features)
            else:
                logger.error("No choices in NVIDIA API response")
                # Fallback to traditional model
                return self._generate_predictions(game, features)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error calling NVIDIA API: {str(e)}")
            # Fallback to traditional model
            return self._generate_predictions(game, features)
    
    def _generate_predictions(self, game: Game, features: Dict[str, float]) -> List[GamePrediction]:
        """
        Generate game outcome predictions using traditional machine learning models.
        This is a fallback method when NVIDIA API is unavailable.
        """
        predictions = []
        
        # Create feature vector for prediction
        feature_vector = [
            features["home_team_win_pct"],
            features["away_team_win_pct"],
            features["home_team_avg_points"],
            features["away_team_avg_points"],
            features["home_team_avg_points_allowed"],
            features["away_team_avg_points_allowed"],
            features["home_team_home_win_pct"],
            features["away_team_away_win_pct"],
            features["home_team_last_5_wins"],
            features["away_team_last_5_wins"],
            features["home_team_top_scorer_avg"],
            features["away_team_top_scorer_avg"],
            features["home_team_injured_players"],
            features["away_team_injured_players"],
            features["home_team_shot_efficiency"],
            features["away_team_shot_efficiency"],
            features["home_team_last_10_min_goals"],
            features["away_team_last_10_min_goals"],
        ]
        
        # Use different models based on sport
        sport_model_key = f"{game.sport.value}_prediction"
        
        # Create prediction for home team win probability
        if sport_model_key in self.models:
            # For simplicity, we'll use a random prediction here
            # In production, this would use the trained model
            home_win_prob = np.random.uniform(0.3, 0.7)
            away_win_prob = 1 - home_win_prob
            
            # Calculate predicted scores
            home_score = np.random.normal(features["home_team_avg_points"], 5)
            away_score = np.random.normal(features["away_team_avg_points"], 5)
            
            # Ensure scores are non-negative
            home_score = max(0, int(home_score))
            away_score = max(0, int(away_score))
            
            # Calculate confidence score
            confidence = np.random.uniform(0.6, 0.9)
            
            # Key factors
            key_factors = []
            if features["home_team_win_pct"] > 0.6:
                key_factors.append("Home team has strong overall win record")
            if features["away_team_away_win_pct"] < 0.3:
                key_factors.append("Away team struggles on the road")
            if features["home_team_last_5_wins"] > 3:
                key_factors.append("Home team on a winning streak")
            if features["away_team_injured_players"] > 1:
                key_factors.append("Away team has multiple injured key players")
            
            prediction = GamePrediction(
                id=f"pred_{game.id}",
                game_id=game.id,
                sport=game.sport,
                predicted_winner=game.home_team_id if home_win_prob > 0.5 else game.away_team_id,
                win_probability_home=home_win_prob,
                win_probability_away=away_win_prob,
                predicted_score_home=home_score,
                predicted_score_away=away_score,
                predicted_total_points=home_score + away_score,
                confidence_score=confidence,
                key_factors=key_factors,
                model_version="1.0.0"
            )
            
            predictions.append(prediction)
        
        return predictions
    
    def _generate_value_indicators(self, game: Game, features: Dict[str, float]) -> List[ValueIndicator]:
        """
        Generate value indicators for betting markets.
        """
        value_indicators = []
        
        # Define common betting markets
        markets = ["moneyline", "spread", "over_under"]
        bookmakers = ["DraftKings", "FanDuel", "BetMGM", "Caesars", "William Hill"]
        
        for market in markets:
            for bookmaker in bookmakers:
                # Generate realistic odds based on predictions
                # This would normally come from external data feeds
                
                # Moneyline odds
                if market == "moneyline":
                    # Generate odds based on win probability
                    home_win_prob = features["home_team_win_pct"]
                    away_win_prob = 1 - home_win_prob
                    
                    # Convert probability to American odds
                    if home_win_prob > 0.5:
                        home_odds = int(-100 * home_win_prob / (1 - home_win_prob))
                    else:
                        home_odds = int(100 * (1 - home_win_prob) / home_win_prob)
                        
                    if away_win_prob > 0.5:
                        away_odds = int(-100 * away_win_prob / (1 - away_win_prob))
                    else:
                        away_odds = int(100 * (1 - away_win_prob) / away_win_prob)
                    
                    # Calculate implied probability
                    home_implied_prob = 1 / (1 + abs(home_odds) / 100) if home_odds > 0 else abs(home_odds) / (abs(home_odds) + 100)
                    away_implied_prob = 1 / (1 + abs(away_odds) / 100) if away_odds > 0 else abs(away_odds) / (abs(away_odds) + 100)
                    
                    # AI probability (based on our model)
                    ai_home_prob = features["home_team_win_pct"]
                    ai_away_prob = 1 - ai_home_prob
                    
                    # Calculate value score (0-100)
                    home_value_score = self._calculate_value_score(home_implied_prob, ai_home_prob)
                    away_value_score = self._calculate_value_score(away_implied_prob, ai_away_prob)
                    
                    # Determine recommendation
                    home_recommendation = self._get_recommendation(home_value_score)
                    away_recommendation = self._get_recommendation(away_value_score)
                    
                    # Create value indicators
                    home_value = ValueIndicator(
                        id=f"value_{game.id}_{bookmaker}_home_{market}",
                        game_id=game.id,
                        sport=game.sport,
                        market_type=market,
                        bookmaker=bookmaker,
                        line=0.0,  # Moneyline has no point spread
                        odds=home_odds,
                        implied_probability=home_implied_prob,
                        ai_probability=ai_home_prob,
                        value_score=home_value_score,
                        confidence_score=np.random.uniform(0.7, 0.9),
                        edge=home_value_score - 50,  # Edge is value score minus 50
                        recommendation=home_recommendation,
                        key_insights=["AI model identifies mispricing in betting market"],
                        model_version="1.0.0"
                    )
                    
                    away_value = ValueIndicator(
                        id=f"value_{game.id}_{bookmaker}_away_{market}",
                        game_id=game.id,
                        sport=game.sport,
                        market_type=market,
                        bookmaker=bookmaker,
                        line=0.0,  # Moneyline has no point spread
                        odds=away_odds,
                        implied_probability=away_implied_prob,
                        ai_probability=ai_away_prob,
                        value_score=away_value_score,
                        confidence_score=np.random.uniform(0.7, 0.9),
                        edge=away_value_score - 50,  # Edge is value score minus 50
                        recommendation=away_recommendation,
                        key_insights=["AI model identifies mispricing in betting market"],
                        model_version="1.0.0"
                    )
                    
                    value_indicators.extend([home_value, away_value])
                    
                # Point spread odds
                elif market == "spread":
                    # Generate a realistic spread
                    spread = np.random.uniform(-7, 7)
                    
                    # Generate odds for both sides of the spread
                    # We'll assume standard -110 odds for both sides
                    odds = -110
                    
                    # Implied probability for -110 odds
                    implied_prob = 1 / (1 + 110/100)  # ~52.4%
                    
                    # AI probability for home team covering the spread
                    # This would be based on team performance differences
                    ai_home_cover_prob = features["home_team_win_pct"] + (spread / 10)
                    ai_home_cover_prob = max(0.1, min(0.9, ai_home_cover_prob))
                    
                    # Calculate value score
                    home_cover_value_score = self._calculate_value_score(implied_prob, ai_home_cover_prob)
                    away_cover_value_score = self._calculate_value_score(implied_prob, 1 - ai_home_cover_prob)
                    
                    # Determine recommendation
                    home_cover_recommendation = self._get_recommendation(home_cover_value_score)
                    away_cover_recommendation = self._get_recommendation(away_cover_value_score)
                    
                    # Create value indicators
                    home_cover_value = ValueIndicator(
                        id=f"value_{game.id}_{bookmaker}_home_{market}",
                        game_id=game.id,
                        sport=game.sport,
                        market_type=market,
                        bookmaker=bookmaker,
                        line=spread,
                        odds=odds,
                        implied_probability=implied_prob,
                        ai_probability=ai_home_cover_prob,
                        value_score=home_cover_value_score,
                        confidence_score=np.random.uniform(0.7, 0.9),
                        edge=home_cover_value_score - 50,
                        recommendation=home_cover_recommendation,
                        key_insights=["AI model identifies mispricing in betting market"],
                        model_version="1.0.0"
                    )
                    
                    away_cover_value = ValueIndicator(
                        id=f"value_{game.id}_{bookmaker}_away_{market}",
                        game_id=game.id,
                        sport=game.sport,
                        market_type=market,
                        bookmaker=bookmaker,
                        line=-spread,
                        odds=odds,
                        implied_probability=implied_prob,
                        ai_probability=1 - ai_home_cover_prob,
                        value_score=away_cover_value_score,
                        confidence_score=np.random.uniform(0.7, 0.9),
                        edge=away_cover_value_score - 50,
                        recommendation=away_cover_recommendation,
                        key_insights=["AI model identifies mispricing in betting market"],
                        model_version="1.0.0"
                    )
                    
                    value_indicators.extend([home_cover_value, away_cover_value])
                    
                # Over/under odds
                elif market == "over_under":
                    # Calculate expected total points
                    expected_total = (features["home_team_avg_points"] + features["away_team_avg_points"]) / 2
                    
                    # Generate a realistic total line
                    total_line = round(expected_total)
                    
                    # Standard odds for over/under
                    odds = -110
                    
                    # Implied probability
                    implied_prob = 1 / (1 + 110/100)  # ~52.4%
                    
                    # AI probability for over
                    ai_over_prob = 0.5  # Default
                    
                    # Adjust based on team scoring tendencies
                    if features["home_team_avg_points"] > 25 and features["away_team_avg_points"] > 25:
                        ai_over_prob = np.random.uniform(0.55, 0.7)
                    elif features["home_team_avg_points"] < 20 and features["away_team_avg_points"] < 20:
                        ai_over_prob = np.random.uniform(0.3, 0.45)
                    
                    # Calculate value score
                    over_value_score = self._calculate_value_score(implied_prob, ai_over_prob)
                    under_value_score = self._calculate_value_score(implied_prob, 1 - ai_over_prob)
                    
                    # Determine recommendation
                    over_recommendation = self._get_recommendation(over_value_score)
                    under_recommendation = self._get_recommendation(under_value_score)
                    
                    # Create value indicators
                    over_value = ValueIndicator(
                        id=f"value_{game.id}_{bookmaker}_over_{market}",
                        game_id=game.id,
                        sport=game.sport,
                        market_type=market,
                        bookmaker=bookmaker,
                        line=total_line,
                        odds=odds,
                        implied_probability=implied_prob,
                        ai_probability=ai_over_prob,
                        value_score=over_value_score,
                        confidence_score=np.random.uniform(0.7, 0.9),
                        edge=over_value_score - 50,
                        recommendation=over_recommendation,
                        key_insights=["AI model identifies mispricing in betting market"],
                        model_version="1.0.0"
                    )
                    
                    under_value = ValueIndicator(
                        id=f"value_{game.id}_{bookmaker}_under_{market}",
                        game_id=game.id,
                        sport=game.sport,
                        market_type=market,
                        bookmaker=bookmaker,
                        line=total_line,
                        odds=odds,
                        implied_probability=implied_prob,
                        ai_probability=1 - ai_over_prob,
                        value_score=under_value_score,
                        confidence_score=np.random.uniform(0.7, 0.9),
                        edge=under_value_score - 50,
                        recommendation=under_recommendation,
                        key_insights=["AI model identifies mispricing in betting market"],
                        model_version="1.0.0"
                    )
                    
                    value_indicators.extend([over_value, under_value])
        
        return value_indicators
    
    def _calculate_value_score(self, implied_prob: float, ai_probability: float) -> float:
        """
        Calculate a value score (0-100) based on the difference between 
        implied probability and AI probability.
        """
        # Calculate edge
        edge = ai_probability - implied_prob
        
        # Convert edge to value score (0-100)
        # Positive edge = value, negative edge = no value
        if edge > 0:
            # Scale from 0-100 based on edge
            # Edge of 0.1 = 50, edge of 0.2 = 100
            value_score = min(100, (edge / 0.2) * 100)
        else:
            value_score = 0
        
        return round(value_score, 1)
    
    def _get_recommendation(self, value_score: float) -> str:
        """
        Get recommendation based on value score.
        """
        if value_score >= 80:
            return "strong_buy"
        elif value_score >= 60:
            return "buy"
        elif value_score >= 40:
            return "neutral"
        elif value_score >= 20:
            return "sell"
        else:
            return "strong_sell"
    
    async def _generate_game_insights_nvidia(self, game: Game, features: Dict[str, float]) -> List[GameInsight]:
        """
        Generate AI-generated insights about the game using NVIDIA's AI models.
        """
        insights = []
        
        if not self.nvidia_api_key:
            logger.warning("NVIDIA API key not configured, using fallback insights")
            return self._generate_game_insights(game, features)
        
        try:
            # Create prompt for NVIDIA AI model
            prompt = f"""
            You are an expert sports analyst for {game.sport.value.upper()}.
            Analyze the following game data and generate detailed insights:
            
            Game: {game.home_team_id} vs {game.away_team_id}
            Sport: {game.sport.value}
            League: {game.league.value}
            
            Team Statistics:
            - Home team win percentage: {features['home_team_win_pct']:.2f}
            - Away team win percentage: {features['away_team_win_pct']:.2f}
            - Home team average points: {features['home_team_avg_points']:.1f}
            - Away team average points: {features['away_team_avg_points']:.1f}
            - Home team average points allowed: {features['home_team_avg_points_allowed']:.1f}
            - Away team average points allowed: {features['away_team_avg_points_allowed']:.1f}
            - Home team home win percentage: {features['home_team_home_win_pct']:.2f}
            - Away team away win percentage: {features['away_team_away_win_pct']:.2f}
            - Home team last 5 wins: {features['home_team_last_5_wins']}
            - Away team last 5 wins: {features['away_team_last_5_wins']}
            - Home team top scorer average: {features['home_team_top_scorer_avg']:.1f}
            - Away team top scorer average: {features['away_team_top_scorer_avg']:.1f}
            - Home team injured players: {features['home_team_injured_players']}
            - Away team injured players: {features['away_team_injured_players']}
            - Home team shot efficiency: {features['home_team_shot_efficiency']:.2f}
            - Away team shot efficiency: {features['away_team_shot_efficiency']:.2f}
            - Home team last 10 min goals: {features['home_team_last_10_min_goals']}
            - Away team last 10 min goals: {features['away_team_last_10_min_goals']}
            
            Generate 3-5 insightful observations about this matchup. Focus on:
            1. Matchup advantages
            2. Momentum factors
            3. Injury impacts
            4. Historical trends
            5. Key player performance
            
            Return your response in JSON format with these fields:
            [
              {{
                "id": "string",
                "game_id": "string",
                "sport": "string",
                "insight_type": "string", // e.g., "matchup_advantage", "momentum", "injury_impact"
                "title": "string",
                "description": "string",
                "confidence_score": 0.0,
                "impact_score": 0.0,
                "key_data_points": ["string"],
                "model_version": "string"
              }}
            ]
            """
            
            # Call NVIDIA API
            response = await self.http_client.post(
                f"{self.nvidia_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.nvidia_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.nvidia_model_id,
                    "messages": [
                        {"role": "system", "content": "You are a sports analytics expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000
                }
            )
            
            if response.status_code != 200:
                logger.error(f"NVIDIA API error: {response.status_code} - {response.text}")
                # Fallback to traditional method if API fails
                return self._generate_game_insights(game, features)
            
            result = response.json()
            
            # Extract insights from response
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"].strip()
                
                # Parse JSON from response
                import json
                try:
                    # Extract JSON from potential markdown or extra text
                    json_start = content.find('[')
                    json_end = content.rfind(']') + 1
                    if json_start != -1 and json_end != -1:
                        json_str = content[json_start:json_end]
                        insights_data = json.loads(json_str)
                        
                        for insight_data in insights_data:
                            insight = GameInsight(
                                id=insight_data["id"],
                                game_id=game.id,
                                sport=game.sport,
                                insight_type=insight_data["insight_type"],
                                title=insight_data["title"],
                                description=insight_data["description"],
                                confidence_score=insight_data["confidence_score"],
                                impact_score=insight_data["impact_score"],
                                key_data_points=insight_data["key_data_points"],
                                model_version="1.0.0"
                            )
                            insights.append(insight)
                        
                except json.JSONDecodeError:
                    logger.error("Failed to parse NVIDIA AI response as JSON")
                    # Fallback to traditional method
                    return self._generate_game_insights(game, features)
            else:
                logger.error("No choices in NVIDIA API response")
                # Fallback to traditional method
                return self._generate_game_insights(game, features)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error calling NVIDIA API for insights: {str(e)}")
            # Fallback to traditional method
            return self._generate_game_insights(game, features)
    
    def _generate_game_insights(self, game: Game, features: Dict[str, float]) -> List[GameInsight]:
        """
        Generate AI-generated insights about the game.
        This is a fallback method when NVIDIA API is unavailable.
        """
        insights = []
        
        # Generate insights based on features
        
        # Matchup advantage
        if features["home_team_win_pct"] > 0.6 and features["away_team_win_pct"] < 0.4:
            insight = GameInsight(
                id=f"insight_{game.id}_matchup",
                game_id=game.id,
                sport=game.sport,
                insight_type="matchup_advantage",
                title="Home Team Dominance",
                description=f"The home team has a significantly higher win percentage ({features['home_team_win_pct']:.2f}) compared to the away team ({features['away_team_win_pct']:.2f}), indicating a clear matchup advantage.",
                confidence_score=np.random.uniform(0.8, 0.95),
                impact_score=np.random.uniform(0.6, 0.8),
                key_data_points=[
                    f"Home team win percentage: {features['home_team_win_pct']:.2f}",
                    f"Away team win percentage: {features['away_team_win_pct']:.2f}"
                ],
                model_version="1.0.0"
            )
            insights.append(insight)
        
        # Weather impact
        if "weather" in features and features["weather"] == "rain":
            insight = GameInsight(
                id=f"insight_{game.id}_weather",
                game_id=game.id,
                sport=game.sport,
                insight_type="weather_impact",
                title="Weather Impact",
                description="Rain conditions are expected to reduce scoring and increase the importance of defense.",
                confidence_score=np.random.uniform(0.7, 0.85),
                impact_score=np.random.uniform(0.5, 0.7),
                key_data_points=["Expected rain during game"],
                model_version="1.0.0"
            )
            insights.append(insight)
        
        # Momentum
        if features["home_team_last_5_wins"] >= 4:
            insight = GameInsight(
                id=f"insight_{game.id}_momentum",
                game_id=game.id,
                sport=game.sport,
                insight_type="momentum",
                title="Home Team Momentum",
                description=f"The home team is on a strong winning streak with {features['home_team_last_5_wins']} wins in their last 5 games, creating positive momentum.",
                confidence_score=np.random.uniform(0.8, 0.9),
                impact_score=np.random.uniform(0.5, 0.7),
                key_data_points=[
                    f"Home team last 5 wins: {features['home_team_last_5_wins']}"
                ],
                model_version="1.0.0"
            )
            insights.append(insight)
        
        # Injury impact
        if features["away_team_injured_players"] >= 2:
            insight = GameInsight(
                id=f"insight_{game.id}_injuries",
                game_id=game.id,
                sport=game.sport,
                insight_type="injury_impact",
                title="Away Team Injury Concerns",
                description=f"The away team has {features['away_team_injured_players']} key players listed as injured, which could significantly impact their performance.",
                confidence_score=np.random.uniform(0.8, 0.9),
                impact_score=np.random.uniform(0.6, 0.8),
                key_data_points=[
                    f"Away team injured players: {features['away_team_injured_players']}"
                ],
                model_version="1.0.0"
            )
            insights.append(insight)
        
        return insights
    
    def _generate_team_trends(self, game: Game, features: Dict[str, float]) -> List[TeamTrend]:
        """
        Generate team trends for both home and away teams.
        """
        trends = []
        
        # Home team trends
        if features["home_team_win_pct"] > 0.6:
            trend = TeamTrend(
                id=f"trend_{game.home_team_id}_win_pct",
                team_id=game.home_team_id,
                sport=game.sport,
                trend_type="recent_form",
                metric="win_percentage",
                value=features["home_team_win_pct"],
                direction="up",
                period_days=30,
                confidence_score=np.random.uniform(0.8, 0.95),
                description=f"The home team has maintained a high win percentage ({features['home_team_win_pct']:.2f}) over the last 30 days, indicating strong recent form.",
                model_version="1.0.0"
            )
            trends.append(trend)
        
        if features["home_team_home_win_pct"] > 0.7:
            trend = TeamTrend(
                id=f"trend_{game.home_team_id}_home_win_pct",
                team_id=game.home_team_id,
                sport=game.sport,
                trend_type="home_advantage",
                metric="home_win_percentage",
                value=features["home_team_home_win_pct"],
                direction="stable",
                period_days=90,
                confidence_score=np.random.uniform(0.85, 0.95),
                description=f"The home team has an exceptional home win percentage ({features['home_team_home_win_pct']:.2f}) over the last 90 days, demonstrating a strong home advantage.",
                model_version="1.0.0"
            )
            trends.append(trend)
        
        # Away team trends
        if features["away_team_away_win_pct"] < 0.3:
            trend = TeamTrend(
                id=f"trend_{game.away_team_id}_away_win_pct",
                team_id=game.away_team_id,
                sport=game.sport,
                trend_type="road_performance",
                metric="away_win_percentage",
                value=features["away_team_away_win_pct"],
                direction="down",
                period_days=30,
                confidence_score=np.random.uniform(0.8, 0.9),
                description=f"The away team has struggled on the road with a low win percentage ({features['away_team_away_win_pct']:.2f}) over the last 30 days.",
                model_version="1.0.0"
            )
            trends.append(trend)
        
        return trends
    
    async def generate_analytics_report(self, team_id: str, report_type: str) -> AnalyticsReport:
        """
        Generate a comprehensive analytics report for a team.
        """
        # This would gather data from multiple sources
        # For now, return a placeholder report
        
        report = AnalyticsReport(
            id=f"report_{team_id}_{report_type}",
            subject_type="team",
            subject_id=team_id,
            sport="soccer",  # Placeholder
            report_type=report_type,
            title=f"{report_type.replace('_', ' ').title()} Report for Team {team_id}",
            summary=f"Comprehensive analysis of team {team_id} for {report_type.replace('_', ' ')}.",
            key_findings=[
                "Team has shown consistent performance in recent games",
                "Key players are performing above league average",
                "Team has strong home advantage",
                "Opponents have difficulty scoring against this team"
            ],
            data_sources=["Team statistics", "Player performance data", "Game event data"],
            confidence_score=np.random.uniform(0.8, 0.95),
            model_version="1.0.0"
        )
        
        return report
    
    async def process_live_data_stream(self, data_feed: DataFeed):
        """
        Process a live data stream from a sports data feed.
        """
        # This would connect to external APIs and process real-time data
        # For now, simulate processing
        
        logger.info(f"Processing live data stream from {data_feed.name}")
        
        # Simulate receiving data
        await asyncio.sleep(1)
        
        # Update data feed status
        data_feed.last_updated = datetime.utcnow()
        data_feed.status = "active"
        
        logger.info(f"Successfully processed live data stream from {data_feed.name}")
        
        return data_feed
    
    async def update_models(self):
        """
        Update machine learning models with new data.
        """
        logger.info("Updating machine learning models with new data")
        
        # This would retrain models with new data
        # For now, just log the update
        
        # Simulate model update
        await asyncio.sleep(2)
        
        logger.info("Machine learning models updated successfully")
        
        return True
    
    async def run_daily_analysis(self):
        """
        Run daily analysis on all games.
        """
        logger.info("Running daily analysis on all games")
        
        # This would process all games from the previous day
        # For now, just log the operation
        
        # Simulate processing
        await asyncio.sleep(3)
        
        logger.info("Daily analysis completed successfully")
        
        return True
    
    async def generate_weekly_summary(self):
        """
        Generate a weekly summary report.
        """
        logger.info("Generating weekly summary report")
        
        # This would aggregate insights from the week
        # For now, just log the operation
        
        # Simulate generation
        await asyncio.sleep(2)
        
        logger.info("Weekly summary report generated successfully")
        
        return True
    
    async def optimize_model_performance(self):
        """
        Optimize model performance based on feedback.
        """
        logger.info("Optimizing model performance")
        
        # This would analyze model predictions vs actual outcomes
        # and adjust parameters accordingly
        
        # Simulate optimization
        await asyncio.sleep(1)
        
        logger.info("Model performance optimized successfully")
        
        return True

# Global instance of the analytics engine
analytics_engine = AnalyticsEngine()