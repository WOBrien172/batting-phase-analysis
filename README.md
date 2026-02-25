## Batting Analysis Tool
A Python-based analysis tool designed to extract deeper batting patterns from basic ball-by-ball cricket data (e.g. batter, bowler, ball number, runs scored).

## Features
- Scoring distribution breakdown (dots, singles, twos, boundaries)
- Post-event scoring tendencies (e.g. performance after dot balls)
- Phase-based run analysis (powerplay, middle overs, death overs)
- Ball-in-over scoring trends
- Six-ball segment momentum tracking
- Boundary timing identification

## Inputs
- Match format (20–50 overs)
- Batter entry and exit overs
- Ball-by-ball input per over

## Outputs
- Structured console summaries
- Spreadsheet-ready tab-separated outputs for further aggregation and modelling

## Context
While platforms such as Play-Cricket provide aggregate metrics (runs, boundaries, strike rate), 
this tool focuses on micro-pattern analysis within an innings. The aim is to uncover behavioural 
and situational trends that may support:
- Match-up planning
- Phase-specific strategy development
- Momentum analysis
- Player profiling across multiple innings

Strike rate and cumulative metrics are designed to be calculated externally across aggregated innings to support longitudinal analysis.
