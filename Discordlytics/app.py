import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Verhindert GUI-Fehler in Flask
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template_string

app = Flask(__name__)

# --- CSV einlesen ---
df = pd.read_csv("server_activity.csv", sep=None, engine="python")
df.columns = df.columns.str.strip()

df.rename(columns={
    'Datum': 'timestamp',
    'User': 'user',
    'Channel': 'channel',
    'Inhalt': 'message'
}, inplace=True)

# --- Zeitspalten vorbereiten ---
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', dayfirst=True)
df = df.dropna(subset=['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour
df['weekday'] = df['timestamp'].dt.day_name()

# --- Hilfsfunktion: matplotlib -> Base64 ---
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)
    return img

# --- Diagramme erstellen ---
def create_plots():
    plots = {}
    sns.set_style("whitegrid")
    plt.rcParams.update({'axes.facecolor': '#ffffff', 'figure.facecolor': '#ffffff'})

    # Top User Diagramm
    user_counts = df['user'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=user_counts.values, y=user_counts.index, palette="Blues_r", ax=ax)
    ax.set_title("Top 10 aktive User", fontsize=13, fontweight='bold')
    ax.set_xlabel("Nachrichten")
    ax.set_ylabel("User")
    plots['user'] = fig_to_base64(fig)

    # Top Channels Diagramm
    channel_counts = df['channel'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=channel_counts.values, y=channel_counts.index, palette="viridis", ax=ax)
    ax.set_title("Top Channels", fontsize=13, fontweight='bold')
    ax.set_xlabel("Nachrichten")
    ax.set_ylabel("Channel")
    plots['channel'] = fig_to_base64(fig)

    # Nachrichten über Zeit Diagramm
    daily = df.groupby('date').size()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(x=daily.index, y=daily.values, marker="o", color="#0d6efd", ax=ax)
    ax.set_title("Nachrichtenaktivität über Zeit", fontsize=13, fontweight='bold')
    ax.set_xlabel("Datum")
    ax.set_ylabel("Nachrichten")
    plots['time'] = fig_to_base64(fig)

    # Heatmap: Wochentag & Stunde Diagramm
    pivot = df.pivot_table(index='weekday', columns='hour', values='message', aggfunc='count').fillna(0)
    pivot = pivot.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(pivot, cmap="YlGnBu", ax=ax)
    ax.set_title("Aktivität nach Wochentag & Stunde", fontsize=13, fontweight='bold')
    plots['heatmap'] = fig_to_base64(fig)

    # 5️Durchschnittliche Nachrichten pro User Diagramm
    avg_msgs = df.groupby('user').size().mean()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.barh(["Durchschnitt"], [avg_msgs], color="#198754")
    ax.set_title("Durchschnittliche Nachrichten pro User", fontsize=13, fontweight='bold')
    plots['avg'] = fig_to_base64(fig)

    # Aktivität pro Wochentag Diagramm
    weekday_counts = df['weekday'].value_counts().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=weekday_counts.index, y=weekday_counts.values, palette="coolwarm", ax=ax)
    ax.set_title("Aktivität pro Wochentag", fontsize=13, fontweight='bold')
    ax.set_ylabel("Nachrichten")
    ax.set_xlabel("Wochentag")
    plots['weekday'] = fig_to_base64(fig)

    # Aktivität pro Stunde Diagramm
    hour_counts = df['hour'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(x=hour_counts.index, y=hour_counts.values, marker="o", color="#ff6600", ax=ax)
    ax.set_title("Aktivität pro Stunde", fontsize=13, fontweight='bold')
    ax.set_xlabel("Stunde")
    ax.set_ylabel("Nachrichten")
    plots['hour'] = fig_to_base64(fig)

    return plots

# --- Startseite mit Diagramme ---
TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Server Activity Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark" style="background: linear-gradient(90deg, #0d6efd, #3a7afe);">
  <div class="container-fluid">
    <a class="navbar-brand fs-4 fw-bold" href="/">Server Dashboard</a>
    <div class="ms-auto">
      <a href="/" class="btn btn-outline-light btn-sm me-2">Home</a>
      <a href="/users" class="btn btn-outline-light btn-sm">Userliste</a>
    </div>
  </div>
</nav>

<!-- Dashboard Container -->
<div class="container-fluid py-4">
  <div class="row g-4">

    <div class="col-md-6 d-flex">
      <div class="card shadow-sm flex-fill border-0">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title text-center text-primary fw-semibold mb-3">Top User</h5>
          <img src="data:image/png;base64,{{ plots['user'] }}" class="img-fluid rounded flex-fill">
        </div>
      </div>
    </div>

    <div class="col-md-6 d-flex">
      <div class="card shadow-sm flex-fill border-0">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title text-center text-primary fw-semibold mb-3">Nachrichten über Zeit</h5>
          <img src="data:image/png;base64,{{ plots['time'] }}" class="img-fluid rounded flex-fill">
        </div>
      </div>
    </div>

    <div class="col-md-6 d-flex">
      <div class="card shadow-sm flex-fill border-0">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title text-center text-primary fw-semibold mb-3">Aktivität nach Wochentag & Stunde</h5>
          <img src="data:image/png;base64,{{ plots['heatmap'] }}" class="img-fluid rounded flex-fill">
        </div>
      </div>
    </div>

    <div class="col-md-6 d-flex">
      <div class="card shadow-sm flex-fill border-0">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title text-center text-primary fw-semibold mb-3">Aktivität pro Wochentag</h5>
          <img src="data:image/png;base64,{{ plots['weekday'] }}" class="img-fluid rounded flex-fill">
        </div>
      </div>
    </div>

    <div class="col-md-6 d-flex">
      <div class="card shadow-sm flex-fill border-0">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title text-center text-primary fw-semibold mb-3">Aktivität pro Stunde</h5>
          <img src="data:image/png;base64,{{ plots['hour'] }}" class="img-fluid rounded flex-fill">
        </div>
      </div>
    </div>

  </div>
</div>

<!-- Footer -->
<footer class="text-center text-muted py-3">
  <p>Erstellt mit Flask & Matplotlib | © 2025 Dashboard</p>
</footer>

</body>
</html>
"""


# --- Userliste ---
USER_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Benutzerübersicht</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark" style="background: linear-gradient(90deg, #0d6efd, #3a7afe);">
  <div class="container-fluid">
    <a class="navbar-brand fs-4 fw-bold" href="/">Server Dashboard</a>
    <div class="ms-auto">
      <a href="/" class="btn btn-outline-light btn-sm me-2">Home</a>
      <a href="/users" class="btn btn-outline-light btn-sm active">Userliste</a>
    </div>
  </div>
</nav>

<!-- Container -->
<div class="container py-4">
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <h4 class="text-center text-primary fw-semibold mb-4">Alle User & Nachrichtenanzahl</h4>
      <div class="table-responsive">
        <table class="table table-striped align-middle">
          <thead class="table-primary">
            <tr>
              <th>User</th>
              <th class="text-end">Nachrichten</th>
            </tr>
          </thead>
          <tbody>
            {% for _, row in users.iterrows() %}
            <tr>
              <td>{{ row['User'] }}</td>
              <td class="text-end">{{ row['Nachrichten'] }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<!-- Footer -->
<footer class="text-center text-muted py-3">
  <p>Erstellt mit Flask & Matplotlib | © 2025 Dashboard</p>
</footer>

</body>
</html>
"""

# --- Flask Routes ---
@app.route("/")
def index():
    plots = create_plots()
    return render_template_string(TEMPLATE, plots=plots)

@app.route("/users")
def users():
    user_stats = df['user'].value_counts().reset_index()
    user_stats.columns = ['User', 'Nachrichten']
    return render_template_string(USER_TEMPLATE, users=user_stats)

if __name__ == "__main__":
    app.run(debug=True)

