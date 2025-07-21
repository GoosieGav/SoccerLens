import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from players.models import Player


class Command(BaseCommand):
    help = 'Load player data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing player data'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing player data before loading new data'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Number of records to process in each batch (default: 1000)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        clear_data = options['clear']
        batch_size = options['batch_size']

        try:
            # Read CSV file
            self.stdout.write(f'Reading CSV file: {csv_file}')
            df = pd.read_csv(csv_file)
            
            self.stdout.write(f'Found {len(df)} rows in CSV file')
            self.stdout.write(f'Columns: {list(df.columns)[:10]}...') # Show first 10 columns
            
            # Clear existing data if requested
            if clear_data:
                self.stdout.write('Clearing existing player data...')
                Player.objects.all().delete()
                self.stdout.write('Existing data cleared.')

            # Process data in batches
            total_created = 0
            total_errors = 0
            
            for start_idx in range(0, len(df), batch_size):
                end_idx = min(start_idx + batch_size, len(df))
                batch_df = df.iloc[start_idx:end_idx]
                
                self.stdout.write(f'Processing batch {start_idx + 1}-{end_idx} of {len(df)}')
                
                created, errors = self.process_batch(batch_df)
                total_created += created
                total_errors += errors
                
                self.stdout.write(f'Batch complete: {created} created, {errors} errors')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded {total_created} players with {total_errors} errors'
                )
            )

        except FileNotFoundError:
            raise CommandError(f'CSV file "{csv_file}" not found.')
        except Exception as e:
            raise CommandError(f'Error processing CSV file: {str(e)}')

    def process_batch(self, batch_df):
        """Process a batch of player records."""
        created_count = 0
        error_count = 0
        players_to_create = []

        for index, row in batch_df.iterrows():
            try:
                player_data = self.extract_player_data(row)
                if player_data:
                    players_to_create.append(Player(**player_data))
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Error processing row {index}: {str(e)}')
                )
                error_count += 1

        # Bulk create players
        if players_to_create:
            try:
                with transaction.atomic():
                    Player.objects.bulk_create(players_to_create, ignore_conflicts=True)
                    created_count = len(players_to_create)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error bulk creating players: {str(e)}')
                )
                error_count += len(players_to_create)

        return created_count, error_count

    def extract_player_data(self, row):
        """Extract player data from CSV row and map to model fields."""
        try:
            # Helper function to safely convert values
            def safe_float(value, default=0.0):
                if pd.isna(value) or value == '' or value == ',':
                    return default
                try:
                    return float(str(value).replace(',', ''))
                except (ValueError, TypeError):
                    return default

            def safe_int(value, default=0):
                if pd.isna(value) or value == '' or value == ',':
                    return default
                try:
                    return int(float(str(value).replace(',', '')))
                except (ValueError, TypeError):
                    return default

            def safe_str(value, default=''):
                if pd.isna(value) or value == '':
                    return default
                return str(value).strip()

            # Extract basic information
            full_name = safe_str(row.get('Player'))
            last_name = full_name.split()[-1] if full_name else ''
            
            # Normalize special characters for sorting
            import unicodedata
            normalized_last_name = unicodedata.normalize('NFD', last_name).encode('ascii', 'ignore').decode('ascii').lower()
            
            player_data = {
                'rank': safe_int(row.get('Rk')),
                'name': full_name,
                'last_name': normalized_last_name,
                'nation': safe_str(row.get('Nation')),
                'position': safe_str(row.get('Pos')),
                'squad': safe_str(row.get('Squad')),
                'competition': safe_str(row.get('Comp')),
                'age': safe_float(row.get('Age')),
                'born_year': safe_int(row.get('Born')),
                
                # Playing time
                'matches_played': safe_int(row.get('MP')),
                'starts': safe_int(row.get('Starts')),
                'minutes': safe_int(row.get('Min')),
                'minutes_per_90': safe_float(row.get('90s')),
                
                # Goals and assists
                'goals': safe_int(row.get('Gls')),
                'assists': safe_int(row.get('Ast')),
                'goals_assists': safe_int(row.get('G+A')),
                'goals_minus_penalties': safe_int(row.get('G-PK')),
                'penalties_scored': safe_int(row.get('PK')),
                'penalties_attempted': safe_int(row.get('PKatt')),
                
                # Cards
                'yellow_cards': safe_int(row.get('CrdY')),
                'red_cards': safe_int(row.get('CrdR')),
                
                # Advanced stats
                'expected_goals': safe_float(row.get('xG')),
                'expected_goals_non_penalty': safe_float(row.get('npxG')),
                'expected_assists': safe_float(row.get('xAG')),
                
                # Shooting stats
                'shots': safe_int(row.get('Sh')),
                'shots_on_target': safe_int(row.get('SoT')),
                'shots_on_target_percentage': safe_float(row.get('SoT%')),
                'shots_per_90': safe_float(row.get('Sh/90')),
                'shots_on_target_per_90': safe_float(row.get('SoT/90')),
                
                # Passing stats
                'passes_completed': safe_int(row.get('Cmp')),
                'passes_attempted': safe_int(row.get('Att')),
                'pass_completion_percentage': safe_float(row.get('Cmp%')),
                'key_passes': safe_int(row.get('KP')),
                
                # Defensive stats
                'tackles': safe_int(row.get('Tkl')),
                'tackles_won': safe_int(row.get('TklW')),
                'interceptions': safe_int(row.get('Int')),
                'blocks': safe_int(row.get('Sh_stats_defense')),
                'clearances': safe_int(row.get('Clr')),
                
                # Possession stats
                'touches': safe_int(row.get('Touches')),
                'dribbles_attempted': safe_int(row.get('Att_stats_possession')),
                'dribbles_successful': safe_int(row.get('Succ')),
                'dribble_success_percentage': safe_float(row.get('Succ%')),
                
                # Performance metrics
                'progressive_carries': safe_int(row.get('PrgC')),
                'progressive_passes': safe_int(row.get('PrgP')),
                'progressive_receptions': safe_int(row.get('PrgR')),
            }

            # Add goalkeeper stats if available (only for GKs)
            if safe_str(row.get('Pos')).upper() == 'GK':
                player_data.update({
                    'goals_against': safe_float(row.get('GA')),
                    'goals_against_per_90': safe_float(row.get('GA90')),
                    'shots_faced': safe_int(row.get('SoTA')),
                    'saves': safe_int(row.get('Saves')),
                    'save_percentage': safe_float(row.get('Save%')),
                    'clean_sheets': safe_int(row.get('CS')),
                })

            # Validate required fields
            if not player_data['name'] or not player_data['position']:
                return None

            return player_data

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Error extracting data from row: {str(e)}')
            )
            return None 