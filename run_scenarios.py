"""
Run different scenarios for the Circular Economy Simulation
Compare the impact of different parameters on environmental outcomes
"""

from circular_economy_simulation import CircularEconomyModel
import pandas as pd


def run_scenario(name, **kwargs):
    """Run a single scenario and return results"""
    print(f"\n{'='*70}")
    print(f"SCENARIO: {name}")
    print('='*70)

    model = CircularEconomyModel(**kwargs)

    print(f"\nConfiguration:")
    print(f"  Users: {model.num_users}")
    print(f"  Recycling Facilities: {model.num_recyclers}")
    print(f"  Remanufacturing Facilities: {model.num_remanufacturers}")
    print(f"  CO2 Tax Rate: ${model.co2_tax_rate} per unit")
    print(f"  Recycling Rate: {model.recycling_rate * 100}%")

    print(f"\nRunning simulation...")
    model.run_model(n_steps=100)

    # Calculate metrics
    total_recycled = sum(agent.products_recycled for agent in model.recycling_agents)
    total_remanufactured = sum(agent.products_remanufactured for agent in model.remanufacturing_agents)
    remanu_rate = (total_remanufactured / model.products_sold * 100) if model.products_sold > 0 else 0

    results = {
        'scenario': name,
        'total_co2': model.total_co2,
        'co2_tax_collected': model.total_co2_tax_collected,
        'waste_generated': model.waste_generated,
        'products_sold': model.products_sold,
        'products_recycled': total_recycled,
        'products_remanufactured': total_remanufactured,
        'remanufactured_rate': remanu_rate,
        'final_inventory': model.remanufactured_inventory
    }

    print(f"\nResults:")
    print(f"  Total CO2 Emissions: {results['total_co2']:.2f} units")
    print(f"  CO2 Tax Collected: ${results['co2_tax_collected']:.2f}")
    print(f"  Waste Generated: {results['waste_generated']} products")
    print(f"  Products Sold: {results['products_sold']}")
    print(f"  Products Recycled: {results['products_recycled']}")
    print(f"  Products Remanufactured: {results['products_remanufactured']}")
    print(f"  Remanufactured Rate: {results['remanufactured_rate']:.1f}%")

    return results, model


def main():
    """Run multiple scenarios and compare results"""
    print("="*70)
    print("CIRCULAR ECONOMY SIMULATION - SCENARIO COMPARISON")
    print("="*70)

    scenarios = []

    # Scenario 1: Baseline - No CO2 Tax
    print("\n\n🔴 Scenario 1: NO CO2 TAX (Baseline)")
    print("What happens without economic incentives for sustainability?")
    results, model = run_scenario(
        "No CO2 Tax",
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.0,  # No tax
        recycling_rate=0.7
    )
    scenarios.append(results)

    # Scenario 2: Low CO2 Tax
    print("\n\n🟡 Scenario 2: LOW CO2 TAX")
    print("Small economic incentive for sustainable choices")
    results, model = run_scenario(
        "Low CO2 Tax",
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.25,  # Low tax
        recycling_rate=0.7
    )
    scenarios.append(results)

    # Scenario 3: Moderate CO2 Tax (Current default)
    print("\n\n🟢 Scenario 3: MODERATE CO2 TAX")
    print("Balanced economic incentive")
    results, model = run_scenario(
        "Moderate CO2 Tax",
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,  # Moderate tax
        recycling_rate=0.7
    )
    scenarios.append(results)

    # Scenario 4: High CO2 Tax
    print("\n\n🔵 Scenario 4: HIGH CO2 TAX")
    print("Strong economic incentive for sustainability")
    results, model = run_scenario(
        "High CO2 Tax",
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=1.0,  # High tax
        recycling_rate=0.7
    )
    scenarios.append(results)

    # Scenario 5: Low Recycling Rate
    print("\n\n🟠 Scenario 5: LOW RECYCLING RATE")
    print("Poor recycling culture - only 30% recycle")
    results, model = run_scenario(
        "Low Recycling",
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,
        recycling_rate=0.3  # Low recycling
    )
    scenarios.append(results)

    # Scenario 6: High Recycling Rate
    print("\n\n🟢 Scenario 6: HIGH RECYCLING RATE")
    print("Excellent recycling culture - 95% recycle")
    results, model = run_scenario(
        "High Recycling",
        n_users=50,
        n_recyclers=5,
        n_remanufacturers=3,
        co2_tax_rate=0.5,
        recycling_rate=0.95  # High recycling
    )
    scenarios.append(results)

    # Scenario 7: Limited Recycling Infrastructure
    print("\n\n🔴 Scenario 7: LIMITED INFRASTRUCTURE")
    print("Only 2 recycling centers and 1 remanufacturing facility")
    results, model = run_scenario(
        "Limited Infrastructure",
        n_users=50,
        n_recyclers=2,  # Few recyclers
        n_remanufacturers=1,  # Few remanufacturers
        co2_tax_rate=0.5,
        recycling_rate=0.7
    )
    scenarios.append(results)

    # Scenario 8: Expanded Infrastructure
    print("\n\n💚 Scenario 8: EXPANDED INFRASTRUCTURE")
    print("10 recycling centers and 6 remanufacturing facilities")
    results, model = run_scenario(
        "Expanded Infrastructure",
        n_users=50,
        n_recyclers=10,  # Many recyclers
        n_remanufacturers=6,  # Many remanufacturers
        co2_tax_rate=0.5,
        recycling_rate=0.7
    )
    scenarios.append(results)

    # Scenario 9: Best Case
    print("\n\n⭐ Scenario 9: BEST CASE")
    print("High tax + High recycling + Expanded infrastructure")
    results, model = run_scenario(
        "Best Case",
        n_users=50,
        n_recyclers=10,
        n_remanufacturers=6,
        co2_tax_rate=1.0,
        recycling_rate=0.95
    )
    scenarios.append(results)

    # Scenario 10: Worst Case
    print("\n\n💀 Scenario 10: WORST CASE")
    print("No tax + Low recycling + Limited infrastructure")
    results, model = run_scenario(
        "Worst Case",
        n_users=50,
        n_recyclers=2,
        n_remanufacturers=1,
        co2_tax_rate=0.0,
        recycling_rate=0.3
    )
    scenarios.append(results)

    # Create comparison table
    print("\n\n" + "="*70)
    print("COMPARATIVE ANALYSIS")
    print("="*70)

    df = pd.DataFrame(scenarios)

    # Display key metrics
    print("\n📊 CO2 EMISSIONS COMPARISON:")
    print("-" * 70)
    for _, row in df.iterrows():
        bar_length = int(row['total_co2'] / 100)
        bar = '█' * bar_length
        print(f"{row['scenario']:<25} {row['total_co2']:>8.0f} CO2 {bar}")

    print("\n💰 CO2 TAX REVENUE COMPARISON:")
    print("-" * 70)
    for _, row in df.iterrows():
        bar_length = int(row['co2_tax_collected'] / 100)
        bar = '█' * bar_length
        print(f"{row['scenario']:<25} ${row['co2_tax_collected']:>7.0f} {bar}")

    print("\n🗑️  WASTE GENERATION COMPARISON:")
    print("-" * 70)
    for _, row in df.iterrows():
        bar_length = int(row['waste_generated'] / 10)
        bar = '█' * bar_length
        print(f"{row['scenario']:<25} {row['waste_generated']:>4.0f} units {bar}")

    print("\n♻️  REMANUFACTURING RATE COMPARISON:")
    print("-" * 70)
    for _, row in df.iterrows():
        bar_length = int(row['remanufactured_rate'] / 2)
        bar = '█' * bar_length
        print(f"{row['scenario']:<25} {row['remanufactured_rate']:>5.1f}% {bar}")

    # Find best and worst performers
    print("\n\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70)

    best_co2 = df.loc[df['total_co2'].idxmin()]
    worst_co2 = df.loc[df['total_co2'].idxmax()]

    print(f"\n🏆 LOWEST CO2 EMISSIONS:")
    print(f"   {best_co2['scenario']}: {best_co2['total_co2']:.0f} units")

    print(f"\n⚠️  HIGHEST CO2 EMISSIONS:")
    print(f"   {worst_co2['scenario']}: {worst_co2['total_co2']:.0f} units")

    print(f"\n📉 EMISSIONS REDUCTION POTENTIAL:")
    reduction = ((worst_co2['total_co2'] - best_co2['total_co2']) / worst_co2['total_co2'] * 100)
    print(f"   {reduction:.1f}% reduction possible by optimizing policies")

    best_remanu = df.loc[df['remanufactured_rate'].idxmax()]
    print(f"\n♻️  BEST REMANUFACTURING RATE:")
    print(f"   {best_remanu['scenario']}: {best_remanu['remanufactured_rate']:.1f}%")

    least_waste = df.loc[df['waste_generated'].idxmin()]
    print(f"\n🗑️  LEAST WASTE GENERATED:")
    print(f"   {least_waste['scenario']}: {least_waste['waste_generated']:.0f} products")

    print("\n\n" + "="*70)
    print("POLICY RECOMMENDATIONS")
    print("="*70)
    print("""
1. 💰 CO2 TAXATION: Higher taxes significantly reduce emissions by making
   remanufactured products more economically attractive.

2. ♻️  RECYCLING CULTURE: Increasing recycling rates from 30% to 95%
   dramatically reduces waste and enables circular economy.

3. 🏭 INFRASTRUCTURE: More recycling/remanufacturing facilities improve
   material flow and reduce bottlenecks in the circular system.

4. 🎯 COMBINED APPROACH: The best results come from combining high taxes,
   high recycling rates, and expanded infrastructure.

5. 💡 ECONOMIC IMPACT: CO2 taxes generate revenue that can be reinvested
   in green infrastructure and circular economy programs.
    """)

    print("\n" + "="*70)
    print("Simulation complete! All scenarios have been analyzed.")
    print("="*70)

    return df


if __name__ == "__main__":
    results_df = main()
