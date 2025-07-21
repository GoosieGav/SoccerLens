"""
Vector search service for player similarity.
Combines statistical similarity with NLP-based style analysis.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from django.db.models import Q
from django.conf import settings
from .models import Player
import logging

logger = logging.getLogger(__name__)


class VectorSearchService:
    """
    Service for finding similar players using vector similarity.
    """
    
    def __init__(self):
        self.vector_config = getattr(settings, 'VECTOR_SEARCH_CONFIG', {})
        self.enabled = self.vector_config.get('ENABLED', False)
        self.similarity_threshold = self.vector_config.get('SIMILARITY_THRESHOLD', 0.7)
    
    def find_similar_players(self, player: Player, limit: int = 10, 
                           method: str = 'hybrid') -> List[Player]:
        """
        Find similar players using specified method.
        
        Args:
            player: Player to find similarities for
            limit: Maximum number of similar players to return
            method: 'statistical', 'nlp', or 'hybrid'
            
        Returns:
            List of similar players with similarity scores
        """
        if method == 'statistical':
            return self._find_statistical_similarities(player, limit)
        elif method == 'nlp':
            return self._find_nlp_similarities(player, limit)
        elif method == 'hybrid':
            return self._find_hybrid_similarities(player, limit)
        else:
            raise ValueError(f"Invalid method: {method}. Use 'statistical', 'nlp', or 'hybrid'")
    
    def _find_statistical_similarities(self, player: Player, limit: int) -> List[Player]:
        """
        Find similar players based on statistical vectors.
        """
        try:
            player_vector = player.get_statistics_vector()
            
            # Get all players with similar position and competition
            similar_players = Player.objects.filter(
                position=player.position,
                competition=player.competition
            ).exclude(id=player.id)
            
            # Calculate similarities
            similarities = []
            for other_player in similar_players:
                other_vector = other_player.get_statistics_vector()
                similarity = self._cosine_similarity(player_vector, other_vector)
                
                if similarity >= self.similarity_threshold:
                    other_player.similarity_score = similarity
                    similarities.append((other_player, similarity))
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x[1], reverse=True)
            return [player for player, _ in similarities[:limit]]
            
        except Exception as e:
            logger.error(f"Error in statistical similarity search: {e}")
            return self._fallback_similarity_search(player, limit)
    
    def _find_nlp_similarities(self, player: Player, limit: int) -> List[Player]:
        """
        Find similar players based on NLP style descriptions.
        """
        try:
            # Generate style description for the target player
            target_description = player.generate_style_description()
            
            # Get players with similar positions
            similar_players = Player.objects.filter(
                position=player.position
            ).exclude(id=player.id)
            
            # Calculate text-based similarities
            similarities = []
            for other_player in similar_players:
                other_description = other_player.generate_style_description()
                similarity = self._text_similarity(target_description, other_description)
                
                if similarity >= self.similarity_threshold:
                    other_player.similarity_score = similarity
                    similarities.append((other_player, similarity))
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x[1], reverse=True)
            return [player for player, _ in similarities[:limit]]
            
        except Exception as e:
            logger.error(f"Error in NLP similarity search: {e}")
            return self._fallback_similarity_search(player, limit)
    
    def _find_hybrid_similarities(self, player: Player, limit: int) -> List[Player]:
        """
        Find similar players using both statistical and NLP methods.
        """
        try:
            # Get both types of similarities
            statistical_similar = self._find_statistical_similarities(player, limit * 2)
            nlp_similar = self._find_nlp_similarities(player, limit * 2)
            
            # Combine and rank
            all_similar = {}
            
            # Add statistical similarities
            for p in statistical_similar:
                all_similar[p.id] = {
                    'player': p,
                    'statistical_score': p.similarity_score,
                    'nlp_score': 0.0
                }
            
            # Add NLP similarities
            for p in nlp_similar:
                if p.id in all_similar:
                    all_similar[p.id]['nlp_score'] = p.similarity_score
                else:
                    all_similar[p.id] = {
                        'player': p,
                        'statistical_score': 0.0,
                        'nlp_score': p.similarity_score
                    }
            
            # Calculate hybrid scores (weighted average)
            hybrid_scores = []
            for player_id, data in all_similar.items():
                hybrid_score = (data['statistical_score'] * 0.6 + data['nlp_score'] * 0.4)
                data['player'].similarity_score = hybrid_score
                hybrid_scores.append((data['player'], hybrid_score))
            
            # Sort by hybrid score and return top results
            hybrid_scores.sort(key=lambda x: x[1], reverse=True)
            return [player for player, _ in hybrid_scores[:limit]]
            
        except Exception as e:
            logger.error(f"Error in hybrid similarity search: {e}")
            return self._fallback_similarity_search(player, limit)
    
    def _cosine_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        """
        try:
            v1 = np.array(vector1)
            v2 = np.array(vector2)
            
            # Handle zero vectors
            if np.all(v1 == 0) or np.all(v2 == 0):
                return 0.0
            
            dot_product = np.dot(v1, v2)
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two text descriptions.
        Simple word overlap similarity for now.
        """
        try:
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union)
        except Exception as e:
            logger.error(f"Error calculating text similarity: {e}")
            return 0.0
    
    def _fallback_similarity_search(self, player: Player, limit: int) -> List[Player]:
        """
        Fallback similarity search using basic criteria.
        """
        try:
            # Simple similarity based on position, age range, and performance
            similar_players = Player.objects.filter(
                position=player.position,
                age__range=[player.age - 3, player.age + 3],
                competition=player.competition
            ).exclude(id=player.id).order_by(
                '-goals', '-assists'
            )[:limit]
            
            # Add default similarity scores
            for p in similar_players:
                p.similarity_score = 0.5
            
            return list(similar_players)
            
        except Exception as e:
            logger.error(f"Error in fallback similarity search: {e}")
            return []
    
    def generate_embeddings_for_all_players(self):
        """
        Generate style descriptions and embeddings for all players.
        This would be used in a background task.
        """
        try:
            players = Player.objects.all()
            updated_count = 0
            
            for player in players:
                # Generate style description
                style_description = player.generate_style_description()
                
                # Generate statistics vector
                stats_vector = player.get_statistics_vector()
                
                # Update player
                player.style_description = style_description
                player.style_embedding = stats_vector
                player.save(update_fields=['style_description', 'style_embedding'])
                
                updated_count += 1
            
            logger.info(f"Generated embeddings for {updated_count} players")
            return updated_count
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return 0


# Convenience functions
def find_similar_players(player: Player, limit: int = 10, method: str = 'hybrid') -> List[Player]:
    """Find similar players using the vector search service."""
    service = VectorSearchService()
    return service.find_similar_players(player, limit, method)

def generate_all_embeddings():
    """Generate embeddings for all players."""
    service = VectorSearchService()
    return service.generate_embeddings_for_all_players() 