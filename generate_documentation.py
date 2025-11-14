"""
Generate visualizations and comprehensive documentation for the Circular Economy Simulation
"""

from circular_economy_simulation import CircularEconomyModel
from cannibalization_analysis import CircularEconomyModelWithCannibalization, ProductQuality
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Create output directory for figures
os.makedirs('figures', exist_ok=True)

print("="*80)
print("GENERATING COMPREHENSIVE DOCUMENTATION AND VISUALIZATIONS")
print("="*80)

# ============================================================================
# PART 1: Basic Scenarios Comparison
# ============================================================================
print("\n1. Running scenarios for comparison...")

scenarios_data = []

# Scenario 1: No CO2 Tax
print("   - No CO2 Tax")
model = CircularEconomyModel(n_users=50, n_recyclers=5, n_remanufacturers=3,
                              co2_tax_rate=0.0, recycling_rate=0.7)
model.run_model(n_steps=100)
data = model.datacollector.get_model_vars_dataframe()
scenarios_data.append(('No CO2 Tax', data))

# Scenario 2: Moderate CO2 Tax
print("   - Moderate CO2 Tax")
model = CircularEconomyModel(n_users=50, n_recyclers=5, n_remanufacturers=3,
                              co2_tax_rate=0.5, recycling_rate=0.7)
model.run_model(n_steps=100)
data = model.datacollector.get_model_vars_dataframe()
scenarios_data.append(('Moderate CO2 Tax ($0.5)', data))

# Scenario 3: High CO2 Tax
print("   - High CO2 Tax")
model = CircularEconomyModel(n_users=50, n_recyclers=5, n_remanufacturers=3,
                              co2_tax_rate=1.0, recycling_rate=0.7)
model.run_model(n_steps=100)
data = model.datacollector.get_model_vars_dataframe()
scenarios_data.append(('High CO2 Tax ($1.0)', data))

# Scenario 4: Low Recycling
print("   - Low Recycling Rate")
model = CircularEconomyModel(n_users=50, n_recyclers=5, n_remanufacturers=3,
                              co2_tax_rate=0.5, recycling_rate=0.3)
model.run_model(n_steps=100)
data = model.datacollector.get_model_vars_dataframe()
scenarios_data.append(('Low Recycling (30%)', data))

# Scenario 5: High Recycling
print("   - High Recycling Rate")
model = CircularEconomyModel(n_users=50, n_recyclers=5, n_remanufacturers=3,
                              co2_tax_rate=0.5, recycling_rate=0.95)
model.run_model(n_steps=100)
data = model.datacollector.get_model_vars_dataframe()
scenarios_data.append(('High Recycling (95%)', data))

# ============================================================================
# PART 2: Generate Graphs for Policy Scenarios
# ============================================================================
print("\n2. Generating policy scenario graphs...")

# Graph 1: CO2 Emissions Over Time
plt.figure(figsize=(12, 6))
for name, data in scenarios_data:
    plt.plot(data.index, data['Total CO2'], label=name, linewidth=2)
plt.xlabel('Time Steps', fontsize=12)
plt.ylabel('Total CO2 Emissions (units)', fontsize=12)
plt.title('CO2 Emissions Over Time - Policy Comparison', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/1_co2_emissions_comparison.png', dpi=300)
print("   ✓ Saved: 1_co2_emissions_comparison.png")
plt.close()

# Graph 2: Products Sold Over Time
plt.figure(figsize=(12, 6))
for name, data in scenarios_data:
    plt.plot(data.index, data['Products Sold'], label=name, linewidth=2)
plt.xlabel('Time Steps', fontsize=12)
plt.ylabel('Cumulative Products Sold', fontsize=12)
plt.title('Product Sales Over Time - Policy Comparison', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/2_products_sold_comparison.png', dpi=300)
print("   ✓ Saved: 2_products_sold_comparison.png")
plt.close()

# Graph 3: Waste Generation Comparison
plt.figure(figsize=(12, 6))
for name, data in scenarios_data:
    plt.plot(data.index, data['Waste Generated'], label=name, linewidth=2)
plt.xlabel('Time Steps', fontsize=12)
plt.ylabel('Cumulative Waste Generated', fontsize=12)
plt.title('Waste Generation Over Time - Policy Comparison', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/3_waste_generation_comparison.png', dpi=300)
print("   ✓ Saved: 3_waste_generation_comparison.png")
plt.close()

# Graph 4: CO2 Tax Revenue
plt.figure(figsize=(12, 6))
for name, data in scenarios_data:
    if data['CO2 Tax Collected'].iloc[-1] > 0:  # Only plot scenarios with tax
        plt.plot(data.index, data['CO2 Tax Collected'], label=name, linewidth=2)
plt.xlabel('Time Steps', fontsize=12)
plt.ylabel('CO2 Tax Revenue Collected ($)', fontsize=12)
plt.title('CO2 Tax Revenue Over Time', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/4_co2_tax_revenue.png', dpi=300)
print("   ✓ Saved: 4_co2_tax_revenue.png")
plt.close()

# ============================================================================
# PART 3: Cannibalization Analysis Graphs
# ============================================================================
print("\n3. Running cannibalization scenarios...")

cannib_data = []

# Planned Obsolescence
print("   - Planned Obsolescence")
model = CircularEconomyModelWithCannibalization(
    n_users=50, n_recyclers=5, n_remanufacturers=3,
    co2_tax_rate=0.5, recycling_rate=0.7,
    product_quality=ProductQuality.LOW,
    reconditioning_quality=ProductQuality.LOW
)
model.run_model(n_steps=100)
data = model.datacollector.get_model_vars_dataframe()
cannib_data.append(('Planned Obsolescence', data, model))

# Standard Quality
print("   - Standard Quality")
model = CircularEconomyModelWithCannibalization(
    n_users=50, n_recyclers=5, n_remanufacturers=3,
    co2_tax_rate=0.5, recycling_rate=0.7,
    product_quality=ProductQuality.MEDIUM,
    reconditioning_quality=ProductQuality.MEDIUM
)
model.run_model(n_steps=100)
data = model.datacollector.get_model_vars_dataframe()
cannib_data.append(('Standard Quality', data, model))

# High Durability
print("   - High Durability")
model = CircularEconomyModelWithCannibalization(
    n_users=50, n_recyclers=5, n_remanufacturers=3,
    co2_tax_rate=0.5, recycling_rate=0.7,
    product_quality=ProductQuality.HIGH,
    reconditioning_quality=ProductQuality.HIGH
)
model.run_model(n_steps=100)
data = model.datacollector.get_model_vars_dataframe()
cannib_data.append(('High Durability', data, model))

print("\n4. Generating cannibalization graphs...")

# Graph 5: Sales Volume - Cannibalization Effect
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Sales over time
for name, data, model in cannib_data:
    ax1.plot(data.index, data['Products Sold'], label=name, linewidth=2)
ax1.set_xlabel('Time Steps', fontsize=12)
ax1.set_ylabel('Cumulative Products Sold', fontsize=12)
ax1.set_title('Cannibalization Effect on Sales Volume', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Final sales comparison
names = [name for name, _, _ in cannib_data]
final_sales = [data['Products Sold'].iloc[-1] for _, data, _ in cannib_data]
colors = ['#e74c3c', '#f39c12', '#27ae60']
ax2.bar(names, final_sales, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_ylabel('Total Products Sold', fontsize=12)
ax2.set_title('Final Sales Volume Comparison', fontsize=14, fontweight='bold')
ax2.grid(True, axis='y', alpha=0.3)

# Add value labels on bars
for i, v in enumerate(final_sales):
    ax2.text(i, v + 20, str(int(v)), ha='center', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('figures/5_cannibalization_sales.png', dpi=300)
print("   ✓ Saved: 5_cannibalization_sales.png")
plt.close()

# Graph 6: Revenue Impact
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Revenue over time
for name, data, model in cannib_data:
    ax1.plot(data.index, data['Total Revenue'], label=name, linewidth=2)
ax1.set_xlabel('Time Steps', fontsize=12)
ax1.set_ylabel('Total Revenue ($)', fontsize=12)
ax1.set_title('Revenue Impact of Product Durability', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Final revenue comparison
revenues = [data['Total Revenue'].iloc[-1] for _, data, _ in cannib_data]
ax2.bar(names, revenues, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_ylabel('Total Revenue ($)', fontsize=12)
ax2.set_title('Final Revenue Comparison', fontsize=14, fontweight='bold')
ax2.grid(True, axis='y', alpha=0.3)

# Add value labels
for i, v in enumerate(revenues):
    ax2.text(i, v + 1000, f'${int(v):,}', ha='center', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('figures/6_cannibalization_revenue.png', dpi=300)
print("   ✓ Saved: 6_cannibalization_revenue.png")
plt.close()

# Graph 7: Environmental vs Business Trade-off
fig, ax = plt.subplots(figsize=(12, 8))

final_co2 = [data['Total CO2'].iloc[-1] for _, data, _ in cannib_data]
revenues = [data['Total Revenue'].iloc[-1] for _, data, _ in cannib_data]

scatter = ax.scatter(final_co2, revenues, s=500, c=colors, alpha=0.6, edgecolors='black', linewidth=2)

# Add labels
for i, name in enumerate(names):
    ax.annotate(name, (final_co2[i], revenues[i]),
                fontsize=12, fontweight='bold', ha='center', va='bottom',
                xytext=(0, 10), textcoords='offset points')

ax.set_xlabel('Total CO2 Emissions (units)', fontsize=12)
ax.set_ylabel('Total Revenue ($)', fontsize=12)
ax.set_title('Environmental vs Business Trade-off\n(The Cannibalization Paradox)',
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Add arrow showing the trade-off
ax.annotate('', xy=(final_co2[2], revenues[2]), xytext=(final_co2[0], revenues[0]),
            arrowprops=dict(arrowstyle='->', lw=2, color='red', ls='--'))
ax.text((final_co2[0] + final_co2[2])/2, (revenues[0] + revenues[2])/2,
        'Trade-off Direction', fontsize=11, color='red', fontweight='bold',
        ha='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('figures/7_tradeoff_analysis.png', dpi=300)
print("   ✓ Saved: 7_tradeoff_analysis.png")
plt.close()

# Graph 8: Multi-metric Dashboard
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

metrics = ['Products Sold', 'Total Revenue', 'Total CO2', 'Waste Generated']
titles = ['Products Sold', 'Revenue ($)', 'CO2 Emissions', 'Waste Generated']

for idx, (metric, title) in enumerate(zip(metrics, titles)):
    row = idx // 2
    col = (idx % 2) * 1.5

    ax = fig.add_subplot(gs[row, int(col):int(col+1)])

    values = [data[metric].iloc[-1] if metric in data.columns else model.total_revenue
              for _, data, model in cannib_data]

    ax.bar(names, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    ax.tick_params(axis='x', rotation=15)

    # Add value labels
    for i, v in enumerate(values):
        if metric == 'Total Revenue':
            label = f'${int(v):,}'
        else:
            label = f'{int(v)}'
        ax.text(i, v * 1.02, label, ha='center', fontsize=10, fontweight='bold')

# Add summary text
ax_text = fig.add_subplot(gs[2, :])
ax_text.axis('off')

summary_text = f"""
CANNIBALIZATION SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sales Reduction (Planned → High Durability): {((final_sales[0] - final_sales[2])/final_sales[0]*100):.1f}%
Revenue Loss (Planned → High Durability): ${int(revenues[0] - revenues[2]):,} ({((revenues[0] - revenues[2])/revenues[0]*100):.1f}%)

CO2 Reduction (Planned → High Durability): {int(final_co2[0] - final_co2[2]):,} units ({((final_co2[0] - final_co2[2])/final_co2[0]*100):.1f}%)
Waste Reduction (Planned → High Durability): {int(cannib_data[0][1]['Waste Generated'].iloc[-1] - cannib_data[2][1]['Waste Generated'].iloc[-1])} units

KEY INSIGHT: Better products = Lower sales = Higher sustainability
"""

ax_text.text(0.5, 0.5, summary_text, ha='center', va='center', fontsize=11,
             family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.savefig('figures/8_dashboard_summary.png', dpi=300)
print("   ✓ Saved: 8_dashboard_summary.png")
plt.close()

print("\n" + "="*80)
print("✓ All visualizations generated successfully!")
print("✓ Figures saved in 'figures/' directory")
print("="*80)
