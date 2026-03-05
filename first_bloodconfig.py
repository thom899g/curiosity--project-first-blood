"""
Configuration management for FIRST BLOOD trading system.
Centralizes environment variables and constants with validation.
"""
import os
from dataclasses import dataclass
from typing import Optional, Dict, List
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class TradingConfig:
    """Configuration for trading parameters"""
    # Trading parameters
    MIN_CONFIDENCE_THRESHOLD: float = 0.70
    INITIAL_CAPITAL: float = 5.0
    TARGET_PROFIT: float = 1.0  # $1 profit from $5 = 20% return
    MAX_POSITION_SIZE: float = 5.0
    STOP_LOSS_PCT: float = 0.10  # 10% stop loss
    
    # Social media parameters
    TARGET_COINS: List[str] = None  # Will be initialized
    SOCIAL_PLATFORMS: List[str] = None
    
    # Time parameters
    SCAN_INTERVAL_MINUTES: int = 15
    SIGNAL_WINDOW_HOURS: int = 6
    
    # Exchange parameters (using CCXT)
    EXCHANGE_ID: str = "binance"
    TESTNET: bool = True
    
    def __post_init__(self):
        """Initialize mutable defaults"""
        if self.TARGET_COINS is None:
            self.TARGET_COINS = [
                "DOGE", "SHIB", "PEPE", "FLOKI", "BONK",
                "WIF", "MEME", "BOME", "POPCAT"
            ]
        
        if self.SOCIAL_PLATFORMS is None:
            self.SOCIAL_PLATFORMS = ["twitter", "reddit"]
        
        # Validate critical values
        assert 0 < self.MIN_CONFIDENCE_THRESHOLD <= 1.0, \
            "Confidence threshold must be between 0 and 1"
        assert self.INITIAL_CAPITAL > 0, "Initial capital must be positive"
        assert self.STOP_LOSS_PCT > 0, "Stop loss must be positive"


@dataclass
class APIConfig:
    """API credentials and endpoints"""
    # Firebase
    FIREBASE_PROJECT_ID: Optional[str] = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_CREDENTIALS_PATH: Optional[str] = os.getenv("FIREBASE_CREDENTIALS_PATH")
    
    # Telegram for emergency contact
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    
    # Social Media (if available)
    TWITTER_BEARER_TOKEN: Optional[str] = os.getenv("TWITTER_BEARER_TOKEN")
    REDDIT_CLIENT_ID: Optional[str] = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET: Optional[str] = os.getenv("REDDIT_CLIENT_SECRET")
    
    def validate(self) -> bool:
        """Validate essential configuration"""
        missing = []
        
        if not self.FIREBASE_PROJECT_ID:
            missing.append("FIREBASE_PROJECT_ID")
        
        if not self.FIREBASE_CREDENTIALS_PATH:
            missing.append("FIREBASE_CREDENTIALS_PATH")
        
        if missing:
            logger.error(f"Missing required environment variables: {missing}")
            return False
        
        # Check if Firebase credentials file exists
        if not os.path.exists(self.FIREBASE_CREDENTIALS_PATH):
            logger.error(f"Firebase credentials file not found: {self.FIREBASE_CREDENTIALS_PATH}")
            return False
            
        return True


class ConfigManager:
    """Singleton configuration manager"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize configuration"""
        self.trading = TradingConfig()
        self.api = APIConfig()
        
        # Validate configuration
        if not self.api.validate():
            raise ValueError("Invalid configuration. Check environment variables.")
        
        logger.info("Configuration loaded successfully")
    
    def get_trading_config(self) -> TradingConfig:
        """Get trading configuration"""
        return self.trading
    
    def get_api_config(self) -> APIConfig:
        """Get API configuration"""
        return self.api