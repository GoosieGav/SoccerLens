#!/bin/bash

# SoccerLens Backend Management Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Activate virtual environment
source venv/bin/activate

case "$1" in
    "setup")
        echo -e "${GREEN}Setting up SoccerLens Backend...${NC}"
        pip install -r requirements.txt
        python manage.py migrate
        echo -e "${GREEN}Setup complete!${NC}"
        ;;
    "loaddata")
        echo -e "${YELLOW}Loading player data...${NC}"
        python manage.py load_players players_data-2024_2025.csv --clear
        echo -e "${GREEN}Data loaded successfully!${NC}"
        ;;
    "run")
        echo -e "${GREEN}Starting development server...${NC}"
        python manage.py runserver
        ;;
    "migrate")
        python manage.py makemigrations
        python manage.py migrate
        echo -e "${GREEN}Migrations complete!${NC}"
        ;;
    "test")
        echo -e "${YELLOW}Testing API endpoints...${NC}"
        echo "1. API Root:"
        curl -s http://127.0.0.1:8000/ | head -200
        echo -e "\n\n2. Top players:"
        curl -s "http://127.0.0.1:8000/api/players/?page_size=3"
        echo -e "\n\n3. Search test:"
        curl -s "http://127.0.0.1:8000/api/players/search/?q=Kane&page_size=2"
        echo -e "\n\n4. Extensible sorting test:"
        curl -s "http://127.0.0.1:8000/api/players/?sort_by=goals_assists&sort_order=desc&page_size=3"
        echo -e "\n\n5. Sort options:"
        curl -s "http://127.0.0.1:8000/api/players/sort_options/?category=attacking" | head -100
        echo -e "\n\n6. Vector similarity test:"
        curl -s "http://127.0.0.1:8000/api/players/1692/similar/?method=hybrid&limit=3"
        echo -e "\n${GREEN}Test complete!${NC}"
        ;;
    "admin")
        echo -e "${YELLOW}Creating superuser...${NC}"
        python manage.py createsuperuser
        ;;
    *)
        echo -e "${YELLOW}SoccerLens Backend Management${NC}"
        echo "Usage: $0 {setup|loaddata|run|migrate|test|admin}"
        echo ""
        echo "Commands:"
        echo "  setup    - Install dependencies and run migrations"
        echo "  loaddata - Load player data from CSV"
        echo "  run      - Start development server"
        echo "  migrate  - Create and apply database migrations"
        echo "  test     - Test API endpoints"
        echo "  admin    - Create Django admin superuser"
        echo "  embeddings - Generate player style embeddings"
        ;;
    "embeddings")
        echo -e "${YELLOW}Generating player style embeddings...${NC}"
        python manage.py generate_embeddings --batch-size=100
        echo -e "${GREEN}Embeddings generated!${NC}"
        ;;

esac 