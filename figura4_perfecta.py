import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def add_box(ax, x, y, width, height, label, facecolor, fontsize=12, fontweight='normal', linewidth=1.5):
    patch = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.08",
        facecolor=facecolor,
        edgecolor='black',
        linewidth=linewidth
    )
    ax.add_patch(patch)
    ax.text(x + width / 2, y + height / 2, label, ha='center', va='center', fontsize=fontsize, fontweight=fontweight)
    return patch


def side_center(patch, side, t=0.5):
    x = patch.get_x()
    y = patch.get_y()
    width = patch.get_width()
    height = patch.get_height()

    if side == 'top':
        return x + width * t, y + height
    if side == 'bottom':
        return x + width * t, y
    if side == 'left':
        return x, y + height * t
    if side == 'right':
        return x + width, y + height * t
    return x + width / 2, y + height / 2


def connect_boxes(ax, source_patch, target_patch, color='black', lw=1.8, source_side='top', target_side='bottom', source_t=0.5, target_t=0.5):
    source_point = side_center(source_patch, source_side, source_t)
    target_point = side_center(target_patch, target_side, target_t)
    ax.annotate(
        '',
        xy=target_point,
        xytext=source_point,
        arrowprops=dict(
            arrowstyle='->',
            lw=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
            connectionstyle='arc3,rad=0'
        )
    )


fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 14)
ax.axis('off')

# Layout levels (uniform central spacing)
y_origins = 12.2
y_top = 9.8
level_gap = 2.0
y_ros = y_top - level_gap
y_antiox = y_ros - level_gap
y_damage = y_antiox - level_gap
y_bottom = 2.0

# Main boxes
box_oxidative = add_box(ax, 5.3, y_top, 5.4, 0.9, 'Estrés Oxidativo', 'lightyellow', fontsize=20, fontweight='bold', linewidth=2)
box_ros = add_box(ax, 5.0, y_ros, 6.0, 0.9, 'Generación de ROS', 'lightblue', fontsize=20, fontweight='bold', linewidth=2)
box_antiox = add_box(ax, 5.4, y_antiox, 5.2, 0.9, 'Disminución de Antioxidantes endógenos', 'lightgreen', fontsize=15, fontweight='bold')
box_damage = add_box(ax, 6.3, y_damage, 3.4, 0.9, 'Daño Celular', 'salmon', fontsize=20, fontweight='bold', linewidth=2)

# Origin boxes (same level)
origin_boxes = [
    add_box(ax, 0.9, y_origins, 2.6, 0.9, 'Radiación UV', 'lavender', fontsize=17, fontweight='bold'),
    add_box(ax, 4.2, y_origins, 2.0, 0.75, 'Polución', 'wheat', fontsize=17, fontweight='bold'),
    add_box(ax, 6.9, y_origins, 2.0, 0.75, 'Tabaquismo', 'wheat', fontsize=17, fontweight='bold'),
    add_box(ax, 9.6, y_origins, 2.0, 0.75, 'Inflamación', 'wheat', fontsize=17, fontweight='bold'),
    add_box(ax, 12.1, y_origins, 2.6, 0.9, 'Edad', 'lavender', fontsize=17, fontweight='bold')
]

# Bottom outcome boxes
bot_w = 1.95
bot_h = 0.75
bot_labels = ['Envejecimiento\nAcelerado', 'Melasma', 'Acné', 'Psoriasis', 'Dermatitis\nAtópica', 'Vitíligo', 'Cáncer\nde Piel']
bot_x = np.linspace(1.2, 14.2, 7)
bottom_boxes = []
for x, label in zip(bot_x, bot_labels):
    bottom_boxes.append(
        add_box(ax, x - bot_w / 2, y_bottom, bot_w, bot_h, label, 'pink', fontsize=14)
    )

# Connections: clean edge-to-edge arrows
top_targets = [0.08, 0.30, 0.50, 0.70, 0.92]
for box, t in zip(origin_boxes, top_targets):
    connect_boxes(
        ax, box, box_oxidative,
        color='black', lw=1.7,
        source_side='bottom', target_side='top',
        source_t=0.5, target_t=t
    )

connect_boxes(ax, box_oxidative, box_ros, color='black', lw=2.3, source_side='bottom', target_side='top')
connect_boxes(ax, box_ros, box_antiox, color='darkblue', lw=2.4, source_side='bottom', target_side='top')
connect_boxes(ax, box_antiox, box_damage, color='darkgreen', lw=2.4, source_side='bottom', target_side='top')

for box in bottom_boxes:
    connect_boxes(ax, box_damage, box, color='darkred', lw=1.5, source_side='bottom', target_side='top')

plt.title('Figura 4. Factores de riesgo para generación de ROS y afectaciones cutáneas\nElaboración propia',
          fontsize=22, pad=24, fontweight='bold')
plt.tight_layout()

output_file = r"D:\Users\ASUS\Downloads\Figura factores de riesgo ROS.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f'¡Diagrama generado: {output_file}')
