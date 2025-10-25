# Circular Economy Simulation with CO2 Taxes

A Mesa-based agent-based model simulating a circular economy with users, recycling centers, remanufacturing facilities, and CO2 taxation.

## Features

- **User Agents**: Consumers who buy, use, and dispose of products
- **Recycling Agents**: Facilities that process used products into recycled materials
- **Remanufacturing Agents**: Facilities that turn recycled materials into remanufactured products
- **CO2 Tax System**: Economic incentive to reduce carbon emissions
- **Product Lifecycle**: NEW → USED → RECYCLED → REMANUFACTURED → back to market

## Installation

```bash
pip install -r requirements.txt
```

## Running the Simulation

```bash
python circular_economy_simulation.py
```

## How It Works

### Agents

1. **UserAgent**:
   - Purchase new or remanufactured products
   - Pay CO2 taxes based on product carbon footprint
   - Use products until they wear out
   - Decide to recycle or throw away used products

2. **RecyclingAgent**:
   - Process used products from recycling queue
   - Convert products to recycled materials
   - Has capacity and efficiency constraints
   - Generates some CO2 during recycling

3. **RemanufacturingAgent**:
   - Transform recycled materials into remanufactured products
   - Products have lower CO2 footprint than new (5 vs 20 units)
   - Add inventory for users to purchase

### CO2 Tax System

- New products: 20 CO2 units → Tax = $10 (at 0.5 rate)
- Remanufactured products: 5 CO2 units → Tax = $2.50
- Incentivizes circular economy practices

### Key Parameters

- `n_users`: Number of consumer agents (default: 50)
- `n_recyclers`: Number of recycling facilities (default: 5)
- `n_remanufacturers`: Number of remanufacturing facilities (default: 3)
- `co2_tax_rate`: Tax per CO2 unit (default: 0.5)
- `recycling_rate`: Probability of recycling vs disposal (default: 0.7)

## Metrics Tracked

- Total CO2 emissions
- CO2 tax revenue collected
- Waste generated
- Products sold (new + remanufactured)
- Recycling queue length
- Remanufactured inventory
- Products in use

## Example Output

```
CIRCULAR ECONOMY SIMULATION WITH CO2 TAXES
============================================================

Model Configuration:
  Users: 50
  Recycling Facilities: 5
  Remanufacturing Facilities: 3
  CO2 Tax Rate: $0.5 per unit
  Recycling Rate: 70%

Running simulation for 100 steps...

SIMULATION RESULTS
============================================================

Final Metrics:
  Total CO2 Emissions: 1250.30 units
  Total CO2 Tax Collected: $625.15
  Total Waste Generated: 45 products
  Products Sold: 150
  Remanufactured Inventory: 12
```

## Insights

- CO2 taxes create economic incentives for sustainable choices
- Higher recycling rates significantly reduce waste and emissions
- Circular economy model reduces environmental impact compared to linear "take-make-dispose"
- Remanufactured products cost less to produce and generate less CO2
