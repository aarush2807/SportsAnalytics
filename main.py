import json
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

def load_nba_data(file_path, season=2025):
    """Loads JSON data and returns a cleaned DataFrame for a specific season."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    rows = []
    for p in data['players']:
        name = p.get('name') or f"{p.get('firstName', '')} {p.get('lastName', '')}".strip()
        
        # Extract specific season stats
        for s in p.get('stats', []):
            if s['season'] == season and not s['playoffs']:
                rows.append({
                    'Name': name,
                    'Points': s['pts'],
                    'Assists': s['ast'],
                    'Rebounds': s['orb'] + s['drb'],
                    'Steals': s['stl'],
                    'Blocks': s['blk'],
                    'Minutes': s['min'],
                    'Games': s['gp']
                })
    return pd.DataFrame(rows)

def plot_nba_stats(df, stat_name):
    """Creates a bar chart of leaders and a scatter plot for efficiency."""
    # Calculate Per Game stat for the bar chart
    per_game_col = f"{stat_name} Per Game"
    df[per_game_col] = df[stat_name] / df['Games']
    
    # Sort by Per Game stats for the Top 10
    top_10 = df.sort_values(by=per_game_col, ascending=False).head(10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # --- Graph 1: Top 10 Leaders (Per Game) ---
    ax1.bar(top_10['Name'], top_10[per_game_col], color='skyblue')
    ax1.set_title(f'Top 10 Leaders: {stat_name} Per Game')
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_ylabel(f'{stat_name} / Game')

    # --- Graph 2: Efficiency (Minutes vs Total Stat) ---
    ax2.scatter(df['Minutes'], df[stat_name], alpha=0.4, color='orange')
    ax2.set_title(f'Minutes Played vs. Total {stat_name}')
    
    # Annotations
    texts = []
    refs = ["LeBron James", "Stephen Curry"]
    
    # Label the Top 10 (from the Per Game list) and Specific Reference players
    for _, row in df.iterrows():
        is_top_10 = row['Name'] in top_10['Name'].values
        is_ref = row['Name'] in refs
        
        if is_top_10 or is_ref:
            color = 'red' if is_ref else 'black'
            weight = 'bold' if is_ref else 'normal'
            t = ax2.text(row['Minutes'], row[stat_name], row['Name'], 
                         fontsize=9, color=color, fontweight=weight)
            texts.append(t)
            
            if is_ref: # Highlight reference player dots
                ax2.scatter(row['Minutes'], row[stat_name], color='red', s=60)

    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    plt.tight_layout()
    plt.show()

# --- Execution ---
if __name__ == "__main__":
    nba_df = load_nba_data('2025-26.NBA.Roster.json')
    
    print("Stats available: Points, Assists, Rebounds, Steals, Blocks")
    user_choice = input("Enter a stat: ").strip().title()

    if user_choice in nba_df.columns:
        plot_nba_stats(nba_df, user_choice)
    else:
        print("Invalid stat choice.")
