import logging
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from players.models import Player
from players.vector_search import generate_all_embeddings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate style descriptions and embeddings for all players'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of players to process in each batch (default: 100)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate embeddings even if they already exist'
        )
        parser.add_argument(
            '--player-id',
            type=int,
            help='Generate embedding for specific player ID only'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        force = options['force']
        player_id = options['player_id']

        try:
            if player_id:
                # Generate for specific player
                try:
                    player = Player.objects.get(id=player_id)
                    self._generate_player_embedding(player, force)
                    self.stdout.write(
                        self.style.SUCCESS(f'Generated embedding for player {player.name}')
                    )
                except Player.DoesNotExist:
                    raise CommandError(f'Player with ID {player_id} not found')
            else:
                # Generate for all players
                total_players = Player.objects.count()
                self.stdout.write(f'Found {total_players} players to process')

                if not force:
                    # Check how many already have embeddings
                    with_embeddings = Player.objects.filter(
                        style_description__isnull=False
                    ).count()
                    self.stdout.write(f'{with_embeddings} players already have embeddings')

                # Process in batches
                processed = 0
                for i in range(0, total_players, batch_size):
                    batch_players = Player.objects.all()[i:i + batch_size]
                    
                    with transaction.atomic():
                        for player in batch_players:
                            if force or not player.style_description:
                                self._generate_player_embedding(player, force=True)
                                processed += 1
                    
                    self.stdout.write(f'Processed batch {i//batch_size + 1}: {processed} players updated')

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully generated embeddings for {processed} players')
                )

        except Exception as e:
            logger.error(f'Error generating embeddings: {e}')
            raise CommandError(f'Error generating embeddings: {str(e)}')

    def _generate_player_embedding(self, player: Player, force: bool = False):
        """
        Generate embedding for a single player.
        """
        try:
            # Generate style description
            style_description = player.generate_style_description()
            
            # Generate statistics vector
            stats_vector = player.get_statistics_vector()
            
            # Update player
            player.style_description = style_description
            player.style_embedding = stats_vector
            player.save(update_fields=['style_description', 'style_embedding'])
            
        except Exception as e:
            logger.error(f'Error generating embedding for player {player.id}: {e}')
            raise 