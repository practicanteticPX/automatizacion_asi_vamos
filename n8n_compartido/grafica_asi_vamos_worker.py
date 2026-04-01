import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import base64, io

# Variables inyectadas por el worker (no definir aquí):
#   nombre_cliente (str)
#   ventas_2024, ventas_2025, ventas_2026 (float)

# ── Colores ───────────────────────────────────────────
COLOR_BARRA = '#E87722'
COLOR_BG    = '#FFFFFF'
COLOR_PANEL = '#F2F2F2'

# ── Figura ────────────────────────────────────────────
fig = plt.figure(figsize=(9, 6.5))
fig.patch.set_facecolor(COLOR_BG)

# Título: nombre del cliente
fig.text(0.5, 0.93, nombre_cliente,
         ha='center', va='top',
         fontsize=16, fontweight='bold')

# Separador horizontal
line = plt.Line2D([0.08, 0.92], [0.88, 0.88],
                  transform=fig.transFigure,
                  color='#CCCCCC', linewidth=1)
fig.add_artist(line)

# ── Área del gráfico ──────────────────────────────────
ax = fig.add_axes([0.1, 0.08, 0.82, 0.75])
ax.set_facecolor(COLOR_PANEL)

# ── Barras ────────────────────────────────────────────
years  = ['2024', '2025', '2026']
values = [ventas_2024, ventas_2025, ventas_2026]

bars = ax.bar(years, values, color=COLOR_BARRA, width=0.45, zorder=3)

# Valores sobre cada barra
max_val = max(values) if max(values) > 0 else 1
for bar, val in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + max_val * 0.015,
        f"{val:,.2f}",
        ha='center', va='bottom',
        fontsize=9, fontweight='bold', color='#333333'
    )

# ── Eje Y ─────────────────────────────────────────────
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
)
ax.set_ylim(0, max_val * 1.18)
ax.tick_params(axis='y', labelsize=8)

# ── Eje X ─────────────────────────────────────────────
ax.tick_params(axis='x', labelsize=11, length=0)

# ── Grid y bordes ─────────────────────────────────────
ax.yaxis.grid(True, color='white', linewidth=1.2, zorder=0)
ax.set_axisbelow(True)
for spine in ['top', 'right', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')

# ── Título del gráfico ────────────────────────────────
ax.set_title('Comportamiento Ventas', fontsize=12,
             pad=10, loc='center', color='#333333')

# ── Exportar (result es capturado por el worker) ──────
buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=150,
            bbox_inches='tight', facecolor=COLOR_BG)
buf.seek(0)
result = base64.b64encode(buf.read()).decode('utf-8')
plt.close()
