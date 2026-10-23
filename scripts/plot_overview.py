"""Render assets/imgs/project-overview.png: pipeline, age distribution, and accuracy vs. benchmark.

Usage:
    python scripts/plot_overview.py
"""

import glob
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ACCENT = "#B5533C"
GRAY = "#8A8A8A"
INK = "#1E1E1E"
plt.rcParams["font.family"] = ["Helvetica Neue", "Arial", "DejaVu Sans"]

fig = plt.figure(figsize=(16, 8.6), dpi=110)
fig.text(0.5, 0.94, "Age & Gender Detection with CNNs", ha="center", fontsize=26, color=INK)
for x in (0.355, 0.68):
    fig.add_artist(plt.Line2D([x, x], [0.08, 0.86], color="#CCCCCC", ls=(0, (4, 4)), lw=1))

# ---------------- Panel 1: pipeline ----------------
ax = fig.add_axes([0.02, 0.06, 0.32, 0.82])
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
fig.text(0.18, 0.84, "Two-CNN Pipeline", ha="center", fontsize=17, color=GRAY)

faces = sorted(glob.glob(f"{REPO}/data/test_age/(25-32)/*.jpg"))[:1] + \
    sorted(glob.glob(f"{REPO}/data/test_age/(0-2)/*.jpg"))[5:6] + \
    sorted(glob.glob(f"{REPO}/data/test_age/(60-100)/*.jpg"))[3:4] + \
    sorted(glob.glob(f"{REPO}/data/test_age/(8-12)/*.jpg"))[7:8]
for i, f in enumerate(faces):
    r, c = divmod(i, 2)
    x0, y0 = 0.15 + c * 1.3, 5.4 - r * 1.6
    im = Image.open(f).convert("RGB").resize((150, 150))
    ax.imshow(im, extent=(x0, x0 + 1.15, y0, y0 + 1.15), zorder=2, aspect="auto")
    ax.add_patch(FancyBboxPatch((x0, y0), 1.15, 1.15, boxstyle="square,pad=0",
                                fc="none", ec=INK, lw=1.2, zorder=3))
ax.text(1.4, 3.35, "Adience faces\n150×150×3 RGB", ha="center", va="top", fontsize=11.5, color=INK)


def box(x, y, w, h, text, ec=INK, fs=11.5, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.25",
                                fc="white", ec=ec, lw=1.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK, weight=weight)


def arrow(p, q, color=INK, dashed=False):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, lw=1.6, color=color,
                                 ls=(0, (4, 3)) if dashed else "-"))


box(3.55, 6.9, 3.45, 1.7, "Gender CNN\n3× Conv(32)\nFC 128 → 64", fs=11)
box(3.55, 3.3, 3.45, 1.7, "Age CNN\n3× Conv(64)\nFC 128 → 64", ec=ACCENT, fs=11)
arrow((2.85, 6.4), (3.5, 7.5))
arrow((2.85, 5.0), (3.5, 4.2), color=ACCENT)
box(7.65, 7.2, 2.25, 1.1, "Male / Female\nsigmoid", fs=11)
box(7.65, 3.6, 2.25, 1.1, "8 age groups\nsoftmax", ec=ACCENT, fs=11)
arrow((7.05, 7.75), (7.6, 7.75))
arrow((7.05, 4.15), (7.6, 4.15), color=ACCENT)
ax.text(5.3, 2.75, "class-weighted loss\nfor skewed age labels", ha="center", va="top",
        fontsize=11, color=ACCENT, style="italic")
ax.text(5.0, 0.9, "augment: shear · zoom · horizontal flip\noptimizer: RMSprop   split: 80 / 10 / 10",
        ha="center", fontsize=11, color=GRAY)

# ---------------- Panel 2: age distribution ----------------
ax2 = fig.add_axes([0.405, 0.16, 0.25, 0.62])
fig.text(0.5175, 0.84, "Skewed Age Distribution", ha="center", fontsize=17, color=GRAY)
groups = ["0-2", "4-6", "8-12", "15-20", "25-32", "38-43", "48-53", "60-100"]
counts = [len(glob.glob(f"{REPO}/data/train_age/({g})/*")) for g in groups]
colors = [ACCENT if g == "25-32" else "white" for g in groups]
bars = ax2.bar(groups, counts, color=colors, edgecolor=INK, lw=1.3, width=0.7)
for b, n in zip(bars, counts):
    ax2.text(b.get_x() + b.get_width() / 2, n + 50, f"{n:,}", ha="center", fontsize=9.5, color=INK)
ax2.set_ylabel("Training images", fontsize=13, color=INK)
ax2.set_xlabel("Age group (years)", fontsize=13, color=INK)
ax2.tick_params(axis="x", rotation=40, labelsize=10.5)
ax2.tick_params(axis="y", labelsize=10)
ax2.set_ylim(0, max(counts) * 1.15)
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)
ax2.text(4, max(counts) * 1.1, "~6× more than 48-53", ha="center", fontsize=10.5, color=ACCENT, style="italic")

# ---------------- Panel 3: results ----------------
ax3 = fig.add_axes([0.73, 0.16, 0.25, 0.62])
fig.text(0.855, 0.84, "Test Accuracy vs. Benchmark", ha="center", fontsize=17, color=GRAY)
tasks = ["Gender", "Age"]
ours, bench = [80.5, 43.0], [84.7, 50.7]
x = range(len(tasks))
w = 0.36
b1 = ax3.bar([i - w / 2 for i in x], ours, w, color=ACCENT, edgecolor=INK, lw=1.3, label="Ours")
b2 = ax3.bar([i + w / 2 for i in x], bench, w, color="white", edgecolor=INK, lw=1.3, label="Levi & Hassner (2015)")
for bs in (b1, b2):
    for b in bs:
        ax3.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5, f"{b.get_height():.1f}%",
                 ha="center", fontsize=11, color=INK)
ax3.set_xticks(list(x)); ax3.set_xticklabels(tasks, fontsize=13)
ax3.set_ylabel("Accuracy (%)", fontsize=13, color=INK)
ax3.set_ylim(0, 100); ax3.set_xlim(-0.5, 1.5)
ax3.tick_params(axis="y", labelsize=10)
ax3.legend(frameon=False, fontsize=10.5, loc="upper right")
for s in ("top", "right"):
    ax3.spines[s].set_visible(False)

fig.savefig(f"{REPO}/assets/imgs/project-overview.png", dpi=110, facecolor="white")
