# Sports Betting Analytics Dashboard

A Streamlit application for analyzing sports betting statistics and performance by analyst.

## Features

- Overall betting statistics (win rate, ROI, net units)
- Member-specific performance metrics
- Recent plays tracking
- Detailed view of each analyst's picks

## Setup

### Prerequisites

- Python 3.10 or higher
- UV package manager (already installed)

### Installation

1. Navigate to the project directory:
```bash
cd /Users/cromano/Documents/Top_Plays
```

2. Create a virtual environment and install dependencies using UV:
```bash
uv venv
source .venv/bin/activate
uv pip install streamlit pandas numpy
```

## Running the Application

1. Ensure your virtual environment is activated:
```bash
source .venv/bin/activate
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser to the URL shown in the terminal (typically http://localhost:8501)

## Data Structure

The application expects a CSV file named `top_plays.csv` with the following columns:

- **DATE**: Date of the play
- **PLAY**: Description of the bet
- **ODDS**: Betting odds
- **MEMBER**: Analyst who made the pick
- **MASTER**: Result (W/L/P for Win/Loss/Push)
- **UNITS_OUT**: Units risked
- **UNITS_IN**: Units won

## Files

- `app.py`: Main Streamlit application
- `top_plays.csv`: Betting data
- `legup.png`: Logo image
- `pyproject.toml`: Project dependencies managed by UV
